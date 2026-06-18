---
argos_import: project_file
source_path: file6s/requirements-compute.txt
source_abs: F:\debug\argoss\file6s\requirements-compute.txt
source_ext: .txt
source_sha256: 3c5e644ca266ab1c2d8ef9fac04b1093fe5123fd03f65b772925a01b0c13bc6c
text_sha256: 3c5e644ca266ab1c2d8ef9fac04b1093fe5123fd03f65b772925a01b0c13bc6c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# requirements-compute.txt

- Source: `file6s/requirements-compute.txt`
- Extract: `text`
- SHA256: `3c5e644ca266ab1c2d8ef9fac04b1093fe5123fd03f65b772925a01b0c13bc6c`

## Content

# ARGOS Compute Center — dependencies
# Установка:  pip install -r requirements-compute.txt
#
# ВАЖНО: пакет `azure-ai-openai` на PyPI НЕ существует. Класс AzureOpenAI
# живёт в пакете `openai` (>=1.0). `aioredis` deprecated с 2021 — использовать
# `redis.asyncio` из пакета `redis>=4.2`.

pydantic<3,>=1.9.0
openai>=1.0.0
aiohttp>=3.9
redis>=4.2
python-dotenv>=1.0

# Azure SDK — все опциональные (код переходит в dry mode при их отсутствии),
# но нужны для реальной работы с Azure OpenAI / Cosmos / Storage.
azure-identity>=1.15
azure-cosmos>=4.5
azure-storage-blob>=12.19

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
