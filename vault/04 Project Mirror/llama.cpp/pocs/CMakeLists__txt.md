---
argos_import: project_file
source_path: llama.cpp/pocs/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\pocs\CMakeLists.txt
source_ext: .txt
source_sha256: dafbd6dcf43e2260fb9f104510470072b0e6a761afaa208962a514c450e2c36b
text_sha256: 24a96d97492e28df1634866410394cf67043f60a0661140ee80dff37a9a73d45
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/pocs/CMakeLists.txt`
- Extract: `text`
- SHA256: `dafbd6dcf43e2260fb9f104510470072b0e6a761afaa208962a514c450e2c36b`

## Content

# dependencies

find_package(Threads REQUIRED)

# third-party

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

if (EMSCRIPTEN)
else()
    if (NOT GGML_BACKEND_DL)
        add_subdirectory(vdot)
    endif()
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
