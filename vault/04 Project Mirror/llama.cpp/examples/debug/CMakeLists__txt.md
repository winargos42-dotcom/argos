---
argos_import: project_file
source_path: llama.cpp/examples/debug/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\debug\CMakeLists.txt
source_ext: .txt
source_sha256: b40eac769ccfee60c1d828d65cd41bad18e29de26dbe2d73636a28bdb90e7359
text_sha256: 71624de72a3fc484849b4f2b696d5429cdff31468a805484d7ad6ad7ec88f80f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# CMakeLists.txt

- Source: `llama.cpp/examples/debug/CMakeLists.txt`
- Extract: `text`
- SHA256: `b40eac769ccfee60c1d828d65cd41bad18e29de26dbe2d73636a28bdb90e7359`

## Content

set(TARGET llama-debug)
add_executable(${TARGET} debug.cpp)
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
