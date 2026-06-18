---
argos_import: project_file
source_path: llama.cpp/examples/speculative/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\speculative\CMakeLists.txt
source_ext: .txt
source_sha256: bbb988b92227d80b7c95398097d7b71216ceca6f507573ae77430c7ddf57b265
text_sha256: 15d32bd07f65b4bb1e35b7e9e08ed59d621473cc16e47206426b2b6589b62008
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/speculative/CMakeLists.txt`
- Extract: `text`
- SHA256: `bbb988b92227d80b7c95398097d7b71216ceca6f507573ae77430c7ddf57b265`

## Content

set(TARGET llama-speculative)
add_executable(${TARGET} speculative.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

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
