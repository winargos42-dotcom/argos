---
argos_import: project_file
source_path: llama.cpp/docs/multimodal/gemma3.md
source_abs: F:\debug\argoss\llama.cpp\docs\multimodal\gemma3.md
source_ext: .md
source_sha256: da578f50924adf9cf272c5090ab59c6211c85663b7033f2ea78ec4857b193136
text_sha256: 57e49f25cd5363e0993f77c6db451495ddf2da2ee4b4fc598cbdf0e3dca07a12
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# gemma3.md

- Source: `llama.cpp/docs/multimodal/gemma3.md`
- Extract: `text`
- SHA256: `da578f50924adf9cf272c5090ab59c6211c85663b7033f2ea78ec4857b193136`

## Content

# Gemma 3 vision

> [!IMPORTANT]
>
> This is very experimental, only used for demo purpose.

## Quick started

You can use pre-quantized model from [ggml-org](https://huggingface.co/ggml-org)'s Hugging Face account

```bash
# build
cmake -B build
cmake --build build --target llama-mtmd-cli

# alternatively, install from brew (MacOS)
brew install llama.cpp

# run it
llama-mtmd-cli -hf ggml-org/gemma-3-4b-it-GGUF
llama-mtmd-cli -hf ggml-org/gemma-3-12b-it-GGUF
llama-mtmd-cli -hf ggml-org/gemma-3-27b-it-GGUF

# note: 1B model does not support vision
```

## How to get mmproj.gguf?

Simply to add `--mmproj` in when converting model via `convert_hf_to_gguf.py`:

```bash
cd gemma-3-4b-it
python ../llama.cpp/convert_hf_to_gguf.py --outfile model.gguf --outtype f16 --mmproj .
# output file: mmproj-model.gguf
```

## How to run it?

What you need:
- The text model GGUF, can be converted using `convert_hf_to_gguf.py`
- The mmproj file from step above
- An image file

```bash
# build
cmake -B build
cmake --build build --target llama-mtmd-cli

# run it
./build/bin/llama-mtmd-cli -m {text_model}.gguf --mmproj mmproj.gguf --image your_image.jpg
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
