---
argos_import: project_file
source_path: llama.cpp/examples/gen-docs/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\gen-docs\CMakeLists.txt
source_ext: .txt
source_sha256: c1aaad6c17fa73b307bdeab45c472741733e8831ba4c51eb5c6dd213aad82879
text_sha256: 1a51f5893ace277af6164ac6501e5574bf7c1bb59092d3e66f5a63b7406ea710
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# CMakeLists.txt

- Source: `llama.cpp/examples/gen-docs/CMakeLists.txt`
- Extract: `text`
- SHA256: `c1aaad6c17fa73b307bdeab45c472741733e8831ba4c51eb5c6dd213aad82879`

## Content

set(TARGET llama-gen-docs)
add_executable(${TARGET} gen-docs.cpp)
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
