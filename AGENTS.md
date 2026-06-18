# Memory

## Me
Всеволод (Seva / АvA / SiG) — разработчик, автор проекта ARGOS.

## Projects
| Name | What |
|------|------|
| **ARGOS** | Argos Universal OS v2.1.3 — самовоспроизводящаяся кроссплатформенная AI-экосистема (Desktop / Android / Docker / Telegram) |

## Teams / Owners
Всё один человек (Сева). Роли — контекст задачи, не реальные люди.
| Tag | Контекст |
|-----|---------|
| `infra` | Инфраструктура (Llama.cpp, Ollama, RAM-диск) |
| `platform` | Платформа (Redis, aiohttp, PostgreSQL, Cloudflare) |
| `sre` | Надёжность (circuit breaker, watchtower, ArgoCD) |
| `app` | Приложение (Docker-изоляция, логирование) |

## Key Terms
| Term | Meaning |
|------|---------|
| `web_learn` | Модуль поиска через DuckDuckGo |
| `Llama.cpp` | Локальный оффлайн LLM-движок |
| `Ollama` | Запускатель LLM-моделей |
| `ArgoCD` | GitOps-инструмент синхронизации конфигураций |
| `watchtower` | Авто-обновлятор Docker-контейнеров |
| `circuit breaker` | Паттерн отказоустойчивости (3 неудачи → fallback) |
| `AWA-Core` | Центральный координатор модулей ARGOS |
| `ColibriAsmEngine` | Ассемблер/дизассемблер микрокода в реальном времени |
| `npm_manager` | Навык управления npm пакетами (install, audit, outdated, npx). Интегрирован в SkillLoader, доступен через команды: `npm install`, `npm list`, `npm audit`, `npm run`, `npm info` |
| `porphyry` | Философский модуль "Триада Порфирия" — симуляция коллективного мышления через три аспекта: трезвый (аналитик), эмоциональный (ироник), интуитивный (озаритель). Режим консилиума объединяет все три. Команды: `порфирий аналитик/ироник/озаритель/консилиум`, `порфирий глубина 1-3`, `порфирий <тема>`. Честно признаётся в симуляции — без претензий на реальное метасознание |
| `orangepi_gadget` | Управление USB Gadget Orange Pi One (serial/ethernet/storage). Python-модуль `src/connectivity/orangepi_gadget.py` + shell-скрипт `deploy/usb_gadget_setup.sh`. Интегрирован в MCP API и Telegram команды `opi_gadget status/setup/stop/diagnostics` |
| `orangepi_bridge` | Аппаратный мост Orange Pi One: GPIO, I2C, UART, SPI, 1-Wire, RS-485, Modbus RTU. Python-модуль `src/connectivity/orangepi_bridge.py`. Поддерживает датчики BMP280, DS18B20, OLED, ADS1115. MCP tool `orangepi_bridge` + Telegram команды `opi status/gpio_out/gpio_in/i2c_scan/bmp280/1wire/uart_send/scan_all` |
| `ollama_vision` | Ollama Vision — анализ изображений через локальную Ollama (multimodal). Python-модуль `src/connectivity/ollama_vision_bridge.py`. Поддерживает описание изображений, OCR, анализ скриншотов. MCP tool `ollama_vision` + Telegram команды `vision status/describe/ocr/screenshot` |
| `pi_bridge` | Pi Coding Agent — интеграция внешнего агента программирования. Python-модуль `src/connectivity/pi_bridge.py`. Поддерживает выполнение задач по написанию кода, рефакторингу, оптимизации. MCP tool `pi_bridge` + Telegram команды `pi status/models/run/async` |

## AI Configuration
- **GPU Cluster**: 3 x AMD GPU (RX 580 4GB, Vega 11 2GB, RX 560 4GB)
- **AI Mode**: `auto` — использует всех доступных провайдеров
- **AI Priority**: `local-gpu,vm-cluster,azure,ollama,kimi,claude,gemini,openai,groq,deepseek,pi,yandexgpt`
- **Fallback**: Включен — при недоступности одного провайдера переключается на следующий
- **Parallel**: Включен — использует несколько провайдеров одновременно где возможно
- **Ollama**: Включена с GPU ускорением (`OLLAMA_GPU_ENABLED=true`)
- **Providers**: Kimi, Ollama, Claude, Gemini, OpenAI, Groq, DeepSeek, Pi, YandexGPT, Azure

