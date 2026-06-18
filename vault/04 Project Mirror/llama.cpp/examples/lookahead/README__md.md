---
argos_import: project_file
source_path: llama.cpp/examples/lookahead/README.md
source_abs: F:\debug\argoss\llama.cpp\examples\lookahead\README.md
source_ext: .md
source_sha256: 1b737984e0388b5f7543af577cb50b530dfa14cff816005b0720daae03ec7be7
text_sha256: a5308cccd7a7b1f185957a402ae05ae3d8bafe6a08c4980c56ad63bc466a3285
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# README.md

- Source: `llama.cpp/examples/lookahead/README.md`
- Extract: `text`
- SHA256: `1b737984e0388b5f7543af577cb50b530dfa14cff816005b0720daae03ec7be7`

## Content

# llama.cpp/examples/lookahead

Demonstration of lookahead decoding technique:

https://lmsys.org/blog/2023-11-21-lookahead-decoding/

More info: https://github.com/ggml-org/llama.cpp/pull/4207

Sample command:

```bash
llama-lookahead -hf ggml-org/Qwen2.5-Coder-3B-Q8_0-GGUF -p "// network server implemented in C\n// author: Peter Hacker\n\n#include" -e -ngl 99 -t 4 -n 512 -c 4096 -kvu
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
