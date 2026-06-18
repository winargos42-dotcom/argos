---
argos_import: project_file
source_path: llama.cpp/tools/perplexity/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\perplexity\CMakeLists.txt
source_ext: .txt
source_sha256: b969dd0ca9bcf7d96e69f201b83a7faba1dd94f3d7cdb019995985b1fd43a940
text_sha256: ba8421eedc40c1309f757904a8469821a9bea439422530f97206ce8861dffc87
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# CMakeLists.txt

- Source: `llama.cpp/tools/perplexity/CMakeLists.txt`
- Extract: `text`
- SHA256: `b969dd0ca9bcf7d96e69f201b83a7faba1dd94f3d7cdb019995985b1fd43a940`

## Content

set(TARGET llama-perplexity)
add_executable(${TARGET} perplexity.cpp)
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
