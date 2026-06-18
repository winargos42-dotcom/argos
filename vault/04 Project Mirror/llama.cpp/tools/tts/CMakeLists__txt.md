---
argos_import: project_file
source_path: llama.cpp/tools/tts/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\tts\CMakeLists.txt
source_ext: .txt
source_sha256: d1aeb523d3510a4bb96120e65d2d038030d5d05f580fb344dbda45315b4d2887
text_sha256: 66f37d1f9ba73a20bdf9a557b43b45ff34f99fd2fef9cdd2f17de6be0591d79d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# CMakeLists.txt

- Source: `llama.cpp/tools/tts/CMakeLists.txt`
- Extract: `text`
- SHA256: `d1aeb523d3510a4bb96120e65d2d038030d5d05f580fb344dbda45315b4d2887`

## Content

set(TARGET llama-tts)
add_executable(${TARGET} tts.cpp)
target_link_libraries(${TARGET} PRIVATE llama llama-common ${CMAKE_THREAD_LIBS_INIT})
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
