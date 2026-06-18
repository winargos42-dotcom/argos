---
argos_import: project_file
source_path: llama.cpp/ggml/src/ggml-vulkan/vulkan-shaders/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\ggml\src\ggml-vulkan\vulkan-shaders\CMakeLists.txt
source_ext: .txt
source_sha256: ceb88b39f8d6c0dcc407323f9a1b14ef5bc5e570fbd4e69940d9859d52c304bd
text_sha256: 4b17954fc3348cba339bd375a881409fcd416dc4774eff137c38337f22ef4027
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/ggml/src/ggml-vulkan/vulkan-shaders/CMakeLists.txt`
- Extract: `text`
- SHA256: `ceb88b39f8d6c0dcc407323f9a1b14ef5bc5e570fbd4e69940d9859d52c304bd`

## Content

cmake_minimum_required(VERSION 3.19)
project("vulkan-shaders-gen" C CXX)

find_package (Threads REQUIRED)

if (GGML_VULKAN_COOPMAT_GLSLC_SUPPORT)
    add_compile_definitions(GGML_VULKAN_COOPMAT_GLSLC_SUPPORT)
    message(STATUS "Enabling coopmat glslc support")
endif()
if (GGML_VULKAN_COOPMAT2_GLSLC_SUPPORT)
    add_compile_definitions(GGML_VULKAN_COOPMAT2_GLSLC_SUPPORT)
    message(STATUS "Enabling coopmat2 glslc support")
endif()
if (GGML_VULKAN_INTEGER_DOT_GLSLC_SUPPORT)
    add_compile_definitions(GGML_VULKAN_INTEGER_DOT_GLSLC_SUPPORT)
    message(STATUS "Enabling dot glslc support")
endif()
if (GGML_VULKAN_BFLOAT16_GLSLC_SUPPORT)
    add_compile_definitions(GGML_VULKAN_BFLOAT16_GLSLC_SUPPORT)
    message(STATUS "Enabling bfloat16 glslc support")
endif()
if (GGML_VULKAN_SHADER_DEBUG_INFO)
    add_compile_definitions(GGML_VULKAN_SHADER_DEBUG_INFO)
    message(STATUS "Enabling shader debug info")
endif()

set(TARGET vulkan-shaders-gen)
add_executable(${TARGET} vulkan-shaders-gen.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_compile_features(${TARGET} PRIVATE cxx_std_17)
target_link_libraries(vulkan-shaders-gen PUBLIC Threads::Threads)

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
