---
argos_import: project_file
source_path: llama.cpp/examples/idle/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\idle\CMakeLists.txt
source_ext: .txt
source_sha256: 0f845b4edeb73cd29b2b4593339b7c4629242500cdfee384c298a02c43d85efd
text_sha256: d5bb9f24883b5c75f6aaa9909b1ca8e2c74ab8572516fbb1f2fc3d992b77118e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# CMakeLists.txt

- Source: `llama.cpp/examples/idle/CMakeLists.txt`
- Extract: `text`
- SHA256: `0f845b4edeb73cd29b2b4593339b7c4629242500cdfee384c298a02c43d85efd`

## Content

set(TARGET llama-idle)
add_executable(${TARGET} idle.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE llama llama-common ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_11)

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
