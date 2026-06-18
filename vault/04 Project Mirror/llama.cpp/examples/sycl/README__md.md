---
argos_import: project_file
source_path: llama.cpp/examples/sycl/README.md
source_abs: F:\debug\argoss\llama.cpp\examples\sycl\README.md
source_ext: .md
source_sha256: 171c1d1dd57b1c9c4ce3894922133bde50790579ac127f1ce8714df3acdbc3c7
text_sha256: 4a5bbd177daf56f3b21af012b56366b9ad23b5d64dfe7ad088079f9d0272c73e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# README.md

- Source: `llama.cpp/examples/sycl/README.md`
- Extract: `text`
- SHA256: `171c1d1dd57b1c9c4ce3894922133bde50790579ac127f1ce8714df3acdbc3c7`

## Content

# llama.cpp/example/sycl

This example program provides the tools for llama.cpp for SYCL on Intel GPU.

## Tool

|Tool Name| Function|Status|
|-|-|-|
|llama-ls-sycl-device| List all SYCL devices with ID, compute capability, max work group size, etc.|Support|

### llama-ls-sycl-device

List all SYCL devices with ID, compute capability, max work group size, etc.

1. Build the llama.cpp for SYCL for the specified target *(using GGML_SYCL_TARGET)*.

2. Enable oneAPI running environment *(if GGML_SYCL_TARGET is set to INTEL -default-)*

```
source /opt/intel/oneapi/setvars.sh
```

3. Execute

```
./build/bin/llama-ls-sycl-device
```

Check the ID in startup log, like:

```
found 2 SYCL devices:
|  |                   |                                       |       |Max    |        |Max  |Global |                     |
|  |                   |                                       |       |compute|Max work|sub  |mem    |                     |
|ID|        Device Type|                                   Name|Version|units  |group   |group|size   |       Driver version|
|--|-------------------|---------------------------------------|-------|-------|--------|-----|-------|---------------------|
| 0| [level_zero:gpu:0]|                Intel Arc A770 Graphics|    1.3|    512|    1024|   32| 16225M|            1.3.29138|
| 1| [level_zero:gpu:1]|                 Intel UHD Graphics 750|    1.3|     32|     512|   32| 62631M|            1.3.29138|

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
