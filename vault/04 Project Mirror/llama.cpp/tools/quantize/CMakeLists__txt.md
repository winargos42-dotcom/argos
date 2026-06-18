---
argos_import: project_file
source_path: llama.cpp/tools/quantize/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\quantize\CMakeLists.txt
source_ext: .txt
source_sha256: ef86d9d2be39fc2ebc64e9b7827ba1225f7e4ac563ed673e3fd46af009d85ddb
text_sha256: 98b366a3b7cac4be2018cd00ecf4de474ede2317499cd3d5359ed594cb6d9c6b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# CMakeLists.txt

- Source: `llama.cpp/tools/quantize/CMakeLists.txt`
- Extract: `text`
- SHA256: `ef86d9d2be39fc2ebc64e9b7827ba1225f7e4ac563ed673e3fd46af009d85ddb`

## Content

set(TARGET llama-quantize)
add_executable(${TARGET} quantize.cpp)
target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
target_include_directories(${TARGET} PRIVATE ../../common)
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
