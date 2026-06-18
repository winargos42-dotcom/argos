---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-10.6.0/src/gallium/tests/graw/geometry-shader/mov-cb-2d.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-10.6.0\src\gallium\tests\graw\geometry-shader\mov-cb-2d.txt
source_ext: .txt
source_sha256: 7cb80d5fa59fa7f6cbc643ee280cf3b645a6c8eff2ba847166a7680f1b5282b0
text_sha256: 1f34542e4756cddd8e79034d3df484d7aa73ec57881056992ad1f9b4f9ad3c80
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:33
---

# mov-cb-2d.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-10.6.0/src/gallium/tests/graw/geometry-shader/mov-cb-2d.txt`
- Extract: `text`
- SHA256: `7cb80d5fa59fa7f6cbc643ee280cf3b645a6c8eff2ba847166a7680f1b5282b0`

## Content

GEOM
PROPERTY GS_INPUT_PRIMITIVE TRIANGLES
PROPERTY GS_OUTPUT_PRIMITIVE TRIANGLE_STRIP
PROPERTY GS_MAX_OUTPUT_VERTICES 3
DCL IN[][0], POSITION, CONSTANT
DCL IN[][1], COLOR, CONSTANT
DCL OUT[0], POSITION, CONSTANT
DCL OUT[1], COLOR, CONSTANT
DCL CONST[1][0..6]

MOV OUT[0], IN[0][0]
MOV OUT[1], CONST[1][0]
EMIT

MOV OUT[0], IN[1][0]
MOV OUT[1], CONST[1][1]
EMIT

MOV OUT[0], IN[2][0]
MOV OUT[1], CONST[1][4]
EMIT

ENDPRIM

END

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
