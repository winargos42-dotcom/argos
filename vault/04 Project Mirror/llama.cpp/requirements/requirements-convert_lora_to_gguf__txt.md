---
argos_import: project_file
source_path: llama.cpp/requirements/requirements-convert_lora_to_gguf.txt
source_abs: F:\debug\argoss\llama.cpp\requirements\requirements-convert_lora_to_gguf.txt
source_ext: .txt
source_sha256: ecda95c2fffd9d988ed810ca2176e17db10c2a78599b4ab0bc0a544870c9225c
text_sha256: c7ea8e4c64f08759c2527702adb51eb70ca481928e58d0d05bbbbe9c83f71b8d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# requirements-convert_lora_to_gguf.txt

- Source: `llama.cpp/requirements/requirements-convert_lora_to_gguf.txt`
- Extract: `text`
- SHA256: `ecda95c2fffd9d988ed810ca2176e17db10c2a78599b4ab0bc0a544870c9225c`

## Content

-r ./requirements-convert_hf_to_gguf.txt
--extra-index-url https://download.pytorch.org/whl/cpu
# torch s390x packages can only be found from nightly builds
--extra-index-url https://download.pytorch.org/whl/nightly

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
