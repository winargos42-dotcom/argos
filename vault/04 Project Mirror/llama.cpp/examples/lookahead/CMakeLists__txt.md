---
argos_import: project_file
source_path: llama.cpp/examples/lookahead/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\lookahead\CMakeLists.txt
source_ext: .txt
source_sha256: 7b01e0daef3d286f7bbd3b3970ea9b98864a28f20f99fc076f5e23301d878e23
text_sha256: 3235a9270094d67bfda33c3c0ac5fce981de35d33fdc8d8446775d224deca47d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/lookahead/CMakeLists.txt`
- Extract: `text`
- SHA256: `7b01e0daef3d286f7bbd3b3970ea9b98864a28f20f99fc076f5e23301d878e23`

## Content

set(TARGET llama-lookahead)
add_executable(${TARGET} lookahead.cpp)
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
