---
argos_import: project_file
source_path: llama.cpp/examples/speculative-simple/README.md
source_abs: F:\debug\argoss\llama.cpp\examples\speculative-simple\README.md
source_ext: .md
source_sha256: 19add71e37c21ce54a964ca585cd3971b7bf08909a7dfcb7843a3224f81e4b65
text_sha256: 9ccf73901f57ecf787ebfbf2bcc7aae13fc41a5f60256f325cf09f8777c40c83
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# README.md

- Source: `llama.cpp/examples/speculative-simple/README.md`
- Extract: `text`
- SHA256: `19add71e37c21ce54a964ca585cd3971b7bf08909a7dfcb7843a3224f81e4b65`

## Content

# llama.cpp/examples/speculative-simple

Demonstration of basic greedy speculative decoding

```bash
./bin/llama-speculative-simple \
    -m  ../models/qwen2.5-32b-coder-instruct/ggml-model-q8_0.gguf \
    -md ../models/qwen2.5-1.5b-coder-instruct/ggml-model-q4_0.gguf \
    -f test.txt -c 0 -ngl 99 --color \
    --sampling-seq k --top-k 1 -fa --temp 0.0 \
    -ngld 99 --draft-max 16 --draft-min 5 --draft-p-min 0.9
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
