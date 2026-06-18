---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/src/gallium/tests/graw/geometry-shader/add.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-9.2.5\src\gallium\tests\graw\geometry-shader\add.txt
source_ext: .txt
source_sha256: 7bae220c368d6cbcb1dde988dd76d669e0421da39692c37176a45d8da5156b7a
text_sha256: d79cfc1f6a1e950c23f810f6c72c6233179f40e7872b58a4a91e0cb862f75c3f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:35
---

# add.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/src/gallium/tests/graw/geometry-shader/add.txt`
- Extract: `text`
- SHA256: `7bae220c368d6cbcb1dde988dd76d669e0421da39692c37176a45d8da5156b7a`

## Content

GEOM
PROPERTY GS_INPUT_PRIMITIVE TRIANGLES
PROPERTY GS_OUTPUT_PRIMITIVE LINE_STRIP
PROPERTY GS_MAX_OUTPUT_VERTICES 3
DCL IN[][0], POSITION, CONSTANT
DCL IN[][1], COLOR, CONSTANT
DCL OUT[0], POSITION, CONSTANT
DCL OUT[1], COLOR, CONSTANT

MOV OUT[0], IN[0][0]
ADD OUT[1], IN[0][1], IN[0][1]
EMIT

MOV OUT[0], IN[1][0]
ADD OUT[1], IN[1][1], IN[1][1]
EMIT

MOV OUT[0], IN[2][0]
ADD OUT[1], IN[2][1], IN[2][1]
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
