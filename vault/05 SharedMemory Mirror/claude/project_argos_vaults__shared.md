---
argos_import: sharedmemory_mirror
source_path: claude/project_argos_vaults.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_argos_vaults.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_argos_vaults.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_argos_vaults.md`
- Category: [[Claude Hub]]

## Content

---
name: Obsidian хранилища ARGOS
description: Два отдельных Obsidian vault — SharedMemory и личный ARGOS vault
type: project
originSessionId: 81a638d4-f034-4bbb-8b6c-d15b46bb4b71
---
## Хранилище 1 — SharedMemory (общая память агентов)
- **Ноутбук:** `~/Documents/MyObsidianVault/SharedMemory/`
- **ПК:** `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\`
- **Назначение:** Claude, ARGOS, OpenCode читают/пишут сюда
- **Синхронизация:** каждые 2 мин через systemd

## Хранилище 2 — Личный vault ARGOS (на ПК)
- **Путь:** `F:\debug\аргос\` (кириллица!)
- **Заметки (11 шт):**
  - `01 Projects/ARGOS.md`
  - `01 Projects/ARGOS Memory DB 2026-04-11.md`
  - `01 Projects/ARGOS Root Cleanup Audit.md`
  - `01 Projects/Post Reboot Plan.md`
  - `01 Projects/SiGtRiP v2.2.0.md`
  - `02 Logs/2026-05-03.md`
  - `03 Memory/` (папка)
  - `2026-05-03.md`
  - другие заметки
- **Назначение:** личные заметки Всеволода о проекте

## Связь между хранилищами
- ARGOS ищет заметки Claude → они в `SharedMemory/claude/` (не в личном vault)
- Claude Code читает `SharedMemory/claude/MEMORY.md` при старте
- Личный vault НЕ синхронизируется автоматически с ноутбуком

**How to apply:** При вопросах "где мои заметки Claude" → указывать `SharedMemory/claude/`.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_argos_vaults.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
