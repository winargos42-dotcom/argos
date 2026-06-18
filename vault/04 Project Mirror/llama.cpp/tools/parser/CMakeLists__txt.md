---
argos_import: project_file
source_path: llama.cpp/tools/parser/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\parser\CMakeLists.txt
source_ext: .txt
source_sha256: 0862a28adb2a2babf6038b4bb0d1fa722ebe13d0859cc4890aea40420d27ddab
text_sha256: a783ea61cf4767c2c2f92d78628a80e5f5fce86fe2326065fd946f9f2888a9a0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# CMakeLists.txt

- Source: `llama.cpp/tools/parser/CMakeLists.txt`
- Extract: `text`
- SHA256: `0862a28adb2a2babf6038b4bb0d1fa722ebe13d0859cc4890aea40420d27ddab`

## Content

if (NOT WIN32 OR NOT BUILD_SHARED_LIBS)
    # this tool is disabled on Windows when building with shared libraries because it uses internal functions not exported with LLAMA_API
    set(TARGET llama-debug-template-parser)
    add_executable(${TARGET} debug-template-parser.cpp)
    target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
    target_compile_features(${TARGET} PRIVATE cxx_std_17)

    if(LLAMA_TOOLS_INSTALL)
        install(TARGETS ${TARGET} RUNTIME)
    endif()
endif()

set(TARGET llama-template-analysis)
add_executable(${TARGET} template-analysis.cpp)
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
