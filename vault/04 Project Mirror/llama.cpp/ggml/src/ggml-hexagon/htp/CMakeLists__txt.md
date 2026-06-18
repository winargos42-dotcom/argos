---
argos_import: project_file
source_path: llama.cpp/ggml/src/ggml-hexagon/htp/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\ggml\src\ggml-hexagon\htp\CMakeLists.txt
source_ext: .txt
source_sha256: 5d71b2621d14e82b718ff4fa128388c7fc55fac5705284f200d91fd8fdcd9450
text_sha256: a2fef4af0fe29d149fecd60102a51d3b1a4277426db6dcb6e037f0197882bf0e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/ggml/src/ggml-hexagon/htp/CMakeLists.txt`
- Extract: `text`
- SHA256: `5d71b2621d14e82b718ff4fa128388c7fc55fac5705284f200d91fd8fdcd9450`

## Content

cmake_minimum_required(VERSION 3.22.2)
project(ggml-htp C CXX ASM)

include(${HEXAGON_SDK_ROOT}/build/cmake/hexagon_fun.cmake)

include_directories(
    ${HEXAGON_SDK_ROOT}/incs
    ${HEXAGON_SDK_ROOT}/incs/stddef
    ${CMAKE_CURRENT_SOURCE_DIR}/../../../include
    ${CMAKE_CURRENT_SOURCE_DIR}/../..
    ${CMAKE_CURRENT_SOURCE_DIR}/..
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_BINARY_DIR})

set(HTP_LIB ggml-htp-${DSP_VERSION})

add_library(${HTP_LIB} SHARED
    main.c
    htp_iface_skel.c
    worker-pool.c
    hex-dma.c
    matmul-ops.c
    binary-ops.c
    unary-ops.c
    sum-rows-ops.c
    softmax-ops.c
    act-ops.c
    rope-ops.c
    flash-attn-ops.c
    set-rows-ops.c
    get-rows-ops.c
    cpy-ops.c
    repeat-ops.c
    argsort-ops.c
    ssm-conv.c
    cumsum-ops.c
    fill-ops.c
    diag-ops.c
    solve-tri-ops.c
)

target_compile_definitions(${HTP_LIB} PRIVATE
    $<IF:$<BOOL:${HEXAGON_HTP_DEBUG}>,HTP_DEBUG=1,NDEBUG=1>
    $<IF:$<BOOL:${HEXAGON_HTP_DEBUG}>,FARF_HIGH=1,>
    FP32_QUANTIZE_GROUP_SIZE=${GGML_HEXAGON_FP32_QUANTIZE_GROUP_SIZE})

# HMX acceleration: available on v73+ architectures
set(HTP_HMX_VERSIONS v73 v75 v79 v81)
list(FIND HTP_HMX_VERSIONS ${DSP_VERSION} _hmx_idx)

if (_hmx_idx GREATER_EQUAL 0)
    target_sources(${HTP_LIB} PRIVATE
        hmx-queue.c
        hmx-matmul-ops.c
    )

    # -mhmx enables HMX instruction set (needed by files that include hmx-utils.h)
    set_source_files_properties(
        hmx-matmul-ops.c
        PROPERTIES COMPILE_OPTIONS "-mhmx"
    )

    target_compile_definitions(${HTP_LIB} PRIVATE HTP_HAS_HMX=1)
endif()

build_idl(htp_iface.idl ${HTP_LIB})

set_target_properties(${HTP_LIB} PROPERTIES EXPORT_COMPILE_COMMANDS ON)

install(TARGETS ${HTP_LIB})

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
