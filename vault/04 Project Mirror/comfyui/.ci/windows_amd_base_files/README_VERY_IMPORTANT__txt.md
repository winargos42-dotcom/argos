---
argos_import: project_file
source_path: comfyui/.ci/windows_amd_base_files/README_VERY_IMPORTANT.txt
source_abs: F:\debug\argoss\comfyui\.ci\windows_amd_base_files\README_VERY_IMPORTANT.txt
source_ext: .txt
source_sha256: 38e28a3f68f3e203b686069905578e38dd99415751bb6231879d33975093838e
text_sha256: 5f0341f86593b38011db97d091ca111a41e1caf57dcafac814c14949725ccff6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:58
---

# README_VERY_IMPORTANT.txt

- Source: `comfyui/.ci/windows_amd_base_files/README_VERY_IMPORTANT.txt`
- Extract: `text`
- SHA256: `38e28a3f68f3e203b686069905578e38dd99415751bb6231879d33975093838e`

## Content

As of the time of writing this you need this driver for best results:
https://www.amd.com/en/resources/support-articles/release-notes/RN-AMDGPU-WINDOWS-PYTORCH-7-1-1.html

HOW TO RUN:

If you have a AMD gpu:

run_amd_gpu.bat

If you have memory issues you can try disabling the smart memory management by running comfyui with:

run_amd_gpu_disable_smart_memory.bat

IF YOU GET A RED ERROR IN THE UI MAKE SURE YOU HAVE A MODEL/CHECKPOINT IN: ComfyUI\models\checkpoints

You can download the stable diffusion XL one from: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/sd_xl_base_1.0_0.9vae.safetensors


RECOMMENDED WAY TO UPDATE:
To update the ComfyUI code: update\update_comfyui.bat


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
