---
argos_import: project_file
source_path: llama.cpp/tools/completion/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\completion\CMakeLists.txt
source_ext: .txt
source_sha256: dfbd210c73e0032833dc364b544f1bdb969b6c3c30d661af9a96e7f63d2e17a2
text_sha256: 32343744001cdb0067cf16e8bc5f754cfb7e433d777f06c6ebb43bd09b32d67c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/tools/completion/CMakeLists.txt`
- Extract: `text`
- SHA256: `dfbd210c73e0032833dc364b544f1bdb969b6c3c30d661af9a96e7f63d2e17a2`

## Content

set(TARGET llama-completion)
add_executable(${TARGET} completion.cpp)
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
