---
argos_import: project_file
source_path: llama.cpp/examples/embedding/README.md
source_abs: F:\debug\argoss\llama.cpp\examples\embedding\README.md
source_ext: .md
source_sha256: 5d650f6751fb61e2b3acc0ecee7260b169b4a85129dcae573e6e1825a4227d52
text_sha256: bd4fe8d672c803b2070ff45c6bc3c6f36a09cb46f1948d245c61d07819c08a8a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# README.md

- Source: `llama.cpp/examples/embedding/README.md`
- Extract: `text`
- SHA256: `5d650f6751fb61e2b3acc0ecee7260b169b4a85129dcae573e6e1825a4227d52`

## Content

# llama.cpp/example/embedding

This example demonstrates generate high-dimensional embedding vector of a given text with llama.cpp.

## Quick Start

To get started right away, run the following command, making sure to use the correct path for the model you have:

### Unix-based systems (Linux, macOS, etc.):

```bash
./llama-embedding -m ./path/to/model --pooling mean --log-disable -p "Hello World!" 2>/dev/null
```

### Windows:

```powershell
llama-embedding.exe -m ./path/to/model --pooling mean --log-disable -p "Hello World!" 2>$null
```

The above command will output space-separated float values.

## extra parameters
### --embd-normalize $integer$
| $integer$ | description         | formula |
|-----------|---------------------|---------|
| $-1$      | none                |
| $0$       | max absolute int16  | $\Large{{32760 * x_i} \over\max \lvert x_i\rvert}$
| $1$       | taxicab             | $\Large{x_i \over\sum \lvert x_i\rvert}$
| $2$       | euclidean (default) | $\Large{x_i \over\sqrt{\sum x_i^2}}$
| $>2$      | p-norm              | $\Large{x_i \over\sqrt[p]{\sum \lvert x_i\rvert^p}}$

### --embd-output-format $'string'$
| $'string'$ | description                  |  |
|------------|------------------------------|--|
| ''         | same as before               | (default)
| 'array'    | single embeddings            | $\[\[x_1,...,x_n\]\]$
|            | multiple embeddings          | $\[\[x_1,...,x_n],[x_1,...,x_n],...,[x_1,...,x_n\]\]$
| 'json'     | openai style                 |
| 'json+'    | add cosine similarity matrix |
| 'raw'      | plain text output            |

### --embd-separator $"string"$
| $"string"$   | |
|--------------|-|
| "\n"         | (default)
| "<#embSep#>" | for example
| "<#sep#>"    | other example

## examples
### Unix-based systems (Linux, macOS, etc.):

```bash
./llama-embedding -p 'Castle<#sep#>Stronghold<#sep#>Dog<#sep#>Cat' --pooling mean --embd-separator '<#sep#>' --embd-normalize 2  --embd-output-format '' -m './path/to/model.gguf' --n-gpu-layers 99 --log-disable 2>/dev/null
```

### Windows:

```powershell
llama-embedding.exe -p 'Castle<#sep#>Stronghold<#sep#>Dog<#sep#>Cat' --pooling mean --embd-separator '<#sep#>' --embd-normalize 2  --embd-output-format '' -m './path/to/model.gguf' --n-gpu-layers 99 --log-disable 2>/dev/null
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
