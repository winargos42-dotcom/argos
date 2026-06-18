---
argos_import: project_file
source_path: llama.cpp/examples/parallel/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\parallel\CMakeLists.txt
source_ext: .txt
source_sha256: 01c811b21b8160ae2d945be64caf50349c057f541692be1f393972cce35d05e2
text_sha256: dceb77b9d969a0dd3f3d16903c0d7705a148f4ca723439e3122d9610d0579fbd
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/parallel/CMakeLists.txt`
- Extract: `text`
- SHA256: `01c811b21b8160ae2d945be64caf50349c057f541692be1f393972cce35d05e2`

## Content

set(TARGET llama-parallel)
add_executable(${TARGET} parallel.cpp)
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
