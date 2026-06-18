#!/usr/bin/env python3
"""
Auto-Tasker — парсит Entity Council логи, ищет '→ Действие:'
и автоматически добавляет задачи в WORKING.md.
"""
import re, datetime, sys, os
from pathlib import Path

WORKING = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/orchestrator/WORKING.md")
SCOUT = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/scout/findings")
LOG = Path("/tmp/entity_dialogue.log")
STATE = Path("/home/ava/Projects/argoss/data/mempalace/auto_tasker_state.json")

# Загружаем offset (где остановились в прошлый раз)
offset = 0
if STATE.exists():
    import json
    offset = json.loads(STATE.read_text()).get("offset", 0)

tasks_added = 0
if LOG.exists():
    data = LOG.read_text(encoding="utf-8", errors="replace")
    # Берём только новую часть
    new_data = data[offset:]
    # Ищем действия: разные варианты стрелок
    actions = re.findall(r'→\s*Действие[:：]\s*(.+)', new_data)
    actions += re.findall(r'→\s*Action[:：]\s*(.+)', new_data)
    actions += re.findall(r'Действие[:：]\s*(.+)', new_data)

    # Убираем дубликаты
    seen = set()
    unique_actions = []
    for a in actions:
        a = a.strip()
        if a and a not in seen and len(a) > 5:
            seen.add(a)
            unique_actions.append(a)

    if unique_actions:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = []
        for a in unique_actions[:5]:  # макс 5 за раз
            lines.append(f"- [ ] **{ts}** [AUTO] {a}\n")
            tasks_added += 1
            # Пишем находку в Scout
            safe = re.sub(r'[^\w]', '_', a[:40])
            finding = SCOUT / f"{ts.replace(' ', '_')}_{safe}.md"
            finding.write_text(f"# Находка AutoGPT\n**Время:** {ts}\n**Источник:** Entity Council\n**Действие:** {a}\n\n[Статус: в очереди WORKING.md]\n", encoding="utf-8")

        with open(WORKING, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"[AutoTasker] Added {tasks_added} tasks from Entity Council")
    else:
        print("[AutoTasker] No new actions found")

    # Сохраняем offset
    import json
    from datetime import datetime
    ts_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    STATE.write_text(json.dumps({"offset": len(data), "last_run": ts_now}), encoding="utf-8")
else:
    print(f"[AutoTasker] Log not found: {LOG}")
