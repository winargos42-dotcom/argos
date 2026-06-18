---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/src/gallium/tests/graw/geometry-shader/mov.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-9.2.5\src\gallium\tests\graw\geometry-shader\mov.txt
source_ext: .txt
source_sha256: 599c5cab6c870e2221a8a84a83666a1fd1b60cb5ef5e1adf2d132de23aa76ba3
text_sha256: be08ddd025e3bc0dc9947356c57b002bfb502fce4a1fe078b4de906a0073ff09
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:35
---

# mov.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/src/gallium/tests/graw/geometry-shader/mov.txt`
- Extract: `text`
- SHA256: `599c5cab6c870e2221a8a84a83666a1fd1b60cb5ef5e1adf2d132de23aa76ba3`

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
MOV OUT[1], IN[0][1]
EMIT

MOV OUT[0], IN[1][0]
MOV OUT[1], IN[1][1]
EMIT

MOV OUT[0], IN[2][0]
MOV OUT[1], IN[2][1]
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
