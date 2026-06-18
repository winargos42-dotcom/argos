---
argos_import: project_file
source_path: llama.cpp/tools/cvector-generator/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\cvector-generator\CMakeLists.txt
source_ext: .txt
source_sha256: 991cf6cd9792f0751a95a9d5ca80bbaa95c8165a289cafb393a5311eab420976
text_sha256: 40b16b58e0ab662efc5089a4e5a6e72ef79f9adbb8e3dda892561788385b88c0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/tools/cvector-generator/CMakeLists.txt`
- Extract: `text`
- SHA256: `991cf6cd9792f0751a95a9d5ca80bbaa95c8165a289cafb393a5311eab420976`

## Content

set(TARGET llama-cvector-generator)
add_executable(${TARGET} cvector-generator.cpp pca.hpp)
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