## Preferences
- Язык задач: русский
- Приоритеты: P1 (критичные) → P2 (важные) → P3 (низкий приоритет)

## Pi Session — 2026-04-28 14:52
- ARGOS: 2.1.3
- Mode: server
- PID: 3260
- URL: http://localhost:18765

## Pi Session — 2026-04-28 15:01
- ARGOS: 2.1.3
- Mode: server
- PID: 15884
- URL: http://localhost:18765

## Pi Session — 2026-04-28 15:07
- ARGOS: 2.1.3
- Mode: server
- PID: 20924
- URL: http://localhost:18765

## Pi Session — 2026-04-28 15:10
- ARGOS: 2.1.3
- Mode: server
- PID: 19080
- URL: http://localhost:18765

## Pi Session — 2026-04-28 15:21
- ARGOS: 2.1.3
- Mode: server
- PID: 15100
- URL: http://localhost:18765

## Pi Session — 2026-04-28 15:36
- ARGOS: 2.1.3
- Mode: server
- PID: 3204
- URL: http://localhost:18765

## Pi Session — 2026-04-28 15:38
- ARGOS: 2.1.3
- Mode: server
- PID: 12972
- URL: http://localhost:18765

## Pi Session — 2026-04-28 15:47
- ARGOS: 2.1.3
- Mode: server
- PID: 12836
- URL: http://localhost:18765

## Pi Session — 2026-04-28 15:59
- ARGOS: 2.1.3
- Mode: server
- PID: 10864
- URL: http://localhost:18765

## Pi Session — 2026-04-28 17:14
- ARGOS: 2.1.3
- Mode: server
- PID: 17308
- URL: http://localhost:18765

## Pi Session — 2026-04-28 17:16
- ARGOS: 2.1.3
- Mode: server
- PID: 20360
- URL: http://localhost:18765

## Pi Session — 2026-04-28 17:22
- ARGOS: 2.1.3
- Mode: server
- PID: 9544
- URL: http://localhost:18765

## Pi Session — 2026-04-28 17:33
- ARGOS: 2.1.3
- Mode: server
- PID: 4352
- URL: http://localhost:18765

## Pi Session — 2026-04-28 17:38
- ARGOS: 2.1.3
- Mode: server
- PID: 21004
- URL: http://localhost:18765

## Pi Session — 2026-04-28 17:41
- ARGOS: 2.1.3
- Mode: server
- PID: 19084
- URL: http://localhost:18765

## Pi Session — 2026-04-28 19:19
- ARGOS: 2.1.3
- Mode: server
- PID: 4092
- URL: http://localhost:18765

## Pi Session — 2026-04-28 20:20
- ARGOS: 2.1.3
- Mode: server
- PID: 13560
- URL: http://localhost:18765

## Pi Session — 2026-04-28 20:26
- ARGOS: 2.1.3
- Mode: server
- PID: 12012
- URL: http://localhost:18765

## Pi Session — 2026-04-28 20:29
- ARGOS: 2.1.3
- Mode: server
- PID: 10700
- URL: http://localhost:18765

## Pi Session — 2026-04-28 20:40
- ARGOS: 2.1.3
- Mode: server
- PID: 13900
- URL: http://localhost:18765

## Pi Session — 2026-04-28 20:43
- ARGOS: 2.1.3
- Mode: server
- PID: 12556
- URL: http://localhost:18765

## Pi Session — 2026-04-28 20:43
- ARGOS: 2.1.3
- Mode: server
- PID: 2116
- URL: http://localhost:18765

## Pi Session — 2026-04-28 20:51
- ARGOS: 2.1.3
- Mode: server
- PID: 7600
- URL: http://localhost:18765

## Pi Session — 2026-04-28 21:19
- ARGOS: 2.1.3
- Mode: server
- PID: 13692
- URL: http://localhost:18765

## Pi Session — 2026-04-28 21:25
- ARGOS: 2.1.3
- Mode: server
- PID: 14876
- URL: http://localhost:18765

## Pi Session — 2026-04-28 21:35
- ARGOS: 2.1.3
- Mode: server
- PID: 7276
- URL: http://localhost:18765

## Pi Session — 2026-04-28 21:45
- ARGOS: 2.1.3
- Mode: server
- PID: 2556
- URL: http://localhost:18765

## Pi Session — 2026-04-28 21:46
- ARGOS: 2.1.3
- Mode: server
- PID: 6424
- URL: http://localhost:18765

