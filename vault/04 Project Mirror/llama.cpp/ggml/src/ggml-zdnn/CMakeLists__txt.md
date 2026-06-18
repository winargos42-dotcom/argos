---
argos_import: project_file
source_path: llama.cpp/ggml/src/ggml-zdnn/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\ggml\src\ggml-zdnn\CMakeLists.txt
source_ext: .txt
source_sha256: 12b2ab331296c979fa763dde217dd78189f966686d23f7d2f5d0c8f8a169072a
text_sha256: 50e5b114c2268fb5df1f308a0953d6437991b98a5fe9b2998c8a448d4e9f9fc8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/ggml/src/ggml-zdnn/CMakeLists.txt`
- Extract: `text`
- SHA256: `12b2ab331296c979fa763dde217dd78189f966686d23f7d2f5d0c8f8a169072a`

## Content

if (DEFINED ZDNN_ROOT)
    message(STATUS "zdnn: using ZDNN_ROOT override: ${ZDNN_ROOT}")
    set(ZDNN_HINT "${ZDNN_ROOT}")
else()
    set(ZDNN_HINT "")
endif()

find_path(ZDNN_INCLUDE
            NAMES zdnn.h
            HINTS ${ZDNN_HINT} /usr /usr/local
            PATH_SUFFIXES include)
if (ZDNN_INCLUDE)
    message(STATUS "zdnn: found include: ${ZDNN_INCLUDE}")
else()
    message(FATAL_ERROR "zdnn: include directory not found, please set ZDNN_ROOT to the proper path if necessary")
endif()

find_library(ZDNN_LIB
                NAMES zdnn
                HINTS ${ZDNN_HINT} /usr /usr/local
                PATH_SUFFIXES lib lib64)
if (ZDNN_LIB)
    message(STATUS "zdnn: found library: ${ZDNN_LIB}")
else()
    message(FATAL_ERROR "zdnn: library not found, please set ZDNN_ROOT to the proper path if necessary")
endif()

file(GLOB GGML_SOURCES_ZDNN "*.c" "*.cpp")
file(GLOB GGML_HEADERS_ZDNN "*.h" "*.hpp")

ggml_add_backend_library(ggml-zdnn ${GGML_HEADERS_ZDNN} ${GGML_SOURCES_ZDNN})
target_link_libraries(ggml-zdnn PRIVATE ${ZDNN_LIB})
target_include_directories(ggml-zdnn PRIVATE ${ZDNN_INCLUDE})
target_link_directories(ggml-zdnn PRIVATE ${ZDNN_LIB})

target_compile_definitions(ggml-zdnn PRIVATE GGML_USE_ZDNN)

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
