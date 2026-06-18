---
argos_import: project_file
source_path: llama.cpp/examples/save-load-state/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\save-load-state\CMakeLists.txt
source_ext: .txt
source_sha256: d9dd3b32accab1498aba0b6bbae5a9b05f283a15baa6dd1dc28a661ed4145794
text_sha256: bb2b0a094dd1f26b548e497bc17cfa11c0c42fc7b967c4619e0e38a02a3acd43
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/save-load-state/CMakeLists.txt`
- Extract: `text`
- SHA256: `d9dd3b32accab1498aba0b6bbae5a9b05f283a15baa6dd1dc28a661ed4145794`

## Content

set(TARGET llama-save-load-state)
add_executable(${TARGET} save-load-state.cpp)
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
