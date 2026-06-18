---
argos_import: project_file
source_path: llama.cpp/tools/cli/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\cli\CMakeLists.txt
source_ext: .txt
source_sha256: dae0299a7d2aba3feb8c18ff8f565715acaf2f40651149adc6633df6b53d4f0b
text_sha256: 0af665c052ca6b89c3f6600b85ebee9183b928821f6ebec37dc2495cacd94917
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/tools/cli/CMakeLists.txt`
- Extract: `text`
- SHA256: `dae0299a7d2aba3feb8c18ff8f565715acaf2f40651149adc6633df6b53d4f0b`

## Content

set(TARGET llama-cli)
add_executable(${TARGET} cli.cpp)
target_link_libraries(${TARGET} PRIVATE server-context PUBLIC llama-common ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

include_directories(../server)

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
