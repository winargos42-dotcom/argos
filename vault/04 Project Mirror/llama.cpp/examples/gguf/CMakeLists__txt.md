---
argos_import: project_file
source_path: llama.cpp/examples/gguf/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\gguf\CMakeLists.txt
source_ext: .txt
source_sha256: cb042cd41af20e13a432f4115e4b489f42480aaea30b7f8035a48837544be306
text_sha256: 88385c090deb2b2778f539ac346a8d352a66613352165e6fbc1eea5aa9df28a6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# CMakeLists.txt

- Source: `llama.cpp/examples/gguf/CMakeLists.txt`
- Extract: `text`
- SHA256: `cb042cd41af20e13a432f4115e4b489f42480aaea30b7f8035a48837544be306`

## Content

set(TARGET llama-gguf)
add_executable(${TARGET} gguf.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE ggml ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

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
