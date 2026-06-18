---
argos_import: project_file
source_path: llama.cpp/examples/eval-callback/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\eval-callback\CMakeLists.txt
source_ext: .txt
source_sha256: 7e14f95e0e7640edde0740cea70b951379f3615a571263527a9da37595069e66
text_sha256: 54854a0829f124a242d79b0f942bf4e2119ae98bc869f20be097c6c998a601af
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# CMakeLists.txt

- Source: `llama.cpp/examples/eval-callback/CMakeLists.txt`
- Extract: `text`
- SHA256: `7e14f95e0e7640edde0740cea70b951379f3615a571263527a9da37595069e66`

## Content

set(TARGET llama-eval-callback)
add_executable(${TARGET} eval-callback.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE llama-common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

if(LLAMA_BUILD_TESTS)
    if(NOT ${CMAKE_SYSTEM_PROCESSOR} MATCHES "s390x")
        set(MODEL_NAME "tinyllamas/stories15M-q4_0.gguf")
        set(MODEL_HASH "SHA256=66967fbece6dbe97886593fdbb73589584927e29119ec31f08090732d1861739")
    else()
        set(MODEL_NAME "tinyllamas/stories15M-be.Q4_0.gguf")
        set(MODEL_HASH "SHA256=9aec857937849d976f30397e97eb1cabb53eb9dcb1ce4611ba8247fb5f44c65d")
    endif()
    set(MODEL_DEST "${CMAKE_BINARY_DIR}/${MODEL_NAME}")
    set(TEST_TARGET test-eval-callback)
    add_test(NAME ${TEST_TARGET}-download-model COMMAND ${CMAKE_COMMAND}
        -DDEST=${MODEL_DEST}
        -DNAME=${MODEL_NAME}
        -DHASH=${MODEL_HASH}
        -P ${CMAKE_SOURCE_DIR}/cmake/download-models.cmake
    )
    set_tests_properties(${TEST_TARGET}-download-model PROPERTIES FIXTURES_SETUP ${TEST_TARGET}-download-model)
    add_test(NAME ${TEST_TARGET} COMMAND llama-eval-callback -m "${MODEL_DEST}" --prompt hello --seed 42 -ngl 0)
    set_tests_properties(${TEST_TARGET} PROPERTIES FIXTURES_REQUIRED ${TEST_TARGET}-download-model)
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