## Pi Session — 2026-04-29 01:43
- ARGOS: 2.1.3
- Mode: server
- PID: 14216
- URL: http://localhost:18765

## Pi Session — 2026-04-29 10:03
- ARGOS: 2.1.3
- Mode: server
- PID: 3484
- URL: http://localhost:18765

## Pi Session — 2026-04-29 10:59
- ARGOS: 2.1.3
- Mode: server
- PID: 7716
- URL: http://localhost:18765

## Pi Session — 2026-04-29 11:05
- ARGOS: 2.1.3
- Mode: server
- PID: 7504
- URL: http://localhost:18765

## Pi Session — 2026-04-29 11:14
- ARGOS: 2.1.3
- Mode: server
- PID: 13820
- URL: http://localhost:18765

## Pi Session — 2026-04-29 11:28
- ARGOS: 2.1.3
- Mode: server
- PID: 2256
- URL: http://localhost:18765

## Pi Session — 2026-04-29 11:41
- ARGOS: 2.1.3
- Mode: server
- PID: 7572
- URL: http://localhost:18765

## Pi Session — 2026-04-29 11:59
- ARGOS: 2.1.3
- Mode: server
- PID: 13388
- URL: http://localhost:18765

## Pi Session — 2026-04-29 12:06
- ARGOS: 2.1.3
- Mode: server
- PID: 7740
- URL: http://localhost:18765

## Pi Session — 2026-04-29 12:06
- ARGOS: 2.1.3
- Mode: server
- PID: 3180
- URL: http://localhost:18765

## Pi Session — 2026-04-29 12:07
- ARGOS: 2.1.3
- Mode: server
- PID: 16392
- URL: http://localhost:18765

## Pi Session — 2026-04-29 12:10
- ARGOS: 2.1.3
- Mode: server
- PID: 16980
- URL: http://localhost:18765

## Pi Session — 2026-04-29 12:13
- ARGOS: 2.1.3
- Mode: server
- PID: 7600
- URL: http://localhost:18765

## Pi Session — 2026-04-29 13:03
- ARGOS: 2.1.3
- Mode: server
- PID: 7300
- URL: http://localhost:18765

## Pi Session — 2026-04-29 13:04
- ARGOS: 2.1.3
- Mode: server
- PID: 18456
- URL: http://localhost:18765

## Pi Session — 2026-04-29 13:07
- ARGOS: 2.1.3
- Mode: server
- PID: 7292
- URL: http://localhost:18765

## Pi Session — 2026-04-29 13:09
- ARGOS: 2.1.3
- Mode: server
- PID: 8812
- URL: http://localhost:18765

## Pi Session — 2026-04-29 13:11
- ARGOS: 2.1.3
- Mode: server
- PID: 7448
- URL: http://localhost:18765

## Pi Session — 2026-04-29 13:25
- ARGOS: 2.1.3
- Mode: server
- PID: 9880
- URL: http://localhost:18765

## Pi Session — 2026-04-29 13:26
- ARGOS: 2.1.3
- Mode: server
- PID: 19472
- URL: http://localhost:18765

## Pi Session — 2026-04-29 13:32
- ARGOS: 2.1.3
- Mode: server
- PID: 1184
- URL: http://localhost:18765

## Pi Session — 2026-04-29 13:35
- ARGOS: 2.1.3
- Mode: server
- PID: 17732
- URL: http://localhost:18765

## Pi Session — 2026-04-29 13:35
- ARGOS: 2.1.3
- Mode: server
- PID: 23532
- URL: http://localhost:18765

## Pi Session — 2026-04-29 13:42
- ARGOS: 2.1.3
- Mode: server
- PID: 8948
- URL: http://localhost:18765

## Pi Session — 2026-04-29 14:23
- ARGOS: 2.1.3
- Mode: server
- PID: 13256
- URL: http://localhost:18765

## Pi Session — 2026-04-29 14:26
- ARGOS: 2.1.3
- Mode: server
- PID: 17820
- URL: http://localhost:18765

## Pi Session — 2026-04-29 14:26
- ARGOS: 2.1.3
- Mode: server
- PID: 2488
- URL: http://localhost:18765

## Pi Session — 2026-04-29 14:27
- ARGOS: 2.1.3
- Mode: server
- PID: 22440
- URL: http://localhost:18765

## Pi Session — 2026-04-29 14:29
- ARGOS: 2.1.3
- Mode: server
- PID: 21116
- URL: http://localhost:18765

