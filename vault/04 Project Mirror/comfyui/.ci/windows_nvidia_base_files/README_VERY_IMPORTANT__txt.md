---
argos_import: project_file
source_path: comfyui/.ci/windows_nvidia_base_files/README_VERY_IMPORTANT.txt
source_abs: F:\debug\argoss\comfyui\.ci\windows_nvidia_base_files\README_VERY_IMPORTANT.txt
source_ext: .txt
source_sha256: ff1823d28236fbaa6dec71df5d267c5a7e8912c9965383533ffafccc4118958b
text_sha256: 020e7446d77ffc150d576ea093cd184675ad291c43588987832354c3f43453af
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:58
---

# README_VERY_IMPORTANT.txt

- Source: `comfyui/.ci/windows_nvidia_base_files/README_VERY_IMPORTANT.txt`
- Extract: `text`
- SHA256: `ff1823d28236fbaa6dec71df5d267c5a7e8912c9965383533ffafccc4118958b`

## Content

HOW TO RUN:

if you have a NVIDIA gpu:

run_nvidia_gpu.bat

if you want to enable the fast fp16 accumulation (faster for fp16 models with slightly less quality):

run_nvidia_gpu_fast_fp16_accumulation.bat


To run it in slow CPU mode:

run_cpu.bat



IF YOU GET A RED ERROR IN THE UI MAKE SURE YOU HAVE A MODEL/CHECKPOINT IN: ComfyUI\models\checkpoints

You can download the stable diffusion 1.5 one from: https://huggingface.co/Comfy-Org/stable-diffusion-v1-5-archive/blob/main/v1-5-pruned-emaonly-fp16.safetensors


RECOMMENDED WAY TO UPDATE:
To update the ComfyUI code: update\update_comfyui.bat



To update ComfyUI with the python dependencies, note that you should ONLY run this if you have issues with python dependencies.
update\update_comfyui_and_python_dependencies.bat


TO SHARE MODELS BETWEEN COMFYUI AND ANOTHER UI:
In the ComfyUI directory you will find a file: extra_model_paths.yaml.example
Rename this file to: extra_model_paths.yaml and edit it with your favorite text editor.

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
