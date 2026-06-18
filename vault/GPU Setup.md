# GPU Setup

## Hardware
- **RX 580** — Polaris 20 (gfx803), 4GB GDDR5, PCIe slot 0
- **RX 560** — Polaris 21 (gfx803), 4GB GDDR5, PCIe slot 1
- **Vega 11** — APU iGPU (gfx902), 2GB shared, integrated

## Ollama Multi-GPU Configuration
Three separate Ollama instances, each pinned to one GPU via `HIP_VISIBLE_DEVICES`.

### Environment Variables
```
OLLAMA_NUM_GPU=999
OLLAMA_FLASH_ATTENTION=1
GPU_MAX_ALLOC_PERCENT=100
OLLAMA_MODELS=F:\model
```

### Instance Configuration
| Instance | Port | HIP_VISIBLE_DEVICES | GPU | Model | Role |
|----------|------|---------------------|-----|-------|------|
| smart | 8082 | 0 | RX 580 | qwen2.5:3b | General reasoning |
| fast | 8083 | 2 | Vega 11 | tinyllama | Quick responses |
| code | 8084 | 1 | RX 560 | qwen2.5-coder:7b | Code generation |

### Startup
```batch
scripts\ollama_three_gpu.bat
```

### Known Issues
- **phi4-mini** incompatible with ROCm on Polaris (gfx803) GPUs — crashes with "llama runner process has terminated"
- Replaced with qwen2.5-coder:7b which works via partial GPU offload (4.7GB model on 4GB VRAM)

## Benchmark Results (2026-05-02)
- RX 580 / qwen2.5:3b: **12.7 tok/s** (57 tokens)
- Vega 11 / tinyllama: **54.2 tok/s** (86 tokens)
- RX 560 / qwen2.5-coder:7b: **5.1 tok/s** (55 tokens)

## Consensus Test
All 3 GPUs answered "4" to "What is 2+2?" — consensus verified.
