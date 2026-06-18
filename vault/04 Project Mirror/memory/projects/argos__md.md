---
argos_import: project_file
source_path: memory/projects/argos.md
source_abs: F:\debug\argoss\memory\projects\argos.md
source_ext: .md
source_sha256: c558daf818a3e0e8d7d76919a7d9b0fee7debf9725ae4b2284ded02fa9fbd064
text_sha256: c558daf818a3e0e8d7d76919a7d9b0fee7debf9725ae4b2284ded02fa9fbd064
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# argos.md

- Source: `memory/projects/argos.md`
- Extract: `text`
- SHA256: `c558daf818a3e0e8d7d76919a7d9b0fee7debf9725ae4b2284ded02fa9fbd064`

## Content

# ARGOS Universal OS

**Version:** 2.1.3
**Repo:** github.com/iliyaqdrwalqu/Argoss
**Author:** Всеволод (Seva / АvA / SiG)
**License:** Apache 2.0

## Description
Самовоспроизводящаяся кроссплатформенная AI-экосистема с квантовой логикой, P2P-подключением и интеграцией с IoT.

## Platforms
- Desktop (Windows / Linux)
- Android APK
- Docker (`ghcr.io/iliyaqdrwalqu/argoss:latest`)
- Telegram Bot
- Google Colab

## AI Providers Supported
Gemini, GigaChat, YandexGPT, LM Studio, OpenAI, Grok, Ollama/Llama3, IBM Watsonx (Llama-3.1-70B)

## Key Modules
| Module | Function |
|--------|----------|
| AWA-Core | Центральный координатор, capability-routing |
| web_learn | DuckDuckGo веб-поиск |
| ColibriAsmEngine | Ассемблер/дизассемблер микрокода |
| ArgosOSBuilder | Сборка загрузочного ISO/ZIP образа |
| AndroidFlasher | Прошивка Android через fastboot/ADB |
| FirmwareBuilder | Компиляция прошивок ESP32/AVR/ARM |
| DeviceScanner | Автосканирование + адаптивный образ |

## Stack
- Python (core)
- Redis (кэш)
- PostgreSQL (хранилище)
- Docker / Docker Compose
- SQLite (локальная память агента)
- aiohttp (async HTTP)
- Kivy (GUI, optional)

## CI/CD Workflows
- `build_apk.yml` — Android APK
- `release.yml` — Release билды
- `docker.yml` — Docker образ
- `ci.yml` — Общий CI
- `status_report.yml` — Статус-репорт

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
