---
argos_import: project_file
source_path: llama.cpp/requirements/requirements-convert_hf_to_gguf.txt
source_abs: F:\debug\argoss\llama.cpp\requirements\requirements-convert_hf_to_gguf.txt
source_ext: .txt
source_sha256: 853ce6d7784bd22a6fbc6f07a7dd482a6ad190dfa87a70fa41b0e76af6c713fc
text_sha256: 958ad0b45ea5c961c529ba86d0c2a07f3e8f1c6a1b7073de9d45a24bbba886f9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# requirements-convert_hf_to_gguf.txt

- Source: `llama.cpp/requirements/requirements-convert_hf_to_gguf.txt`
- Extract: `text`
- SHA256: `853ce6d7784bd22a6fbc6f07a7dd482a6ad190dfa87a70fa41b0e76af6c713fc`

## Content

-r ./requirements-convert_legacy_llama.txt
--extra-index-url https://download.pytorch.org/whl/cpu

## Embedding Gemma requires PyTorch 2.6.0 or later
torch~=2.6.0; platform_machine != "s390x"

# torch s390x packages can only be found from nightly builds
--extra-index-url https://download.pytorch.org/whl/nightly
torch>=0.0.0.dev0; platform_machine == "s390x"

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
