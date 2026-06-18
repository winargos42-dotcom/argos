"""
chat_memory.py — сессионная память для телеграм-бота ARGOS.
Сохраняет последние N сообщений пользователя → бот НЕ забывает контекст.
Каждое сообщение дополняется реальным временем.
"""
import json, os, re
from datetime import datetime
from pathlib import Path

CHAT_DIR = Path("/home/ava/Projects/argoss/data/mempalace/chat_sessions")
CHAT_DIR.mkdir(parents=True, exist_ok=True)
MAX_HISTORY = 15  # сколько сообщений помним

def _user_file(user_id: str) -> Path:
    safe = re.sub(r'[^\w-]', '_', str(user_id))
    return CHAT_DIR / f"chat_{safe}.json"

def load_history(user_id: str) -> list:
    """Последние N сообщений для пользователя."""
    f = _user_file(user_id)
    if not f.exists():
        return []
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        return data.get("messages", [])
    except:
        return []

def save_history(user_id: str, user_msg: str, bot_msg: str):
    """Добавляем пару сообщений."""
    f = _user_file(user_id)
    hist = load_history(user_id)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hist.append({"ts": ts, "role": "user", "text": user_msg})
    hist.append({"ts": ts, "role": "bot", "text": bot_msg})
    hist = hist[-MAX_HISTORY * 2:]  # N пар
    CHAT_DIR.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"messages": hist}, ensure_ascii=False, indent=2), encoding="utf-8")

def build_context(user_id: str, current_question: str, system_ctx: str = "") -> tuple:
    """
    Возвращает (history_for_api, enhanced_system_prompt).
    history_for_api — список {"role": "...", "content": "..."} для Claude/DeepSeek
    enhanced_system_prompt — с реальным временем и памятью.
    """
    hist = load_history(user_id)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tz = datetime.now().astimezone().strftime("%z")  # +1000 для Vladivostok

    # system prompt с реальным временем (чтобы AI не фантазировал)
    sys = (
        f"Ты ARGOS autopilot. Сегодня {now} (UTC{tz}).\n"
        f"История диалога с пользователем (последние строки):\n"
    )
    # Добавляем историю
    recent = []
    for m in hist[-MAX_HISTORY * 2:]:
        prefix = "👤 User: " if m["role"] == "user" else "🤖 ARGOS: "
        recent.append(f"[{m['ts']}] {prefix}{m['text'][:120]}")

    if recent:
        sys += "\n".join(recent) + "\n\n"
    sys += f"Текущий контекст системы: {system_ctx}\n\n"

    # Формируем messages для Claude API — включаем историю диалога
    messages = [{"role": "system", "content": sys}]
    for m in hist:
        role = "user" if m["role"] == "user" else "assistant"
        messages.append({"role": role, "content": m["text"]})
    # Текущий вопрос — БЕЗ «Контекст: ...» обёртки
    messages.append({"role": "user", "content": current_question})

    return messages, sys

def get_real_time_prompt() -> str:
    """Однострочник с реальным временем для вставки в любой ответ."""
    return f"Текущее время: {datetime.now().strftime('%Y-%m-%d %H:%M')} (UTC{datetime.now().astimezone().strftime('%z')})"
