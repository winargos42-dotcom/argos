---
argos_import: project_file
source_path: llama.cpp/examples/debug/README.md
source_abs: F:\debug\argoss\llama.cpp\examples\debug\README.md
source_ext: .md
source_sha256: f6ae928107cd96bb42fcf7236792482f0de9e9461d7495f5872a73ba934517be
text_sha256: 1e2ac180e5187501f0438eb9df7de235ba6968a65ce432ba9944bd909ee498fd
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# README.md

- Source: `llama.cpp/examples/debug/README.md`
- Extract: `text`
- SHA256: `f6ae928107cd96bb42fcf7236792482f0de9e9461d7495f5872a73ba934517be`

## Content

# llama.cpp/examples/debug

This is a utility intended to help debug a model by registering a callback that
logs GGML operations and tensor data. It can also store the generated logits or
embeddings as well as the prompt and token ids for comparison with the original
model.

### Usage

```shell
llama-debug \
  --hf-repo ggml-org/models \
  --hf-file phi-2/ggml-model-q4_0.gguf \
  --model phi-2-q4_0.gguf \
  --prompt hello \
  --save-logits \
  --verbose
```
The tensor data is logged as debug and required the --verbose flag. The reason
for this is that while useful for a model with many layers there can be a lot of
output. You can filter the tensor names using the `--tensor-filter` option.

A recommended approach is to first run without `--verbose` and see if the
generated logits/embeddings are close to the original model. If they are not,
then it might be required to inspect tensor by tensor and in that case it is
useful to enable the `--verbose` flag along with `--tensor-filter` to focus on
specific tensors.

### Options
This example supports all standard `llama.cpp` options and also accepts the
following options:
```console
$ llama-debug --help
...

----- example-specific params -----

--save-logits                           save final logits to files for verification (default: false)
--logits-output-dir PATH                directory for saving logits output files (default: data)
--tensor-filter REGEX                   filter tensor names for debug output (regex pattern, can be specified multiple times)
```

### Output Files

When `--save-logits` is enabled, the following files are created in the output
directory:

* `llamacpp-<model>[-embeddings].bin`        - Binary output (logits or embeddings)
* `llamacpp-<model>[-embeddings].txt`        - Text output (logits or embeddings, one per line)
* `llamacpp-<model>[-embeddings]-prompt.txt` - Prompt text and token IDs
* `llamacpp-<model>[-embeddings]-tokens.bin` - Binary token IDs for programmatic comparison

These files can be compared against the original model's output to verify the
converted model.

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
