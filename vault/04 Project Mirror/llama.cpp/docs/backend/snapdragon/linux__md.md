---
argos_import: project_file
source_path: llama.cpp/docs/backend/snapdragon/linux.md
source_abs: F:\debug\argoss\llama.cpp\docs\backend\snapdragon\linux.md
source_ext: .md
source_sha256: 26422ecd7402dffaaad4188acf36ec7ef910e0cd95ce1f698af496d795070342
text_sha256: 0eeb8b650f302b83578737173fd1f02dfabf22bd4f0c7e0467a9fe9492ac3b61
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# linux.md

- Source: `llama.cpp/docs/backend/snapdragon/linux.md`
- Extract: `text`
- SHA256: `26422ecd7402dffaaad4188acf36ec7ef910e0cd95ce1f698af496d795070342`

## Content

# Snapdragon-based Linux devices

## Docker Setup

The easiest way to build llama.cpp for a Snapdragon-based Linux device is using the toolchain Docker image (see [github.com/snapdragon-toolchain](https://github.com/snapdragon-toolchain)).
This image includes OpenCL SDK, Hexagon SDK, CMake, and the ARM64 Linux cross-compilation toolchain.

Cross-compilation is supported on **Linux X86** hosts. The resulting binaries are deployed to and run on the target **Qualcomm Snapdragon ARM64 Linux** device.

```
~/src/llama.cpp$ docker run -it -u $(id -u):$(id -g) --volume $(pwd):/workspace --platform linux/amd64 ghcr.io/snapdragon-toolchain/arm64-linux:v0.1
[d]/> cd /workspace
```

Note: The rest of the **Linux** build process assumes that you're running inside the toolchain container.


## How to Build

Let's build llama.cpp with CPU, OpenCL, and Hexagon backends via CMake presets:

```
[d]/workspace> cp docs/backend/snapdragon/CMakeUserPresets.json .

[d]/workspace> cmake --preset arm64-linux-snapdragon-release -B build-snapdragon

[d]/workspace> cmake --build build-snapdragon -j $(nproc)
```

To generate an installable "package" simply use cmake --install, then zip it:

```
[d]/workspace> cmake --install build-snapdragon --prefix pkg-snapdragon
[d]/workspace> zip -r pkg-snapdragon.zip pkg-snapdragon
```

## How to Install

For this step, you will deploy the built binaries and libraries to the target Linux device. Transfer `pkg-snapdragon.zip` to the target device, then unzip it and set up the environment variables:

```
$ unzip pkg-snapdragon.zip
$ cd pkg-snapdragon
$ export LD_LIBRARY_PATH=./lib
$ export ADSP_LIBRARY_PATH=./lib
```

At this point, you should also download some models onto the device:

```
$ wget https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_0.gguf
```

## How to Run
Next, since we have setup the environment variables, we can run the llama-cli with the Hexagon backends:
```
$ ./bin/llama-cli -m Llama-3.2-3B-Instruct-Q4_0.gguf --device HTP0 -ngl 99 -p "what is the most popular cookie in the world?"
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
