---
argos_import: project_file
source_path: llama.cpp/requirements/requirements-all.txt
source_abs: F:\debug\argoss\llama.cpp\requirements\requirements-all.txt
source_ext: .txt
source_sha256: 071c47ce36770ece9ecab87206174db7f053e6e370d27ff0d943b561da95a272
text_sha256: 449994b4859f6c734b7a7dce0573726a8113e607d9aa01a7f4c034b152c037c9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# requirements-all.txt

- Source: `llama.cpp/requirements/requirements-all.txt`
- Extract: `text`
- SHA256: `071c47ce36770ece9ecab87206174db7f053e6e370d27ff0d943b561da95a272`

## Content

-r ../tools/mtmd/requirements.txt
-r ../tools/server/bench/requirements.txt
-r ../tools/server/tests/requirements.txt

-r ./requirements-compare-llama-bench.txt
-r ./requirements-server-bench.txt
-r ./requirements-pydantic.txt
-r ./requirements-test-tokenizer-random.txt

-r ./requirements-convert_hf_to_gguf.txt
-r ./requirements-convert_hf_to_gguf_update.txt
-r ./requirements-convert_legacy_llama.txt
-r ./requirements-convert_llama_ggml_to_gguf.txt
-r ./requirements-tool_bench.txt

-r ./requirements-gguf_editor_gui.txt

-r ../examples/model-conversion/requirements.txt

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
