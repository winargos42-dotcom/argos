---
argos_import: project_file
source_path: reports/requirements_android.txt
source_abs: F:\debug\argoss\reports\requirements_android.txt
source_ext: .txt
source_sha256: f4bd3031583ee6df73017c16534cc177c086d7fb8a3b232dd25448e14f62bcee
text_sha256: f4bd3031583ee6df73017c16534cc177c086d7fb8a3b232dd25448e14f62bcee
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:26
---

# requirements_android.txt

- Source: `reports/requirements_android.txt`
- Extract: `text`
- SHA256: `f4bd3031583ee6df73017c16534cc177c086d7fb8a3b232dd25448e14f62bcee`

## Content

# ARGOS Android/Termux requirements
# Установка: pip install -r requirements_android.txt

# Обязательные
requests>=2.31.0
python-dotenv>=1.0.0
python-telegram-bot>=20.0
aiohttp>=3.9.0

# IoT
paho-mqtt>=2.0.0
pyserial>=3.5

# Парсинг
beautifulsoup4>=4.12.0

# Утилиты
packaging>=23.0
networkx>=3.2.1

# Системные (устанавливать через pkg, не pip)
# pkg install python-psutil
# pkg install python-cryptography

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
