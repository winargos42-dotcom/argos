---
argos_import: project_file
source_path: llama.cpp/tools/llama-bench/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\llama-bench\CMakeLists.txt
source_ext: .txt
source_sha256: c362e315a326759f8edecac771169f2d3748c4e7ff826467c2de3d5a9137247f
text_sha256: 2cdd19234c575c0065c37d479d6ef6f4558b7a41ecdb0107bf8e7ccf5f5fcdcc
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/tools/llama-bench/CMakeLists.txt`
- Extract: `text`
- SHA256: `c362e315a326759f8edecac771169f2d3748c4e7ff826467c2de3d5a9137247f`

## Content

set(TARGET llama-bench)
add_executable(${TARGET} llama-bench.cpp)
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
