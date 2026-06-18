---
argos_import: project_file
source_path: llama.cpp/examples/parallel/README.md
source_abs: F:\debug\argoss\llama.cpp\examples\parallel\README.md
source_ext: .md
source_sha256: cd738d43a9e32ee00abab2be51f8ac2a128313f5a01d60a58f24130b2ab516d9
text_sha256: f3c97fc5d46798998ff69c15b23fc6edd69073d6ebf00f4a9ea6bee3e85f8945
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# README.md

- Source: `llama.cpp/examples/parallel/README.md`
- Extract: `text`
- SHA256: `cd738d43a9e32ee00abab2be51f8ac2a128313f5a01d60a58f24130b2ab516d9`

## Content

# llama.cpp/example/parallel

Simplified simulation of serving incoming requests in parallel

## Example

Generate 128 client requests (`-ns 128`), simulating 8 concurrent clients (`-np 8`). The system prompt is shared (`-pps`), meaning that it is computed once at the start. The client requests consist of up to 10 junk questions (`--junk 10`) followed by the actual question.

```bash
llama-parallel -m model.gguf -np 8 -ns 128 --top-k 1 -pps --junk 10 -c 16384
```

> [!NOTE]
> It's recommended to use base models with this example. Instruction tuned models might not be able to properly follow the custom chat template specified here, so the results might not be as expected.

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
