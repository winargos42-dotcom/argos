---
argos_import: project_file
source_path: llama.cpp/examples/convert-llama2c-to-ggml/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\convert-llama2c-to-ggml\CMakeLists.txt
source_ext: .txt
source_sha256: 0a7e41b667be2846381cf169421d23cf1248d3d73b7d028f03c352ee06f92054
text_sha256: 979f8e1641b53b6fa29afebce017091e061914ae5f5fcdf5b6c687dd94d37645
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# CMakeLists.txt

- Source: `llama.cpp/examples/convert-llama2c-to-ggml/CMakeLists.txt`
- Extract: `text`
- SHA256: `0a7e41b667be2846381cf169421d23cf1248d3d73b7d028f03c352ee06f92054`

## Content

set(TARGET llama-convert-llama2c-to-ggml)
add_executable(${TARGET} convert-llama2c-to-ggml.cpp)
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
