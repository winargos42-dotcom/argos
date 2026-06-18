---
argos_import: project_file
source_path: llama.cpp/tools/export-lora/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\export-lora\CMakeLists.txt
source_ext: .txt
source_sha256: ad766ac371536d2903aa15895a13d7830b6391e63172b4d77c405b93723a00c2
text_sha256: e86289a064c28bfe45ac0bcabe492157a49a73b224d123fd0a2b7d8ef8abab57
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/tools/export-lora/CMakeLists.txt`
- Extract: `text`
- SHA256: `ad766ac371536d2903aa15895a13d7830b6391e63172b4d77c405b93723a00c2`

## Content

set(TARGET llama-export-lora)
add_executable(${TARGET} export-lora.cpp)
target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

if(LLAMA_TOOLS_INSTALL)
    install(TARGETS ${TARGET} RUNTIME)
endif()

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Training Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Training Hub]]
