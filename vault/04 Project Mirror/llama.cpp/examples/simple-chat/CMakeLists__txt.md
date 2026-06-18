---
argos_import: project_file
source_path: llama.cpp/examples/simple-chat/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\simple-chat\CMakeLists.txt
source_ext: .txt
source_sha256: fc7db399191ea893221748abc2107d28c146871d00069590d7da92206b96883d
text_sha256: d938b71d4de5058258d71b1c3264f476a9786195bd0bc84fd9ac1e840b51f3d2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/simple-chat/CMakeLists.txt`
- Extract: `text`
- SHA256: `fc7db399191ea893221748abc2107d28c146871d00069590d7da92206b96883d`

## Content

set(TARGET llama-simple-chat)
add_executable(${TARGET} simple-chat.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE llama ${CMAKE_THREAD_LIBS_INIT})
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
