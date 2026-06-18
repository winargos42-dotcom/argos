#!/usr/bin/env python3
"""
ARGOS Dataset Cleaner & Unifier
================================
Сводит все источники в единый канонический датасет argos_canonical.jsonl:
  • JSONL-датасеты в 4 форматах → единый chat-формат {messages:[{role,content}]}
  • Telegram HTML-экспорты (Ava=user, Argos=assistant) → диалоговые пары
  • дедупликация по содержанию, фильтрация мусора, train/val split

Запуск:
    python scripts/clean_datasets.py
Выход:
    data/argos_canonical.jsonl        (всё уникальное)
    data/argos_canonical_train.jsonl  (97%)
    data/argos_canonical_val.jsonl    (3%)
    data/argos_canonical_report.md    (отчёт)
"""
from __future__ import annotations

import glob
import hashlib
import json
import random
import re
from collections import Counter
from pathlib import Path

BASE = Path("/home/ava/Projects/argoss")
DATA = BASE / "data"
TG_DIR = Path("/home/ava/Downloads/Telegram Desktop")

DEFAULT_SYSTEM = ("Ты — АРГОС (Argos Universal OS), автономная AI-система Всеволода. "
                  "Отвечай по-русски, по делу. Выполняй задачи, а не описывай их.")

# JSONL-источники (исключены: 5 крупных-подмножеств dal_full, quantum_train, val-файлы,
# entity_dataset (монологи без user), служебные arc_history/evolution_history)
JSONL_SOURCES = [
    "argos_dal_full_dataset.jsonl",   # надмножество all_combined/final_train/final_v2/full/dal
    "argos_train_v2.jsonl",
    "argos_train_clean.jsonl",         # HF AvaSiG/argos-dataset
    "argos_ru_classic.jsonl",
    "argos_memory_train.jsonl",
    "argos_train_mistral.jsonl",
    "argos_synthetic.jsonl",
    "evolver_dataset.jsonl",
]

TG_EXPORTS = [
    "ChatExport_2026-05-27",
    "ChatExport_2026-05-26 (2)",
    "ChatExport_2026-05-26 (1)",
]

stats = Counter()
rejects = Counter()


# ── нормализация в messages ────────────────────────────────────────────────
def clean_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    return re.sub(r"[ \t]+", " ", s.replace("\r", "")).strip()


def norm_record(o: dict) -> list | None:
    """Любой из 4 форматов → список messages [{role,content}] или None."""
    msgs = []
    if "messages" in o and isinstance(o["messages"], list):
        for m in o["messages"]:
            if isinstance(m, dict) and m.get("role") in ("system", "user", "assistant"):
                msgs.append({"role": m["role"], "content": clean_text(m.get("content", ""))})
    elif "user" in o and "assistant" in o and "answer" not in o:
        # {user, assistant}
        msgs = [{"role": "system", "content": DEFAULT_SYSTEM},
                {"role": "user", "content": clean_text(o["user"])},
                {"role": "assistant", "content": clean_text(o["assistant"])}]
    elif "answer" in o and "user" in o:
        # evolver: {ts, user, answer, context}
        sysc = clean_text(o.get("context", "")) or DEFAULT_SYSTEM
        msgs = [{"role": "system", "content": sysc[:2000]},
                {"role": "user", "content": clean_text(o["user"])},
                {"role": "assistant", "content": clean_text(o["answer"])}]
    else:
        return None
    return msgs or None


# маркеры служебного/мусорного ответа бота в TG (рассинхрон, эхо, ошибки, команды)
TG_JUNK_PATTERNS = [
    re.compile(r"^\s*ARGOS\s*🤖\s*\|\s*/help", re.I),
    re.compile(r"не найден[ао]?\s+в\s+[`/]?[A-Z]:\\", re.I),
    re.compile(r"^\s*🎵\s*Аудио", re.I),
    re.compile(r"^\s*ARGOS\s*\[System\]", re.I),
    re.compile(r"/help\s+для\s+команд", re.I),
    re.compile(r"^\s*❌", ),
    re.compile(r"^\s*(ок|ok|да|нет|ага|угу|\.+|\?+)\s*$", re.I),
    re.compile(r"Введи\s+`покажи файлы", re.I),
    re.compile(r"^\s*ARGOS\s*\[Skill\]\s*🤖\s*AutoGPT:\s*принято", re.I),  # эхо-подтверждение
]

