---
argos_import: project_file
source_path: llama.cpp/examples/simple-cmake-pkg/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\simple-cmake-pkg\CMakeLists.txt
source_ext: .txt
source_sha256: 397d6d7c02b4522310f144e0e885b1deb8e9de1f2b741f2f91dc0c522f40759c
text_sha256: bb2b3ed603d2f5e886413e2f0f0c4d4a3941ff1e422a279f01fbc864e0ef167a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/simple-cmake-pkg/CMakeLists.txt`
- Extract: `text`
- SHA256: `397d6d7c02b4522310f144e0e885b1deb8e9de1f2b741f2f91dc0c522f40759c`

## Content

cmake_minimum_required(VERSION 3.12)
project(llama-simple-cmake-pkg)

set(TARGET llama-simple-cmake-pkg)

find_package(Llama REQUIRED)

add_executable(${TARGET} ${CMAKE_CURRENT_LIST_DIR}/../simple/simple.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE llama ggml::all ${CMAKE_THREAD_LIBS_INIT})
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
