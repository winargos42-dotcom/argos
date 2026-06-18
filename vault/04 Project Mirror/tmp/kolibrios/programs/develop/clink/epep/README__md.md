---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/clink/epep/README.md
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\clink\epep\README.md
source_ext: .md
source_sha256: 15e08b53362a56a23842d5c16c79e9461980b9ae55a90f2d33522e28cf414284
text_sha256: aa597bb630cc9ef5214da9fc930d43e6df2654be72d04f07ce22160676bd5241
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:42
---

# README.md

- Source: `tmp/kolibrios/programs/develop/clink/epep/README.md`
- Extract: `text`
- SHA256: `15e08b53362a56a23842d5c16c79e9461980b9ae55a90f2d33522e28cf414284`

## Content

# epep - Embeddable PE Parser
## Features

- PE header (including Data Directories as a part Optional Header)
- Section Headers
- COFF Symbols
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
