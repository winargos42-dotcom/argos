---
argos_import: project_file
source_path: llama.cpp/examples/embedding/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\embedding\CMakeLists.txt
source_ext: .txt
source_sha256: a6aa77d0840b5f4b253a6ddefc086d8ab425faafa3e57111ed1537023da5f3c9
text_sha256: 1cf460f35453625d5399d6b9d115f56ee8e388a0fc0939b0e6e95ac2e6216c56
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# CMakeLists.txt

- Source: `llama.cpp/examples/embedding/CMakeLists.txt`
- Extract: `text`
- SHA256: `a6aa77d0840b5f4b253a6ddefc086d8ab425faafa3e57111ed1537023da5f3c9`

## Content

set(TARGET llama-embedding)
add_executable(${TARGET} embedding.cpp)
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
