---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-10.6.0/src/gallium/tests/graw/geometry-shader/line.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-10.6.0\src\gallium\tests\graw\geometry-shader\line.txt
source_ext: .txt
source_sha256: 1b90c57a224006d296f1258d24550bea87ddc070a882e6316d05272f84e40316
text_sha256: 7b0c36faaaa81273aa5fac0fd7d0e9d5da70b43f2faf65f07fed44f09b48da7f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:33
---

# line.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-10.6.0/src/gallium/tests/graw/geometry-shader/line.txt`
- Extract: `text`
- SHA256: `1b90c57a224006d296f1258d24550bea87ddc070a882e6316d05272f84e40316`

## Content

GEOM
PROPERTY GS_INPUT_PRIMITIVE TRIANGLES
PROPERTY GS_OUTPUT_PRIMITIVE LINE_STRIP
PROPERTY GS_MAX_OUTPUT_VERTICES 4
DCL IN[][0], POSITION, CONSTANT
DCL IN[][1], COLOR, CONSTANT
DCL OUT[0], POSITION, CONSTANT
DCL OUT[1], COLOR, CONSTANT

MOV OUT[0], IN[0][0]
MOV OUT[1], IN[0][1]
EMIT

MOV OUT[0], IN[1][0]
MOV OUT[1], IN[0][1]
EMIT

MOV OUT[0], IN[2][0]
MOV OUT[1], IN[2][1]
EMIT

MOV OUT[0], IN[0][0]
MOV OUT[1], IN[0][1]
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
