---
argos_import: project_file
source_path: llama.cpp/ggml/src/ggml-openvino/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\ggml\src\ggml-openvino\CMakeLists.txt
source_ext: .txt
source_sha256: 87b7e0c45514f46ecf7d1ff824aba47a0df85303430bf70248d3306787ed1e8b
text_sha256: 400734439c6386fdd0b2c5273dbc01bb95fe27c4b75db8b186a8adad7043d5ad
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/ggml/src/ggml-openvino/CMakeLists.txt`
- Extract: `text`
- SHA256: `87b7e0c45514f46ecf7d1ff824aba47a0df85303430bf70248d3306787ed1e8b`

## Content

find_package(OpenVINO REQUIRED)
find_package(OpenCL REQUIRED)

include("${OpenVINO_DIR}/../3rdparty/tbb/lib/cmake/TBB/TBBConfig.cmake")

file(GLOB_RECURSE GGML_HEADERS_OPENVINO "*.h" "*.hpp")
file(GLOB_RECURSE GGML_SOURCES_OPENVINO "*.cpp")

ggml_add_backend_library(ggml-openvino
    ${GGML_SOURCES_OPENVINO}
    ${GGML_HEADERS_OPENVINO}
)

target_link_libraries(ggml-openvino PRIVATE openvino::runtime TBB::tbb OpenCL::OpenCL)

if (GGML_OPENVINO)
    if (CMAKE_SYSTEM_PROCESSOR STREQUAL "aarch64")
    elseif (CMAKE_SYSTEM_PROCESSOR STREQUAL "x86_64" OR CMAKE_SYSTEM_PROCESSOR STREQUAL "amd64" OR CMAKE_SYSTEM_PROCESSOR STREQUAL "AMD64")
    else()
        message(FATAL_ERROR "OpenVINO: OpenVINO toolkit supports x86-64 and arm64 but not ${CMAKE_SYSTEM_PROCESSOR}")
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