# ответы-ошибки (применяются ко ВСЕМ источникам — это не данные, а сбои рантайма)
ERROR_PATTERNS = [
    re.compile(r"No API provider registered", re.I),
    re.compile(r"все AI[- ]?провайдеры недоступны", re.I),
    re.compile(r"Офлайн:\s*все", re.I),
    re.compile(r"\[Timeout\]", re.I),
    re.compile(r"Unable to init", re.I),
    re.compile(r"Traceback \(most recent", re.I),
    re.compile(r"требуется\s+GEMINI_API_KEY", re.I),
    re.compile(r"(rate.?limit|429 Too Many)", re.I),
]


def is_error_answer(text: str) -> bool:
    for pat in ERROR_PATTERNS:
        if pat.search(text):
            return True
    # повтор одной фразы дважды подряд ("X X") — частый признак сбоя
    half = len(text) // 2
    if half > 15 and text[:half].strip() == text[half:].strip():
        return True
    return False


def tg_assistant_is_junk(text: str, user: str) -> bool:
    if len(text) < 12:
        return True
    for pat in TG_JUNK_PATTERNS:
        if pat.search(text):
            return True
    # эхо: ответ почти дословно повторяет запрос (нормализуем регистр/пробелы)
    nt = re.sub(r"\s+", " ", text.lower())
    nu = re.sub(r"\s+", " ", user.lower())
    if nu and nu[:60] in nt:
        return True
    return False


def valid_dialogue(msgs: list) -> bool:
    """Качество: есть user и непустой осмысленный assistant."""
    if not msgs:
        return False
    roles = [m["role"] for m in msgs]
    if "assistant" not in roles or "user" not in roles:
        rejects["no_user_or_assistant"] += 1
        return False
    last_a = next((m["content"] for m in reversed(msgs) if m["role"] == "assistant"), "")
    last_u = next((m["content"] for m in reversed(msgs) if m["role"] == "user"), "")
    if len(last_a) < 3:
        rejects["assistant_too_short"] += 1
        return False
    if len(last_u) < 2:
        rejects["user_too_short"] += 1
        return False
    if is_error_answer(last_a):
        rejects["error_answer"] += 1
        return False
    return True


def sig(msgs: list) -> str:
    """Подпись для дедупа — по user+assistant контенту (без system)."""
    txt = "".join(m["content"].lower() for m in msgs if m["role"] in ("user", "assistant"))
    txt = re.sub(r"\s+", " ", txt).strip()
    return hashlib.md5(txt.encode()).hexdigest()


# ── Telegram HTML парсинг ──────────────────────────────────────────────────
def parse_tg_export(folder: Path) -> list:
    from bs4 import BeautifulSoup
    files = sorted(folder.glob("messages*.html"),
                   key=lambda p: int(re.sub(r"\D", "", p.stem) or "1"))
    turns = []  # (sender, text) в хронологии
    last_sender = None
    for fn in files:
        soup = BeautifulSoup(fn.read_text(encoding="utf-8"), "html.parser")
        for m in soup.select("div.message"):
            if "service" in (m.get("class") or []):
                continue
            fn_el = m.select_one(".from_name")
            if fn_el:
                last_sender = fn_el.get_text(strip=True)
            tx = m.select_one(".text")
            if not tx or not last_sender:
                continue
            text = clean_text(tx.get_text(separator=" ", strip=True))
            if text:
                turns.append((last_sender, text))

    # склеить подряд идущие реплики одного отправителя, собрать пары Ava→Argos
    pairs = []
    cur_user, cur_asst = [], []

    def flush():
        if cur_user and cur_asst:
            u = " ".join(cur_user).strip()
            a = " ".join(cur_asst).strip()
            if len(u) >= 2 and len(a) >= 3:
                if tg_assistant_is_junk(a, u):
                    rejects["tg_junk_answer"] += 1
                else:
                    pairs.append([
                        {"role": "system", "content": DEFAULT_SYSTEM},
                        {"role": "user", "content": u},
                        {"role": "assistant", "content": a},
                    ])

    for sender, text in turns:
        is_user = sender.startswith("Ava")
        is_asst = sender.startswith("Argos")
        if is_user:
            if cur_asst:        # завершилась пара
                flush()
                cur_user, cur_asst = [], []
            cur_user.append(text)
        elif is_asst:
            if cur_user:
                cur_asst.append(text)
            # assistant без предшествующего user — пропускаем
    flush()
    return pairs


