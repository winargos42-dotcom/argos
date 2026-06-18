---
argos_import: project_file
source_path: llama.cpp/tools/imatrix/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\imatrix\CMakeLists.txt
source_ext: .txt
source_sha256: 7e347d2633bffc86619e01d837f2936981bb0a8db37fcd522765027ebfcf7de2
text_sha256: 6c0fe64d9aa4a3712f97f24ac2cc58fe64a0aeb5caecc33c4c57473cfdfba0f8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/tools/imatrix/CMakeLists.txt`
- Extract: `text`
- SHA256: `7e347d2633bffc86619e01d837f2936981bb0a8db37fcd522765027ebfcf7de2`

## Content

set(TARGET llama-imatrix)
add_executable(${TARGET} imatrix.cpp)
target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

if(LLAMA_TOOLS_INSTALL)
    install(TARGETS ${TARGET} RUNTIME)
endif()

if (CMAKE_SYSTEM_NAME MATCHES "AIX")
    # AIX's flock() function comes from libbsd.a
    target_link_libraries(${TARGET} PRIVATE -lbsd)
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
