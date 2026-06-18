---
argos_import: project_file
source_path: llama.cpp/tools/batched-bench/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\batched-bench\CMakeLists.txt
source_ext: .txt
source_sha256: b506deb66cf08a5712da0cf5aa82cfb5e6a9dfa0dfe3baf028146791fe77df6c
text_sha256: 41f7481dc5e680493aaf0e3caf127d8bbdbb96533791f5516164c1b5f9ab8c30
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/tools/batched-bench/CMakeLists.txt`
- Extract: `text`
- SHA256: `b506deb66cf08a5712da0cf5aa82cfb5e6a9dfa0dfe3baf028146791fe77df6c`

## Content

set(TARGET llama-batched-bench)
add_executable(${TARGET} batched-bench.cpp)
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
