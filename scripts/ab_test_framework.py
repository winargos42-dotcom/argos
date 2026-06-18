#!/usr/bin/env python3
"""
A/B Test Framework — сравнивает идеи Entity между собой.
Берёт 2 последние [AUTO] задачи → оценивает → сохраняет champion.
Метрики: RL score, время закрытия, упоминания в логах.
"""
import json, os, re, datetime
from pathlib import Path
from collections import defaultdict

BANK = Path("/home/ava/Projects/argoss/data/mempalace/idea_bank.json")
CHAMPION = Path("/home/ava/Projects/argoss/data/mempalace/ab_champion.json")
HISTORY = Path("/home/ava/Projects/argoss/data/mempalace/ab_history.json")

def load_data():
    bank = {"ideas": []}
    if BANK.exists():
        bank = json.loads(BANK.read_text())
    
    hist = []
    if HISTORY.exists():
        hist = json.loads(HISTORY.read_text())
    
    champion = None
    if CHAMPION.exists():
        champion = json.loads(CHAMPION.read_text())
    
    return bank, hist, champion

def score_idea(idea):
    """Оценка идеи по нескольким метрикам."""
    score = 0.0
    
    # RL score (-2 .. +N)
    rl = idea.get("score", 0)
    score += rl * 10  # базовый вес
    
    # Закрыта ли?
    if idea.get("closed"):
        score += 20
        # Как быстро закрыта?
        if idea.get("closed_ts") and idea.get("created"):
            try:
                c = datetime.datetime.strptime(idea["created"], "%Y-%m-%d")
                cl = datetime.datetime.strptime(idea["closed_ts"], "%Y-%m-%d")
                days = (cl - c).days
                if days < 2:
                    score += 15  # fast close
                elif days < 7:
                    score += 5
            except: pass
    
    # Длина описания — чем конкретней, тем лучше
    text = idea.get("text", "")
    if len(text) > 100:
        score += 3
    
    return round(score, 1)

def run_ab_test():
    bank, history, champion = load_data()
    ideas = bank.get("ideas", [])
    
    if len(ideas) < 2:
        print("[A/B] Not enough ideas for A/B test (need 2+)")
        return
    
    # Берём 2 последние (и закрытые, и открытые)
    candidates = ideas[-4:]
    if len(candidates) < 2:
        print("[A/B] Not enough ideas for A/B test (need 2+)")
        return
    
    scored = []
    for idea in candidates:
        s = score_idea(idea)
        scored.append({"idea": idea, "score": s})
        print(f"[A/B] '{idea['text'][:40]}'... → score {s}")
    
    scored.sort(key=lambda x: x["score"], reverse=True)
    winner = scored[0]
    loser = scored[-1]
    
    # Champion update
    current_champ_score = 0
    if champion:
        current_champ_score = champion.get("score", 0)
    
    if winner["score"] > current_champ_score:
        CHAMPION.write_text(json.dumps(winner, ensure_ascii=False, indent=2))
        print(f"[A/B] NEW CHAMPION: '{winner['idea']['text'][:50]}' score={winner['score']}")
    else:
        print(f"[A/B] Champion holds: score={current_champ_score}, best challenger={winner['score']}")
    
    # History
    round_data = {
        "ts": datetime.datetime.now().isoformat(),
        "winner": {"text": winner["idea"]["text"][:60], "score": winner["score"]},
        "loser": {"text": loser["idea"]["text"][:60], "score": loser["score"]},
    }
    history.append(round_data)
    HISTORY.write_text(json.dumps(history[-50:], ensure_ascii=False, indent=2))
    
    return winner

if __name__ == "__main__":
    run_ab_test()