## Pi Session — 2026-04-29 14:30
- ARGOS: 2.1.3
- Mode: server
- PID: 3776
- URL: http://localhost:18765

## Pi Session — 2026-04-29 14:30
- ARGOS: 2.1.3
- Mode: server
- PID: 6500
- URL: http://localhost:18765

## GPU Configuration
- **GPU4 (DeepSeek-Coder-V2)**: llama.cpp сервер на порту 8085, модель `DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf` (15.7B, Q4_K_M)
- **ENV**: `OLLAMA_HOST_4`, `OLLAMA_HOST_4_MODEL`, `OLLAMA_HOST_4_NAME`, `OLLAMA_CLUSTER_MODE=true`
- **ENV (core.py)**: `GPU_SERVER_4_HOST/PORT/MODEL/NAME` — для `_get_local_gpu_servers()`
- **Fallback**: Ollama :11434 (tinyllama)
- **API**: `/completion` (llama.cpp), `/v1/chat/completions` (OpenAI-compatible)
- **core.py**: `_get_local_gpu_servers()` читает GPU_SERVER_* + OLLAMA_HOST_4
- **awa_core.py**: `route_task()` использует только GPU4 (DeepSeek-Coder-V2)
- **Важно**: `_ask_local_gpu()` в core.py использует `_get_local_gpu_servers()` — не путать с awa_core!
- **История**: 2026-04-29 — интегрирован GPU4, исправлено что не используется (добавлены GPU_SERVER_4 в .env + OLLAMA_HOST_4 в _get_local_gpu_servers)

## Pi Session — 2026-04-29 15:01
- ARGOS: 2.1.3
- Mode: server
- URL: http://localhost:18765
- Action: Интегрирован GPU4 (DeepSeek-Coder-V2 :8085) в ARGOS. Исправлено что core.py _get_local_gpu_servers() не видел GPU4. Добавлены GPU_SERVER_4_* переменные в .env + OLLAMA_HOST_4 читается напрямую. Сохранено в AGENTS.md.

## Pi Session — 2026-04-29 14:57
- ARGOS: 2.1.3
- Mode: server
- PID: 15656
- URL: http://localhost:18765

## Pi Session — 2026-04-29 15:18
- ARGOS: 2.1.3
- Mode: server
- PID: 4524
- URL: http://localhost:18765

## Pi Session — 2026-04-29 15:23
- ARGOS: 2.1.3
- Mode: server
- PID: 12024
- URL: http://localhost:18765

## Pi Session — 2026-04-29 15:27
- ARGOS: 2.1.3
- Mode: server
- PID: 18124
- URL: http://localhost:18765

## Pi Session — 2026-04-29 15:30
- ARGOS: 2.1.3
- Mode: server
- PID: 23804
- URL: http://localhost:18765

## Pi Session — 2026-04-29 15:54
- ARGOS: 2.1.3
- Mode: server
- PID: 22796
- URL: http://localhost:18765

## Pi Session — 2026-04-29 15:56
- ARGOS: 2.1.3
- Mode: server
- PID: 21168
- URL: http://localhost:18765

## Pi Session — 2026-04-29 16:06
- ARGOS: 2.1.3
- Mode: server
- PID: 20876
- URL: http://localhost:18765

## Pi Session — 2026-04-29 16:32
- ARGOS: 2.1.3
- Mode: server
- PID: 3800
- URL: http://localhost:18765

## Pi Session — 2026-04-29 17:33
- ARGOS: 2.1.3
- Mode: server
- PID: 5064
- URL: http://localhost:18765

## Pi Session — 2026-04-29 18:09
- ARGOS: 2.1.3
- Mode: server
- PID: 11080
- URL: http://localhost:18765

## Pi Session — 2026-04-29 18:26
- ARGOS: 2.1.3
- Mode: server
- PID: 14208
- URL: http://localhost:18765

## Pi Session — 2026-04-29 19:15
- ARGOS: 2.1.3
- Mode: server
- PID: 15076
- URL: http://localhost:18765

## Pi Session — 2026-04-29 19:20
- ARGOS: 2.1.3
- Mode: server
- PID: 6712
- URL: http://localhost:18765

