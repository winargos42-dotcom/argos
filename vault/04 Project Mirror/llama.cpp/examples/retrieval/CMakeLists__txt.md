---
argos_import: project_file
source_path: llama.cpp/examples/retrieval/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\retrieval\CMakeLists.txt
source_ext: .txt
source_sha256: bfae8331bfe068c6ef897f8bac946b217a63fcd2c95b12c37f0bd86926eb081a
text_sha256: 115bede727d6955484ed32c0deb755aa31bbbdcdc65e367ea39ead4e8226ab51
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/retrieval/CMakeLists.txt`
- Extract: `text`
- SHA256: `bfae8331bfe068c6ef897f8bac946b217a63fcd2c95b12c37f0bd86926eb081a`

## Content

set(TARGET llama-retrieval)
add_executable(${TARGET} retrieval.cpp)
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
