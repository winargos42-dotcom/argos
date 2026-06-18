---
argos_import: project_file
source_path: llama.cpp/examples/training/README.md
source_abs: F:\debug\argoss\llama.cpp\examples\training\README.md
source_ext: .md
source_sha256: e9108f133ae0a3c7030179a14b80025862b7fe386b1c2fa2032ce11986a35e64
text_sha256: 133d214188b1c9303ebed18d79cf54e0f9211d702c101791eaa1d782243f5730
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# README.md

- Source: `llama.cpp/examples/training/README.md`
- Extract: `text`
- SHA256: `e9108f133ae0a3c7030179a14b80025862b7fe386b1c2fa2032ce11986a35e64`

## Content

# llama.cpp/examples/training

This directory contains examples related to language model training using llama.cpp/GGML.
So far finetuning is technically functional (for FP32 models and limited hardware setups) but the code is very much WIP.
Finetuning of Stories 260K and LLaMA 3.2 1b seems to work with 24 GB of memory.
**For CPU training, compile llama.cpp without any additional backends such as CUDA.**
**For CUDA training, use the maximum number of GPU layers.**

Proof of concept:

``` sh
export model_name=llama_3.2-1b && export quantization=f32
./build/bin/llama-finetune --file wikitext-2-raw/wiki.test.raw -ngl 999 --model models/${model_name}-${quantization}.gguf -c 512 -b 512 -ub 512
./build/bin/llama-perplexity --file wikitext-2-raw/wiki.test.raw -ngl 999 --model finetuned-model.gguf
```

The perplexity value of the finetuned model should be lower after training on the test set for 2 epochs.

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
