---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/src/gallium/tests/graw/geometry-shader/multi-line.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-9.2.5\src\gallium\tests\graw\geometry-shader\multi-line.txt
source_ext: .txt
source_sha256: 87b475397ba3d5bded2060c9354b7f73dcde60c3feb5d49a4692c71a9b85e106
text_sha256: 179661c4f9b024282ca85d4bca24236472811b6adcd63b01e6bb1c6420f5dfb7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:35
---

# multi-line.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/src/gallium/tests/graw/geometry-shader/multi-line.txt`
- Extract: `text`
- SHA256: `87b475397ba3d5bded2060c9354b7f73dcde60c3feb5d49a4692c71a9b85e106`

## Content

GEOM
PROPERTY GS_INPUT_PRIMITIVE TRIANGLES
PROPERTY GS_OUTPUT_PRIMITIVE LINE_STRIP
PROPERTY GS_MAX_OUTPUT_VERTICES 8
DCL IN[][0], POSITION, CONSTANT
DCL IN[][1], COLOR, CONSTANT
DCL OUT[0], POSITION, CONSTANT
DCL OUT[1], COLOR, CONSTANT
DCL TEMP[0]

MOV TEMP[0], IN[0][0]
ADD TEMP[0].y, IN[0][0], IN[1][0]

MOV OUT[0], TEMP[0]
MOV OUT[1], IN[0][1]
EMIT
MOV OUT[0], IN[2][0]
MOV OUT[1], IN[0][1]
EMIT
MOV OUT[0], IN[0][0]
MOV OUT[1], IN[2][1]
EMIT
MOV OUT[0], TEMP[0]
MOV OUT[1], IN[0][1]
EMIT
ENDPRIM

MOV OUT[0], TEMP[0]
MOV OUT[1], IN[0][1]
EMIT
MOV OUT[0], IN[2][0]
MOV OUT[1], IN[0][1]
EMIT
MOV OUT[0], IN[1][0]
MOV OUT[1], IN[2][1]
EMIT
MOV OUT[0], TEMP[0]
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
