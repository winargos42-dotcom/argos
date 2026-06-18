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
