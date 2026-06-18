---
argos_import: project_file
source_path: llama.cpp/tools/gguf-split/README.md
source_abs: F:\debug\argoss\llama.cpp\tools\gguf-split\README.md
source_ext: .md
source_sha256: e6a196a831eede2b617dbf152f803d71511b8cfc3e7f713cd9f929592699c6be
text_sha256: 26d2d3060be442fea859854919ab02179837931b273470630082bbbea4f26fa6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# README.md

- Source: `llama.cpp/tools/gguf-split/README.md`
- Extract: `text`
- SHA256: `e6a196a831eede2b617dbf152f803d71511b8cfc3e7f713cd9f929592699c6be`

## Content

## GGUF split Example

CLI to split / merge GGUF files.

**Command line options:**

- `--split`: split GGUF to multiple GGUF, default operation.
- `--split-max-size`: max size per split in `M` or `G`, f.ex. `500M` or `2G`.
- `--split-max-tensors`: maximum tensors in each split: default(128)
- `--merge`: merge multiple GGUF to a single GGUF. You only need to specify the name of the first GGUF to merge, the name of the merged GGUF, and the CLI will find the other GGUFs it needs within the same folder.

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
