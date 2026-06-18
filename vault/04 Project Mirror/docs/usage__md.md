---
argos_import: project_file
source_path: docs/usage.md
source_abs: F:\debug\argoss\docs\usage.md
source_ext: .md
source_sha256: 3312375b80f78636b73a7f96a43fa385a4c46172f12063901595839669f7d5cf
text_sha256: 3312375b80f78636b73a7f96a43fa385a4c46172f12063901595839669f7d5cf
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:59
---

# usage.md

- Source: `docs/usage.md`
- Extract: `text`
- SHA256: `3312375b80f78636b73a7f96a43fa385a4c46172f12063901595839669f7d5cf`

## Content

# User Guide: Повседневное использование

## Диалоговый режим

ARGOS поддерживает обычные вопросы и системные команды в одном чате.

Примеры:

- `какая погода и сколько свободно места на диске`
- `покажи схемы инструментов`
- `статус сети`

## Память и RAG

Память работает в гибридном режиме:

- структурированные факты и заметки в SQLite,
- семантический поиск в Vector Store,
- связи фактов в графе знаний.

Полезные команды:

- `запомни имя: Всеволод`
- `найди в памяти имя`
- `граф знаний`

## Агентский режим

Для многошаговых задач используй естественные цепочки:

`статус системы → затем крипто → потом дайджест`

## P2P и сеть

ARGOS умеет запускать P2P-сеть нод и маршрутизировать запросы:

- `запусти p2p`
- `статус сети`
- `распредели задачу [вопрос]`

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
