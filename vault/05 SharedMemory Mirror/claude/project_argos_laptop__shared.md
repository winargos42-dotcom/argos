---
argos_import: sharedmemory_mirror
source_path: claude/project_argos_laptop.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_argos_laptop.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_argos_laptop.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_argos_laptop.md`
- Category: [[Claude Hub]]

## Content

---
name: ARGOS на ноутбуке X230
description: Статус запуска ARGOS на ноутбуке — MCP, провайдеры, навыки
type: project
originSessionId: 81a638d4-f034-4bbb-8b6c-d15b46bb4b71
---
## Статус (2026-05-03)
- PID: 200667 (nohup, no-gui)
- MCP: `http://127.0.0.1:8000/mcp` ✅
- Навыки: 51/51 ✅
- AI роутер: **Kimi → DeepSeek** (остальные отключены через _DEFAULT_ORDER)

## Запуск
```bash
cd ~/Projects/argoss
source .venv/bin/activate
nohup python main.py --no-gui > logs/argos_laptop.log 2>&1 &
```

## Изменения для ноутбука
- `src/ai_failover.py` → `_DEFAULT_ORDER = ["kimi", "deepseek"]`
- `.env` → ARGOS_AI_PRIORITY="kimi,deepseek", OLLAMA_ENABLED=false, DISABLE флаги
- `.env` → OBSIDIAN_VAULT_PATH=/home/ava/Documents/MyObsidianVault

## Исправлено (2026-05-03)
- `main.py:685` — `orchestrator.shutdown()` → `self.shutdown()` (NameError при SIGTERM)
- `aiohttp` 1.0.5 → 3.13.5 (Python 3.14 совместимость)
- Навык `evolved_system_health_monitor` — реальный навык, работает через MCP командой "хелс"

## Evolved навык
- Файл: `src/skills/evolved_system_health_monitor.py`
- Триггеры: "хелс", "health monitor", "health check", "system health", "мониторинг здоровья"
- Класс `SystemHealthMonitor`: CPU/RAM/диск/температура/топ процессов, цветовые алерты

## Известные проблемы
- Telegram polling: `set_wakeup_fd only works in main thread` (не критично, retry loop)
- RAM: ~83-91% под нагрузкой (openclaw процессы OpenCode + ARGOS)

**Why:** ноутбук — второй узел ARGOS кластера рядом с ПК (192.168.1.66).
**How to apply:** `curl http://127.0.0.1:8000/mcp` — проверка живости.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_argos_laptop.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
