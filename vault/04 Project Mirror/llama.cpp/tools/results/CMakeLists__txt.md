---
argos_import: project_file
source_path: llama.cpp/tools/results/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\tools\results\CMakeLists.txt
source_ext: .txt
source_sha256: 58766a76682535e705dc4831dd43396bdbd2014739d1fe89fdd734d729b959ad
text_sha256: e1099836927d01c95d7e55a42a876f766453e743b395eabe85c08b3627d04e1e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# CMakeLists.txt

- Source: `llama.cpp/tools/results/CMakeLists.txt`
- Extract: `text`
- SHA256: `58766a76682535e705dc4831dd43396bdbd2014739d1fe89fdd734d729b959ad`

## Content

set(TARGET llama-results)
add_executable(${TARGET} results.cpp)
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
