#!/usr/bin/env python3
"""
telegram_memory_ingest.py — фоновый импорт Telegram-диалогов в долгосрочную память ARGOS.

Источники:
  • SQLite-таблица `chat_history` из `ARGOS_DB` (сообщения от бота).
  • JSON-экспорт Telegram Desktop (`result.json` / `chat_history_*.json`).

Что делает:
  1. Группирует сообщения в скользящие окна.
  2. Суммаризирует окно локальным LLM на V100 (`OLLAMA_HOST_4` / 8085).
  3. Извлекает факты и сохраняет в `ArgosMemory` (категория `telegram`).
  4. Сохраняет сводку как note.
  5. Ведёт state-файл, чтобы не обрабатывать одно и то же дважды.

Запуск:
  python scripts/telegram_memory_ingest.py --once              # один проход
  python scripts/telegram_memory_ingest.py --daemon --interval 300  # фон
  python scripts/telegram_memory_ingest.py --export ~/Downloads/telegram_export/result.json --once
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

# Добавляем корень проекта в sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.argos_logger import get_logger  # noqa: E402

log = get_logger("argos.tg_memory")


def _load_memory_class():
    """src/memory.py конфликтует с одноимённым пакетом src/memory/,
    поэтому загружаем файл напрямую через importlib."""
    import importlib.util  # noqa: E402
    mod_path = PROJECT_ROOT / "src" / "memory.py"
    spec = importlib.util.spec_from_file_location("argos_memory_mod", str(mod_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ArgosMemory


ArgosMemory = _load_memory_class()

DEFAULT_DB = os.getenv("ARGOS_DB", "data/argos_memory.db")
LLM_URL = os.getenv("OLLAMA_HOST_4", "http://192.168.1.72:8085").rstrip("/")
LLM_MODEL = os.getenv("OLLAMA_HOST_4_MODEL", "argos-v1.q8_0.gguf")
STATE_PATH = Path(os.getenv("ARGOS_TG_INGEST_STATE", "data/.telegram_ingest_state.json"))
WINDOW_SIZE = int(os.getenv("ARGOS_TG_WINDOW", "10"))
WINDOW_STEP = int(os.getenv("ARGOS_TG_STEP", "5"))
MAX_TEXT_LEN = int(os.getenv("ARGOS_TG_MAX_TEXT", "800"))
BATCH_DELAY = float(os.getenv("ARGOS_TG_BATCH_DELAY", "0.2"))


# ───────────────────────────────────────────────────────────────────────────────
# State helpers
# ───────────────────────────────────────────────────────────────────────────────
def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8", errors="ignore"))
        except Exception as e:
            log.warning("Не могу прочитать state: %s", e)
    return {"last_chat_history_id": 0, "exported_files": {}}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


# ───────────────────────────────────────────────────────────────────────────────
# LLM helpers
# ───────────────────────────────────────────────────────────────────────────────
def llm_chat(system: str, user: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
    payload = json.dumps({
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{LLM_URL}/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
        return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    except Exception as e:
        log.warning("LLM call failed: %s", e)
        return ""


def summarize_window(messages: list[dict], chat_name: str = "unknown") -> str:
    if not messages:
        return ""
    lines = []
    for m in messages:
        role = m.get("role", "?")
        text = (m.get("text") or "").replace("\n", " ")[:MAX_TEXT_LEN]
        ts = m.get("ts", "")
        lines.append(f"[{ts}] {role}: {text}")
    dialogue = "\n".join(lines)
    system = (
        "Ты — память системы ARGOS. Прочитай фрагмент Telegram-диалога и выдай краткую сводку.\n"
        "Формат: 2–5 коротких фактов, каждый с новой строки, в формате:\n"
        "КЛЮЧ: ЗНАЧЕНИЕ\n"
        "Не добавляй вводных слов, только факты. Если ничего важного — напиши 'нет фактов'."
    )
    user = f"Чат: {chat_name}\n\n{dialogue}"
    return llm_chat(system, user, max_tokens=512, temperature=0.2)


def parse_facts(text: str) -> list[tuple[str, str]]:
    facts = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.lower().startswith("нет фактов"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key and value and len(key) < 200 and len(value) < 2000:
                facts.append((key, value))
    return facts


# ───────────────────────────────────────────────────────────────────────────────
# Memory ingestion
# ───────────────────────────────────────────────────────────────────────────────
def ingest_window(memory: ArgosMemory, messages: list[dict], chat_name: str = "unknown") -> int:
    summary = summarize_window(messages, chat_name)
    if not summary:
        return 0
    facts = parse_facts(summary)
    if not facts:
        return 0

    saved = 0
    for key, value in facts:
        # Делаем ключ уникальным в рамках чата
        full_key = f"{chat_name}: {key}"[:250]
        res = memory.remember(full_key, value, category="telegram")
        if "✅" in res or "ℹ️" in res:
            saved += 1
        log.debug("remember: %s", res)
        time.sleep(BATCH_DELAY)

    # Сохраняем и полную сводку как note
    window_ts = messages[-1].get("ts", "unknown")
    title = f"TG [{chat_name}] {window_ts}"[:120]
    body = summary[:1900]
    try:
        memory.add_note(title, body)
    except Exception as e:
        log.warning("add_note failed: %s", e)

    log.info("Окно '%s' → сохранено фактов: %d", chat_name, saved)
    return saved


# ───────────────────────────────────────────────────────────────────────────────
# SQLite chat_history source
# ───────────────────────────────────────────────────────────────────────────────
def iter_sqlite_windows(db_path: str, last_id: int):
    import sqlite3
    if not Path(db_path).exists():
        log.warning("БД не найдена: %s", db_path)
        return
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(
            "SELECT id, role, text, category, ts FROM chat_history WHERE id > ? ORDER BY id",
            (last_id,),
        )
        buffer: list[dict] = []
        max_id = last_id
        for row in cur:
            max_id = max(max_id, row["id"])
            buffer.append({
                "id": row["id"],
                "role": row["role"],
                "text": row["text"],
                "category": row["category"],
                "ts": row["ts"],
            })
            if len(buffer) >= WINDOW_SIZE:
                yield buffer.copy(), max_id
                buffer = buffer[WINDOW_STEP:]
        if buffer:
            yield buffer.copy(), max_id
    finally:
        conn.close()


# ───────────────────────────────────────────────────────────────────────────────
# Telegram JSON export source
# ───────────────────────────────────────────────────────────────────────────────
def iter_export_windows(export_path: str):
    p = Path(export_path)
    if not p.exists():
        log.warning("Экспорт не найден: %s", export_path)
        return
    try:
        data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
    except Exception as e:
        log.warning("Не парсится JSON: %s", e)
        return

    chats = data.get("chats", {}).get("list", []) if isinstance(data, dict) else []
    for chat in chats:
        name = chat.get("name") or chat.get("type") or "unknown"
        messages = chat.get("messages", [])
        buffer: list[dict] = []
        for msg in messages:
            if not isinstance(msg, dict):
                continue
            text = msg.get("text") or ""
            if isinstance(text, list):
                text = " ".join(str(x) for x in text)
            if not text:
                continue
            buffer.append({
                "id": msg.get("id"),
                "role": msg.get("from", "unknown"),
                "text": str(text)[:MAX_TEXT_LEN],
                "category": "tg_export",
                "ts": msg.get("date", ""),
            })
            if len(buffer) >= WINDOW_SIZE:
                yield buffer.copy(), name
                buffer = buffer[WINDOW_STEP:]
        if buffer:
            yield buffer.copy(), name


# ───────────────────────────────────────────────────────────────────────────────
# Main loops
# ───────────────────────────────────────────────────────────────────────────────
def run_once(memory: ArgosMemory, state: dict, export_path: str | None = None) -> dict:
    total = 0

    # SQLite
    new_last_id = state.get("last_chat_history_id", 0)
    for window, max_id in iter_sqlite_windows(DEFAULT_DB, new_last_id):
        total += ingest_window(memory, window, chat_name="bot_dialogue")
        new_last_id = max_id
    state["last_chat_history_id"] = new_last_id

    # Export
    if export_path:
        file_hash = hashlib.sha1(Path(export_path).read_bytes()).hexdigest()[:16]
        processed_ids = state["exported_files"].get(file_hash, [])
        for window, chat_name in iter_export_windows(export_path):
            # skip fully processed windows by fingerprint of last message id
            fp = hashlib.sha1(json.dumps(window[-1], sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
            if fp in processed_ids:
                continue
            total += ingest_window(memory, window, chat_name=chat_name[:40])
            processed_ids.append(fp)
        state["exported_files"][file_hash] = processed_ids[-1000:]  # keep last 1000 fingerprints

    save_state(state)
    log.info("Итог одного прохода: сохранено %d фактов, last_id=%s", total, new_last_id)
    return state


def run_daemon(memory: ArgosMemory, state: dict, interval: int, export_path: str | None = None):
    log.info("Фоновый ingest запущен, interval=%ds", interval)
    while True:
        try:
            state = run_once(memory, state, export_path)
        except Exception as e:
            log.error("Ошибка прохода: %s", e)
        time.sleep(interval)


# ───────────────────────────────────────────────────────────────────────────────
# CLI
# ───────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Импорт Telegram-диалогов в память ARGOS")
    parser.add_argument("--once", action="store_true", help="Один проход и выход")
    parser.add_argument("--daemon", action="store_true", help="Запустить фоновый цикл")
    parser.add_argument("--interval", type=int, default=300, help="Интервал цикла в секундах (default 300)")
    parser.add_argument("--export", type=str, default=None, help="Путь к JSON-экспорту Telegram Desktop")
    args = parser.parse_args()

    os.chdir(PROJECT_ROOT)
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    memory = ArgosMemory()
    state = load_state()

    if args.daemon:
        run_daemon(memory, state, args.interval, args.export)
    else:
        run_once(memory, state, args.export)


if __name__ == "__main__":
    main()
