---
argos_import: project_file
source_path: llama.cpp/docs/multimodal/minicpmv2.5.md
source_abs: F:\debug\argoss\llama.cpp\docs\multimodal\minicpmv2.5.md
source_ext: .md
source_sha256: 6bf16e7d9319f4cb942780ff46dd1a45a0f7ed8d10a622d0d290bf06ab973ac5
text_sha256: 9f8434250be4c860b58083bfe8b4310ab99aa71a8cff240ed981bf733d3fa88c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# minicpmv2.5.md

- Source: `llama.cpp/docs/multimodal/minicpmv2.5.md`
- Extract: `text`
- SHA256: `6bf16e7d9319f4cb942780ff46dd1a45a0f7ed8d10a622d0d290bf06ab973ac5`

## Content

## MiniCPM-Llama3-V 2.5

### Prepare models and code

Download [MiniCPM-Llama3-V-2_5](https://huggingface.co/openbmb/MiniCPM-Llama3-V-2_5) PyTorch model from huggingface to "MiniCPM-Llama3-V-2_5" folder.


### Build llama.cpp
Readme modification time: 20250206

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


### Usage of MiniCPM-Llama3-V 2.5

Convert PyTorch model to gguf files (You can also download the converted [gguf](https://huggingface.co/openbmb/MiniCPM-Llama3-V-2_5-gguf) by us)

```bash
python ./tools/mtmd/legacy-models/minicpmv-surgery.py -m ../MiniCPM-Llama3-V-2_5
python ./tools/mtmd/legacy-models/minicpmv-convert-image-encoder-to-gguf.py -m ../MiniCPM-Llama3-V-2_5 --minicpmv-projector ../MiniCPM-Llama3-V-2_5/minicpmv.projector --output-dir ../MiniCPM-Llama3-V-2_5/ --minicpmv_version 2
python ./convert_hf_to_gguf.py ../MiniCPM-Llama3-V-2_5/model

# quantize int4 version
./build/bin/llama-quantize ../MiniCPM-Llama3-V-2_5/model/model-8B-F16.gguf ../MiniCPM-Llama3-V-2_5/model/ggml-model-Q4_K_M.gguf Q4_K_M
```


Inference on Linux or Mac
```bash
# run in single-turn mode
./build/bin/llama-mtmd-cli -m ../MiniCPM-Llama3-V-2_5/model/model-8B-F16.gguf --mmproj ../MiniCPM-Llama3-V-2_5/mmproj-model-f16.gguf -c 4096 --temp 0.7 --top-p 0.8 --top-k 100 --repeat-penalty 1.05 --image xx.jpg -p "What is in the image?"

# run in conversation mode
./build/bin/llama-mtmd-cli -m ../MiniCPM-Llama3-V-2_5/model/ggml-model-Q4_K_M.gguf --mmproj ../MiniCPM-Llama3-V-2_5/mmproj-model-f16.gguf
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
