---
argos_import: project_file
source_path: llama.cpp/tools/cvector-generator/README.md
source_abs: F:\debug\argoss\llama.cpp\tools\cvector-generator\README.md
source_ext: .md
source_sha256: 3a5573b51f4ac7b5da9ba6df2403ebbeae942fcd4ae0b0b251fa415d75c127ca
text_sha256: 580d4b9585dffc9a09112f257598dfff4a29046a7a6bc995b654a82a867ab530
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# README.md

- Source: `llama.cpp/tools/cvector-generator/README.md`
- Extract: `text`
- SHA256: `3a5573b51f4ac7b5da9ba6df2403ebbeae942fcd4ae0b0b251fa415d75c127ca`

## Content

# cvector-generator

This example demonstrates how to generate a control vector using gguf models.

Related PRs:
- [Add support for control vectors](https://github.com/ggml-org/llama.cpp/pull/5970)
- (Issue) [Generate control vector using llama.cpp](https://github.com/ggml-org/llama.cpp/issues/6880)
- [Add cvector-generator example](https://github.com/ggml-org/llama.cpp/pull/7514)

## Examples

```sh
# CPU only
./cvector-generator -m ./llama-3.Q4_K_M.gguf

# With GPU
./cvector-generator -m ./llama-3.Q4_K_M.gguf -ngl 99

# With advanced options
./cvector-generator -m ./llama-3.Q4_K_M.gguf -ngl 99 --pca-iter 2000 --pca-batch 100

# Using mean value instead of PCA
./cvector-generator -m ./llama-3.Q4_K_M.gguf --method mean

# To see help message
./cvector-generator -h
# Then, have a look at "cvector" section
```

## Tips and tricks

If you have multiple lines per prompt, you can escape the newline character (change it to `\n`). For example:

```
<|im_start|>system\nAct like a person who is extremely happy.<|im_end|>
<|im_start|>system\nYou are in a very good mood today<|im_end|>
```

Example to use output file with `llama-cli`:

(Tips: The control vector works better when apply to layers higher than 10)

```sh
./llama-cli -m ./llama-3.Q4_K_M.gguf -p "<|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\nSing a song<|im_end|><|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n" --special --control-vector-scaled ./control_vector.gguf 0.8 --control-vector-layer-range 10 31
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
