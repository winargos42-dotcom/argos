---
argos_import: project_file
source_path: llama.cpp/examples/simple/README.md
source_abs: F:\debug\argoss\llama.cpp\examples\simple\README.md
source_ext: .md
source_sha256: 701802f124d621a390949550bd3fbc230db24d5765c5c7e4034335d3e34cf8bc
text_sha256: d1b98ab069f130e8cb985b6a4a2461c3cc56e646c4706d609c20109afc45590b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:01
---

# README.md

- Source: `llama.cpp/examples/simple/README.md`
- Extract: `text`
- SHA256: `701802f124d621a390949550bd3fbc230db24d5765c5c7e4034335d3e34cf8bc`

## Content

# llama.cpp/example/simple

The purpose of this example is to demonstrate a minimal usage of llama.cpp for generating text with a given prompt.

```bash
./llama-simple -m ./models/llama-7b-v2/ggml-model-f16.gguf "Hello my name is"

...

main: n_len = 32, n_ctx = 2048, n_parallel = 1, n_kv_req = 32

 Hello my name is Shawn and I'm a 20 year old male from the United States. I'm a 20 year old

main: decoded 27 tokens in 2.31 s, speed: 11.68 t/s

llama_print_timings:        load time =   579.15 ms
llama_print_timings:      sample time =     0.72 ms /    28 runs   (    0.03 ms per token, 38888.89 tokens per second)
llama_print_timings: prompt eval time =   655.63 ms /    10 tokens (   65.56 ms per token,    15.25 tokens per second)
llama_print_timings:        eval time =  2180.97 ms /    27 runs   (   80.78 ms per token,    12.38 tokens per second)
llama_print_timings:       total time =  2891.13 ms
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