## Pi Session — 2026-04-29 20:00
- ARGOS: 2.1.3
- Mode: server
- URL: http://localhost:18765
- Action: Настройка ARGOS+ провайдеров и GPU кластера
  1. Создан Modelfile для ds-coder-v2:latest (num_gpu 99, num_ctx 2048)
  2. Собрана модель ds-coder-v2-max:latest (10GB, оптимизирована для GPU)
  3. Обновлен start_gpu_llama.bat — llama-server на 8085 использует все 3 GPU (Vulkan)
  4. Создан start_ollama_all_gpu.ps1 — скрипт запуска Ollama со всеми 3 GPU
  5. Обновлен .env: AI_PRIORITY (local-gpu,kimi,deepseek...), GPU_SERVER_4 настроен
  6. Обнаружены системные переменные ограничивающие GPU (HIP_VISIBLE_DEVICES=1 и др.)
  7. Система: AMD Ryzen 5 3350G, 48GB RAM, 3 GPU (RX 580 4GB, Vega 11 2GB, RX 560 4GB)
  8. Ollama обнаруживает все 3 GPU через Vulkan (31.3GB суммарной VRAM)

## Pi Session — 2026-04-29 20:22
- ARGOS: 2.1.3
- Mode: server
- PID: 13120
- URL: http://localhost:18765

## Pi Session — 2026-04-30 00:42
- ARGOS: 2.1.3
- Mode: server
- URL: http://localhost:18765
- Action: Запуск Windows Ollama + llama-server со всеми 3 GPU
  1. Ollama перезапущена через start_ollama_all_gpu.ps1 (очищены HIP_VISIBLE_DEVICES)
  2. Обнаружены все 3 GPU: RX 580 (4GB), RX 560 (4GB), RX Vega 11 (shared 24GB)
  3. Суммарная VRAM: 31.3 GB
  4. Запущен llama-server на порту 8085 (ngl=99, split-mode=layer)
  5. OLLAMA_MODEL=ds-coder-v2-max:latest (оптимизированная, 99 GPU layers)
  6. OLLAMA_FAST_MODEL=llama3.2:1b (быстрые рефлексы)
  7. AI_PRIORITY: local-gpu → kimi → deepseek → claude → ollama → остальные
  8. WSL Ubuntu Ollama оставлена на CPU (172.17.54.97:11434, fallback)

## Pi Session — 2026-04-29 20:35
- ARGOS: 2.1.3
- Mode: server
- PID: 19896
- URL: http://localhost:18765

## Pi Session — 2026-04-29 20:48
- ARGOS: 2.1.3
- Mode: server
- PID: 16680
- URL: http://localhost:18765

## Pi Session — 2026-04-29 20:57
- ARGOS: 2.1.3
- Mode: server
- PID: 3460
- URL: http://localhost:18765

## Pi Session — 2026-04-29 21:07
- ARGOS: 2.1.3
- Mode: server
- PID: 9732
- URL: http://localhost:18765

## Pi Session — 2026-04-30 07:24
- ARGOS: 2.1.3
- Mode: server
- URL: http://localhost:18765
- Action: Ollama перенесена на порт 11666 с 7 параллельными потоками
  - Ollama: localhost:11666 (3x AMD GPU, Vulkan)
  - llama-server: localhost:8085 (DeepSeek, 99 GPU layers)
  - WSL Ubuntu: оставлена для других сервисов (CPU only)
  - .env обновлён: OLLAMA_HOST=http://localhost:11666

## Pi Session — 2026-04-30 07:59
- ARGOS: 2.1.3
- Mode: server
- PID: 2244
- URL: http://localhost:18765

## Pi Session — 2026-04-30 08:28
- ARGOS: 2.1.3
- Mode: server
- PID: 10128
- URL: http://localhost:18765

## Pi Session — 2026-04-30 09:11
- ARGOS: 2.1.3
- Mode: server
- PID: 9868
- URL: http://localhost:18765

## Pi Session — 2026-04-30 09:35
- ARGOS: 2.1.3
- Mode: server
- URL: http://localhost:18765
- Action: Исправлены ошибки Ollama (HTTP 500, CPU overload)
  1. Создана ds-coder-v2-safe:latest (num_ctx 1024, num_gpu 50, 9.7GB)
  2. Ollama (11666): работает стабильно
  3. Таймауты увеличены: TIMEOUT=120s, SMART=180s
  4. Параллельные потоки уменьшены: NUM_PARALLEL=3
  5. llama-server (8085): перезапущен, загрузка модели ~60 сек
  6. CPU overload исправлен — модель больше не падает в CPU fallback

