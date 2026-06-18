---
argos_import: project_file
source_path: llama.cpp/examples/convert-llama2c-to-ggml/README.md
source_abs: F:\debug\argoss\llama.cpp\examples\convert-llama2c-to-ggml\README.md
source_ext: .md
source_sha256: 25692e64bd1202616afc3802f5d2c8279a8ca4dc693b62ede5f65937d3ba5a08
text_sha256: 374883b2360b547e8505310f184944f207bc8ea4954c3166461b888c7ceb5cec
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# README.md

- Source: `llama.cpp/examples/convert-llama2c-to-ggml/README.md`
- Extract: `text`
- SHA256: `25692e64bd1202616afc3802f5d2c8279a8ca4dc693b62ede5f65937d3ba5a08`

## Content

## Convert llama2.c model to ggml

This example reads weights from project [llama2.c](https://github.com/karpathy/llama2.c) and saves them in ggml compatible format. The vocab that is available in `models/ggml-vocab.bin` is used by default.

To convert the model first download the models from the [llama2.c](https://github.com/karpathy/llama2.c) repository.

```
usage: ./llama-convert-llama2c-to-ggml [options]

options:
  -h, --help                       show this help message and exit
  --copy-vocab-from-model FNAME    path of gguf llama model or llama2.c vocabulary from which to copy vocab (default 'models/7B/ggml-model-f16.gguf')
  --llama2c-model FNAME            [REQUIRED] model path from which to load Karpathy's llama2.c model
  --llama2c-output-model FNAME     model path to save the converted llama2.c model (default ak_llama_model.bin')
```

An example command using a model from [karpathy/tinyllamas](https://huggingface.co/karpathy/tinyllamas) is as follows:

`$ ./llama-convert-llama2c-to-ggml --copy-vocab-from-model llama-2-7b-chat.gguf.q2_K.bin --llama2c-model stories42M.bin --llama2c-output-model stories42M.gguf.bin`

Note: The vocabulary for `stories260K.bin` should be its own tokenizer `tok512.bin` found in [karpathy/tinyllamas/stories260K](https://huggingface.co/karpathy/tinyllamas/tree/main/stories260K).

Now you can use the model with a command like:

`$ ./llama-cli -m stories42M.gguf.bin -p "One day, Lily met a Shoggoth" -n 500 -c 256`

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
