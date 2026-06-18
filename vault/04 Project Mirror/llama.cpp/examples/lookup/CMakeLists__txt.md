---
argos_import: project_file
source_path: llama.cpp/examples/lookup/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\lookup\CMakeLists.txt
source_ext: .txt
source_sha256: 7524bae5f7bb8599d7fb2ab8907a189617e43cb92def2c340dfabb42b1b363da
text_sha256: 1b02f01a4b7a4ef90a97684ccdf711560300b83dfafbe21d35ddbe26165d29a5
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/lookup/CMakeLists.txt`
- Extract: `text`
- SHA256: `7524bae5f7bb8599d7fb2ab8907a189617e43cb92def2c340dfabb42b1b363da`

## Content

set(TARGET llama-lookup)
add_executable(${TARGET} lookup.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

set(TARGET llama-lookup-create)
add_executable(${TARGET} lookup-create.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

set(TARGET llama-lookup-merge)
add_executable(${TARGET} lookup-merge.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

set(TARGET llama-lookup-stats)
add_executable(${TARGET} lookup-stats.cpp)
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
