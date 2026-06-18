---
argos_import: project_file
source_path: llama.cpp/tools/gguf-split/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\gguf-split\CMakeLists.txt
source_ext: .txt
source_sha256: cb23b6f87862bec10d01c9cefad6daeacd35586eb27aa6d42fdf87a36580f146
text_sha256: 82a4bacd338ebb2bf2b1f566e9fa81c6e36c64ad49b91d771e8151aec7830721
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/tools/gguf-split/CMakeLists.txt`
- Extract: `text`
- SHA256: `cb23b6f87862bec10d01c9cefad6daeacd35586eb27aa6d42fdf87a36580f146`

## Content

set(TARGET llama-gguf-split)
add_executable(${TARGET} gguf-split.cpp)
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
