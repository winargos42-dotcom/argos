---
argos_import: project_file
source_path: llama.cpp/examples/simple/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\simple\CMakeLists.txt
source_ext: .txt
source_sha256: aaa4be64d3f97e2c552f4b93b86b952a7707299413e1c7b8e7bb1f7c628e9211
text_sha256: c4acc5493295ac4b9a1223f60004e6ea5b054efd75d5f3dc498032c464b24817
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/simple/CMakeLists.txt`
- Extract: `text`
- SHA256: `aaa4be64d3f97e2c552f4b93b86b952a7707299413e1c7b8e7bb1f7c628e9211`

## Content

set(TARGET llama-simple)
add_executable(${TARGET} simple.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE llama ${CMAKE_THREAD_LIBS_INIT})
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
