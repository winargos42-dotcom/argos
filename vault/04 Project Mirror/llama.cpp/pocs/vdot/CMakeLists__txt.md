---
argos_import: project_file
source_path: llama.cpp/pocs/vdot/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\pocs\vdot\CMakeLists.txt
source_ext: .txt
source_sha256: 77085c0b46fbf4c67f629692ff86b9fc7418856b737959d47b794a811109f0f4
text_sha256: 7aea4bb7bc71605f62c044ef5320cdbb3242a97fb057292b3cb1ef8a45d46c6b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/pocs/vdot/CMakeLists.txt`
- Extract: `text`
- SHA256: `77085c0b46fbf4c67f629692ff86b9fc7418856b737959d47b794a811109f0f4`

## Content

set(TARGET llama-vdot)
add_executable(${TARGET} vdot.cpp)
target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

set(TARGET llama-q8dot)
add_executable(${TARGET} q8dot.cpp)
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
