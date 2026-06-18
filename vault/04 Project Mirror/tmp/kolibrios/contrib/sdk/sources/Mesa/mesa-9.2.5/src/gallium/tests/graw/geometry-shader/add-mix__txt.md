---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/src/gallium/tests/graw/geometry-shader/add-mix.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-9.2.5\src\gallium\tests\graw\geometry-shader\add-mix.txt
source_ext: .txt
source_sha256: 9a1122dc5682c0c8ce0c9df5fe91f8756f0195e3ee35f80e1106f1a0819500da
text_sha256: 424f1e1242212a8d2147d2a0e07b4898cc2d80cd9ff2deac7868aa8af9cc21ef
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:35
---

# add-mix.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/src/gallium/tests/graw/geometry-shader/add-mix.txt`
- Extract: `text`
- SHA256: `9a1122dc5682c0c8ce0c9df5fe91f8756f0195e3ee35f80e1106f1a0819500da`

## Content

GEOM
PROPERTY GS_INPUT_PRIMITIVE TRIANGLES
PROPERTY GS_OUTPUT_PRIMITIVE TRIANGLE_STRIP
PROPERTY GS_MAX_OUTPUT_VERTICES 3
DCL IN[][0], POSITION, CONSTANT
DCL IN[][1], COLOR, CONSTANT
DCL OUT[0], POSITION, CONSTANT
DCL OUT[1], COLOR, CONSTANT

MOV OUT[0], IN[0][0]
ADD OUT[1], IN[0][1], IN[1][1]
EMIT

MOV OUT[0], IN[1][0]
ADD OUT[1], IN[1][1], IN[2][1]
EMIT

MOV OUT[0], IN[2][0]
ADD OUT[1], IN[2][1], IN[0][1]
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
