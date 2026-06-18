---
argos_import: project_file
source_path: tmp/kolibrios/programs/bcc32/patch/compile.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\bcc32\patch\compile.txt
source_ext: .txt
source_sha256: b113a4f5538346c113e9f831f618d82f5cd95325fbfda93105492cc3c3457767
text_sha256: 99907b02539b01c0c2e7c88886dcebad77d1bd45a0dcc01f66483db36ebf324b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:42
---

# compile.txt

- Source: `tmp/kolibrios/programs/bcc32/patch/compile.txt`
- Extract: `text`
- SHA256: `b113a4f5538346c113e9f831f618d82f5cd95325fbfda93105492cc3c3457767`

## Content

В файле kos32-bcc.asm находится патч для компилятора Borland C++ 5.5.1.
После применения данного патча компилятор в режиме компиляции с опцией '-S'
выдает *.asm файлы с синтаксисом более похожим на ассемблер fasm.

Применение:
fasm kos32-bcc.asm kos32-bcc.exe

bcc32.exe должен лежать рядом с kos32-bcc.asm

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
