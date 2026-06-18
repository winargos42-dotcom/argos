---
argos_import: project_file
source_path: GPU_FINAL_STATUS.txt
source_abs: F:\debug\argoss\GPU_FINAL_STATUS.txt
source_ext: .txt
source_sha256: 608843734ffabfa0ec615e0ad123f6b2d5f3d5f619341604312b6c27f505987b
text_sha256: 608843734ffabfa0ec615e0ad123f6b2d5f3d5f619341604312b6c27f505987b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# GPU_FINAL_STATUS.txt

- Source: `GPU_FINAL_STATUS.txt`
- Extract: `text`
- SHA256: `608843734ffabfa0ec615e0ad123f6b2d5f3d5f619341604312b6c27f505987b`

## Content

ARGOS GPU CONFIGURATION - FINAL STATUS
======================================

GPU SERVERS (All 3 Online):
- GPU0-RX580:  localhost:8082 - qwen2.5-3b (1.8GB)
- GPU1-Vega11: localhost:8083 - tinyllama (637MB)
- GPU2-RX560:  localhost:8084 - phi4-mini (2.3GB)

IMPORTANT NOTE:
phi4-mini-3.8b-q4_k_m.gguf was corrupted (0 bytes), 
so GPU2 uses phi4-mini.gguf (2.3GB) instead.

AI MODE: local-gpu (set in .env)
ARGOS will use GPU servers instead of Ollama CPU.

PERFORMANCE:
- GPU0: Fast (RX 580 4GB, qwen2.5-3b)
- GPU1: Very fast (Vega 11 2GB, tinyllama)
- GPU2: Medium (RX 560 4GB, phi4-mini 2.3GB)

If GPU2 is slow, ARGOS will try GPU1 or GPU0 first.

TO START:
1. GPU servers: .\start_gpu_auto.bat
2. ARGOS: .\start_argos.bat

Files saved:
- src/core.py (modified with local-gpu support)
- .env (ARGOS_AI_MODE=local-gpu)
- start_gpu_auto.bat (starts all 3 GPU servers)
- verify_all.py (verification script)

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
