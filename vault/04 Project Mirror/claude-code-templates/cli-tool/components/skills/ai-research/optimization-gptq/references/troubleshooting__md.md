---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/optimization-gptq/references/troubleshooting.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\optimization-gptq\references\troubleshooting.md
source_ext: .md
source_sha256: 5a7d23462c01f7c9d52107603bcc5a91a38afb72207a4f11ac5541658f201c13
text_sha256: c20b085b6feda47397eef85ea4a47dcf59062da26149741966bd2900805c6e59
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# troubleshooting.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/optimization-gptq/references/troubleshooting.md`
- Extract: `text`
- SHA256: `5a7d23462c01f7c9d52107603bcc5a91a38afb72207a4f11ac5541658f201c13`

## Content

# GPTQ Troubleshooting Guide

Common issues and solutions for GPTQ quantization and inference.

## Installation Issues

### CUDA mismatch
```bash
# Check CUDA version
nvcc --version
python -c "import torch; print(torch.version.cuda)"

# Install matching version
pip install auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu118/  # CUDA 11.8
```

### Build errors
```bash
# Install build dependencies
pip install auto-gptq --no-build-isolation

# On Ubuntu
sudo apt-get install python3-dev
```

## Runtime Issues

### Slow inference
```python
# Try different backends
model = AutoGPTQForCausalLM.from_quantized(
    model_name,
    use_exllama=True  # Fastest (try v1 or v2)
)

# Or Marlin (Ampere+ GPUs)
model = AutoGPTQForCausalLM.from_quantized(
    model_name,
    use_marlin=True
)
```

### OOM during inference
```python
# Reduce batch size
outputs = model.generate(**inputs, batch_size=1)

# Use CPU offloading
model = AutoGPTQForCausalLM.from_quantized(
    model_name,
    device_map="auto",
    max_memory={"cpu": "100GB"}
)

# Reduce context
model.seqlen = 1024  # Instead of 2048
```

### Poor quality outputs
```python
# Requantize with better calibration
# 1. Use more samples (256 instead of 128)
# 2. Use domain-specific data
# 3. Lower dampening: damp_percent=0.005
# 4. Enable desc_act=True
```

## Quantization Issues

### Very slow quantization
```bash
# Expected times (7B model):
# - A100: 10-15 min
# - RTX 4090: 20-30 min
# - CPU: 2-4 hours

# Speed up:
# 1. Use GPU
# 2. Reduce samples (64 instead of 256)
# 3. Disable desc_act
# 4. Use multi-GPU
```

### Quantization crashes
```python
# Reduce memory usage
model = AutoGPTQForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    max_memory={"cpu": "100GB"}  # Offload to CPU
)

# Or quantize layer-by-layer (slower but works)
model.quantize(calibration_data, batch_size=1)
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
