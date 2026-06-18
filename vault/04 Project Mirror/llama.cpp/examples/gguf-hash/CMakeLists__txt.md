---
argos_import: project_file
source_path: llama.cpp/examples/gguf-hash/CMakeLists.txt
source_abs: F:\debug\argoss\llama.cpp\examples\gguf-hash\CMakeLists.txt
source_ext: .txt
source_sha256: 150ae4bcfdacae6fa84dec0115db5bc0da6f5c41b2c0e3952b9199187373037a
text_sha256: f52b81f7084fa7fbb5e21b63637df1cee398ebde60a9284cefba974ae37bcb00
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# CMakeLists.txt

- Source: `llama.cpp/examples/gguf-hash/CMakeLists.txt`
- Extract: `text`
- SHA256: `150ae4bcfdacae6fa84dec0115db5bc0da6f5c41b2c0e3952b9199187373037a`

## Content

set(TARGET llama-gguf-hash)
add_executable(${TARGET} gguf-hash.cpp)
install(TARGETS ${TARGET} RUNTIME)

# clibs dependencies
include_directories(deps/)

add_library(xxhash OBJECT deps/xxhash/xxhash.c deps/xxhash/xxhash.h)
target_link_libraries(${TARGET} PRIVATE xxhash)

add_library(sha1 OBJECT deps/sha1/sha1.c deps/sha1/sha1.h)
target_link_libraries(${TARGET} PRIVATE sha1)
if (NOT MSVC)
    # disable warnings in 3rd party code
    target_compile_options(sha1 PRIVATE -w)
endif()

add_library(sha256 OBJECT deps/sha256/sha256.c deps/sha256/sha256.h)
target_link_libraries(${TARGET} PRIVATE sha256)

target_link_libraries(${TARGET} PRIVATE ggml ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Training Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Training Hub]]
