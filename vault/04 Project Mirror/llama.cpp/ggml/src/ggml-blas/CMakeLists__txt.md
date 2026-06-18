---
argos_import: project_file
source_path: llama.cpp/ggml/src/ggml-blas/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\ggml\src\ggml-blas\CMakeLists.txt
source_ext: .txt
source_sha256: 15b4bc404bba0c15a9f52a683216ea95a86dcf1dc0e2462422ca579a6af8ad23
text_sha256: dc7028c2c7207e8c334fd61ea4556599a326710cd9b33050bace38833529df71
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# CMakeLists.txt

- Source: `llama.cpp/ggml/src/ggml-blas/CMakeLists.txt`
- Extract: `text`
- SHA256: `15b4bc404bba0c15a9f52a683216ea95a86dcf1dc0e2462422ca579a6af8ad23`

## Content

if (GGML_STATIC)
    set(BLA_STATIC ON)
endif()
#if (CMAKE_VERSION VERSION_GREATER_EQUAL 3.22)
#    set(BLA_SIZEOF_INTEGER 8)
#endif()

set(BLA_VENDOR ${GGML_BLAS_VENDOR})
find_package(BLAS)

if (BLAS_FOUND)
    message(STATUS "BLAS found, Libraries: ${BLAS_LIBRARIES}")

    ggml_add_backend_library(ggml-blas
                             ggml-blas.cpp
                            )

    if (${GGML_BLAS_VENDOR} MATCHES "Apple")
        add_compile_definitions(ACCELERATE_NEW_LAPACK)
        add_compile_definitions(ACCELERATE_LAPACK_ILP64)
        add_compile_definitions(GGML_BLAS_USE_ACCELERATE)
    elseif ("${BLAS_INCLUDE_DIRS}" STREQUAL "")
        # BLAS_INCLUDE_DIRS is missing in FindBLAS.cmake.
        # see https://gitlab.kitware.com/cmake/cmake/-/issues/20268
        find_package(PkgConfig REQUIRED)
        if (${GGML_BLAS_VENDOR} MATCHES "Generic")
            pkg_check_modules(DepBLAS blas)
        elseif (${GGML_BLAS_VENDOR} MATCHES "OpenBLAS")
            # As of openblas v0.3.22, the 64-bit is named openblas64.pc
            pkg_check_modules(DepBLAS openblas64)
            if (NOT DepBLAS_FOUND)
                pkg_check_modules(DepBLAS openblas)
            endif()
        elseif (${GGML_BLAS_VENDOR} MATCHES "FLAME")
            pkg_check_modules(DepBLAS blis)
        elseif (${GGML_BLAS_VENDOR} MATCHES "ATLAS")
            pkg_check_modules(DepBLAS blas-atlas)
        elseif (${GGML_BLAS_VENDOR} MATCHES "FlexiBLAS")
            pkg_check_modules(DepBLAS flexiblas_api)
        elseif (${GGML_BLAS_VENDOR} MATCHES "Intel")
            # all Intel* libraries share the same include path
            pkg_check_modules(DepBLAS mkl-sdl)
        elseif (${GGML_BLAS_VENDOR} MATCHES "NVHPC")
            # this doesn't provide pkg-config
            # suggest to assign BLAS_INCLUDE_DIRS on your own
            if ("${NVHPC_VERSION}" STREQUAL "")
                message(WARNING "Better to set NVHPC_VERSION")
            else()
                set(DepBLAS_FOUND ON)
                set(DepBLAS_INCLUDE_DIRS "/opt/nvidia/hpc_sdk/${CMAKE_SYSTEM_NAME}_${CMAKE_SYSTEM_PROCESSOR}/${NVHPC_VERSION}/math_libs/include")
            endif()
        endif()
        if (DepBLAS_FOUND)
            set(BLAS_INCLUDE_DIRS ${DepBLAS_INCLUDE_DIRS})
        else()
            message(WARNING "BLAS_INCLUDE_DIRS neither been provided nor been automatically"
            " detected by pkgconfig, trying to find cblas.h from possible paths...")
            find_path(BLAS_INCLUDE_DIRS
                NAMES cblas.h
                HINTS
                    /usr/include
                    /usr/local/include
                    /usr/include/openblas
                    /opt/homebrew/opt/openblas/include
                    /usr/local/opt/openblas/include
                    /usr/include/x86_64-linux-gnu/openblas/include
            )
        endif()
    endif()

    message(STATUS "BLAS found, Includes: ${BLAS_INCLUDE_DIRS}")

    target_compile_options(ggml-blas PRIVATE ${BLAS_LINKER_FLAGS})

    if ("${GGML_BLAS_VENDOR}" STREQUAL "")
        message(WARNING "GGML_BLAS_VENDOR is not set; some methods may not link properly.")
    endif()

    if ("${GGML_BLAS_VENDOR}" MATCHES "Intel" OR ("${BLAS_INCLUDE_DIRS}" MATCHES "mkl" AND "${GGML_BLAS_VENDOR}" MATCHES "Generic"))
        add_compile_definitions(GGML_BLAS_USE_MKL)
    endif()

    if ("${GGML_BLAS_VENDOR}" MATCHES "OpenBLAS")
        add_compile_definitions(GGML_BLAS_USE_OPENBLAS)
    endif()

    if ("${GGML_BLAS_VENDOR}" MATCHES "FLAME" OR "${GGML_BLAS_VENDOR}" MATCHES "AOCL" OR "${GGML_BLAS_VENDOR}" MATCHES "AOCL_mt")
        add_compile_definitions(GGML_BLAS_USE_BLIS)
    endif()

    if ("${GGML_BLAS_VENDOR}" MATCHES "NVPL")
        add_compile_definitions(GGML_BLAS_USE_NVPL)
    endif()

    target_link_libraries     (ggml-blas PRIVATE ${BLAS_LIBRARIES})
    target_include_directories(ggml-blas SYSTEM PRIVATE ${BLAS_INCLUDE_DIRS})
else()
    message(FATAL_ERROR "BLAS not found, please refer to "
                        "https://cmake.org/cmake/help/latest/module/FindBLAS.html#blas-lapack-vendors"
                        " to set correct GGML_BLAS_VENDOR")
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
