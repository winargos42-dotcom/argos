---
argos_import: project_file
source_path: llama.cpp/docs/multimodal/minicpmv4.0.md
source_abs: F:\debug\argoss\llama.cpp\docs\multimodal\minicpmv4.0.md
source_ext: .md
source_sha256: 13583025d5d016b87169dde213a75a7588a0eff7229cd075f02bcc053d1d9e6b
text_sha256: d4d4abda08ca8d8fe8fce6ba4ed5350088d183abb86de854e3e8f9bd1f9e7c75
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# minicpmv4.0.md

- Source: `llama.cpp/docs/multimodal/minicpmv4.0.md`
- Extract: `text`
- SHA256: `13583025d5d016b87169dde213a75a7588a0eff7229cd075f02bcc053d1d9e6b`

## Content

## MiniCPM-V 4

### Prepare models and code

Download [MiniCPM-V-4](https://huggingface.co/openbmb/MiniCPM-V-4) PyTorch model from huggingface to "MiniCPM-V-4" folder.


### Build llama.cpp
Readme modification time: 20250731

If there are differences in usage, please refer to the official build [documentation](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md)

Clone llama.cpp:
```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
```

Build llama.cpp using `CMake`:
```bash
cmake -B build
cmake --build build --config Release
```


### Usage of MiniCPM-V 4

Convert PyTorch model to gguf files (You can also download the converted [gguf](https://huggingface.co/openbmb/MiniCPM-V-4-gguf) by us)

```bash
python ./tools/mtmd/legacy-models/minicpmv-surgery.py -m ../MiniCPM-V-4
python ./tools/mtmd/legacy-models/minicpmv-convert-image-encoder-to-gguf.py -m ../MiniCPM-V-4 --minicpmv-projector ../MiniCPM-V-4/minicpmv.projector --output-dir ../MiniCPM-V-4/ --minicpmv_version 5
python ./convert_hf_to_gguf.py ../MiniCPM-V-4/model

# quantize int4 version
./build/bin/llama-quantize ../MiniCPM-V-4/model/ggml-model-f16.gguf ../MiniCPM-V-4/model/ggml-model-Q4_K_M.gguf Q4_K_M
```


Inference on Linux or Mac
```bash
# run in single-turn mode
./build/bin/llama-mtmd-cli -m ../MiniCPM-V-4/model/ggml-model-f16.gguf --mmproj ../MiniCPM-V-4/mmproj-model-f16.gguf -c 4096 --temp 0.7 --top-p 0.8 --top-k 100 --repeat-penalty 1.05 --image xx.jpg -p "What is in the image?"

# run in conversation mode
./build/bin/llama-mtmd-cli -m ../MiniCPM-V-4/model/ggml-model-Q4_K_M.gguf --mmproj ../MiniCPM-V-4/mmproj-model-f16.gguf
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
