---
argos_import: project_file
source_path: llama.cpp/tools/export-lora/README.md
source_abs: F:\debug\argoss\llama.cpp\tools\export-lora\README.md
source_ext: .md
source_sha256: 71588596c723bd86e8c77efc6b55446b6bcfbbf19f99caa2001cb419f78bad87
text_sha256: 229f6864467d81705b2dea7c1f3ce64a0baa00cd7822299f6d7e4490b463ee3b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# README.md

- Source: `llama.cpp/tools/export-lora/README.md`
- Extract: `text`
- SHA256: `71588596c723bd86e8c77efc6b55446b6bcfbbf19f99caa2001cb419f78bad87`

## Content

# export-lora

Apply LORA adapters to base model and export the resulting model.

```
usage: llama-export-lora [options]

options:
  -m,    --model                  model path from which to load base model (default '')
         --lora FNAME             path to LoRA adapter  (can be repeated to use multiple adapters)
         --lora-scaled FNAME S    path to LoRA adapter with user defined scaling S  (can be repeated to use multiple adapters)
  -t,    --threads N              number of threads to use during computation (default: 4)
  -o,    --output FNAME           output file (default: 'ggml-lora-merged-f16.gguf')
```

For example:

```bash
./bin/llama-export-lora \
    -m open-llama-3b-v2.gguf \
    -o open-llama-3b-v2-english2tokipona-chat.gguf \
    --lora lora-open-llama-3b-v2-english2tokipona-chat-LATEST.gguf
```

Multiple LORA adapters can be applied by passing multiple `--lora FNAME` or `--lora-scaled FNAME S` command line parameters:

```bash
./bin/llama-export-lora \
    -m your_base_model.gguf \
    -o your_merged_model.gguf \
    --lora-scaled lora_task_A.gguf 0.5 \
    --lora-scaled lora_task_B.gguf 0.5
```

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
