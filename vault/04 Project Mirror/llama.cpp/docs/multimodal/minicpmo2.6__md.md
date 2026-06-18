---
argos_import: project_file
source_path: llama.cpp/docs/multimodal/minicpmo2.6.md
source_abs: F:\debug\argoss\llama.cpp\docs\multimodal\minicpmo2.6.md
source_ext: .md
source_sha256: 857f6aaa969d78db29062113746e9988b95cc76fe76f01c40fc65dd496561527
text_sha256: 78b99bc806c7b097ee183a707f86bfb6cc76a2971553e7f70e83359707b777e3
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# minicpmo2.6.md

- Source: `llama.cpp/docs/multimodal/minicpmo2.6.md`
- Extract: `text`
- SHA256: `857f6aaa969d78db29062113746e9988b95cc76fe76f01c40fc65dd496561527`

## Content

## MiniCPM-o 2.6
Currently, this readme only supports minicpm-omni's image capabilities, and we will update the full-mode support as soon as possible.

### Prepare models and code

Download [MiniCPM-o-2_6](https://huggingface.co/openbmb/MiniCPM-o-2_6) PyTorch model from huggingface to "MiniCPM-o-2_6" folder.


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


### Usage of MiniCPM-o 2.6

Convert PyTorch model to gguf files (You can also download the converted [gguf](https://huggingface.co/openbmb/MiniCPM-o-2_6-gguf) by us)

```bash
python ./tools/mtmd/legacy-models/minicpmv-surgery.py -m ../MiniCPM-o-2_6
python ./tools/mtmd/legacy-models/minicpmv-convert-image-encoder-to-gguf.py -m ../MiniCPM-o-2_6 --minicpmv-projector ../MiniCPM-o-2_6/minicpmv.projector --output-dir ../MiniCPM-o-2_6/ --minicpmv_version 4
python ./convert_hf_to_gguf.py ../MiniCPM-o-2_6/model

# quantize int4 version
./build/bin/llama-quantize ../MiniCPM-o-2_6/model/ggml-model-f16.gguf ../MiniCPM-o-2_6/model/ggml-model-Q4_K_M.gguf Q4_K_M
```


Inference on Linux or Mac
```bash
# run in single-turn mode
./build/bin/llama-mtmd-cli -m ../MiniCPM-o-2_6/model/ggml-model-f16.gguf --mmproj ../MiniCPM-o-2_6/mmproj-model-f16.gguf -c 4096 --temp 0.7 --top-p 0.8 --top-k 100 --repeat-penalty 1.05 --image xx.jpg -p "What is in the image?"

# run in conversation mode
./build/bin/llama-mtmd-cli -m ../MiniCPM-o-2_6/model/ggml-model-Q4_K_M.gguf --mmproj ../MiniCPM-o-2_6/mmproj-model-f16.gguf
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
