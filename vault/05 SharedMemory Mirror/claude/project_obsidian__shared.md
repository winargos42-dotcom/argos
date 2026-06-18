---
argos_import: sharedmemory_mirror
source_path: claude/project_obsidian.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_obsidian.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_obsidian.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_obsidian.md`
- Category: [[Claude Hub]]

## Content

---
name: Проект Obsidian и SharedMemory
description: Структура хранилища Obsidian, синхронизация памяти между ПК и ноутбуком
type: project
originSessionId: 81a638d4-f034-4bbb-8b6c-d15b46bb4b71
---
## Хранилище Obsidian
- **Ноутбук:** `~/Documents/MyObsidianVault/`
- **Папки:** Inbox, 01_Inbox, Projects, 02_Projects, Archive, 03_Archive, Templates, SharedMemory/

## SharedMemory — общая память всех агентов
| Папка | Агент |
|-------|-------|
| `shared/` | Общие данные, читают все |
| `claude/` | Claude Code |
| `argos/` | ARGOS |
| `opencode/` | OpenCode |
| `ollama/` | Ollama |

## Синхронизация ноутбук ↔ ПК
- **Скрипт:** `~/.local/bin/sync-obsidian-memory.py`
- **Таймер:** systemd user timer, каждые 2 минуты
- **Путь на ПК:** `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\`
- **Логика:** двусторонняя, побеждает файл с более новой меткой времени

**Why:** пользователь хочет единую память для всех AI-агентов на обеих машинах.
**How to apply:** при работе на любой машине читать SharedMemory/shared/SHARED.md, писать в свою папку.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_obsidian.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
