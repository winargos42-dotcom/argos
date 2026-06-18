---
argos_import: sharedmemory_mirror
source_path: claude/reference_memory_sync.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\reference_memory_sync.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/reference_memory_sync.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\reference_memory_sync.md`
- Category: [[Claude Hub]]

## Content

---
name: Синхронизация памяти ноутбук↔ПК
description: Где хранится память Claude Code на каждом устройстве и как синхронизировать
type: reference
originSessionId: f0e9ecac-e2f3-4284-a912-79646f263ea0
---
## Пути к памяти

| Устройство | Путь |
|-----------|------|
| Ноутбук X230 (Arch, root) | `/root/.claude/projects/-home-ava/memory/` |
| ПК Windows (F:\debug\argoss) | `C:\Users\AvA\.claude\projects\F--debug-argoss\memory\` |

## Синхронизация (ноутбук → ПК)

```bash
SSH_AUTH_SOCK=/home/ava/.ssh/agent scp -i /home/ava/.ssh/id_ed25519 \
  -o ProxyCommand="none" \
  /root/.claude/projects/-home-ava/memory/*.md \
  "AvA@192.168.1.66:C:/Users/AvA/.claude/projects/F--debug-argoss/memory/"
```

**Важно:** MEMORY.md нужно объединять вручную — на ПК есть свои записи (`feedback_language.md`, `project_argos_infra_status.md`, `project_argos_skills_audit.md`).

## Последняя синхронизация
- 2026-05-03: скопированы все файлы с ноутбука на ПК, MEMORY.md объединён (13 файлов)

**Why:** пользователь хочет единую базу знаний на обоих устройствах.
**How to apply:** при изменении важных записей предлагать синхронизировать на ПК.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/reference_memory_sync.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
