---
argos_import: sharedmemory_mirror
source_path: claude/project_argos.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_argos.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_argos.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_argos.md`
- Category: [[Claude Hub]]

## Content

---
name: Проект ARGOS
description: ARGOS Universal OS — автономная AI-экосистема, основной проект пользователя
type: project
originSessionId: 81a638d4-f034-4bbb-8b6c-d15b46bb4b71
---
ARGOS Universal OS v2.1.4 — самовоспроизводящаяся кроссплатформенная AI-экосистема (Desktop / Android / Docker / Telegram).

## Пути
- **ПК (Windows):** `F:\debug\argoss\`
- **Ноутбук (Arch):** `~/Projects/argoss/` (Python venv: `.venv`, Python 3.14)

## Стек
- Python 3.14, Node.js, llama.cpp Vulkan, AMD GPU x3
- AI провайдеры: local-gpu → vm-cluster → azure → ollama → kimi → claude → gemini → openai → groq → deepseek → pi → yandexgpt
- P2P mesh, Telegram бот, Cloudflare туннели (argosssss.win)
- Redis, aiohttp, PostgreSQL, Docker

## Запуск
```bash
cd ~/Projects/argoss
source .venv/bin/activate
python genesis.py      # создаёт структуру папок
python main.py         # Desktop GUI + все подсистемы
python health_check.py # проверка целостности
```

## Режимы
```bash
python main.py --no-gui --dashboard  # headless сервер + вебпанель :8080
python main.py --full                # GUI + Dashboard + Wake Word
python main.py --shell               # REPL
```

## Cloudflare туннели (argosssss.win)
| Домен | Сервис |
|-------|--------|
| ssh-pc.argosssss.win | SSH → ПК :22 |
| ssh-laptop.argosssss.win | SSH → ноутбук :22 |
| api.argosssss.win | ARGOS API :5010 |
| app.argosssss.win | Dashboard :8081 |

## SSH доступ
- ПК из интернета: `ssh argos-pc` (через cloudflared)
- Ноутбук из интернета: `ssh argos-laptop` (через cloudflared)
- ПК локально: `ssh AvA@192.168.1.66`

**Why:** основной проект пользователя, всё остальное строится вокруг него.
**How to apply:** при любой работе с кодом — это контекст.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_argos.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
