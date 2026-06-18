---
argos_import: project_file
source_path: GPU_INTEGRATION_README.txt
source_abs: F:\debug\argoss\GPU_INTEGRATION_README.txt
source_ext: .txt
source_sha256: ebc15b87d5c36d19fbcfcd3e4ec5f7d3567ac2fde2834c6327fedacaf2414433
text_sha256: ebc15b87d5c36d19fbcfcd3e4ec5f7d3567ac2fde2834c6327fedacaf2414433
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# GPU_INTEGRATION_README.txt

- Source: `GPU_INTEGRATION_README.txt`
- Extract: `text`
- SHA256: `ebc15b87d5c36d19fbcfcd3e4ec5f7d3567ac2fde2834c6327fedacaf2414433`

## Content

ARGOS GPU INTEGRATION - POST-REBOOT INSTRUCTIONS
=================================================

WHAT WAS DONE:
1. Added 'local-gpu' AI mode to src/core.py
2. Set ARGOS_AI_MODE=local-gpu in .env
3. Created GPU server connection methods:
   - _get_local_gpu_servers() - reads GPU config
   - _check_gpu_server_health() - checks /health endpoint
   - _ask_local_gpu() - queries llama-server via /completion API
4. LocalGPU has HIGHEST priority in auto mode
5. Fallback to Ollama if GPU unavailable

GPU SERVERS CONFIGURED:
- GPU0-RX580: localhost:8082 (qwen2.5:3b)
- GPU1-Vega11: localhost:8083 (tinyllama)
- GPU2-RX560: localhost:8084 (phi4-mini)

AFTER REBOOT:
1. GPU servers should auto-start (check watchdog)
2. Start ARGOS: .\start_argos.bat
3. Check GPU status: python test_gpu.py
4. Test in Telegram: say "Hello"

IF GPU RETURNS ERRORS:
- ARGOS will fallback to Ollama automatically
- Check GPU servers: python test_gpu.py
- Restart GPU: use watchdog_menu.bat

CREATED FILES:
- test_gpu.py - GPU health check
- test_local_gpu.py - GPU integration test
- argos_watchdog.ps1 - System monitor
- watchdog_auto.bat - Auto-start monitor
- watchdog_menu.bat - Interactive menu
- setup_comfyui.ps1 - ComfyUI installer
- SYSTEM_STATUS.md - System status backup
- BACKUP_CONFIGS.md - Config backup

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