# ── основной конвейер ──────────────────────────────────────────────────────
def main():
    seen = set()
    canonical = []
    per_source = Counter()

    # 1) JSONL
    for fn in JSONL_SOURCES:
        p = DATA / fn
        if not p.exists():
            print(f"  ⚠ нет {fn}")
            continue
        n_in = n_ok = 0
        with p.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                n_in += 1
                try:
                    o = json.loads(line)
                except Exception:
                    rejects["bad_json"] += 1
                    continue
                msgs = norm_record(o)
                if not msgs or not valid_dialogue(msgs):
                    continue
                s = sig(msgs)
                if s in seen:
                    rejects["duplicate"] += 1
                    continue
                seen.add(s)
                canonical.append({"messages": msgs, "source": fn.replace(".jsonl", "")})
                per_source[fn] += 1
                n_ok += 1
        print(f"  {fn:34} вход={n_in:6} уникальных+чистых={n_ok}")
        stats["jsonl_in"] += n_in

    # 2) Telegram
    for d in TG_EXPORTS:
        folder = TG_DIR / d
        if not folder.exists():
            print(f"  ⚠ нет TG {d}")
            continue
        pairs = parse_tg_export(folder)
        n_ok = 0
        for msgs in pairs:
            if not valid_dialogue(msgs):
                continue
            s = sig(msgs)
            if s in seen:
                rejects["duplicate"] += 1
                continue
            seen.add(s)
            canonical.append({"messages": msgs, "source": f"telegram/{d}"})
            per_source[f"telegram/{d}"] += 1
            n_ok += 1
        print(f"  TG {d:30} пар={len(pairs):6} уникальных+чистых={n_ok}")

    # 3) split
    random.seed(3233339492)
    random.shuffle(canonical)
    n_val = max(1, int(len(canonical) * 0.03))
    val, train = canonical[:n_val], canonical[n_val:]

    out_all = DATA / "argos_canonical.jsonl"
    out_tr = DATA / "argos_canonical_train.jsonl"
    out_vl = DATA / "argos_canonical_val.jsonl"
    for path, rows in [(out_all, canonical), (out_tr, train), (out_vl, val)]:
        with path.open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # 4) отчёт
    report = [
        "# ARGOS Canonical Dataset — отчёт чистки",
        "",
        f"**Итого уникальных чистых примеров:** {len(canonical)}",
        f"- train: {len(train)} → `data/argos_canonical_train.jsonl`",
        f"- val:   {len(val)} → `data/argos_canonical_val.jsonl`",
        "",
        "## Вклад по источникам",
        "",
        "| Источник | Примеров |",
        "|----------|----------|",
    ]
    for src, c in per_source.most_common():
        report.append(f"| {src} | {c} |")
    report += ["", "## Отброшено", "", "| Причина | Кол-во |", "|---------|--------|"]
    for r, c in rejects.most_common():
        report.append(f"| {r} | {c} |")
    report += ["", "## Формат", "",
               "Единый chat: `{\"messages\":[{\"role\":\"system|user|assistant\",\"content\":...}],\"source\":...}`",
               "Дедуп по md5(user+assistant, нормализованный регистр/пробелы).", ""]
    (DATA / "argos_canonical_report.md").write_text("\n".join(report), encoding="utf-8")

    print(f"\n✅ Канон: {len(canonical)} уникальных (train {len(train)} / val {len(val)})")
    print(f"   Отброшено дублей: {rejects['duplicate']}, мусора: "
          f"{sum(v for k,v in rejects.items() if k!='duplicate')}")
    print(f"   Отчёт: data/argos_canonical_report.md")


if __name__ == "__main__":
    main()
