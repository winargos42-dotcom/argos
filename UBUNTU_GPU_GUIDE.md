# ARGOS GPU Setup - Ubuntu + ROCm

## Overview
This setup enables all 3 AMD GPUs (RX 580, RX 560, Vega 11) using Ubuntu with ROCm.

## Why Ubuntu?
- **Windows WDDM**: Blocks compute on RX 580/560 (discrete GPUs show 00% usage)
- **Linux ROCm**: Full compute support for Polaris architecture (RX 580/560)
- **Performance**: All 3 GPUs work at 100% capacity

## Prerequisites
- Ubuntu installed (WSL2, Dual Boot, or Native)
- AMD GPUs: RX 580, RX 560, Vega 11
- Models: qwen2.5-3b.gguf, phi4-mini.gguf, tinyllama-1.1b-chat-q4_k_m.gguf

## Quick Start

### 1. Setup Ubuntu (run in Ubuntu terminal)
```bash
cd ~
# Copy setup script from Windows
cp /mnt/f/debug/argoss/ubuntu_setup_gpu.sh .
chmod +x ubuntu_setup_gpu.sh
./ubuntu_setup_gpu.sh
```

### 2. Start GPU Servers (in Ubuntu)
```bash
cd ~/llama.cpp
./start_argos_gpu.sh
```

### 3. Start ARGOS (in Windows)
```cmd
F:\debug\argoss> start_argos_ubuntu_gpu.bat
```

## GPU Configuration

| GPU | Port | Model | HIP Device | Status |
|-----|------|-------|------------|--------|
| RX 580 | 8082 | qwen2.5-3b | 0 | Primary |
| RX 560 | 8083 | phi4-mini | 1 | Secondary |
| Vega 11 | 8084 | tinyllama | CPU/Vulkan | Fallback |

## Troubleshooting

### Vega 11 not working with ROCm
- Vega 11 (iGPU) may not be supported by ROCm
- Use CPU mode or build with Vulkan backend

### WSL2: Models not found
- Ensure F: drive is mounted: `ls /mnt/f/ROCm/models`
- If empty, check Windows path

### Dual Boot: Connection issues
- Find Ubuntu IP: `hostname -I` in Ubuntu
- Update start_argos_ubuntu_gpu.bat with correct IP

## Files
- `ubuntu_setup_gpu.sh` - Full ROCm + llama.cpp setup
- `ubuntu_start_gpu.sh` - GPU server launcher (auto-generated)
- `ubuntu_test_gpu.sh` - GPU health check
- `start_argos_ubuntu_gpu.bat` - Windows ARGOS launcher

## Performance
- RX 580: ~30-50 tokens/sec (qwen2.5-3b)
- RX 560: ~20-30 tokens/sec (phi4-mini)
- Vega 11/CPU: ~10-15 tokens/sec (tinyllama)

## Notes
- After Ubuntu setup, relogin to apply group changes
- GPU servers auto-start on Ubuntu boot (add to crontab)
- Windows ARGOS connects via network (localhost for WSL2)
