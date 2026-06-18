---
argos_import: project_file
source_path: llama.cpp/docs/multimodal/minicpmv4.5.md
source_abs: F:\debug\argoss\llama.cpp\docs\multimodal\minicpmv4.5.md
source_ext: .md
source_sha256: 9417c197977652c2ad2efbde654989aeeafcebace3b57dc74ea2825079608648
text_sha256: 9bfe076a2aad6b04cf801ecc397675f2206a0a478cb211bac7973aab8c0a1330
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# minicpmv4.5.md

- Source: `llama.cpp/docs/multimodal/minicpmv4.5.md`
- Extract: `text`
- SHA256: `9417c197977652c2ad2efbde654989aeeafcebace3b57dc74ea2825079608648`

## Content

## MiniCPM-V 4.5

### Prepare models and code

Download [MiniCPM-V-4_5](https://huggingface.co/openbmb/MiniCPM-V-4_5) PyTorch model from huggingface to "MiniCPM-V-4_5" folder.


### Build llama.cpp
Readme modification time: 20250826

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

Convert PyTorch model to gguf files (You can also download the converted [gguf](https://huggingface.co/openbmb/MiniCPM-V-4_5-gguf) by us)

```bash
python ./tools/mtmd/legacy-models/minicpmv-surgery.py -m ../MiniCPM-V-4_5
python ./tools/mtmd/legacy-models/minicpmv-convert-image-encoder-to-gguf.py -m ../MiniCPM-V-4_5 --minicpmv-projector ../MiniCPM-V-4_5/minicpmv.projector --output-dir ../MiniCPM-V-4_5/ --minicpmv_version 6
python ./convert_hf_to_gguf.py ../MiniCPM-V-4_5/model

# quantize int4 version
./build/bin/llama-quantize ../MiniCPM-V-4_5/model/ggml-model-f16.gguf ../MiniCPM-V-4_5/model/ggml-model-Q4_K_M.gguf Q4_K_M
```


Inference on Linux or Mac
```bash
# run in single-turn mode
./build/bin/llama-mtmd-cli -m ../MiniCPM-V-4_5/model/ggml-model-f16.gguf --mmproj ../MiniCPM-V-4_5/mmproj-model-f16.gguf -c 4096 --temp 0.7 --top-p 0.8 --top-k 100 --repeat-penalty 1.05 --image xx.jpg -p "What is in the image?"

# run in conversation mode
./build/bin/llama-mtmd-cli -m ../MiniCPM-V-4_5/model/ggml-model-Q4_K_M.gguf --mmproj ../MiniCPM-V-4_5/mmproj-model-f16.gguf
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
