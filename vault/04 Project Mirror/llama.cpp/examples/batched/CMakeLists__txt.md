---
argos_import: project_file
source_path: llama.cpp/examples/batched/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\batched\CMakeLists.txt
source_ext: .txt
source_sha256: cf31fc3ffe9c8b1cfa9196e3cacb2339f3b9bd1897c1401ca5a10674ba5d1107
text_sha256: c7fdbb56aa7daca62ac30b202309e77c1738252fa27dd97463cc04178dd28b5d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# CMakeLists.txt

- Source: `llama.cpp/examples/batched/CMakeLists.txt`
- Extract: `text`
- SHA256: `cf31fc3ffe9c8b1cfa9196e3cacb2339f3b9bd1897c1401ca5a10674ba5d1107`

## Content

set(TARGET llama-batched)
add_executable(${TARGET} batched.cpp)
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