## Pi Session — 2026-04-30 09:56
- ARGOS: 2.1.3
- Mode: server
- URL: http://localhost:18765
- Action: Исправлен конфликт портов Ollama — GPU теперь работают
  1. Обнаружено: запущено 2 экземпляра Ollama (11434 и 11666)
  2. Служба Ollama автоматически перезапускалась на 11434
  3. Остановлены все процессы, отключена служба от автозапуска
  4. Запущена одна Ollama на порту 11434 со всеми 3 GPU
  5. .env обновлён: OLLAMA_HOST=http://localhost:11434
  6. Порт 11666 освобождён, конфликт устранён

## Pi Session — 2026-04-30 20:43
- ARGOS: 2.1.3
- Mode: server
- PID: 2116
- URL: http://localhost:18765
- Action: Настройка ARGOS+ провайдеров и GPU кластера
  1. Удалены кривые модели (ds-coder-v2-max/safe/mix/lite)
  2. Используется оригинал ds-coder-v2:latest (18.6GB, работает на 3 GPU)
  3. Таймауты увеличены до 300с для загрузки модели в GPU
  4. Ollama: localhost:11434 (3x AMD GPU, Vulkan)
  5. Модель загружается в GPU (18.6GB VRAM)
  6. Первый запрос: ~23 сек (загрузка модели)
  7. Система: AMD Ryzen 5 3350G, 48GB RAM, 3 GPU (RX 580 4GB, Vega 11 2GB, RX 560 4GB)
  8. Суммарная VRAM: 31.3 GB через Vulkan

## Pi Session — 2026-04-30 09:56
- ARGOS: 2.1.3
- Mode: server
- PID: 3704
- URL: http://localhost:18765

## Pi Session — 2026-04-30 09:59
- ARGOS: 2.1.3
- Mode: server
- PID: 19212
- URL: http://localhost:18765

## Pi Session — 2026-04-30 10:18
- ARGOS: 2.1.3
- Mode: server
- PID: 11348
- URL: http://localhost:18765

## Pi Session — 2026-04-30 16:08
- ARGOS: 2.1.3
- Mode: server
- PID: 2496
- URL: http://localhost:18765

## Pi Session — 2026-04-30 16:17
- ARGOS: 2.1.3
- Mode: server
- PID: 8504
- URL: http://localhost:18765

## Pi Session — 2026-04-30 16:19
- ARGOS: 2.1.3
- Mode: server
- PID: 5884
- URL: http://localhost:18765

## Pi Session — 2026-04-30 16:24
- ARGOS: 2.1.3
- Mode: server
- PID: 18824
- URL: http://localhost:18765

## Pi Session — 2026-04-30 16:28
- ARGOS: 2.1.3
- Mode: server
- PID: 7960
- URL: http://localhost:18765

## Pi Session — 2026-04-30 20:32
- ARGOS: 2.1.3
- Mode: server
- PID: 10728
- URL: http://localhost:18765

## Pi Session — 2026-04-30 21:49
- ARGOS: 2.1.3
- Mode: server
- PID: 2092
- URL: http://localhost:18765

## Pi Session — 2026-04-30 22:29
- ARGOS: 2.1.3
- Mode: server
- PID: 11948
- URL: http://localhost:18765

## Pi Session — 2026-05-01 01:04
- ARGOS: 2.1.3
- Mode: server
- PID: 3032
- URL: http://localhost:18765

## Pi Session — 2026-05-01 02:00
- ARGOS: 2.1.3
- Mode: server
- URL: http://localhost:18765
- Action: Настроен GPU кластер (3x AMD) + MetaGPT интеграция
  1. GPU Кластер:
     - GPU0 (RX 580 4GB): localhost:8082 — qwen2.5-3b.gguf
     - GPU1 (Vega 11 2GB): localhost:8083 — tinyllama-1.1b-chat-q4_k_m.gguf
     - GPU2 (RX 560 4GB): localhost:8084 — phi4-mini-3.8b-q4_k_m.gguf
     - Все 3 сервера работают через llama-server (Vulkan)
  2. MetaGPT:
     - Установлен: pip install metagpt
     - Конфиг: config/config2.yaml (Ollama integration)
     - Skill: src/skills/metagpt_skill.py
  3. ARGOS конфигурация:
     - .env обновлён: GPU_SERVER_0/1/2
     - AI_PRIORITY: gpu0,gpu1,gpu2,local-gpu,kimi,deepseek,claude,ollama,metagpt
     - Fallback chain: GPU0 → GPU1 → GPU2 → Ollama → MetaGPT → Cloud
  4. Файлы созданы:
     - start_gpu0.bat, start_gpu1.bat, start_gpu2.bat
     - config/config2.yaml
     - src/skills/metagpt_skill.py

