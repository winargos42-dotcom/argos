---
argos_import: project_file
source_path: llama.cpp/tools/rpc/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\rpc\CMakeLists.txt
source_ext: .txt
source_sha256: 33c38df61e6aa5509b3b3c4929bdbd22eb206746ee3cd7e4d55139f77fe75829
text_sha256: 92a073869e532364bc3cc811a0324e0e750f5d6b1fe16d412fe82d6d644f20a1
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# CMakeLists.txt

- Source: `llama.cpp/tools/rpc/CMakeLists.txt`
- Extract: `text`
- SHA256: `33c38df61e6aa5509b3b3c4929bdbd22eb206746ee3cd7e4d55139f77fe75829`

## Content

set(TARGET rpc-server)
add_executable(${TARGET} rpc-server.cpp)
target_link_libraries(${TARGET} PRIVATE ggml)
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
