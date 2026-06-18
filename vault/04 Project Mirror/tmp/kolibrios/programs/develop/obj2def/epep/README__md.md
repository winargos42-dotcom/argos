---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/obj2def/epep/README.md
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\obj2def\epep\README.md
source_ext: .md
source_sha256: 0db0911e8fa7c1e860d49e518d7c951a8521ff3cb8d95b334daf2208172a0596
text_sha256: 0b392921cf5b52bd89aea2937c29dfb8f6b71cd94fa1049d3059724f761482b0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:44
---

# README.md

- Source: `tmp/kolibrios/programs/develop/obj2def/epep/README.md`
- Extract: `text`
- SHA256: `0db0911e8fa7c1e860d49e518d7c951a8521ff3cb8d95b334daf2208172a0596`

## Content

# epep - Embeddable PE Parser
## Features

- PE header (including Data Directories as a part Optional Header)
- Section Headers
- COFF Symbols
- COFF Relocations
- COFF Linenumbers
- Imports
- Exports
- Base relocations (DLL)

## How to use

To declare functions from the library include it:

```C
#include "epep.h"
```

The functions they shoud be instantiated somewhere in the project like so:

```C
#define EPEP_INST
#include "epep.h"
```

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