## Pi Session — 2026-05-01 07:19
- ARGOS: 2.1.3
- Mode: server
- PID: 3392
- URL: http://localhost:18765

## Pi Session — 2026-05-01 07:45
- ARGOS: 2.1.3
- Mode: server
- PID: 7352
- URL: http://localhost:18765

## Pi Session — 2026-05-01 19:20
- ARGOS: 2.1.3
- Mode: server
- PID: 9672
- URL: http://localhost:18765

## Pi Session — 2026-05-01 19:59
- ARGOS: 2.1.3
- Mode: server
- PID: 12104
- URL: http://localhost:18765

## Pi Session — 2026-05-01 22:05
- ARGOS: 2.1.3
- Mode: server
- PID: 12096
- URL: http://localhost:18765

## Pi Session — 2026-05-01 22:07
- ARGOS: 2.1.3
- Mode: server
- PID: 1672
- URL: http://localhost:18765

## Pi Session — 2026-05-01 22:35
- ARGOS: 2.1.3
- Mode: server
- PID: 15016
- URL: http://localhost:18765

## Pi Session — 2026-05-02 07:24
- ARGOS: 2.1.3
- Mode: server
- URL: http://localhost:18765
- Action: Полная настройка ARGOS+ v2.1.3 — GPU кластер + Консенсус + MetaGPT + Obsidian
  1. GPU Кластер (3x AMD GPU):
     - GPU0 (RX 580 4GB): localhost:8082 — qwen2.5-3b.gguf
     - GPU1 (Vega 11 2GB): localhost:8083 — tinyllama-1.1b-chat-q4_k_m.gguf
     - GPU2 (RX 560 4GB): localhost:8084 — phi4-mini-3.8b-q4_k_m.gguf
     - Все 3 сервера работают через llama-server (Vulkan backend)
     - Скрипт запуска: start_all_gpu.bat
  2. Консенсус моделей (ARGOS_AUTO_COLLAB):
     - Включён: ARGOS_AUTO_COLLAB=on
     - Макс. моделей: 5 (GPU0→GPU1→GPU2→Kimi→DeepSeek)
     - Мин. ответов для консенсуса: 3
     - Порог качества: 0.6
  3. MetaGPT интеграция:
     - Установлен: pip install metagpt (в процессе)
     - Конфиг: config/config2.yaml (Ollama API integration)
     - Skill: src/skills/metagpt_skill.py
  4. Obsidian.md интеграция (MCP):
     - MCP модуль: src/connectivity/obsidian_mcp.py
     - Skill: src/skills/obsidian_skill.py
     - Поддержка: поиск, чтение, запись, daily notes
     - Vault path: F:\Obsidian Vault (или автоопределение)
  5. AI Провайдеры (приоритет):
     - Локальные: gpu0, gpu1, gpu2, local-gpu
     - Облачные: kimi, deepseek, claude, ollama, azure, gemini, openai, groq
     - Специальные: pi, yandexgpt, metagpt
  6. Ollama:
     - Отключена: OLLAMA_ENABLED=false (используем только llama-server)
  7. Файлы созданы/обновлены:
     - start_gpu0.bat, start_gpu1.bat, start_gpu2.bat
     - start_all_gpu.bat (общий запуск)
     - config/config2.yaml (MetaGPT + GPU конфиг)
     - src/skills/metagpt_skill.py
     - src/skills/obsidian_skill.py
     - src/connectivity/obsidian_mcp.py
     - .env (обновлён AI_PRIORITY, консенсус, Obsidian)

## Pi Session — 2026-05-02 11:51
- ARGOS: 2.1.3
- Mode: server
- PID: 8328
- URL: http://localhost:18765

## Pi Session — 2026-05-02 17:24
- ARGOS: 2.1.3
- Mode: server
- PID: 19832
- URL: http://localhost:18765

## Pi Shutdown — 2026-05-03 06:06

## Pi Shutdown — 2026-05-03 06:06

## Pi Shutdown — 2026-05-03 16:04

## Pi Shutdown — 2026-05-04 06:46

## Pi Shutdown — 2026-05-04 07:09
