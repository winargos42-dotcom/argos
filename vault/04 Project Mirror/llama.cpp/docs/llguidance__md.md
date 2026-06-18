---
argos_import: project_file
source_path: llama.cpp/docs/llguidance.md
source_abs: F:\debug\argoss\llama.cpp\docs\llguidance.md
source_ext: .md
source_sha256: b40ca25a81d2fdfe872e6e1bf2591ceb90e44e81039c1c1a7ef91b7ca09dfb09
text_sha256: ef304ff3a7f29768f595ed798ab0ddab827e1ebda4df651e50c707811db27257
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# llguidance.md

- Source: `llama.cpp/docs/llguidance.md`
- Extract: `text`
- SHA256: `b40ca25a81d2fdfe872e6e1bf2591ceb90e44e81039c1c1a7ef91b7ca09dfb09`

## Content

# LLGuidance Support in llama.cpp

[LLGuidance](https://github.com/guidance-ai/llguidance) is a library for constrained decoding (also called constrained sampling or structured outputs) for Large Language Models (LLMs). Initially developed as the backend for the [Guidance](https://github.com/guidance-ai/guidance) library, it can also be used independently.

LLGuidance supports JSON Schemas and arbitrary context-free grammars (CFGs) written in a [variant](https://github.com/guidance-ai/llguidance/blob/main/docs/syntax.md) of Lark syntax. It is [very fast](https://github.com/guidance-ai/jsonschemabench/tree/main/maskbench) and has [excellent](https://github.com/guidance-ai/llguidance/blob/main/docs/json_schema.md) JSON Schema coverage but requires the Rust compiler, which complicates the llama.cpp build process.

## Building

To enable LLGuidance support, build llama.cpp with the `LLAMA_LLGUIDANCE` option:

```sh
cmake -B build -DLLAMA_LLGUIDANCE=ON
make -C build -j
```

For Windows use `cmake --build build --config Release` instead of `make`.

This requires the Rust compiler and the `cargo` tool to be [installed](https://www.rust-lang.org/tools/install).

## Interface

There are no new command-line arguments or modifications to `common_params`. When enabled, grammars starting with `%llguidance` are passed to LLGuidance instead of the [current](../grammars/README.md) llama.cpp grammars. Additionally, JSON Schema requests (e.g., using the `-j` argument in `llama-cli`) are also passed to LLGuidance.

For your existing GBNF grammars, you can use [gbnf_to_lark.py script](https://github.com/guidance-ai/llguidance/blob/main/python/llguidance/gbnf_to_lark.py) to convert them to LLGuidance Lark-like format.

## Performance

Computing a "token mask" (i.e., the set of allowed tokens) for a llama3 tokenizer with 128k tokens takes, on average, 50μs of single-core CPU time for the [JSON Schema Bench](https://github.com/guidance-ai/jsonschemabench). The p99 time is 0.5ms, and the p100 time is 20ms. These results are due to the lexer/parser split and several [optimizations](https://github.com/guidance-ai/llguidance/blob/main/docs/optimizations.md).

## JSON Schema

LLGuidance adheres closely to the JSON Schema specification. For example:

- `additionalProperties` defaults to `true`, unlike current grammars, though you can set `"additionalProperties": false` if needed.
- any whitespace is allowed.
- The definition order in the `"properties": {}` object is maintained, regardless of whether properties are required (current grammars always puts required properties first).

Unsupported schemas result in an error message—no keywords are silently ignored.

## Why Not Reuse GBNF Format?

GBNF lacks the concept of a lexer.

Most programming languages, including JSON, use a two-step process: a lexer (built with regular expressions) converts a byte stream into lexemes, which are then processed by a CFG parser. This approach is faster because lexers are cheaper to evaluate, and there is ~10x fewer lexemes than bytes.
LLM tokens often align with lexemes, so the parser is engaged in under 0.5% of tokens, with the lexer handling the rest.

However, the user has to provide the distinction between lexemes and CFG symbols. In [Lark](https://github.com/lark-parser/lark), lexeme names are uppercase, while CFG symbols are lowercase.
The [gbnf_to_lark.py script](https://github.com/guidance-ai/llguidance/blob/main/scripts/gbnf_to_lark.py) can often take care of this automatically.
See [LLGuidance syntax docs](https://github.com/guidance-ai/llguidance/blob/main/docs/syntax.md#terminals-vs-rules) for more details.

## Error Handling

Errors are currently printed to `stderr`, and generation continues. Improved error handling may be added in the future.

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
