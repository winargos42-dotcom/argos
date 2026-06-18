---
argos_import: project_file
source_path: llama.cpp/examples/passkey/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\passkey\CMakeLists.txt
source_ext: .txt
source_sha256: 47ccb6e17ff7dcd36358a29f4a93b70c0e1dd8f3f4cf3ad3a87f49e86805e231
text_sha256: fe2666390ccb9c1707c6bfdbb2703369bdb8da4cb950b0ca0084feda9a331d5e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/passkey/CMakeLists.txt`
- Extract: `text`
- SHA256: `47ccb6e17ff7dcd36358a29f4a93b70c0e1dd8f3f4cf3ad3a87f49e86805e231`

## Content

set(TARGET llama-passkey)
add_executable(${TARGET} passkey.cpp)
install(TARGETS ${TARGET} RUNTIME)
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
