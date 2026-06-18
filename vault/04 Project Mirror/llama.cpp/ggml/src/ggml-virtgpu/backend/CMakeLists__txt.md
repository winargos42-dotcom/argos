---
argos_import: project_file
source_path: llama.cpp/ggml/src/ggml-virtgpu/backend/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\ggml\src\ggml-virtgpu\backend\CMakeLists.txt
source_ext: .txt
source_sha256: 2d821e8ef300045d6379723e92d78ba0bc309b722fc859a9fb3662a8d127645c
text_sha256: 9b3ca0ffe5db26a210d43faa7c89879dddf47bf69ea1a1a9ef175b39d1324636
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/ggml/src/ggml-virtgpu/backend/CMakeLists.txt`
- Extract: `text`
- SHA256: `2d821e8ef300045d6379723e92d78ba0bc309b722fc859a9fb3662a8d127645c`

## Content

cmake_minimum_required(VERSION 3.19)
cmake_policy(SET CMP0114 NEW)

message(STATUS "Enable the VirtGPU/Virglrenderer backend library")

ggml_add_backend_library(ggml-virtgpu-backend
                         backend.cpp
                         backend-dispatched.cpp
                         backend-dispatched-backend.cpp
                         backend-dispatched-device.cpp
                         backend-dispatched-buffer.cpp
                         backend-dispatched-buffer-type.cpp
                         shared/api_remoting.h
                         shared/apir_backend.h
                         shared/apir_cs.h
                         apir_cs_ggml-rpc-back.cpp)

target_compile_options(ggml-virtgpu-backend PRIVATE -std=c++20)

# Add include directory for ggml-backend-impl.h and other core headers
target_include_directories(ggml-virtgpu-backend PRIVATE ../..)

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
