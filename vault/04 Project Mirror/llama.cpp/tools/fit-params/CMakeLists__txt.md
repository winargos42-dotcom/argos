---
argos_import: project_file
source_path: llama.cpp/tools/fit-params/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\fit-params\CMakeLists.txt
source_ext: .txt
source_sha256: a32483a9c30cadbb99d12e432aecc8a91754468aa2d08dc1ddcb6e0647167b9e
text_sha256: e18bd367642fcf87f08d67c17d0b32d5f449d06c2b7e32be0c988b3ab77ac997
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/tools/fit-params/CMakeLists.txt`
- Extract: `text`
- SHA256: `a32483a9c30cadbb99d12e432aecc8a91754468aa2d08dc1ddcb6e0647167b9e`

## Content

set(TARGET llama-fit-params)
add_executable(${TARGET} fit-params.cpp)
target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

if(LLAMA_TOOLS_INSTALL)
    install(TARGETS ${TARGET} RUNTIME)
endif()

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
