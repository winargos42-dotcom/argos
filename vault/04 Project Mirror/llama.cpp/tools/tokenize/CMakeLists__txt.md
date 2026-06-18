---
argos_import: project_file
source_path: llama.cpp/tools/tokenize/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\tokenize\CMakeLists.txt
source_ext: .txt
source_sha256: 6b3679cb32b1bc0a75e855801a10460114f71d96ace24d8c9d748146dcdf8acd
text_sha256: 075b45f7115774dd35e22d1235301081ec2b298b3ed27bf414ee015ce457e9ee
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# CMakeLists.txt

- Source: `llama.cpp/tools/tokenize/CMakeLists.txt`
- Extract: `text`
- SHA256: `6b3679cb32b1bc0a75e855801a10460114f71d96ace24d8c9d748146dcdf8acd`

## Content

set(TARGET llama-tokenize)
add_executable(${TARGET} tokenize.cpp)
if(LLAMA_TOOLS_INSTALL)
    install(TARGETS ${TARGET} RUNTIME)
endif()
target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

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
