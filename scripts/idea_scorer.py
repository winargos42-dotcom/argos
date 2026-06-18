#!/usr/bin/env python3
"""
Idea Scorer — RL feedback для Entity Council.
Каждая идея из Entity получает score.
Закрытая задача = +1 балл.
Игнорированная >7 дней = -1 балл.
Идеи с score < -2 не показываются.
"""
import json, re, datetime, os
from pathlib import Path

WORKING = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared/WORKING.md")
BANK = Path("/home/ava/Projects/argoss/data/mempalace/idea_bank.json")

def load_bank():
    if BANK.exists:
        try:
            return json.loads(BANK.read_text(encoding="utf-8"))
        except:
            pass
    return {"ideas": []}

def save_bank(data):
    BANK.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def score_working():
    data = load_bank()
    txt = WORKING.read_text(encoding="utf-8")
    today = datetime.datetime.now()

    # Считаем закрытые ([x]) и открытые ([ ])
    closed = re.findall(r'- \[x\] .+\[AUTO\] (.+)', txt)
    open_tasks = re.findall(r'- \[\s?\] .+\[AUTO\] (.+)', txt)

    # Закрытые = +1
    for idea in data["ideas"]:
        for c in closed:
            if idea["text"][:40] in c or c[:40] in idea["text"]:
                idea["score"] += 1
                idea["closed"] = True

    # Новые идеи из WORKING добавляем
    seen = {i["text"][:40] for i in data["ideas"]}
    for o in open_tasks:
        key = o[:40]
        if key not in seen:
            data["ideas"].append({
                "text": o, "score": 0, "created": today.strftime("%Y-%m-%d"),
                "closed": False
            })

    # Игнор >7 дней = -1 (только незакрытые)
    for idea in data["ideas"]:
        if not idea.get("closed"):
            created = datetime.datetime.strptime(idea.get("created", "2026-01-01"), "%Y-%m-%d")
            if (today - created).days > 7:
                idea["score"] -= 1

    # Сортируем
    data["ideas"].sort(key=lambda x: x["score"], reverse=True)

    good = sum(1 for i in data["ideas"] if i["score"] >= 0)
    bad = sum(1 for i in data["ideas"] if i["score"] < -2)

    save_bank(data)
    print(f"[IdeaScorer] Total: {len(data['ideas'])}, Good: {good}, Hidden: {bad}")
    return data

if __name__ == "__main__":
    score_working()
