#!/usr/bin/env python3
"""
ARGOS Emergence Loop — Phase 5 Core.
AI анализирует:
  - WORKING.md (открытые задачи)
  - auto_test_report.json (часто падающие паттерны)
  - survival_samples.json (RAM/disk тренды)
  - ab_champion.json (лучшие идеи)
Решает: какой [AUTO]-задачи НЕТ в списке, но нужна системе.
Генерирует новую задачу → записывает в WORKING.md → MetaTasker/Codegen её подхватят.
"""
import json, os, random, re
from pathlib import Path
from datetime import datetime

VAULT     = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared")
WORKING   = VAULT / "WORKING.md"
MEM_DIR   = Path("/home/ava/Projects/argoss/data/mempalace")
REPORTS   = MEM_DIR / "auto_test_report.json"
SURVIVAL  = MEM_DIR / "survival_samples.json"
CHAMPION  = MEM_DIR / "ab_champion.json"

def load_working():
    if not WORKING.exists(): return ""
    return WORKING.read_text(encoding="utf-8")

def load_json(p):
    if not p.exists(): return []
    try:
        return json.loads(p.read_text())
    except: return []

def analyze_deficits(working_text, test_report, survival, champion):
    """
    Возвращает list of suggested [AUTO] tasks based on system gaps.
    """
    tasks = []
    w = working_text.lower()
    
    # Gap detection
    if "memory leak" not in w and "auto_memory" not in w:
        tasks.append({
            "id": f"AUTO_EMERGE_{datetime.now().strftime('%Y%m%d_%H%M')}_001",
            "title": "[AUTO] Создать Memory Leak Detector — мониторить RAM per-process и убивать рост >50MB/час",
            "source": "emergence_loop: RAM trend analysis gap"
        })
    
    if "network partition" not in w:
        tasks.append({
            "id": f"AUTO_EMERGE_{datetime.now().strftime('%Y%m%d_%H%M')}_002",
            "title": "[AUTO] Network Partition Detector — тестировать связь между узлами каждые 60с",
            "source": "emergence_loop: cross-node health gap"
        })
    
    if len(test_report) > 0:
        fails = [r for r in test_report if not r.get("passed", True)]
        if len(fails) > len(test_report) * 0.3:
            tasks.append({
                "id": f"AUTO_EMERGE_{datetime.now().strftime('%Y%m%d_%H%M')}_003",
                "title": "[AUTO] Improve Codegen Quality — добавить prompt engineering для синтаксической валидности",
                "source": f"emergence_loop: {len(fails)}/{len(test_report)} tests failing"
            })
    
    if "predictive" not in w:
        tasks.append({
            "id": f"AUTO_EMERGE_{datetime.now().strftime('%Y%m%d_%H%M')}_004",
            "title": "[AUTO] Predictive Auto-Scale — предсказывать нагрузку и поднимать поды заранее",
            "source": "emergence_loop: proactive scaling gap"
        })
    
    if "chaos" not in w and "monkey" not in w:
        tasks.append({
            "id": f"AUTO_EMERGE_{datetime.now().strftime('%Y%m%d_%H%M')}_005",
            "title": "[AUTO] Chaos Monkey — каждые 4часа случайно убивать 1 сервис и тестировать self-heal",
            "source": "emergence_loop: resilience testing gap"
        })
    
    return tasks

def write_tasks(tasks):
    if not tasks:
        print("[Emergence] No new gaps detected")
        return 0
    
    lines = WORKING.read_text(encoding="utf-8").splitlines() if WORKING.exists() else []
    header = "## Автономно сгенерированные задачи (Emergence Loop)\n"
    new_block = ["", header]
    for t in tasks:
        new_block.append(f"- [{t['id']}] {t['title']}")
        new_block.append(f"  Source: {t['source']}")
        new_block.append("")
    
    # Insert after first heading
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_idx = i + 1
            break
    lines[insert_idx:insert_idx] = new_block
    
    WORKING.write_text("\n".join(lines), encoding="utf-8")
    print(f"[Emergence] Written {len(tasks)} tasks to WORKING.md")
    return len(tasks)

def run():
    w = load_working()
    t = load_json(REPORTS)
    s = load_json(SURVIVAL)
    c = load_json(CHAMPION)
    tasks = analyze_deficits(w, t, s, c)
    n = write_tasks(tasks)
    
    # Save emergence report
    report = MEM_DIR / f"emergence_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    report.write_text(json.dumps({
        "ts": datetime.now().isoformat(),
        "working_lines": len(w.splitlines()),
        "test_count": len(t),
        "fail_count": len([x for x in t if not x.get("passed",True)]),
        "tasks_generated": n,
        "tasks": tasks
    }, ensure_ascii=False, indent=2))
    print(f"[Emergence] Report: {report}")

if __name__ == "__main__":
    run()
