---
argos_import: sharedmemory_mirror
source_path: shared/SETUP.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\shared\SETUP.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: shared/SETUP.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\shared\SETUP.md`
- Category: [[SharedMemory Hub]]

## Content

# Настройка Shared Memory на Windows

## Claude Code (Windows)
Добавить в `C:\Users\AvA\.claude\settings.json`:
```json
{
  "autoMemoryDirectory": "C:/Users/AvA/Documents/ObsidianShared/claude"
}
```

## ARGOS
В `.env` добавить или изменить путь памяти:
```
ARGOS_MEMORY_PATH=C:\Users\AvA\Documents\ObsidianShared\argos
```

Или в `IDENTITY.md` / `HEARTBEAT.md` указать новый workspace путь.

## OpenCode
В настройках OpenCode указать workspace:
`C:\Users\AvA\Documents\ObsidianShared\opencode`

## Obsidian (Windows)
Открыть vault: `C:\Users\AvA\Documents\ObsidianShared\`

## Синхронизация
Arch → Windows: каждые 5 минут через systemd timer
Запуск вручную: `~/.local/bin/vault-sync.sh`
Логи: `~/.local/share/vault-sync.log`

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[SharedMemory Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `shared/SETUP.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[SharedMemory Hub]]
