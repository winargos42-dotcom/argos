---
argos_import: project_file
source_path: llama.cpp/examples/sycl/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\sycl\CMakeLists.txt
source_ext: .txt
source_sha256: fba84c0f76d76a0895c3308e0efa3fa4413cddfa66740aa41aff50737ce838b0
text_sha256: d2705afee47e2d677f7c7f89645bb4b42b65d11cb7e45ef6b16c0bc8cd2bc177
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/examples/sycl/CMakeLists.txt`
- Extract: `text`
- SHA256: `fba84c0f76d76a0895c3308e0efa3fa4413cddfa66740aa41aff50737ce838b0`

## Content

#  MIT license
#  Copyright (C) 2024 Intel Corporation
#  SPDX-License-Identifier: MIT

set(TARGET llama-ls-sycl-device)
add_executable(${TARGET} ls-sycl-device.cpp)
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
