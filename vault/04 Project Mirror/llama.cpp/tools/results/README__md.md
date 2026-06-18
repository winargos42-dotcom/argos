---
argos_import: project_file
source_path: llama.cpp/tools/results/README.md
source_abs: F:\debug\argoss\llama.cpp\tools\results\README.md
source_ext: .md
source_sha256: f76cd06737b16f1d12faeaeaa9f64eb694f058659a430dfd81f61d48ef230cd9
text_sha256: e91afff9a7188b8ddef89d834e4918e23e10617acaa7040e5c9350199bbd13b7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# README.md

- Source: `llama.cpp/tools/results/README.md`
- Extract: `text`
- SHA256: `f76cd06737b16f1d12faeaeaa9f64eb694f058659a430dfd81f61d48ef230cd9`

## Content

# Results

The `llama-results` tool can be used to `--check` the outputs of a model vs. a previous commit to detect whether they have changed.
Example usage:

``` sh
llama-results --model model.gguf --output results.gguf --prompt "People die when they are killed."  # writes results to file
llama-results --model model.gguf --output results.gguf --prompt "People die when they are killed." --check  # compares results vs file
```

The metric by which the results are compared is the normalized mean squared error (NMSE) with a tolerance of $10^{-6}$.

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
