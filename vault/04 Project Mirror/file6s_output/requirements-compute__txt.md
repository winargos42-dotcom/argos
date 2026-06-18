---
argos_import: project_file
source_path: file6s_output/requirements-compute.txt
source_abs: F:\debug\argoss\file6s_output\requirements-compute.txt
source_ext: .txt
source_sha256: 4eafebe1faaa3feac6d034d672754ad4d8e092860e46e3d64279f50dc09aef50
text_sha256: 4eafebe1faaa3feac6d034d672754ad4d8e092860e46e3d64279f50dc09aef50
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# requirements-compute.txt

- Source: `file6s_output/requirements-compute.txt`
- Extract: `text`
- SHA256: `4eafebe1faaa3feac6d034d672754ad4d8e092860e46e3d64279f50dc09aef50`

## Content

# ═══════════════════════════════════════════════════════════════════════════╗
#  Compute Center — requirements.txt                                      ║
# ═══════════════════════════════════════════════════════════════════════════╝

# Core
aiohttp>=3.10.0
asyncio-redis>=0.16.0
pydantic>=2.8.0

# Azure SDK
openai>=1.50.0
azure-identity>=1.17.0
azure-storage-blob>=12.20.0
azure-cosmos>=4.6.0

# Cache & Storage  
redis>=4.2.0

# Async
uvicorn[standard]>=0.29.0
fastapi>=0.110.0

# Logging
python-dotenv>=1.0.0
psutil>=5.9.0

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
