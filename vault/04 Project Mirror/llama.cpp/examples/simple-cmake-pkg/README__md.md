---
argos_import: project_file
source_path: llama.cpp/examples/simple-cmake-pkg/README.md
source_abs: F:\debug\argoss\llama.cpp\examples\simple-cmake-pkg\README.md
source_ext: .md
source_sha256: 61721b89fdaaac653ba373372ba1825b2c7b907e93739ae4828970b132f1e4f0
text_sha256: f53f65e0a63eeefd8edf27131a25f8fd4076b8d94d19d20b6ad1c3c95f88af5a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# README.md

- Source: `llama.cpp/examples/simple-cmake-pkg/README.md`
- Extract: `text`
- SHA256: `61721b89fdaaac653ba373372ba1825b2c7b907e93739ae4828970b132f1e4f0`

## Content

# llama.cpp/example/simple-cmake-pkg

This program builds [simple](../simple) using a relocatable CMake package. It serves as an example of using the `find_package()` CMake command to conveniently include [llama.cpp](https://github.com/ggml-org/llama.cpp) in projects which live outside of the source tree.

## Building

Because this example is "outside of the source tree", it is important to first build/install llama.cpp using CMake. An example is provided here, but please see the [llama.cpp build instructions](../..) for more detailed build instructions.

### Considerations

When hardware acceleration libraries are used (e.g. CUDA, Metal, Vulkan, etc.), the appropriate dependencies will be searched for automatically. So, for example, when finding a package

### Build llama.cpp and install to llama.cpp/inst

```sh
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -S . -B build
cmake --build build
cmake --install build --prefix inst
```

### Build simple-cmake-pkg

```sh
cd examples/simple-cmake-pkg
cmake -S . -B build -DCMAKE_PREFIX_PATH=../../inst/lib/cmake
cmake --build build
```

### Run simple-cmake-pkg

```sh
./build/llama-simple-cmake-pkg -m ./models/llama-7b-v2/ggml-model-f16.gguf "Hello my name is"
```

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
