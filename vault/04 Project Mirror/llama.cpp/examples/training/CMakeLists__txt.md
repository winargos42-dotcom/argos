---
argos_import: project_file
source_path: llama.cpp/examples/training/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\training\CMakeLists.txt
source_ext: .txt
source_sha256: 099b4202e1ab49cba7c6b3e4a0b7c6f077d967ecacf45dc26f4e1df0d095844d
text_sha256: 4a51519d6982603238d45030d5333c30128f36dc187acd1d3826063920b9281c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/training/CMakeLists.txt`
- Extract: `text`
- SHA256: `099b4202e1ab49cba7c6b3e4a0b7c6f077d967ecacf45dc26f4e1df0d095844d`

## Content

set(TARGET llama-finetune)
add_executable(${TARGET} finetune.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_11)

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Training Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Training Hub]]
