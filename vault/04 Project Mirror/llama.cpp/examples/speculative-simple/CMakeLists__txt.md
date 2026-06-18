---
argos_import: project_file
source_path: llama.cpp/examples/speculative-simple/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\speculative-simple\CMakeLists.txt
source_ext: .txt
source_sha256: 162a3973b5ac7f59f16f88d8b51e5776c1a7e8ea41cc70122de8606184a3f4c1
text_sha256: e8939bcec6e731ce051f7311fe63595d6e1916c543ce4ee9001b9c13a80c6468
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/speculative-simple/CMakeLists.txt`
- Extract: `text`
- SHA256: `162a3973b5ac7f59f16f88d8b51e5776c1a7e8ea41cc70122de8606184a3f4c1`

## Content

set(TARGET llama-speculative-simple)
add_executable(${TARGET} speculative-simple.cpp)
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
