---
argos_import: project_file
source_path: llama.cpp/requirements.txt
source_abs: F:\debug\argoss\llama.cpp\requirements.txt
source_ext: .txt
source_sha256: 0d7204f1f7e98e230ffd04b23c4e035cead5a350f59528ac3b867e1e25a3e5ff
text_sha256: 08e67179ad6863e26c8c763822b53f1080f4d4251cc2ad48c10418be9ee38f7f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# requirements.txt

- Source: `llama.cpp/requirements.txt`
- Extract: `text`
- SHA256: `0d7204f1f7e98e230ffd04b23c4e035cead5a350f59528ac3b867e1e25a3e5ff`

## Content

# These requirements include all dependencies for all top-level python scripts
# for llama.cpp. Avoid adding packages here directly.
#
# Package versions must stay compatible across all top-level python scripts.
#

-r ./requirements/requirements-convert_legacy_llama.txt

-r ./requirements/requirements-convert_hf_to_gguf.txt
-r ./requirements/requirements-convert_hf_to_gguf_update.txt
-r ./requirements/requirements-convert_llama_ggml_to_gguf.txt
-r ./requirements/requirements-convert_lora_to_gguf.txt
-r ./requirements/requirements-tool_bench.txt

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
