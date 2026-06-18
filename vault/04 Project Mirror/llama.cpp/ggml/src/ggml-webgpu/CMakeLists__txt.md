---
argos_import: project_file
source_path: llama.cpp/ggml/src/ggml-webgpu/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\ggml\src\ggml-webgpu\CMakeLists.txt
source_ext: .txt
source_sha256: da1c28117a35fc9da86c79477eea50354b715e0a5d240183c8d299110837fa4f
text_sha256: 7e8655207c58ef7eb8dbe85e32bf727de44ce3ba58f70dbc8a23503bdda99700
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/ggml/src/ggml-webgpu/CMakeLists.txt`
- Extract: `text`
- SHA256: `da1c28117a35fc9da86c79477eea50354b715e0a5d240183c8d299110837fa4f`

## Content

cmake_minimum_required(VERSION 3.13)

find_package(Python3 REQUIRED)

# Shader locations
set(SHADER_DIR "${CMAKE_CURRENT_SOURCE_DIR}/wgsl-shaders")
set(SHADER_OUTPUT_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(SHADER_HEADER "${SHADER_OUTPUT_DIR}/ggml-wgsl-shaders.hpp")
file(MAKE_DIRECTORY ${SHADER_OUTPUT_DIR})

message(STATUS "Shader output dir: ${SHADER_OUTPUT_DIR}")

# Find all WGSL files
file(GLOB WGSL_SHADER_FILES "${SHADER_DIR}/*.wgsl")

# Generate the header using a Python script
add_custom_command(
    OUTPUT ${SHADER_HEADER}
    COMMAND ${CMAKE_COMMAND} -E echo "Embedding WGSL shaders to ggml-wgsl-shaders.hpp"
    COMMAND ${CMAKE_COMMAND} -E make_directory ${SHADER_OUTPUT_DIR}
    COMMAND ${CMAKE_COMMAND} -E env PYTHONIOENCODING=utf-8
        ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/wgsl-shaders/embed_wgsl.py
            --input_dir "${SHADER_DIR}"
            --output_file "${SHADER_HEADER}"
    DEPENDS ${WGSL_SHADER_FILES} ${CMAKE_CURRENT_SOURCE_DIR}/wgsl-shaders/embed_wgsl.py
    VERBATIM
)

add_custom_target(generate_shaders DEPENDS ${SHADER_HEADER})

ggml_add_backend_library(ggml-webgpu
    ggml-webgpu.cpp
    ${SHADER_HEADER}
    ../../include/ggml-webgpu.h
)

add_dependencies(ggml-webgpu generate_shaders)

if(EMSCRIPTEN)
    set(EMDAWNWEBGPU_DIR "" CACHE PATH "Path to emdawnwebgpu_pkg")

    if(NOT EMDAWNWEBGPU_DIR)
        # default built-in port
        target_compile_options(ggml-webgpu PRIVATE "--use-port=emdawnwebgpu")
        target_link_options(ggml-webgpu INTERFACE "--use-port=emdawnwebgpu")
    else()
        # custom port
        target_compile_options(ggml-webgpu PRIVATE "--use-port=${EMDAWNWEBGPU_DIR}/emdawnwebgpu.port.py")
        target_link_options(ggml-webgpu INTERFACE "--use-port=${EMDAWNWEBGPU_DIR}/emdawnwebgpu.port.py")
    endif()

    if (GGML_WEBGPU_JSPI)
        target_compile_options(ggml-webgpu PRIVATE "-fwasm-exceptions")
        target_link_options(ggml-webgpu INTERFACE "-sJSPI" "-fwasm-exceptions")
    else()
        target_compile_options(ggml-webgpu PRIVATE "-fexceptions")
        target_link_options(ggml-webgpu INTERFACE "-sASYNCIFY" "-exceptions")
    endif()
else()
    find_package(Dawn REQUIRED)
    set(DawnWebGPU_TARGET dawn::webgpu_dawn)
endif()

if (GGML_WEBGPU_DEBUG)
    target_compile_definitions(ggml-webgpu PRIVATE GGML_WEBGPU_DEBUG=1)
    if(EMSCRIPTEN)
        target_link_options(ggml-webgpu INTERFACE "-sASSERTIONS=2")
    endif()
endif()

if (GGML_WEBGPU_CPU_PROFILE)
    target_compile_definitions(ggml-webgpu PRIVATE GGML_WEBGPU_CPU_PROFILE=1)
endif()

if (GGML_WEBGPU_GPU_PROFILE)
    target_compile_definitions(ggml-webgpu PRIVATE GGML_WEBGPU_GPU_PROFILE=1)
endif()

target_include_directories(ggml-webgpu PRIVATE ${SHADER_OUTPUT_DIR})
target_link_libraries(ggml-webgpu PRIVATE ${DawnWebGPU_TARGET})

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
