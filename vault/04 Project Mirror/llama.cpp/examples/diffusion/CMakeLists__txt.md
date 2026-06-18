---
argos_import: project_file
source_path: llama.cpp/examples/diffusion/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\diffusion\CMakeLists.txt
source_ext: .txt
source_sha256: b22e34febbb299900a58503f7c5ee7eb601374e012ed9d15c7dfc9c138b50938
text_sha256: 715846c918b56cd585d0d8511ea675629386e623bee917a9e68148e0b1ddf960
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# CMakeLists.txt

- Source: `llama.cpp/examples/diffusion/CMakeLists.txt`
- Extract: `text`
- SHA256: `b22e34febbb299900a58503f7c5ee7eb601374e012ed9d15c7dfc9c138b50938`

## Content

set(TARGET llama-diffusion-cli)
add_executable(${TARGET} diffusion-cli.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE llama llama-common ${CMAKE_THREAD_LIBS_INIT})
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
