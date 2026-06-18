---
argos_import: project_file
source_path: tmp/kolibrios/programs/system/dbgboard/README.md
source_abs: F:\debug\argoss\tmp\kolibrios\programs\system\dbgboard\README.md
source_ext: .md
source_sha256: f7fa592fa835d5e89fa3f2def1d5d9ad3db833a14566c9621f35a30fff4b85db
text_sha256: 8d6cfbbf957112b23ef1bf2b6dc27486e301546cbcc0175740ad020c7090e97f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:47
---

# README.md

- Source: `tmp/kolibrios/programs/system/dbgboard/README.md`
- Extract: `text`
- SHA256: `f7fa592fa835d5e89fa3f2def1d5d9ad3db833a14566c9621f35a30fff4b85db`

## Content

## DBGBOARD - a console-based debug board 
Main advantages over the old board:
* Bigger font
* Scrolling (like in other console apps)
* Messages highligting
    * K : - kernel messages (K: also supported because some code in kernel prints such)
    * L: - launcher messages
    * I: - information
    * W: - warning
    * E: - error
    * S: - success
* Three display modes (You can switch modes using `Tab` key)
    * User messages
    * Kernel messages
    * Both kernel and user messages

Also, like the old board it writes log to /tmp0/1/boardlog.txt (or you can pass another path in args like `/sys/develop/dbgboard /tmp0/1/hgfdhgfh.txt`), you can view log file in cedit by hitting `F2` key

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
