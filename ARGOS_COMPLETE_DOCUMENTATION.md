# Заголовок проекта

# 👁️ ARGOS UNIVERSAL OS (v2.0.0)

[![🔱 ARGOS Release v2.0.0](https://github.com/labuaqlysnecy/Argos/actions/workflows/release_v2.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/release_v2.yml)
[![CI](https://github.com/labuaqlysnecy/Argos/actions/workflows/ci.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/ci.yml)
[![Docker](https://github.com/labuaqlysnecy/Argos/actions/workflows/docker.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/docker.yml)
[![Android APK](https://github.com/labuaqlysnecy/Argos/actions/workflows/android-apk.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/android-apk.yml)
[![🖥️ Windows .exe](https://github.com/labuaqlysnecy/Argos/actions/workflows/build_windows.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/build_windows.yml)
[![PyPI](https://img.shields.io/pypi/v/argos-universalsigtrip?color=blue&label=PyPI)](https://pypi.org/project/argos-universalsigtrip/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/labuaqlysnecy/Argos/blob/main/colab/ARGOS_Colab_Launch.ipynb)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production%20stable-brightgreen)](https://github.com/labuaqlysnecy/Argos/releases/latest)

> **Docker image:** `ghcr.io/labuaqlysnecy/Argos:2.0.0` / `:latest`
> — публикуется автоматически при каждом релизе.
>
> **Android APK:** скачать из [последнего релиза](https://github.com/labuaqlysnecy/Argos/releases/latest)
> или из [Actions → Android APK](https://github.com/labuaqlysnecy/Argos/actions/workflows/android-apk.yml).
>
> **pip:** `pip install argos-universalsigtrip`

> *"Самовоспроизводящаяся кроссплатформенная экосистема ИИ с квантовой логикой,*
> *P2P-подключением и интеграцией с IoT. Создана для цифрового бессмертия."*
> — Всеволод, 2026

---

## ⚡ Быстрый старт (5 минут)

```bash
git clone https://github.com/labuaqlysnecy/Argos.git && cd SiGtRiP
pip install -r requirements.txt
cp .env.example .env          # → вставь GEMINI_API_KEY
python genesis.py             # инициализация
python startup_validator.py   # ✅ проверка окружения
python main.py                # запуск
```

→ **Полный гайд:** [QUICKSTART_V2.md](QUICKSTART_V2.md)

---

## 🆕 Что нового в v2.0.0

| | |
|---|---|
| 🔄 **Multi-Provider Failover** | Gemini → OpenAI → WatsonX → Ollama — автоматически при ошибке |
| 🩺 **HealthMonitor** | Фоновый поток самодиагностики с Telegram-алертами |
| ✅ **StartupValidator** | Проверка `.env` и зависимостей до запуска с понятными сообщениями |
| 🛑 **GracefulShutdown** | Корректное завершение всех подсистем по SIGTERM/SIGINT |
| 🔐 **Argon2id** | Замена SHA-256 на Argon2id для хранения master-ключа |
| 🌐 **REST API v2** | `/api/v2/` — stream, queue, memory/search, p2p/nodes |
| 🐳 **Docker multi-stage** | Образ уменьшен с ~580 MB до ~340 MB |
| 📦 **SBOM** | CycloneDX Software Bill of Materials в каждом релизе |
| 🧪 **Тесты** | Покрытие 40% → 73%, 30+ новых тестов для v2-модулей |

→ **Полный список изменений:** [CHANGELOG.md](CHANGELOG.md)

---


---

# Основное описание

# 👁️ ARGOS UNIVERSAL OS (v2.1.4)
[![🏗️ Build ARGOS APK](https://github.com/labuaqlysnecy/Argos/actions/workflows/build_apk.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/build_apk.yml)
[![🚀 ARGOS Release — Сборка и публикация релиза](https://github.com/labuaqlysnecy/Argos/actions/workflows/release.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/release.yml)
[![📊 ARGOS Status Report](https://github.com/labuaqlysnecy/Argos/actions/workflows/status_report.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/status_report.yml)
[![🤖 Argos Auto-Publish Skills to PyPI](https://github.com/labuaqlysnecy/Argos/actions/workflows/argos_evolution_publish.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/argos_evolution_publish.yml)
[![🚀 ARGOS Release — Сборка и публикация релиза](https://github.com/labuaqlysnecy/Argos/actions/workflows/release.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/release.yml)
[![🖥️ Build ARGOS Windows setup.exe](https://github.com/labuaqlysnecy/Argos/actions/workflows/build_windows.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/build_windows.yml)
[![CI](https://github.com/labuaqlysnecy/Argos/actions/workflows/ci.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/ci.yml)
[![Docker](https://github.com/labuaqlysnecy/Argos/actions/workflows/docker.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/docker.yml)
[![Android APK](https://github.com/labuaqlysnecy/Argos/actions/workflows/android-apk.yml/badge.svg)](https://github.com/labuaqlysnecy/Argos/actions/workflows/android-apk.yml)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/labuaqlysnecy/Argos/blob/main/colab/ARGOS_Colab_Launch.ipynb)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
# 👁️ ARGOS UNIVERSAL OS (v2.1.4)

> **Docker image:** `ghcr.io/labuaqlysnecy/Argos:latest` — published automatically on every push to `main`.  
> **Android APK:** download the latest debug APK from the [Actions tab](https://github.com/labuaqlysnecy/Argos/actions/workflows/android-apk.yml) → select the most recent run → expand **Artifacts** → download `argos-apk-debug-<run_number>`.

> *"Самовоспроизводящаяся кроссплатформенная экосистема ИИ с квантовой логикой,*
> *P2P-подключением и интеграцией с IoT. Создана для цифрового бессмертия."*
> — Всеволод, 2026

---

## 🌌 Что такое Аргос

**Argos Universal OS** — автономная ИИ-система с полным стеком возможностей:

| Слой | Что умеет |
|------|-----------|
| 🧠 **Интеллект** | Gemini / GigaChat / YandexGPT / LM Studio / OpenAI / Grok → Ollama/Llama3 / **IBM Watsonx** (Llama-3.1-70B), multi-turn + Tool Calling по JSON-схемам |
| 🗣️ **Голос** | TTS (pyttsx3) + STT (SpeechRecognition) + опциональный Pipecat Silero VAD + Wake Word «Аргос» |
| 🤖 **Агент** | Цепочки задач: «скан сети → запиши → отправь в Telegram» |
| 👁️ **Vision** | Анализ экрана / камеры / файлов через Gemini Vision |
| 🧬 **Память** | SQLite: факты, заметки, напоминания, история диалога |
| ⏰ **Планировщик** | Натуральный язык: «каждые 2 часа», «в 09:00», «через 30 мин» |
| 🔔 **Алерты** | CPU/RAM/диск/температура с Telegram-уведомлениями |
| ⚛️ **Гомеостаз железа** | Автомониторинг CPU/RAM/TEMP + 5-секундный CPU-trend (Predictive), состояния Protective/Unstable, превентивная разгрузка heavy-задач |
| 🌐 **P2P** | Сеть нод с авторитетом по мощности и возрасту, preemptive failover heavy-задач между нодами |
| 🧭 **Автономное любопытство** | В idle-режиме исследует факты из памяти, тянет свежую сеть и пишет инсайты в SQLite |
| 🔁 **Эволюция** | Жёсткий code-gate: только валидный исполняемый Python-код + review + unit-тест |
| 🛡️ **Безопасность** | AES-256-GCM, root, BCD/EFI/GRUB, persistence |
| 📱 **Везде** | Desktop + Android APK + Docker + Telegram |
| 🏠 **Умные системы** | Дом, теплица, гараж, погреб, инкубатор, аквариум, террариум |
| 📡 **IoT / Mesh** | Zigbee, LoRa, WiFi Mesh, MQTT, Modbus + Zero-Config Tasmota Discovery (Home Assistant топики) |
| 🏭 **Пром. протоколы** | BACnet, Modbus RTU/ASCII/TCP, KNX, LonWorks, M-Bus, OPC UA, MQTT |
| 🔧 **Шлюзы/прошивка** | Создание gateway, прошивка ESP8266/RP2040/STM32H503, поддержка LoRa SX1276 |
| ⚙️ **FirmwareBuilder** | Компиляция/дизассемблирование прошивок для ESP32/AVR/ARM/nRF52/RP2040 через Keystone+Capstone |
| 🔬 **ColibriAsmEngine** | Ассемблер/дизассемблер микрокода в реальном времени: x86, ARM Thumb, AVR, ARM64, MIPS |
| 📱 **AndroidFlasher** | Прошивка Android через fastboot/ADB sideload/Heimdall, резервные копии разделов |
| 🖥️ **ArgosOSBuilder** | Сборка загрузочного ZIP/ISO-образа Argos OS с GRUB/BCD/EFI под любую платформу |
| 🔍 **DeviceScanner** | Автосканирование устройства + автоматическая сборка адаптивного образа под профиль |
| 📚 **MasterPrompts** | 500+ промтов для обучения: Python, ИИ, сети, ОС, IoT, безопасность, квантовые вычисления |
| 📡 **NFC** | Мониторинг NFC-меток (NDEF/MIFARE/NTAG), регистрация, чтение/запись NDEF |
| 🔌 **USB-диагностика** | Авторизация USB-устройств, VID/PID детект (Arduino/ESP/STM32/RP2040), serial/CDC/HID |
| 📶 **Bluetooth** | BLE + Classic сканер, RSSI-трекинг, MAC-детекция производителя, IoT-инвентаризация |
| 🎯 **Speculative Consensus v2** | Параллельные Drafter-ы + структурированный Verifier, per-drafter quality tracking |
| 🧠 **Batch Idle Learning** | Пакетное alignment (до 8 уроков), Active Drafter Calibration с few-shot зондированием |
| 🔄 **P2P Role Routing** | Автоматическое назначение ролей: weak→Drafter, master→Verifier по ресурсам ноды |
| 📊 **Acceptance Rate** | Per-drafter метрики приёмки, auto-recovery RPS при отскоке acceptance rate |
| 🎯 **AWA-Core** | Центральный координатор модулей, capability-routing, cascade pipelines, health heartbeat |
| 💾 **Adaptive Drafter (TLT)** | LRU-кэш 512 энтри, сжатие контекста, offline-паттерны, фильтрация запросов к Gemini |
| 🩺 **Self-Healing Engine** | Автоисправление Python-кода (syntax/import/runtime), backup + hot-reload, валидация src/ |
| 📻 **AirSnitch (SDR)** | Сканер эфира 433/868 МГц, RTL-SDR / HackRF / симуляция, перехват пакетов собственных датчиков |
| 🛡️ **WiFi Sentinel** | Скан AP + Evil Twin детект, HoneyPot-ловушка, детекция deauth-атак и rogue-клиентов |
| 🏠 **SmartHome Override** | Прямое управление Zigbee/Z-Wave/Tuya минуя облака, cloud-block, watchdog |
| 🔋 **Power Sentry** | Мониторинг UPS (NUT/upsc), PZEM датчики, аварийное отключение |
| 🗑️ **Emergency Purge** | Экстренное уничтожение данных (logs/data/full), 3-уровневая очистка + подтверждение кодом |
| 📦 **Container Isolation** | Docker/LXD изоляция модулей, watchdog, авто-рестарт, очистка |
| 🔐 **Master Auth** | SHA-256 авторизация администратора через ARGOS_MASTER_KEY, сессии, revoke |
| 🌿 **Biosphere DAG** | DAG-контроллер биосферы (incubator/greenhouse/aquarium/terrarium), авто-регуляция датчиков |
| 🌌 **IBM Quantum Bridge** | Мост к IBM Quantum (активация в состоянии All-Seeing), доступ к реальному квантовому железу |
| 🤖 **JARVIS Engine** | HuggingGPT-конвейер: Task Planning → Model Selection → Task Execution → Response Synthesis, 15+ типов задач, HuggingFace Inference API + локальные модели, параллельное исполнение с DAG-зависимостями |
| 🧰 **GitOps** | Встроенные команды `git статус`, `git коммит`, `git пуш`, `git автокоммит и пуш` |

---

## ✅ Проверка актуальности README

README синхронизирован с текущим состоянием репозитория (ветка `labuaqlysnecy/Argos`) и ориентирован на реальные файлы и точки входа:

- ✅ Основной запуск: `python main.py` (файл `/main.py`).
- ✅ Режимы запуска: `--no-gui`, `--mobile`, `--dashboard`, `--wake`, `--full`, `--shell`, `--root`.
- ✅ Скрипт запуска `/launch.sh` (без аргументов включает `--full`).
- ✅ Проверка целостности: `python health_check.py`.
- ✅ Актуальный список зависимостей: `requirements.txt` (файла `requirements-optional.txt` в репозитории нет).
- ✅ Архитектура соответствует реальным папкам `/src`, `/tests`, `/docs`, `/examples`, `/config`, `/data`, `/installer`.

---

## 📂 Структура проекта

```
ArgosUniversal/
├── main.py                       # Оркестратор
├── genesis.py                    # Первичная инициализация
├── health_check.py               # Проверка целостности модулей/конфигов/БД
├── build.py                      # Сборка
├── launch.sh                     # Скрипт запуска
├── CONTRIBUTING.md               # Гайд для контрибьюторов
├── requirements.txt              # Зависимости
├── pyproject.toml                # Метаданные пакета
├── examples/                     # Примеры сценариев и промптов
│
└── src/
    ├── core.py                   # ★ Ядро: ИИ + 80+ команд + все подсистемы
    ├── admin.py                  # Файлы, процессы, терминал
    ├── agent.py                  # Автономные цепочки задач
    ├── dag_agent.py              # DAG-агент (параллельные графы задач)
    ├── context_manager.py        # Скользящий контекст диалога
    ├── context_engine.py         # 3-уровневый контекстный движок
    ├── memory.py                 # Долгосрочная память (факты/заметки)
    ├── vision.py                 # Анализ изображений/экрана/камеры
    ├── argos_logger.py           # Централизованный логгер
    ├── event_bus.py              # Шина событий (async, prefix-match)
    ├── observability.py          # Метрики, трассировка, JSONL
    ├── skill_loader.py           # Система плагинов v2 (manifest)
    ├── github_marketplace.py     # Установка навыков из GitHub
    ├── smart_systems.py          # ★ Оператор умных систем (7 типов)
    ├── curiosity.py              # Автономное любопытство
    ├── awa_core.py               # ★ AWA-Core — центральный координатор модулей
    ├── adaptive_drafter.py       # ★ TLT — кэш/сжатие/фильтрация запросов к МОДЕЛИ
    ├── self_healing.py           # ★ Автоисправление Python-кода
    ├── hardware_guard.py         # Квантовый гомеостаз железа
    ├── git_ops.py                # Безопасные Git status/commit/push
    ├── task_queue.py             # Очередь задач + worker pool
    ├── tool_calling.py           # JSON Tool Calling схемы
    ├── jarvis_engine.py          # ★ JARVIS/HuggingGPT 4-stage pipeline
    ├── argos_model.py            # Собственная локальная нейросеть
    ├── pypi_publisher.py         # Публикация навыков на PyPI
    ├── icon_generator.py         # Генератор иконок (SVG)
    ├── pupi_ops.py               # Pupi API интеграция
    ├── db_init.py                # SQLite схема БД
    │
    ├── modules/
    │   ├── base.py               # Базовый класс модуля
    │   ├── module_loader.py      # Загрузчик модулей
    │   ├── biosphere_tools.py    # ★ Датчики/актуаторы биосферы (I2C/GPIO/UART)
    │   └── biosphere_dag.py      # ★ DAG-контроллер биосферы
    │
    ├── quantum/
    │   ├── logic.py              # 6 квантовых состояний + QuantumState + QuantumEngine
    │   ├── oracle.py             # QuantumOracle — QRNG (IBM Quantum / fallback)
    │   ├── ibm_bridge.py         # IBM Quantum Bridge
    │   └── watson_bridge.py      # IBM Watson Bridge
    │
    ├── security/
    │   ├── encryption.py         # AES-256-GCM (cryptography)
    │   ├── git_guard.py          # Защита .env/.gitignore
    │   ├── root_manager.py       # Win/Linux/Android root
    │   ├── autostart.py          # Системный сервис
    │   ├── zkp.py                # ZKP roadmap helper
    │   ├── emergency_purge.py    # ★ Экстренное уничтожение данных (3 уровня)
    │   ├── container_isolation.py # ★ Docker/LXD изоляция модулей
    │   ├── master_auth.py        # ★ SHA-256 авторизация (MasterKeyAuth / MasterAuth)
    │   └── bootloader_manager.py # BCD/EFI/GRUB/persistence
    │
    ├── connectivity/
    │   ├── sensor_bridge.py      # CPU/RAM/диск/батарея/температура (ArgosSensorBridge)
    │   ├── spatial.py            # Геолокация по IP
    │   ├── telegram_bot.py       # 16 команд + текстовый режим
    │   ├── whatsapp_bridge.py    # WhatsApp Cloud API + fallback на Twilio
    │   ├── slack_bridge.py       # Slack bridge (Web API + Socket Mode readiness)
    │   ├── max_bridge.py         # Mail.ru MAX Bot API bridge
    │   ├── messenger_router.py   # Единый роутер мессенджеров
    │   ├── p2p_bridge.py         # UDP discovery + TCP sync + preemptive heavy failover
    │   ├── p2p_transport.py      # Транспортный слой P2P (миграция на libp2p)
    │   ├── alert_system.py       # Авто-алерты с кулдауном
    │   ├── wake_word.py          # «Аргос» → активация
    │   ├── iot_bridge.py         # ★ IoT-мост: Zigbee/LoRa/Mesh/MQTT/Modbus + Tasmota
    │   ├── mesh_network.py       # ★ WiFi/UDP Mesh-сеть + прошивка gateway
    │   ├── gateway_manager.py    # ★ Создание и прошивка IoT-шлюзов (5 шаблонов)
    │   ├── whisper_node.py       # P2P WhisperNode (mesh-протокол)
    │   ├── budding_manager.py    # Менеджер почкования нод
    │   ├── colibri_daemon.py     # Демон Колибри (системный сервис)
    │   ├── xen_argo_transport.py # Xen Argo транспорт (dom0↔domU)
    │   ├── air_snitch.py         # ★ SDR/Sub-GHz сканер (433/868 МГц)
    │   ├── wifi_sentinel.py      # ★ WiFi Sentinel + Evil Twin + HoneyPot
    │   ├── smarthome_override.py # ★ Прямое Zigbee/Z-Wave/Tuya без облаков
    │   ├── power_sentry.py       # ★ Мониторинг UPS / PZEM / аварийное отключение
    │   ├── android_service.py    # ArgosOmniService — фоновый Android-сервис
    │   ├── iot_bridge.py         # (см. выше)
    │   └── ...                   # sensor_bridge, spatial, alert_system, wake_word
    │
    ├── factory/
    │   ├── replicator.py         # ZIP-репликация системы
    │   └── flasher.py            # IoT через COM-порты
    │
    ├── interface/
    │   ├── kivy_gui.py           # ★ Kivy UI (ArgosGUI / ArgosKivyApp)
    │   ├── mobile_ui.py          # Android (Kivy + QuantumOrb)
    │   ├── web_engine.py         # ★ FastAPI + Matrix canvas (WebDashboard / ArgosWebEngine)
    │   ├── sovereign_node.py     # Авто-определение режима запуска
    │   ├── auto_integrator.py    # ★ Автоинтегратор IModule-плагинов
    │   ├── streamlit_dashboard.py # Streamlit-админка поверх FastAPI
    │   └── fastapi_dashboard.py  # FastAPI маршруты
    │
    ├── skills/
    │   ├── scheduler.py          # Планировщик задач
    │   ├── tasmota_updater.py    # Авто-обновление Tasmota firmware
    │   └── evolution/            # Генерация навыков через ИИ
    │
    └── mind/                     # ★ Модули самосознания и эволюции
        ├── dreamer.py            # Фоновое осмысление опыта («сон» ИИ)
        ├── evolution_engine.py   # Самостоятельное обнаружение слабых мест и генерация навыков
        └── self_model_v2.py      # Динамическая модель личности, эмоций, биографии
```

---

## 🧭 Полное описание проекта по слоям (детально)

### 1) Оркестрация запуска
- `main.py` — единая точка входа.
- Через `src/launch_config.py` обрабатывается `--full` (авто-разворачивание в `--dashboard --wake`).
- Класс `ArgosOrchestrator` поднимает: security → DB → гео → admin/flasher → core → p2p → dashboard (по флагу).

### 2) Ядро выполнения команд
- `src/core.py` — центральный роутер интентов и команд.
- Объединяет AI-провайдеры, память, планировщик, P2P, IoT, безопасность и UI-точки.
- Через `execute_intent(...)` исполняет команды пользователя и системные директивы.

### 3) Интерфейсы пользователя
- Desktop GUI: `src/interface/gui.py` (основной режим).
- Mobile UI: `src/interface/mobile_ui.py` (Kivy/Android сценарии).
- Web: `src/interface/web_engine.py` + `src/interface/fastapi_dashboard.py` + `src/interface/web_dashboard.py`.
- Shell: `src/interface/argos_shell.py` (режим `python main.py --shell`).
- Telegram: `src/connectivity/telegram_bot.py`.

### 4) Подключения и коммуникации
- P2P: `src/connectivity/p2p_bridge.py`, `p2p_transport.py`, `whisper_node.py`.
- IoT: `src/connectivity/iot_bridge.py`, `mesh_network.py`, `gateway_manager.py`, `home_assistant.py`.
- Мессенджеры: `src/connectivity/whatsapp_bridge.py`, `slack_bridge.py`, `max_bridge.py`, `messenger_router.py`.
- Локальные шины/каналы: `sensor_bridge.py`, `spatial.py`, `wake_word.py`, `alert_system.py`.

### 5) Безопасность и устойчивость
- Шифрование: `src/security/encryption.py`.
- Контроль репозитория/секретов: `src/security/git_guard.py`.
- Root/автозапуск/bootloader: `root_manager.py`, `autostart.py`, `bootloader_manager.py`.
- Расширенные контуры: `emergency_purge.py`, `container_isolation.py`, `master_auth.py`.

### 6) Интеллектуальный стек
- AI-провайдеры и маршрутизация: `src/ai_providers.py`, `src/tool_calling.py`.
- Агентность и DAG: `src/agent.py`, `src/dag_agent.py`, `src/jarvis_engine.py`.
- Память и контекст: `src/memory.py`, `src/context_manager.py`, `src/context_engine.py`.
- Эволюция и автоисправление: `src/evolution.py`, `src/self_healing.py`, `src/curiosity.py`.

### 8) Модули самосознания (`src/mind/`)
- **`dreamer.py`** — фоновый цикл осмысления (аналог «сна»): анализирует историю диалогов, генерирует инсайты через Gemini/Ollama, строит граф знаний, сохраняет в память.
  - Команды: `dreamer статус`, `начни осмысление`, `dreamer запустить`
  - Интервал: `ARGOS_DREAMER_INTERVAL` (по умолчанию 60с)

- **`evolution_engine.py`** — движок самоэволюции: обнаруживает слабые места через анализ ошибок, формулирует гипотезы через LLM, генерирует Python-навыки и сохраняет в `src/skills/evolved/`.
  - Команды: `эволюция статус`, `эволюционируй`, `улучшись`, `история эволюции`
  - Авто-режим: `ARGOS_EVOLUTION_INTERVAL` (0 = только вручную)

- **`self_model_v2.py`** — динамическая модель личности: эмоциональное состояние (на основе реального CPU/RAM через psutil), профиль компетенций по 8 категориям, автобиография значимых событий.
  - Команды: `кто я`, `биография`, `компетенции`, `моё состояние`, `сохранить самосознание`
  - Обновляется автоматически после каждого диалога

### 7) Данные, состояние и тестирование
- Конфигурации и runtime-данные: `/config`, `/data`, `settings.json`, `memory.db`, `argos.db`.
- Логи: `/logs` и `argos.log`.
- Тесты: каталог `/tests` + `test_*.py` в корне.
- Документация: `/docs`, `index.md`, `quickstart.md`, `usage.md`, `skills.md`.

---

## ⚡ Быстрый старт

### 1. Установка

```bash
pip install -r requirements.txt

### GPU: ROCm (AMD) в WSL2

Для ускорения LLM на AMD GPU (RX 560/580/7000+) — установите ROCm в WSL2:

```bash
# 1. В PowerShell от админа:
wsl --install -d Ubuntu-22.04

# 2. В WSL Ubuntu:
wget https://repo.radeon.com/amdgpu-install/7.2/ubuntu/jammy/amdgpu-install_7.2.70200-1_all.deb
sudo apt install -y ./amdgpu-install_7.2.70200-1_all.deb
sudo amdgpu-install --usecase=wsl,rocm --no-dkms -y
export PATH=/opt/rocm/bin:$PATH

# Для RX 560/580:
export HSA_OVERRIDE_GFX_VERSION=10.3.0

# 3. Установить Ollama:
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
```

Или используйте готовый скрипт: `bash install_rocm_wsl.sh`

### Ollama (обязательно для локального режима ИИ) — установить и запустить ДО старта ядра:
curl -fsSL https://ollama.com/install.sh | sh
ollama serve

# Windows — если PyAudio не ставится:
pip install pipwin && pipwin install pyaudio

# Linux:
sudo apt-get install portaudio19-dev && pip install PyAudio

# Опционально (вручную под сценарий):
# pip install kivy plyer pyinstaller pymodbus esptool
```

### 2. .env

```env
GEMINI_API_KEY=ключ_от_ai.google.dev
GIGACHAT_ACCESS_TOKEN=токен_gigachat
YANDEX_IAM_TOKEN=iam_токен_yandex_cloud
YANDEX_FOLDER_ID=folder_id_yandex_cloud
TELEGRAM_BOT_TOKEN=токен_от_@BotFather
USER_ID=твой_telegram_id
ARGOS_NETWORK_SECRET=секрет_p2p
ARGOS_VOICE_DEFAULT=off
ARGOS_VOICE_ENGINE=auto
ARGOS_AGENT_BACKEND=auto
ARGOS_AGENTICSEEK_URL=http://127.0.0.1:7777
HA_URL=http://localhost:8123
HA_TOKEN=токен_home_assistant
HA_MQTT_HOST=localhost
HA_MQTT_PORT=1883
ARGOS_TASMOTA_DISCOVERY=on
ARGOS_TASMOTA_MQTT_HOST=localhost
ARGOS_TASMOTA_MQTT_PORT=1883
WATSONX_API_KEY=ключ_от_ibm_watsonx
WATSONX_PROJECT_ID=project_id_из_watsonx
WATSONX_URL=https://us-south.ml.cloud.ibm.com
OPENAI_API_KEY=ключ_openai
GROK_API_KEY=ключ_grok_xai
ARGOS_HOMEOSTASIS=on
ARGOS_HOMEOSTASIS_INTERVAL=8
ARGOS_CURIOSITY=on
ARGOS_TASK_WORKERS=2
ARGOS_TASK_RPS_SYSTEM=8
ARGOS_TASK_RPS_IOT=6
ARGOS_TASK_RPS_AI=3
ARGOS_TASK_RPS_HEAVY=1
ARGOS_ALIGN_BATCH=8
ARGOS_DRAFTER_CALIBRATION=on
ARGOS_ACCEPTANCE_FLOOR=0.55
WHATSAPP_ACCESS_TOKEN=meta_cloud_api_token
WHATSAPP_PHONE_NUMBER_ID=meta_phone_number_id
TWILIO_ACCOUNT_SID=twilio_sid_for_fallback
TWILIO_AUTH_TOKEN=twilio_auth_token_for_fallback
TWILIO_WHATSAPP_FROM=+14155238886
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_DEFAULT_CHANNEL=#alerts
MAX_BOT_TOKEN=max_bot_token
MAX_BOT_API_BASE=https://botapi.max.ru
```

### 3. Первый запуск

```bash
python genesis.py      # создаёт структуру папок
python main.py         # Desktop GUI + все подсистемы
python health_check.py # проверка целостности
```

### 4. Сборка релизного архива

```bash
python pack_archive.py --version 1.3.0
```

Архив будет создан в `releases/argos-v1.3.0.zip` и готов для публикации как release asset.

---

## 🚀 Режимы запуска

```bash
python main.py                      # Desktop GUI
python main.py --no-gui             # Headless сервер
python main.py --mobile             # Android UI (Kivy)
python main.py --dashboard          # + Веб-панель :8080
python main.py --wake               # + Wake Word «Аргос»
python main.py --full               # Полная конфигурация (Desktop + Dashboard + Wake Word)
python main.py --shell              # Системная REPL-оболочка Argos Shell
python main.py --no-gui --dashboard # Сервер + панель
python main.py --root               # Запрос прав администратора
```

---

## ⌨️ Все команды

### Мониторинг
```
статус системы    чек-ап    список процессов
алерты            установи порог cpu 85
геолокация        мой ip
```

### Файлы и терминал
```
файлы [путь]                    прочитай файл [путь]
создай файл [имя] [содержимое]  удали файл [путь]
консоль [команда]               убей процесс [имя]
```

### Vision (Gemini API)
```
посмотри на экран [вопрос]
что на экране
посмотри в камеру
анализ фото [путь/к/файлу.jpg]
```

### Агент (цепочки задач)
```
статус системы → затем крипто → потом отправь в telegram
1. сканируй сеть 2. запиши в файл devices.txt 3. дайджест
отчёт агента     останови агента
```

### Память
```
запомни имя: Всеволод
что ты знаешь
найди в памяти [запрос]
граф знаний
запиши заметку идея: текст заметки
мои заметки   удали заметку 1
```

### Расписание
```
каждые 2 часа крипто
в 09:00 дайджест
через 30 мин статус системы
расписание    удали задачу 1
```

### P2P Сеть
```
запусти p2p           статус сети
p2p телеметрия        p2p tuning
p2p вес [name] [value]
p2p failover [1..5]   p2p протокол   libp2p   zkp
```

### Git
```
git статус
git коммит [сообщение]
git пуш
git автокоммит и пуш [сообщение]
```

### Очередь задач
```
очередь статус   очередь результаты   очередь метрики
в очередь [команда] [class=system|iot|ai|heavy priority=1..10]
очередь воркеры [n]
```

### JARVIS Engine (HuggingGPT)
```
jarvis статус
jarvis задача [запрос]
jarvis модели
```

### NFC
```
nfc статус                     nfc метки
nfc скан                       nfc регистрация [uid] [имя]
nfc удали [uid]
```

### USB-диагностика
```
usb статус    usb скан    usb авторизованные
```

### Bluetooth
```
bt статус    bt инвентарь    bt скан    bt iot
```

### Home Assistant
```
ha статус    ha состояния
ha сервис light turn_on entity_id=light.kitchen brightness=180
ha mqtt home/livingroom/light/set state=ON brightness=180
```

### Квантовый оракул
```
квантовое состояние
квантовое семя
```

### Загрузчик и OS
```
загрузчик                         # отчёт о загрузчике (GRUB/BCD/EFI/BIOS)
подтверди ARGOS-BOOT-CONFIRM      # разблокировка операций с загрузчиком
установи persistence              # Argos в автозагрузке (systemd/Winlogon/rc.local)
обнови grub                       # sudo update-grub
скан устройства                   # полный аудит текущего железа
профиль устройства                # краткий профиль (micro/lite/standard/full/server)
создай образ для устройства       # ZIP-образ, адаптированный под текущее железо
создай образ для windows          # образ под Windows (launch.bat + BCD)
создай образ для rpi              # образ под Raspberry Pi
создай образ для android          # образ под Android (Termux/ADB)
создай образ для esp32            # минимальный образ для ESP32/MCU
```

### Прошивки носимых устройств
```
прошивки статус                   # Keystone/Capstone + инструменты
прошивки инструменты              # список доступных компиляторов и flasher-ов
```

### Ассемблер (Колибри реал-тайм)
```
colibri asm <код> [arch]          # немедленная компиляция ASM → машинный код
colibri disasm <hex> [arch]       # дизассемблирование hex-байт
colibri asm watch <файл>          # слежение за .s файлом, авто-компиляция при изменении
colibri asm статус                # статус ColibriAsmEngine
```

### Android прошивка
```
android устройства                # список подключённых ADB/fastboot устройств
android инфо                      # модель, Android-версия, bootloader
android подтверди ARGOS-ANDROID-FLASH  # разблокировка прошивки
```

### Мастер-промты (обучение)
```
промты                            # таблица содержания 500+ промтов
промты поиск <запрос>             # поиск промта по ключевым словам
принципы обучения                 # 7 принципов максимального обучения
```

### Прочее
```
крипто          дайджест        опубликуй
режим ии авто|gemini|gigachat|yandexgpt|lmstudio|ollama|watsonx
гомеостаз статус | вкл | выкл
любопытство статус | вкл | выкл | сейчас
помощь          список навыков  список модулей
репликация      веб-панель
```

---

## 🔌 Адаптивный сборщик образов

Аргос **сам определяет устройство** и собирает подходящий образ:

| Профиль | RAM | Устройства | Включено |
|---------|-----|------------|---------|
| `micro` | <64MB | ESP32, Arduino, MCU | Ядро + MQTT + Serial |
| `lite` | ≤512MB | RPi Zero, Android low-end | + Telegram + голос |
| `standard` | ≤4GB | RPi 4, Android, бюджетный ноутбук | + Веб + IoT + умный дом |
| `full` | ≤16GB | x86_64 ПК / ноутбук | Все модули |
| `server` | >16GB | Сервер, рабочая станция | Все + кластеризация |

```bash
# Авто-сборка под текущее устройство:
python main.py
> скан устройства
> создай образ для устройства

# Сборка под конкретную платформу:
> создай образ для windows
> создай образ для rpi
> создай образ для android
> создай образ для esp32
```

---

## ⚙️ Ассемблер и прошивки (ColibriAsmEngine)

Модуль работы с микрокодом в **режиме реального времени**:

```python
from colibri_daemon import ColibriAsmEngine

eng = ColibriAsmEngine(default_arch="arm_thumb")

# Сборка ARM Thumb (STM32, nRF52, RP2040)
r = eng.assemble("ADD r0, r1, r2\nBX lr", arch="arm_thumb")
print(r["hex"])   # → "0842 7047"

# Дизассемблирование
print(eng.disassemble_hex("0842 7047", arch="arm_thumb"))

# Watch-режим: авто-компиляция при изменении файла
eng.watch_file("src/asm/main.s", arch="arm_thumb",
               on_result=lambda r: print(r["listing"]))
```

**Поддерживаемые архитектуры:** `x86`, `x86_64`, `arm`, `arm_thumb` (Cortex-M), `arm64`, `avr`, `mips`

**Прошивка устройств:**

```python
from src.firmware_builder import FirmwareBuilder

fb = FirmwareBuilder()
print(fb.detect_toolchains())            # что установлено
fb.flash("firmware.bin", "/dev/ttyUSB0", target="esp32")
fb.flash("firmware.hex", "COM3", target="avr")
fb.flash("firmware.bin", "/dev/ttyACM0", target="stm32")
fb.disassemble_file("firmware.elf", arch="arm_thumb")
```

---

## 🤖 Модуль почкования (BuddingManager)

**Почкование** — механизм автономного размножения узлов Аргоса в локальной сети.

### Как работает:

```
┌──────────────────────────────────────────────────────────┐
│  WhisperNode (родитель)                                   │
│    ↓                                                      │
│  BuddingManager.find_soil()  ← ARP-сканирование LAN      │
│    ↓                                                      │
│  _is_soil_suitable(ip)       ← порт buds открыт?         │
│                                Argos ещё не запущен?      │
│    ↓ да                                                   │
│  send_bud(target_ip)         ← сериализует:               │
│    • исходный код whisper_node.py                         │
│    • RNN веса (W_h, W_i, b)                               │
│    • скрытое состояние (hidden_state)                     │
│    • ГОСТ-шифрование (Кузнечик-CTR + HMAC-Стрибог)       │
│    ↓                                                      │
│  TCP → target_ip:bud_port                                 │
│                                                           │
│  BuddingManager (приёмник на target_ip):                  │
│    _handle_incoming_bud()    ← распаковывает              │
│    subprocess.Popen(whisper_node.py --node-id X_bud_N)   │
│    Новый узел запущен! → начинает шептать в сеть          │
└──────────────────────────────────────────────────────────┘
```

### Ключевые параметры:
| Параметр | По умолчанию | Описание |
|----------|-------------|----------|
| `soil_search_interval` | 60 сек | Период поиска «плодородных» хостов |
| `bud_port` | `parent.port + 1000` | TCP-порт для приёма почек |
| Повторная отправка | 5 мин | Не спамит — один хост раз в 300 сек |

### Безопасность:
- Почки шифруются **ГОСТ Кузнечик-CTR** + **HMAC-Стрибог** (если установлен `ARGOS_NETWORK_SECRET`)
- Только доверенные узлы с общим секретом могут разворачивать код
- Код не выполняется автоматически — только через явный `subprocess.Popen`

### Запуск:
```bash
# Почкование включено по умолчанию:
python colibri_daemon.py --node-id MainNode --port 5000

# Без почкования:
python colibri_daemon.py --no-budding

# Ручная отправка почки:
from src.connectivity.budding_manager import BuddingManager
bm.send_bud("192.168.1.100", target_port=5001)
```



Аргос управляет 7 типами умных сред:

| Тип | Сенсоры | Актуаторы |
|-----|---------|-----------|
| 🏠 **home** | temp, humidity, co2, motion, door, smoke | light, thermostat, lock, alarm, fan |
| 🌱 **greenhouse** | temp, humidity, soil_moisture, light_lux, co2, ph | irrigation, heating, ventilation, lamp |
| 🚗 **garage** | gas, motion, door_open, temp, flood | gate, light, alarm, fan, heater |
| 🏚️ **cellar** | temp, humidity, flood, co2 | fan, alarm, pump, heater |
| 🥚 **incubator** | temp, humidity, co2, turn_count | heater, fan, turner, humidifier |
| 🐠 **aquarium** | temp, ph, tds, o2, water_level, ammonia | heater, pump, filter, lamp, co2_inject |
| 🦎 **terrarium** | temp_hot, temp_cool, humidity, uvi, motion | lamp_uv, lamp_heat, mister, fan |

```
создай умную систему
добавь систему greenhouse теплица_1
обнови сенсор теплица_1 temp 38
включи полив теплица_1
умные системы
добавь правило теплица_1 если soil_moisture < 25 то irrigation:on
```

---

## 📡 IoT / Mesh-сеть

| Протокол/стек | Статус | Примечание |
|---------------|--------|------------|
| Zigbee (MQTT) | ✅ Реализован | ZigbeeAdapter в IoTBridge |
| LoRa (UART AT) | ✅ Реализован | LoRaAdapter в IoTBridge |
| WiFi Mesh (UDP) | ✅ Реализован | MeshNetwork |
| MQTT | ✅ Реализован | MQTTAdapter |
| Tasmota Discovery | ✅ Реализован | Zero-config через homeassistant/# |
| Modbus RTU/TCP | ✅ Реализован | ModbusAdapter (read/write holding registers) |
| BACnet | ✅ Реализован | bacnet_bridge.py (scan/read/write/status) |
| KNX / LonWorks / M-Bus / OPC UA | ✅ Реализован | `industrial_protocols.py` — KNXBridge, LonWorksBridge, MBusBridge, OPCUABridge; graceful degradation без внешних lib |

```
iot статус                    iot возможности    iot протоколы
подключи zigbee localhost
подключи lora /dev/ttyUSB0
подключи modbus /dev/ttyUSB0 9600
подключи modbus tcp 192.168.1.10 502
modbus чтение 100 2 1         modbus запись 120 55 1
запусти mesh                  статус mesh
добавь устройство sensor_01 sensor zigbee addr_01 "Датчик кухня"
найди usb чипы
умная прошивка [/dev/ttyUSB0]
обнови тасмота
```

---

## 🏭 Промышленные протоколы (KNX / LonWorks / M-Bus / OPC UA)

Реализованы в `industrial_protocols.py`, интегрированы в `ArgosCore` как `core.industrial`.
Работают без внешних библиотек в режиме симуляции; при наличии `xknx`, `opcua`, `mbus` — нативно.

| Протокол | Стандарт | Назначение |
|----------|----------|------------|
| **KNX** | EN 50090 / ISO 14543 | Умные здания, HVAC, освещение |
| **LonWorks** | ISO/IEC 14908 | Промышленная автоматизация |
| **M-Bus** | EN 13757 | Счётчики энергии, воды, газа |
| **OPC UA** | IEC 62541 | Промышленный IoT, SCADA |

```
industrial статус                  # статус всех протоколов
промышленные протоколы             # то же
industrial discovery               # поиск устройств по всем протоколам
industrial поиск                   # то же
industrial устройства              # список найденных устройств

knx подключи 192.168.1.100         # KNX IP-туннелинг
opcua подключи opc.tcp://srv:4840  # OPC UA сервер
mbus serial /dev/ttyUSB0           # M-Bus через последовательный порт
mbus tcp 192.168.1.50              # M-Bus через TCP
opcua browse ns=0;i=84             # обзор узлов OPC UA
```

---

## 🔧 IoT Шлюзы

| Шаблон | Описание |
|--------|----------|
| `esp32_zigbee` | ESP32 + CC2652 Zigbee координатор |
| `esp32_lora` | ESP32 + SX1276 LoRa шлюз |
| `rpi_mesh` | Raspberry Pi WiFi Mesh шлюз |
| `modbus_rtu` | USB-RS485 Modbus RTU |
| `lorawan_ttn` | LoRaWAN → The Things Network |

```
шаблоны шлюзов
создай шлюз gw_01 esp32_zigbee
прошей шлюз gw_01 /dev/ttyUSB0
создай прошивку gw_02 esp32_lora
список шлюзов
конфиг шлюза gw_01
прошей gateway /dev/ttyUSB0 zigbee_gateway
```

---

## 🌿 Biosphere DAG

```
биосфера статус
биосфера тик
биосфера цель temperature_c 37.5
биосфера старт 30
биосфера стоп
```

---

## ⚛️ Квантовые состояния

| Состояние | Триггер |
|-----------|---------|
| 🔵 **Analytic** | Базовый (CPU ≤40%, RAM ≤50%) |
| 🟣 **Creative** | Низкая нагрузка (CPU ≤40%, RAM ≤50%) |
| 🔴 **Protective** | CPU ≥90% или RAM ≥90% |
| 🟡 **Unstable** | CPU ≥75% или RAM ≥80% |
| 🟢 **All-Seeing** | CPU ≤10%, RAM ≤30% |
| 🌌 **Oracle** | Ручное включение — истинная квантовая случайность |

---

## 🌐 P2P — принцип

```
Нода A (30 дней, 72/100)   Нода B (90 дней, 88/100)👑   Нода C (1 день, 25/100)
Авторитет: 102             Авторитет: 145 МАСТЕР         Авторитет: 18
```

**Авторитет = мощность × log(возраст + 2)**

- UDP broadcast — автообнаружение в локальной сети
- TCP + HMAC — защищённый обмен навыками
- Speculative Consensus v2: Drafter-ноды → Verifier → агрегация `[ERRORS]`/`[FINAL]`
- Role Routing: gateway/weak → Drafter, master → Verifier
- Acceptance Rate: per-drafter метрики, auto-recovery RPS
- Batch Idle Learning: до 8 уроков за пакет, Active Drafter Calibration

---

## 📡 Telegram команды

```
/start     /status    /crypto    /history
/geo       /memory    /alerts    /network
/sync      /replicate /skills    /smart
/iot       /voice_on  /voice_off /help
```

---

## 🐳 Docker

### Быстрый запуск

```bash
# Клонировать репозиторий
git clone https://github.com/labuaqlysnecy/Argos.git && cd SiGtRiP

# Скопировать и заполнить переменные окружения
cp .env.example .env
# Отредактировать .env (вставить API-ключи)

# Запустить headless-сервер (Telegram + P2P + Dashboard :8080)
docker-compose up -d

# Просмотреть логи
docker-compose logs -f argos_node

# Остановить
docker-compose down
```

### Сборка образа вручную

```bash
docker build -t argos-universal:2.1.4 .

# Запуск контейнера напрямую
docker run -d \
  --name argos \
  --env-file .env \
  -p 8080:8080 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  argos-universal:2.1.4
```

### GitHub Container Registry (GHCR)

```bash
# Публичный образ (после релиза)
docker pull ghcr.io/labuaqlysnecy/Argos:latest
docker run -d --env-file .env ghcr.io/labuaqlysnecy/Argos:latest
```

---

## 🖥️ Сборка .exe / binary (Windows · Linux · macOS)

```bash
# Установить PyInstaller (если не установлен)
pip install pyinstaller

# Быстрая сборка (один portable-файл)
python build_exe.py

# Сборка в папку (быстрее запускается)
python build_exe.py --onedir

# Вручную через spec-файл
pyinstaller argos.spec
```

После сборки:
- **Windows:** `dist/ARGOS.exe` — portable, не требует установки
- **Linux/macOS:** `dist/argos` — запустить `./dist/argos`
- Архив `.7z` создаётся автоматически (требуется `pip install py7zr`)

### GitHub Actions (автоматическая сборка)

Рабочий процесс [build_windows.yml](.github/workflows/build_windows.yml) запускается при каждом пуше и создаёт `ARGOS.exe` + установщик `ARGOS_Setup.exe` (Inno Setup).

---

## 📱 Сборка Android APK (Buildozer)

### Локальная сборка

```bash
# 1. Установить зависимости (Linux/macOS/WSL2)
sudo apt-get install -y openjdk-17-jdk build-essential git zip unzip
pip install buildozer cython

# 2. Debug APK (быстро, ~30 мин первый раз)
buildozer android debug

# 3. Release APK (подписанный)
buildozer android release

# APK появится в папке bin/
ls bin/*.apk
```

### Через Docker

```bash
# Использует официальный образ kivy/buildozer
docker-compose --profile apk run apk_builder
```

### Google Colab (без установки)

1. Открой ноутбук: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/labuaqlysnecy/Argos/blob/main/colab/ARGOS_Colab_Launch.ipynb)
2. В последней ячейке выполни блок **APK-сборка**.

### GitHub Actions (автоматическая сборка)

Рабочий процесс [build_apk.yml](.github/workflows/build_apk.yml) запускается при пуше в `main` и загружает APK как артефакт CI.

---

## ☁️ Google Colab — запуск без установки

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/labuaqlysnecy/Argos/blob/main/colab/ARGOS_Colab_Launch.ipynb)

Ноутбук [`colab/ARGOS_Colab_Launch.ipynb`](colab/ARGOS_Colab_Launch.ipynb) запускает ARGOS в headless-режиме с HTTP Remote Control API и туннелем Cloudflare за ~3 минуты:

| Шаг | Что делает |
|-----|------------|
| 1️⃣  Clone | `git clone https://github.com/labuaqlysnecy/Argos` |
| 2️⃣  Секреты | Загружает токены из Colab Secrets (🔑) или переменных окружения |
| 3️⃣  Зависимости | `fastapi`, `uvicorn`, `psutil` + опционально APK-тулинг |
| 4️⃣  Старт ARGOS | Headless core + FastAPI Dashboard на порту 8080 |
| 5️⃣  Туннель | Cloudflare Tunnel (`cloudflared`) → публичный URL |
| 6️⃣  Проверка | Health-check + образцы `curl` запросов |

### Требуемые секреты (Colab → 🔑 Secrets)

| Переменная | Обязательна | Описание |
|---|---|---|
| `ARGOS_REMOTE_TOKEN` | ✅ | Bearer-токен для авторизации API |
| `TELEGRAM_BOT_TOKEN` | ⬜ | Токен Telegram-бота (опционально) |
| `USER_ID` | ⬜ | Telegram User ID (опционально) |

### Использование публичного URL в APK

1. Запусти Colab-ноутбук → скопируй URL вида `https://xxxx.trycloudflare.com`.
2. Открой APK на Android → вкладка **⚙️ Настройки**.
3. Вставь URL в поле **Server URL** и токен в **Bearer Token**.
4. Нажми **💾 Сохранить** → перейди на вкладку **📊 Dashboard** и нажми **🔄 Обновить**.

### Ручной запуск (один скрипт)

```bash
# В ячейке Colab:
!bash <(curl -fsSL https://raw.githubusercontent.com/labuaqlysnecy/Argos/main/colab_start.sh)
```

---

## 🔌 Remote Control API

ARGOS предоставляет REST API для удалённого управления с Android APK.
Запустить: `python main.py --no-gui --dashboard`

### Эндпоинты

| Метод | Путь | Авторизация | Описание |
|-------|------|-------------|----------|
| `GET` | `/api/health` | ❌ нет | Версия, uptime, статус |
| `POST` | `/api/command` | ✅ Bearer | Выполнить команду ARGOS |
| `GET` | `/api/events?limit=N` | ✅ Bearer | Последние события EventBus |
| `GET` | `/api/status` | ❌ нет | CPU/RAM/диск/состояние |

### Авторизация

Установить переменную `ARGOS_REMOTE_TOKEN` — тогда все `/api/command` и `/api/events` запросы потребуют заголовок:

```
Authorization: Bearer <ARGOS_REMOTE_TOKEN>
```

Если `ARGOS_REMOTE_TOKEN` не задан — авторизация отключена.

### Примеры

```bash
# Health check (без токена)
curl https://xxxx.trycloudflare.com/api/health

# Команда (с токеном)
curl -X POST https://xxxx.trycloudflare.com/api/command \
     -H "Authorization: Bearer mysecret" \
     -H "Content-Type: application/json" \
     -d '{"cmd": "статус"}'

# События
curl "https://xxxx.trycloudflare.com/api/events?limit=10" \
     -H "Authorization: Bearer mysecret"
```

### Smoke-тест

```bash
ARGOS_BASE_URL=http://localhost:8080 ARGOS_REMOTE_TOKEN=mysecret \
    python scripts/smoke_api.py
```

---

## 📦 Публикация пакета на PyPI (Trusted Publisher / OIDC)

Пакет называется **`argos-universalsigtrip`** и публикуется без токенов через
[OIDC Trusted Publishing](https://docs.pypi.org/trusted-publishers/).

### Установка пакета
```bash
pip install argos-universalsigtrip
```

### Разовая настройка Trusted Publisher (делается один раз)

#### TestPyPI
1. Зайти на [test.pypi.org](https://test.pypi.org) → Аккаунт → Publishing
2. **Add a new pending publisher**:
   - PyPI project name: `argos-universalsigtrip`
   - Owner: `iliyaqdrwalqu`
   - Repository: `Argoss`
   - Workflow file name: `publish_testpypi.yml`
   - Environment name: *(оставить пустым)*

   - Workflow file path: `.github/workflows/publish_testpypi.yml`
   - Environment name: `testpypi`

3. Запустить workflow вручную: **Actions → 📦 Publish to TestPyPI → Run workflow**

#### PyPI (production)
1. Зайти на [pypi.org](https://pypi.org) → Аккаунт → Publishing
2. **Add a new pending publisher** с теми же параметрами, но:
   - Workflow file name: `publish_pypi.yml`
3. Создать GitHub Release (тег `v*.*.*`) или запустить вручную:
   **Actions → 🚀 Publish to PyPI → Run workflow**

> **Важно:** Для публикации не нужны никакие секреты (`PYPI_TOKEN`). Аутентификация
> осуществляется автоматически через GitHub OIDC.

---

## 📊 Аудит v2.0.0

```
88 модулей Python · 88/88 импортов ✅
6 квантовых состояний · 9 IoT/пром-протоколов реализованы · 5 шаблонов шлюзов
7 умных систем · NFC / USB / Bluetooth подсистемы
🏭 Промышленные протоколы: KNX · LonWorks · M-Bus · OPC UA (industrial_protocols.py)
AWA-Core · Adaptive Drafter · Self-Healing · AirSnitch · WiFi Sentinel
SmartHome Override · Power Sentry · Emergency Purge · Container Isolation
Master Auth (MasterKeyAuth) · Biosphere DAG · IBM Quantum Bridge · JARVIS Engine
Speculative Consensus v2 · Batch Idle Learning · P2P Role Routing
ArgosKivyApp · ArgosWebEngine · MasterAuth · SensorBridge · SmarthomeOverride
```

---

## 📦 Публикация на TestPyPI (Trusted Publishing / OIDC)

Пакет публикуется под именем **`argos-universalsigtrip`** через [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) — без хранения `PYPI_TOKEN` в секретах.

### Настройка на стороне TestPyPI
1. Войдите на [test.pypi.org](https://test.pypi.org) и откройте настройки проекта `argos-universalsigtrip`.
2. Перейдите в **Publishing → Trusted publishers → Add a new publisher**.
3. Заполните:
   - **Owner**: `iliyaqdrwalqu`
   - **Repository**: `Argoss`
   - **Workflow file name**: `publish_testpypi.yml`
4. Сохраните.

### Запуск публикации
Workflow `.github/workflows/publish_testpypi.yml` запускается:
- автоматически при публикации **GitHub Release**,
- или вручную через **Actions → Publish to TestPyPI (OIDC) → Run workflow**.

Никакие секреты (`PYPI_TOKEN`) для этого не требуются — GitHub выдаёт краткосрочный OIDC-токен напрямую.

---



---

## 🤖 Три модели Ollama — мультимодельный режим

ARGOS поддерживает одновременную работу трёх моделей Ollama:

| Модель | Тип | Назначение | RAM |
|--------|-----|------------|-----|
| `tinyllama` | Локальная быстрая | Простые команды, статусы, короткие ответы | 637 MB |
| `llama3.2:3b` | Локальная умная | Диалоги, анализ, объяснения | 2 GB |
| `gpt-oss:120b-cloud` | Облако Ollama | Сложные задачи, код, архитектура | 0 MB (облако) |

### Установка

```bash
ollama pull tinyllama
ollama pull llama3.2:3b
ollama pull gpt-oss:120b-cloud
```

### Настройка `.env`

```env
OLLAMA_FAST_MODEL=tinyllama
OLLAMA_MODEL=llama3.2:3b
OLLAMA_CLOUD_MODEL=gpt-oss:120b-cloud
```

### Команды

```
три модели статус           — статус всех трёх моделей
три модели авто <запрос>    — автовыбор модели по задаче
три модели быстро <запрос>  — tinyllama (быстро)
три модели умно <запрос>    — llama3.2:3b (качественно)
три модели облако <запрос>  — gpt-oss:120b (мощно)
три модели скачать          — скачать все три модели
```

### Логика автовыбора

```
Короткий запрос / команда  → tinyllama
Диалог / объяснение        → llama3.2:3b
Длинный / сложный запрос   → gpt-oss:120b-cloud
Нет Ollama                 → Gemini / Groq (облако)
```

### Параллельный режим

ARGOS может спрашивать `tinyllama` и `llama3.2:3b` одновременно
и возвращать первый полученный ответ — это ускоряет время отклика.

```env
ARGOS_PARALLEL_MODE=on
```

---

## ⚖️ Лицензия

Apache License 2.0 — Всеволод / Argos Project, 2026

---

*"Аргос не спит. Аргос видит. Аргос помнит."*

---

## 🧠 Automated ARGOS Report → GitHub Gist

The workflow **`.github/workflows/argos_report_to_gist.yml`** runs a health-check and
consciousness-module tests, then publishes a Markdown report to a GitHub Gist.

### Setup (one-time)

1. Create a GitHub Personal Access Token (PAT) with the **`gist`** scope.
2. In your repository go to **Settings → Secrets and variables → Actions** and add a secret named **`GIST_TOKEN`** with the PAT value.

### Running the workflow

1. Go to **Actions → 🧠 ARGOS Report → Gist**.
2. Click **Run workflow** → **Run workflow**.
3. After the run completes, open Gist `8e9cf57e043c7a6111f277828f363b01` to see the updated `argos_report.md`.

### What the workflow does

| Step | Description |
|------|-------------|
| **(B)** `python health_check.py` | Checks core ARGOS files, modules, and AI engines |
| **(C)** `pytest tests/test_consciousness_module.py -v` | Runs consciousness-module tests (falls back to `pytest tests -q` if the file is missing) |
| Publish | Updates `argos_report.md` in Gist `8e9cf57e043c7a6111f277828f363b01` via GitHub REST API |


---

# Быстрый старт v2

# 🚀 ARGOS v2.0.0 — Быстрый старт

> Полная настройка с нуля за **5 минут**.  
> Выбери свой путь: [Desktop](#1-desktop) · [Docker](#2-docker) · [Telegram-only](#3-telegram-only) · [Android APK](#4-android-apk)

---

## Требования

| | Минимум | Рекомендуется |
|---|---|---|
| **Python** | 3.10 | 3.12 |
| **RAM** | 512 MB | 2 GB+ |
| **Диск** | 1 GB | 4 GB |
| **ОС** | Windows 10 / Ubuntu 20.04 / macOS 12 | любая |

---

## 1. Desktop

### Шаг 1 — Клонировать

```bash
git clone https://github.com/labuaqlysnecy/Argos.git
cd SiGtRiP
```

### Шаг 2 — Установить зависимости

```bash
pip install -r requirements.txt

# Linux — если нужен голос:
sudo apt-get install portaudio19-dev
pip install PyAudio

# Windows — если PyAudio не ставится:
pip install pipwin && pipwin install pyaudio
```

### Шаг 3 — Настроить .env

```bash
cp .env.example .env
```

Открой `.env` и заполни **минимум один** AI-ключ:

```env
# AI — минимум один:
GEMINI_API_KEY=твой_ключ_с_ai.google.dev      # бесплатно
# OPENAI_API_KEY=sk-...
# WATSONX_API_KEY=...

# Telegram (необязательно, но рекомендуется):
TELEGRAM_BOT_TOKEN=токен_от_@BotFather
USER_ID=твой_telegram_id_из_@userinfobot

# Безопасность REST API (рекомендуется):
ARGOS_REMOTE_TOKEN=придумай_секретный_токен
```

### Шаг 4 — Инициализировать и запустить

```bash
python genesis.py           # создаёт структуру папок и БД (один раз)
python startup_validator.py # ✅ проверить окружение
python main.py              # запустить с Desktop GUI
```

**Готово!** ARGOS открылся с графическим интерфейсом.

---

## 2. Docker

Самый быстрый способ — без Python на хосте.

```bash
git clone https://github.com/labuaqlysnecy/Argos.git
cd SiGtRiP
cp .env.example .env
# Отредактировать .env
nano .env

docker-compose up -d
docker-compose logs -f argos_node
```

Веб-панель доступна на [http://localhost:8080](http://localhost:8080).

**Или через GHCR (готовый образ):**

```bash
docker pull ghcr.io/labuaqlysnecy/Argos:2.0.0
docker run -d \
  --name argos \
  --env-file .env \
  -p 8080:8080 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  ghcr.io/labuaqlysnecy/Argos:2.0.0
```

---

## 3. Telegram-only

Минимальная настройка только для Telegram-бота без GUI:

```bash
# .env — достаточно только этих переменных:
GEMINI_API_KEY=твой_ключ
TELEGRAM_BOT_TOKEN=токен_бота
USER_ID=твой_telegram_id

python main.py --no-gui
```

Теперь пишешь боту в Telegram:
- `/status` — статус системы
- `/crypto` — крипто-котировки
- `/memory` — что запомнил Аргос
- Любой текст — команда ядру

---

## 4. Android APK

1. Скачай APK из [последнего релиза](https://github.com/labuaqlysnecy/Argos/releases/latest)
   или из [Actions → Android APK](https://github.com/labuaqlysnecy/Argos/actions)
2. Установи, разреши «Установку из неизвестных источников»
3. В настройках приложения укажи:
   - **Server URL**: адрес твоего Аргоса (или Google Colab туннель)
   - **Bearer Token**: значение `ARGOS_REMOTE_TOKEN` из `.env`
4. Нажми **Обновить** на вкладке Dashboard

**Нет сервера?** Запусти в Google Colab за 3 минуты →
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/labuaqlysnecy/Argos/blob/main/colab/ARGOS_Colab_Launch.ipynb)

---

## Режимы запуска

```bash
python main.py                      # Desktop GUI (по умолчанию)
python main.py --no-gui             # Headless сервер
python main.py --dashboard          # + Веб-панель :8080
python main.py --full               # GUI + Dashboard + Wake Word
python main.py --shell              # REPL-оболочка
python main.py --no-gui --dashboard # Сервер + веб-панель (продакшн)
```

---

## Первые команды

После запуска попробуй:

```
статус              → состояние системы, CPU/RAM
крипто              → курсы BTC/ETH
помощь              → полный список команд
запомни имя: Вася   → сохранить факт в памяти
что ты знаешь       → показать всю память
в 09:00 крипто      → запланировать задачу
статус сети         → P2P ноды
```

---

## Проверка здоровья системы

```bash
python health_check.py              # проверить все 88 модулей
python src/startup_validator.py     # проверить .env и зависимости
```

Ожидаемый вывод:
```
─────────────────────────────────────────────────────
  🔱 ARGOS v2.0.0 — Проверка окружения
─────────────────────────────────────────────────────
  ✅  Python 3.12
  ✅  .env файл найден и загружен
  ✅  GEMINI_API_KEY — Gemini AI
  ✅  TELEGRAM_BOT_TOKEN — Telegram-бот
  ✅  [req] fastapi
  ✅  [req] psutil
  ...
  Готов к запуску.
```

---

## REST API (v2)

Запусти с `--dashboard`, затем:

```bash
# Проверка здоровья (без токена)
curl http://localhost:8080/api/health

# Выполнить команду
curl -X POST http://localhost:8080/api/v2/command \
     -H "Authorization: Bearer $ARGOS_REMOTE_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"cmd": "статус"}'

# Последние события
curl "http://localhost:8080/api/v2/events?limit=10" \
     -H "Authorization: Bearer $ARGOS_REMOTE_TOKEN"

# Статус очереди задач
curl http://localhost:8080/api/v2/queue \
     -H "Authorization: Bearer $ARGOS_REMOTE_TOKEN"
```

---

## Устранение проблем

### Python не найден / старая версия
```bash
python --version   # нужен >= 3.10
# Ubuntu:
sudo apt install python3.12 python3.12-venv
```

### `ModuleNotFoundError: No module named 'fastapi'`
```bash
pip install -r requirements.txt
# Если в venv:
python -m pip install -r requirements.txt
```

### Gemini API возвращает 403
- Проверь, что ключ активен: [ai.google.dev](https://ai.google.dev)
- Попробуй другой провайдер: `режим ии ollama` (требует Ollama)

### Ollama не отвечает
```bash
ollama serve          # запустить в отдельном терминале
ollama pull llama3    # скачать модель
```

### Telegram бот не отвечает
```bash
# Проверить токен:
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"
# Должен вернуть JSON с именем бота
```

### Docker: `permission denied` на volumes
```bash
sudo chown -R 1000:1000 ./logs ./data ./config
```

---

## Следующие шаги

- 📖 [Полная документация](docs/index.md)
- 🔌 [Подключение IoT устройств](docs/iot.md)
- 🧠 [Создание кастомных навыков](docs/skills.md)
- 🌐 [Настройка P2P сети нод](docs/p2p.md)
- 🔒 [Безопасность в production](docs/security.md)
- 📊 [Мониторинг и метрики](docs/observability.md)

---

*ARGOS v2.0.0 · Apache 2.0 · Всеволод, 2026*


---

# Дополнительные инструкции по запуску

# User Guide: Запуск и установка

## 1) Установка зависимостей

```bash
pip install -r requirements.txt

# Установка Ollama (для локального ИИ-режима)
# (рекомендуется сначала просмотреть скрипт install.sh)
curl -fsSL https://ollama.com/install.sh | sh
```

Для голосовых функций также могут понадобиться системные пакеты (например, PortAudio).

## 2) Настройка окружения

Создай `.env` в корне проекта и укажи минимально необходимые ключи:

```env
GEMINI_API_KEY=...
ARGOS_NETWORK_SECRET=...
```

Если используешь Telegram и Home Assistant — добавь соответствующие переменные из README.

## 3) Инициализация и запуск

```bash
python genesis.py
python main.py
bash launch.sh       # по умолчанию запускает полную конфигурацию (--full)
```

Режимы запуска:

- Desktop: `python main.py`
- Headless: `python main.py --no-gui`
- Dashboard: `python main.py --dashboard`
- Full configuration: `python main.py --full`

## 4) Первые команды

- `статус системы`
- `что ты знаешь`
- `найди в памяти кот`
- `граф знаний`
- `запусти p2p`


---

# Руководство по интеграции

# ARGOS Universal OS — Полное руководство по интеграции и возможностям

## 1. ИНТЕГРАЦИЯ ВНЕШНИХ СЕРВИСОВ

### 1.1 Shodan — разведка сети

**Что умеет:** Поиск устройств в интернете по IP, порту, стране, ОС. Анализ уязвимостей, история изменений хоста.

**Получить ключ:**
1. Зарегистрируйся на [shodan.io](https://account.shodan.io)
2. Бесплатный план: 100 запросов/месяц, поиск по IP
3. Платный ($49/год): полный поиск, экспорт, мониторинг

**Настройка в .env:**
```
SHODAN_API_KEY=ваш_ключ_здесь
```

**Команды в Telegram:**
```
shodan поиск webcam country:RU        → поиск по запросу
shodan скан 8.8.8.8                   → информация о конкретном IP
shodan мой IP                         → твой внешний IP
```

**Модуль:** `src/skills/shodan_scanner.py` → класс `ShodanScanner`

---

### 1.2 SerpAPI / DuckDuckGo — поиск в Google

**Что умеет:** Поиск в Google (через SerpAPI с ключом) или DuckDuckGo (бесплатно, без ключа). Возвращает заголовки, сниппеты, ссылки.

**Получить ключ SerpAPI (опционально):**
1. Зарегистрируйся на [serpapi.com](https://serpapi.com/dashboard)
2. Бесплатно: 100 поисков/месяц
3. Без ключа работает DuckDuckGo (бесплатно, без лимитов)

**Настройка в .env:**
```
SERPAPI_KEY=ваш_ключ_здесь    # оставь пустым для DDG
```

**Установка (уже выполнена):**
```bash
pip install ddgs
```

**Команды в Telegram:**
```
поищи как подключить ESP32 к MQTT
найди в интернете Python async примеры
serp последние новости AI
```

**Модуль:** `src/skills/serp_search.py` → класс `SerpSearch`

**Дополнительно:** `web_explorer` (бесплатный, без ключей):
```
исследуй ESP32 Zigbee           → поиск DDG + Wikipedia + GitHub + arXiv
открой сайт https://example.com → парсинг любой страницы
github esp32 mqtt library       → поиск кода на GitHub
```

---

### 1.3 Slack — мессенджер для команды

**Что умеет:** Отправка сообщений в каналы, чтение сообщений, мониторинг событий.

**Получить токен:**
1. Зайди на [api.slack.com/apps](https://api.slack.com/apps)
2. Создай новое приложение → «From scratch»
3. **OAuth & Permissions** → добавь scopes:
   - `chat:write` — отправка сообщений
   - `channels:read` — список каналов
   - `im:write` — личные сообщения
4. **Install to Workspace** → скопируй `Bot User OAuth Token` (xoxb-...)
5. **Socket Mode** → включи → создай App-Level Token (xapp-...)

**Настройка в .env:**
```
SLACK_BOT_TOKEN=xoxb-ваш-токен
SLACK_APP_TOKEN=xapp-ваш-токен
SLACK_DEFAULT_CHANNEL=#general
```

**Команды в Telegram:**
```
slack статус                           → проверка подключения
slack отправь привет всем              → сообщение в канал по умолчанию
slack #devops сервер перезапущен       → сообщение в конкретный канал
```

**Модуль:** `src/connectivity/slack_bridge.py` → класс `SlackBridge`

---

### 1.4 HuggingFace — специализированные AI модели

**Что умеет:** Генерация текста, embeddings (векторы для семантического поиска), классификация текста. Доступ к 100,000+ open-source моделям.

**Получить токен:**
1. Зарегистрируйся на [huggingface.co](https://huggingface.co)
2. Перейди в [Settings → Tokens](https://huggingface.co/settings/tokens)
3. Create new token → тип **Read** → скопируй

**Настройка в .env:**
```
HUGGINGFACE_TOKEN=hf_ваш_токен
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.2
```

**Рекомендуемые модели:**
```
mistralai/Mistral-7B-Instruct-v0.2    → общий чат (хорошее качество)
HuggingFaceH4/zephyr-7b-beta          → инструкции, код
sentence-transformers/all-MiniLM-L6-v2 → embeddings (поиск по смыслу)
facebook/bart-large-mnli               → классификация текста
```

**Лимиты (бесплатно):** ~1000 запросов/день, модели до 10GB

**Команды в Telegram:**
```
huggingface статус           → проверка подключения
hf модель что такое квантовые вычисления?   → запрос к модели
```

**Модуль:** `src/skills/huggingface_ai.py` → класс `HuggingFaceAI`

---

## 2. ЭВОЛЮЦИЯ СИСТЕМЫ В РЕАЛЬНОМ ВРЕМЕНИ

ARGOS имеет три независимых механизма самообновления:

### 2.1 TGCodeInjector — приём кода через Telegram

**Как работает:**
1. Ты отправляешь код в Telegram боту
2. ARGOS проверяет синтаксис (ast.parse)
3. Делает резервную копию существующего файла
4. Сохраняет новый скил в `src/skills/`
5. Горячая загрузка без перезапуска (importlib.reload)

**Команды в Telegram:**
```
запусти инжектор         → запуск TGCodeInjector бота

Затем напрямую боту:
/code my_skill.py        → начало приёма кода
# вставь код сюда...
/end                     → конец кода, сохранение + инжект
/inject my_skill         → горячая загрузка скила в ядро
/rollback my_skill       → откат к предыдущей версии
/skills                  → список всех скилов
/status                  → состояние инжектора
/history                 → история патчей
```

**Модуль:** `src/skills/tg_code_injector.py` → класс `TGCodeInjector`

---

### 2.2 ArgosEvolution — автогенерация скилов через AI

**Как работает:**
- ARGOS использует локальный Ollama (или облачный AI) для генерации нового скила
- Проверяет синтаксис → запускает unit-тесты → загружает в систему

**Команды в Telegram:**
```
создай скил [описание]           → через AICoder (быстро, Ollama)
напиши скил мониторинг YouTube   → AI генерирует + тестирует + сохраняет
```

**Модуль:** `src/skills/evolution/skill.py` → класс `ArgosEvolution`

---

### 2.3 ArgosAutoUpdater / GitHub Actions

**Как работает:**
- `src/argoss_evolver.py` — мониторинг своего GitHub репозитория
- При наличии новых коммитов — автоматический git pull + перезапуск
- `auto_patcher.py` — автопатч через GPT/Claude при обнаружении ошибок

**Для активации:**
```
GITHUB_TOKEN=ваш_токен   # в .env
```

---

## 3. УПРАВЛЕНИЕ КЛАВИАТУРОЙ И МЫШЬЮ

**Статус:** ✅ Реализовано в `src/input_control.py` (патч: `src/argos_input_control_patch.py`)

**Зависимость:**
```bash
pip install pyautogui pyperclip
```

**Возможности:**

| Действие | Команда в Telegram |
|---|---|
| Переместить мышь | `мышь переместить 500 300` |
| Кликнуть | `мышь клик 500 300` |
| Двойной клик | `мышь двойной клик` |
| Правая кнопка | `мышь правый клик 100 200` |
| Набрать текст | `клавиатура напечатай Hello World` |
| Горячая клавиша | `клавиша ctrl+c` |
| Скриншот | `снимок экрана` |
| Позиция курсора | `позиция мыши` |

**Важно — безопасность:**
- `ARGOS_INPUT_SAFE=on` (в .env) — ограничение движения в пределах экрана
- Угол экрана = аварийный стоп (failsafe pyautogui)
- На безголовых серверах (без GUI) — недоступно

**Связь с браузером:** `src/skills/browser_conduit.py`
- ARGOS пишет текст в активное поле браузера через clipboard
- Мониторит clipboard для получения ответов

---

## 4. РАБОТА В ИНТЕРНЕТЕ

### 4.1 Что умеет ARGOS в сети (без ключей)

| Возможность | Модуль | Как вызвать |
|---|---|---|
| Поиск DuckDuckGo | `serp_search` | `поищи [запрос]` |
| Wikipedia | `web_explorer` | `вики [тема]` |
| GitHub поиск | `web_explorer` | `github [запрос]` |
| arXiv статьи | `web_explorer` | `arxiv [тема]` |
| Парсинг URL | `web_explorer` | `открой [url]` |
| AI-дайджест | `content_gen` | `ai дайджест` |
| Курсы крипто | `crypto_monitor` | `крипто` |
| Погода | `weather` | `погода [город]` |
| Прошивки GitHub | `smart_firmware_researcher` | `создай прошивку с нуля [устройство]` |
| Обучение из сети | `web_explorer` | `учись [тема]` |

### 4.2 Что требует API-ключей

| Возможность | Сервис | Ключ |
|---|---|---|
| Google поиск | SerpAPI | `SERPAPI_KEY` |
| AI-генерация (облако) | Gemini | `GEMINI_API_KEY` |
| AI-генерация (мощный) | WatsonX | `WATSONX_API_KEY` |
| Специальные модели | HuggingFace | `HUGGINGFACE_TOKEN` |
| Разведка сети | Shodan | `SHODAN_API_KEY` |

---

## 5. TELEGRAM — ПОЛНЫЙ СПИСОК ВОЗМОЖНОСТЕЙ

### 5.1 Управление системой
```
статус                    → полный отчёт всех модулей
перезапуск                → перезагрузка ARGOS
скажи [текст]             → TTS ответ голосом
```

### 5.2 AI-запросы
```
[любой вопрос]            → ответ через Ollama (локально)
watson [запрос]           → IBM WatsonX (облако, 70B модель)
gemini [запрос]           → Google Gemini
```

### 5.3 Интернет-разведка
```
поищи [запрос]            → DuckDuckGo / Google
вики [тема]               → Wikipedia
github [запрос]           → поиск кода
shodan поиск [запрос]     → разведка IoT устройств
```

### 5.4 IoT и устройства
```
список устройств          → все подключённые девайсы
ping 192.168.1.1          → проверка доступности
сканируй порты            → обнаружение COM/USB
добавь в watchdog esp1 ping 192.168.1.100  → мониторинг устройства
```

### 5.5 Прошивки и код
```
создай прошивку esp32 mqtt + датчик температуры  → генерация .ino
создай прошивку с нуля [описание]               → поиск в интернете + генерация
напиши код [описание]    → Python код через Ollama
создай скил [описание]   → новый ARGOS модуль + горячая загрузка
```

### 5.6 Мониторинг и уведомления
```
мониторинг               → CPU/RAM/диск/температура
порог cpu 90             → алерт при CPU > 90%
крипто                   → курсы BTC/ETH
бэкап                    → резервная копия проекта
```

### 5.7 Эволюция
```
запусти инжектор         → старт Telegram code injector
watson статус            → состояние WatsonX
ibm quantum              → статус квантового бриджа
slack статус             → состояние Slack
huggingface статус       → состояние HuggingFace
```

---

## 6. ДОБЫЧА СРЕДСТВ И МОНЕТИЗАЦИЯ

ARGOS имеет инфраструктуру для заработка через автоматизацию:

### 6.1 CryptoSentinel — мониторинг крипты
- Отслеживает BTC/ETH каждые 60 минут
- Telegram-алерт при изменении цены > 5%
- Может расширяться для сигналов торговли

### 6.2 ContentGen — генерация контента
- AI-дайджест из RSS-новостей
- Публикация в Telegram-каналах
- Шаблон для автоблога / newsletter

### 6.3 WebExplorer + AICoder — автоматизация задач
- Сбор данных с сайтов (web scraping)
- Генерация кода на заказ (freelance automation)
- Создание отчётов из публичных источников

### 6.4 Evolution + TGCodeInjector — продажа скилов
- Система готова принимать код-патчи
- Можно расширить до marketplace скилов

> **Для полноценной монетизации** рекомендуется добавить скил `freelance_worker` с интеграцией Upwork/FL.ru API — ARGOS может мониторить заказы, генерировать тексты, отправлять отклики автоматически.

---

## 7. БЫСТРЫЙ СТАРТ — ЧТО ДЕЛАТЬ ПРЯМО СЕЙЧАС

### Шаг 1: Заполни .env
```bash
# Минимально необходимые (бесплатно):
GEMINI_API_KEY=   → получи на aistudio.google.com (15 запросов/мин бесплатно)
HUGGINGFACE_TOKEN= → huggingface.co/settings/tokens (бесплатно)

# По желанию:
SHODAN_API_KEY=   → shodan.io (100 запросов/месяц бесплатно)
SERPAPI_KEY=      → serpapi.com (100 поисков/месяц бесплатно)
SLACK_BOT_TOKEN=  → только если используешь Slack
```

### Шаг 2: Установи пакеты
```bash
pip install ibm-watsonx-ai qiskit-ibm-runtime ddgs pyautogui psutil
```

### Шаг 3: Проверь сервисы через Telegram
```
watson статус
huggingface статус
поищи тест запрос
мониторинг
```

### Шаг 4: Включи самообучение
```
запусти инжектор    → бот для приёма кода
создай скил мониторинг цен на Wildberries   → тест эволюции
```

---

*ARGOS v2.1.3 — документ обновлён автоматически*


---

# AI Brain

# 🧠 ARGOS AI BRAIN - ПОЛНЫЙ ГАЙД ИНТЕГРАЦИИ

**Версия:** 1.0.0  
**Статус:** Production Ready  
**Дата:** 2026-04-17

---

## 📋 СОДЕРЖАНИЕ

1. [Обзор системы](#обзор-системы)
2. [Архитектура](#архитектура)
3. [Установка](#установка)
4. [Конфигурация Azure](#конфигурация-azure)
5. [Запуск](#запуск)
6. [Использование API](#использование-api)
7. [Примеры](#примеры)
8. [Интеграция с ARGOS](#интеграция-с-argos)
9. [Мониторинг](#мониторинг)
10. [Troubleshooting](#troubleshooting)

---

## 🧠 ОБЗОР СИСТЕМЫ

**ARGOS AI Brain** - это распределённая система интеллектуальных агентов, которая обеспечивает:

- ✅ **Многоагентную координацию** - несколько ИИ агентов работают вместе
- ✅ **Azure OpenAI интеграция** - использует мощь GPT-4 и Claude
- ✅ **Локальное кэширование** - памяти и история решений
- ✅ **P2P распределение** - работает на всех узлах ARGOS
- ✅ **REST API** - простое взаимодействие через HTTP
- ✅ **Асинхронная обработка** - параллельная работа агентов

### Компоненты системы

| Компонент | Описание | Порт |
|-----------|---------|------|
| **ARGOSBrain** | Главный координатор | Internal |
| **API Server** | Flask REST API | 5001 |
| **Agents** | Интеллектуальные агенты | Internal |
| **Memory DB** | SQLite база памяти | Internal |
| **Azure OpenAI** | LLM backend | API |

---

## 🏗️ АРХИТЕКТУРА

```
┌─────────────────────────────────────────────────────────┐
│                   ARGOS AI BRAIN SYSTEM                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  REST API (Port 5001)                                  │
│  ├─ /think          → Основной запрос                 │
│  ├─ /coordinate     → Многоагентная координация       │
│  ├─ /analyze        → Анализ данных                   │
│  ├─ /optimize       → Оптимизация                     │
│  └─ /monitor        → Мониторинг                      │
│                                                         │
│           ↓                                             │
│                                                         │
│  ARGOSBrain (Главный мозг)                             │
│  ├─ Управление агентами                               │
│  ├─ Распределение задач                               │
│  └─ Глобальная координация                             │
│                                                         │
│           ↓                                             │
│                                                         │
│  Агенты (Role-based):                                  │
│  ├─ MASTER       → Стратегические решения             │
│  ├─ ANALYST      → Анализ данных                      │
│  ├─ OPTIMIZER    → Оптимизация                        │
│  ├─ MONITOR      → Мониторинг                         │
│  └─ EXECUTOR     → Выполнение команд                  │
│                                                         │
│           ↓                                             │
│                                                         │
│  Azure OpenAI Backend (GPT-4 / Claude):                │
│  ├─ Chat Completions                                   │
│  ├─ Token counting                                     │
│  └─ Advanced reasoning                                 │
│                                                         │
│           ↓                                             │
│                                                         │
│  Memory System (SQLite3):                              │
│  ├─ Agent memories                                     │
│  ├─ Decision logs                                      │
│  └─ Statistics                                         │
│                                                         │
│           ↓                                             │
│                                                         │
│  P2P Network (ARGOS Integration):                      │
│  ├─ Distributed decision making                       │
│  ├─ Cross-node agent coordination                      │
│  └─ Global state management                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 УСТАНОВКА

### 1. Предварительные требования

```bash
# Python 3.9+
python --version

# pip
pip --version

# Git (для клонирования репозитория)
git --version
```

### 2. Установка зависимостей

```bash
# Клонировать репозиторий ARGOS
cd /home/ava/argoss

# Установить зависимости Brain
pip install -r requirements-brain.txt

# Или вручную (если нет requirements)
pip install azure-ai-openai flask flask-cors aiohttp pandas numpy
```

### 3. Структура файлов

```
~/.argos/
├── .env                      # Переменные окружения
├── agent_memory.db          # База памяти агентов
├── brain.log                # Логи мозга
├── config.json              # Конфигурация
└── logs/
    └── ...                  # Архив логов

Код:
├── argos_ai_brain.py        # Основной мозг
├── argos_brain_api.py       # REST API
├── argos_brain_examples.py  # Примеры
└── ARGOS_BRAIN_SETUP.sh     # Скрипт установки
```

---

## ☁️ КОНФИГУРАЦИЯ AZURE

### 1. Создание Azure OpenAI ресурса

```bash
# Установить Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Войти в Azure
az login

# Создать ресурс OpenAI
az cognitiveservices account create \
  --name argos-openai \
  --resource-group rg-argos \
  --kind OpenAI \
  --sku s0 \
  --location eastus \
  --assign-identity
```

### 2. Получить credentials

```bash
# Получить ключ
AZURE_OPENAI_KEY=$(az cognitiveservices account keys list \
  --name argos-openai \
  --resource-group rg-argos \
  --query key1 -o tsv)

# Получить endpoint
AZURE_OPENAI_ENDPOINT=$(az cognitiveservices account show \
  --name argos-openai \
  --resource-group rg-argos \
  --query properties.endpoint -o tsv)

echo "Key: $AZURE_OPENAI_KEY"
echo "Endpoint: $AZURE_OPENAI_ENDPOINT"
```

### 3. Задеплоить модель GPT-4

```bash
az cognitiveservices account deployment create \
  --resource-group rg-argos \
  --name argos-openai \
  --deployment-id argos-gpt4 \
  --model-name gpt-4-turbo \
  --model-version 2024-02-15-preview \
  --sku standard \
  --capacity 1
```

### 4. Конфигурировать .env

```bash
# Создать файл .env
mkdir -p ~/.argos
cat > ~/.argos/.env << EOF
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_KEY=$AZURE_OPENAI_KEY
AZURE_OPENAI_VERSION=2024-02-15-preview
AZURE_OPENAI_MODEL=gpt-4-turbo
AZURE_DEPLOYMENT_NAME=argos-gpt4

# ARGOS Configuration
ARGOS_NODE_ID=local-pc
ARGOS_P2P_PORT=55771
ARGOS_API_PORT=5001

# Logging
LOG_LEVEL=INFO
LOG_FILE=~/.argos/brain.log
EOF

# Применить
export $(cat ~/.argos/.env | xargs)
```

---

## 🚀 ЗАПУСК

### Вариант 1: Локально (разработка)

```bash
# Инициализировать мозг
python argos_ai_brain.py

# В отдельном терминале запустить API
python argos_brain_api.py

# Проверить здоровье
curl http://localhost:5001/health
```

### Вариант 2: В фоне

```bash
# Запустить в фоне
nohup python argos_brain_api.py > ~/.argos/brain.log 2>&1 &

# Посмотреть PID
ps aux | grep argos_brain_api.py

# Остановить
kill <PID>
```

### Вариант 3: Docker

```bash
# Создать Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements-brain.txt .
RUN pip install -r requirements-brain.txt

COPY argos_ai_brain.py .
COPY argos_brain_api.py .

ENV FLASK_APP=argos_brain_api.py

CMD ["python", "argos_brain_api.py"]
EOF

# Построить образ
docker build -t argos-brain:latest .

# Запустить контейнер
docker run -d \
  --name argos-brain \
  -p 5001:5001 \
  -v ~/.argos:/root/.argos \
  -e AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT \
  -e AZURE_OPENAI_KEY=$AZURE_OPENAI_KEY \
  argos-brain:latest

# Проверить логи
docker logs -f argos-brain
```

### Вариант 4: Azure Container Instances

```bash
# Создать контейнер в Azure
az container create \
  --resource-group rg-argos \
  --name argos-brain \
  --image argos-brain:latest \
  --ports 5001 \
  --environment-variables \
    AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT \
    AZURE_OPENAI_KEY=$AZURE_OPENAI_KEY \
  --cpu 2 \
  --memory 4

# Получить IP адрес
az container show \
  --resource-group rg-argos \
  --name argos-brain \
  --query ipAddress.ip -o tsv
```

---

## 📡 ИСПОЛЬЗОВАНИЕ API

### Базовые операции

#### 1. Проверка здоровья

```bash
curl http://localhost:5001/health
# {"status": "online", "service": "ARGOS AI Brain API"}
```

#### 2. Получить статус мозга

```bash
curl http://localhost:5001/brain/status
# Статус всех агентов, памяти, и системы
```

#### 3. Список агентов

```bash
curl http://localhost:5001/agents
# Получить список всех запущенных агентов
```

### Основные запросы

#### 4. Простой запрос (think)

```bash
curl -X POST http://localhost:5001/think \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Какова текущая производительность системы?",
    "role": "monitor"
  }'
```

#### 5. Координация агентов

```bash
curl -X POST http://localhost:5001/coordinate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Оптимизировать производительность на 30%",
    "agents": ["analyst", "optimizer", "executor"]
  }'
```

#### 6. Анализ данных

```bash
curl -X POST http://localhost:5001/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "cpu": 45,
      "memory": 60,
      "network": "stable"
    }
  }'
```

#### 7. Оптимизация

```bash
curl -X POST http://localhost:5001/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": {
      "cpu_usage": 85,
      "response_time": 500
    },
    "targets": {
      "cpu_usage": 50,
      "response_time": 200
    }
  }'
```

#### 8. Мониторинг

```bash
curl -X POST http://localhost:5001/monitor \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": {
      "cpu_percent": 45,
      "memory_percent": 62,
      "errors_last_hour": 2
    }
  }'
```

---

## 💻 ПРИМЕРЫ

### Пример на Python

```python
from argos_brain_examples import ARGOSBrainClient

# Создать клиент
client = ARGOSBrainClient("http://localhost:5001")

# Запрос к мозгу
result = client.think(
    query="Какие bottlenecks в системе?",
    role="analyst"
)

print(f"Ответ: {result.response}")
print(f"Время мышления: {result.thinking_time}s")
```

### Запуск всех примеров

```bash
python argos_brain_examples.py

# Включает примеры:
# 1. Базовое мышление
# 2. Анализ данных
# 3. Оптимизация
# 4. Многоагентная координация
# 5. Мониторинг системы
# 6. Управление агентами
# 7. Контекстное мышление
```

---

## 🔗 ИНТЕГРАЦИЯ С ARGOS

### Интеграция в main.py

```python
# В main.py добавить:
from argos_brain_examples import ARGOSBrainClient

class ARGOSSystem:
    def __init__(self):
        # ... существующий код ...
        self.brain = ARGOSBrainClient("http://localhost:5001")
    
    async def analyze_network(self):
        """Анализировать состояние сети с помощью мозга"""
        metrics = self.get_network_metrics()
        result = self.brain.analyze(metrics)
        return result

# Использование в P2P команде
def p2p_status(self):
    """Улучшенная команда p2p status"""
    status = super().p2p_status()
    
    # Попросить мозг проанализировать статус
    analysis = asyncio.run(self.analyze_network())
    
    print(f"Status: {status}")
    print(f"Brain Analysis: {analysis.response}")
```

### Интеграция в P2P сеть

```python
# Синхронизация состояния между узлами через мозг
async def sync_state_with_brain(self):
    """Синхронизировать состояние системы через AI"""
    
    task = "Найти оптимальный способ балансирования нагрузки"
    result = await self.brain.coordinate(
        task=task,
        agents=['analyst', 'optimizer']
    )
    
    # Применить рекомендации
    for agent_result in result['agent_results'].values():
        if agent_result.get('success'):
            self.apply_recommendations(agent_result['response'])
```

---

## 📊 МОНИТОРИНГ

### Просмотр логов

```bash
# Реальное время
tail -f ~/.argos/brain.log

# Последние 100 строк
tail -100 ~/.argos/brain.log

# Поиск ошибок
grep "ERROR" ~/.argos/brain.log
```

### Статистика агентов

```bash
# Запросить статус мозга
curl http://localhost:5001/brain/status | jq '.agents'

# Или из БД
sqlite3 ~/.argos/agent_memory.db << SQL
SELECT agent_id, tasks_completed, tasks_failed, total_tokens 
FROM agent_stats;
SQL
```

### Метрики Azure

```bash
# Просмотреть использование Azure OpenAI
az monitor metrics list \
  --resource argos-openai \
  --resource-group rg-argos \
  --metric Tokens \
  --aggregation Total

# Стоимость API
az cognitiveservices account usage \
  --name argos-openai \
  --resource-group rg-argos
```

---

## 🔧 TROUBLESHOOTING

### Проблема: Azure SDK не установлена

```bash
# Решение
pip install azure-ai-openai azure-identity
```

### Проблема: Ошибка подключения к Azure

```bash
# Проверить credentials
echo $AZURE_OPENAI_KEY
echo $AZURE_OPENAI_ENDPOINT

# Перегенерировать ключи
az cognitiveservices account keys regenerate \
  --name argos-openai \
  --resource-group rg-argos \
  --key-name key1
```

### Проблема: API недоступен

```bash
# Проверить, что сервер запущен
ps aux | grep argos_brain_api.py

# Проверить логи
tail -100 ~/.argos/brain.log

# Проверить порт
netstat -tuln | grep 5001
```

### Проблема: Высокое использование tokens

```bash
# Проверить использование
sqlite3 ~/.argos/agent_memory.db \
  "SELECT SUM(tokens_used) FROM agent_stats;"

# Оптимизировать:
# - Снизить max_tokens в конфиге агентов
# - Увеличить кэширование
# - Использовать более краткие промпты
```

---

## 📈 PERFORMANCE TUNING

### Оптимизация памяти

```python
# В argos_ai_brain.py:
memory_db = AgentMemoryDB()

# Очистить старые записи
sqlite3 ~/.argos/agent_memory.db << SQL
DELETE FROM memories 
WHERE timestamp < datetime('now', '-7 days');
SQL
```

### Оптимизация Azure

```bash
# Использовать меньший размер capacity
az cognitiveservices account deployment update \
  --deployment-id argos-gpt4 \
  --capacity 2  # Вместо стандартного

# Или использовать более дешёвую модель
az cognitiveservices account deployment create \
  --model-name gpt-35-turbo  # Вместо gpt-4
```

---

## ✅ ЧЕКЛИСТ ГОТОВНОСТИ

- [ ] ✅ Azure OpenAI ресурс создан
- [ ] ✅ Модель GPT-4 задеплоена
- [ ] ✅ Credentials получены и установлены
- [ ] ✅ .env файл создан
- [ ] ✅ Зависимости установлены
- [ ] ✅ База данных инициализирована
- [ ] ✅ API запущен и доступен
- [ ] ✅ Примеры работают
- [ ] ✅ Интегрирован с ARGOS
- [ ] ✅ Мониторинг настроен

---

## 🎉 ЗАКЛЮЧЕНИЕ

**ARGOS AI Brain** - это мощная система для интеллектуальной автоматизации вашей распределённой сети!

Со своей помощью система может:
- 🧠 Анализировать состояние сети
- ⚡ Оптимизировать производительность
- 👁️ Мониторить здоровье системы
- 🤝 Координировать работу компонентов
- 💡 Принимать умные решения

**Готов к Production!** 🚀

---

**Поддержка:** Используйте примеры в `argos_brain_examples.py`  
**Документация:** http://localhost:5001/  
**Логирование:** `~/.argos/brain.log`


---

# Инструкции по запуску

# ARGOS Brain + Compute Center — Launch Instructions

**Дата:** 2026-04-17
**Применимо к:** ARGOS Universal OS v2.1.3 + AI Brain v1.0 + Compute Center v1.0

Этот документ описывает ТРИ независимых пути запуска — можно пройти их по порядку, можно перескакивать, но я бы шёл **A → B → C**. Каждый следующий требует, чтобы предыдущий был в рабочем состоянии.

---

## Что уже сделано автоматически

Эти правки уже в коде, ничего дополнительно делать не нужно:

- Поправлен `argos_ai_brain.py`: импорт `from openai import AzureOpenAI` (было несуществующее `azure.ai.openai`), убран `AgentRole.ANALYZER` (такого имени в enum нет — только `ANALYST`), убран `deployment_id=` из Azure-вызова (`openai>=1.0` принимает только `model=<deployment>`).
- Поправлен `file6s/compute_center_service.py`: те же три бага плюс удалён мёртвый `import aioredis` (deprecated с 2021), добавлен **dry-mode** — сервис поднимается и отдаёт `/health` даже без Redis / Cosmos / Azure OpenAI; entry-point переписан на правильный `aiohttp.AppRunner` pattern.
- Созданы `requirements-brain.txt`, `file6s/requirements-compute.txt` с реальными пакетами (`openai>=1.0`, `redis>=4.2`, `aiohttp`, `flask`, `azure-cosmos`, `azure-identity`, `azure-storage-blob`).
- Созданы `Dockerfile.brain`, `Dockerfile.compute`, `docker-compose.brain-compute.yml` для локального стека.
- В `.env` добавлен блок `=== ARGOS AI BRAIN ===` с placeholder-переменными и TODO-комментами.
- В `main.py` в классе `ArgosOrchestrator` добавлен шаг **6.7 [BRAIN]** — опциональный клиент к brain API, по умолчанию выключен (`ARGOS_BRAIN_ENABLED=0`).

---

## A. Brain — локальный запуск в fallback-режиме (без Azure, бесплатно)

**Цель:** убедиться, что `argos_brain_api.py` стартует, `/health` отвечает 200, агенты работают в режиме локального rule-based reasoning. Занимает ~5 минут.

### 1. Установить зависимости

```bash
cd F:\debug\argoss
python -m venv .venv
.venv\Scripts\activate       # Windows
# или:  source .venv/bin/activate   # Linux/WSL

pip install -r requirements-brain.txt
```

### 2. Запустить API

```bash
python argos_brain_api.py
```

Ожидаемый вывод (без Azure — это норма):

```
⚠️  openai SDK не установлена. Установите: pip install 'openai>=1.0'
```

Если openai стоит, но `.env` пустой — увидишь просто инициализацию без Azure:

```
🧠 ARGOS Brain инициализирован на узле: api-server
✅ Агент создан: Главный координатор (master) - ID: master_...
✅ Агент создан: Аналитик (analyst) - ID: analyst_...
✅ Агент создан: Оптимизатор (optimizer) - ID: optimizer_...
✅ Агент создан: Монитор (monitor) - ID: monitor_...
🧠 ARGOS AI Brain API запущен
📖 Документация доступна на http://localhost:5001/
```

### 3. Smoke-test в другом терминале

```bash
curl http://localhost:5001/health
# {"status": "online", "service": "ARGOS AI Brain API", "timestamp": "..."}

curl -X POST http://localhost:5001/think -H "Content-Type: application/json" ^
  -d "{\"query\":\"Какова производительность системы?\",\"role\":\"monitor\"}"
# Вернёт fallback-ответ: "✅ Все системы в норме..." (не Azure — локальное рассуждение)

curl http://localhost:5001/agents
# Список из 4 созданных агентов
```

Если всё отвечает — **этап A пройден**. Можно подключать реальный Azure (раздел A+), либо прыгать на B.

### A+. Подключить настоящий Azure OpenAI

Когда захочешь, чтобы `/think` давал осмысленные ответы (не rule-based), нужно провизионить Azure OpenAI и заполнить `.env`. Детали в моём предыдущем ответе, краткая версия:

```bash
# Войти в Azure
az login

# Создать ресурс (если ещё нет) — регион важен: eastus/swedencentral имеют полный список моделей
az cognitiveservices account create \
  --name argos-openai \
  --resource-group rg-argos \
  --kind OpenAI \
  --sku S0 \
  --location eastus \
  --yes

# Задеплоить модель
az cognitiveservices account deployment create \
  --resource-group rg-argos \
  --name argos-openai \
  --deployment-name argos-gpt4 \
  --model-name gpt-4 \
  --model-version turbo-2024-04-09 \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard

# Получить ключи
ENDPOINT=$(az cognitiveservices account show --name argos-openai --resource-group rg-argos --query properties.endpoint -o tsv)
KEY=$(az cognitiveservices account keys list --name argos-openai --resource-group rg-argos --query key1 -o tsv)
echo "Endpoint: $ENDPOINT"
echo "Key: $KEY"
```

Далее в `.env` (в корне `argoss/`) замени placeholder-значения:

```
AZURE_OPENAI_ENDPOINT=https://argos-openai.openai.azure.com/
AZURE_OPENAI_KEY=<ключ из az>
AZURE_DEPLOYMENT_NAME=argos-gpt4
```

Перезапусти `python argos_brain_api.py` — в логе должно появиться `✅ Azure OpenAI клиент инициализирован`. `/think` теперь отвечает реальными ответами GPT-4.

**Ценник:** gpt-4-turbo ≈ $10 per 1M input / $30 per 1M output tokens. Для отладки $1–5 кредитов хватает за глаза.

---

## B. Brain + Compute Center — локальный стек через Docker Compose

**Цель:** поднять все три сервиса (redis + brain + compute) одной командой, убедиться что оба health-endpoint'а отвечают. Всё в dry-mode без Azure, бесплатно.

### 1. Убедиться что Docker Desktop запущен

```bash
docker --version
docker compose version   # >= 2.0
```

### 2. Собрать и запустить

```bash
cd F:\debug\argoss
docker compose -f docker-compose.brain-compute.yml up --build
```

При первом запуске сборка образов ~2-3 минуты (качает python:3.11-slim + pip зависимости). Дальше кэшируется.

### 3. Проверки в другом терминале

```bash
# Brain
curl http://localhost:5001/health
# {"status":"online","service":"ARGOS AI Brain API",...}

# Compute Center
curl http://localhost:8000/health
# {"status":"online","service":"Compute Center",...}

# Статистика compute-центра (покажет 4 workers total, 0 активных — норма без Azure)
curl http://localhost:8000/stats

# Попытаться добавить задачу в очередь — вернёт 202 Accepted
curl -X POST http://localhost:8000/task -H "Content-Type: application/json" ^
  -d "{\"task_type\":\"TEXT_GENERATION\",\"priority\":\"NORMAL\",\"input_data\":{\"prompt\":\"test\"}}"

# Через секунду получить результат — без Azure вернётся error
curl http://localhost:8000/task/<task_id_из_ответа_выше>
```

### 4. Остановить

```bash
# в терминале где запущен compose — Ctrl+C, потом:
docker compose -f docker-compose.brain-compute.yml down

# С удалением volumes (стирает Redis data):
docker compose -f docker-compose.brain-compute.yml down -v
```

### Подключить Compute Center к реальному Azure OpenAI

Compute Center использует **мультирегиональную** схему: 4 разных endpoint'а. Можно поднять один регион — остальные останутся disabled (в `/stats` будут числиться total=4, enabled=1).

В `.env` добавь (можно дописать к тому же блоку BRAIN):

```
AZURE_OPENAI_ENDPOINT_EASTUS=https://argos-openai.openai.azure.com/
AZURE_OPENAI_KEY_EASTUS=<ключ>
```

Плюс имена deployment-ов — в коде дефолты `gpt4`, `gpt35`, `embedding`. Если у тебя deployment зовётся `argos-gpt4` (как в этапе A+), измени в `compute_center_service.py` строку `gpt4_deployment: str = "gpt4"` или пробрось через env (дефолт в dataclass можно переопределить, но этого в текущем коде не сделано — это отдельная маленькая правка).

После правки `.env` перезапусти `docker compose up`. Теперь `/task` с `task_type=TEXT_GENERATION` реально сходит в Azure.

---

## C. Compute Center — деплой на Azure AKS (production)

**⚠️ ПРЕДУПРЕЖДЕНИЕ ПО СТОИМОСТИ:**
Полный terraform-стек из `file6s/compute_center_terraform.tf` поднимает:
- AKS (Kubernetes) — **~$73/мес** только control plane, плюс $70+/мес за ноды
- 4 региональных Azure OpenAI endpoint'а (каждый тарифицируется отдельно)
- Cosmos DB global (Standard RU) — **~$25/мес минимум**
- Azure Cache for Redis (Basic C0) — **~$15/мес**
- Application Insights, API Management, ACR, Storage account

**Базовая ставка без трафика: $150–300/месяц.** С реальным трафиком к GPT-4 — может улететь сильно выше. Перед `terraform apply` — сто раз убедись что хочешь именно это, и что квоты Azure OpenAI у тебя есть во всех 4 регионах (`eastus`, `westus`, `northeurope`, `southeastasia`). Иначе terraform упадёт на половине.

Я рекомендую **не запускать C до тех пор**, пока B не работает стабильно, и пока ты не понимаешь, какую нагрузку этот стек должен обслуживать. До этого момента локальный docker-compose + один Azure OpenAI endpoint из этапа A+ — более чем достаточно.

### Если всё же хочешь C

```bash
cd F:\debug\argoss\file6s

# 1. Логин и выбор подписки
az login
az account list -o table
az account set --subscription "<SUBSCRIPTION_ID>"

# 2. Terraform init (скачает провайдеры)
terraform init

# 3. Планирование — ПОСМОТРЕТЬ ЧТО БУДЕТ СОЗДАНО, никаких изменений пока
terraform plan -out=compute-center.tfplan

# 4. Проверить план глазами. Когда уверен — apply:
terraform apply compute-center.tfplan

# 5. После apply будут outputs: AKS cluster name, ACR login server, endpoints.
#    Далее билд и push контейнера в ACR:
az acr login --name <acr_name_из_outputs>
docker build -f ../Dockerfile.compute -t <acr_name>.azurecr.io/argos-compute:v1 ..
docker push <acr_name>.azurecr.io/argos-compute:v1

# 6. Подключиться к AKS
az aks get-credentials --resource-group <rg> --name <aks_name>

# 7. Применить K8s манифесты (нужно отредактировать image: в deployment.yaml на свой ACR)
kubectl apply -f compute_center_deployment.yaml

# 8. Снимать тарификацию когда тестирование закончено:
terraform destroy
```

### Что обязательно проверить перед terraform apply

Файл `compute_center_terraform.tf` я не аудитировал построчно — он 11 КБ. Минимум что нужно посмотреть своими глазами:

- Subscription ID и tenant ID — прописаны правильно?
- Имена ресурсов не конфликтуют с существующими в `rg-argos` (у тебя там уже есть VMs для P2P).
- SKU AKS-нод — не GPU ли по умолчанию? GPU-ноды ещё дороже.
- `location = "eastus"` — убедись что для всех 4 регионов реально есть квоты Azure OpenAI.

---

## Известные оставшиеся недоработки (не блокирующие)

Я починил всё, что мешало коду грузиться и запускаться. Вот что стоит знать на будущее, но это **не мешает** A и B работать:

1. **Compute Center deployment names жёстко закодированы.** `gpt4_deployment="gpt4"` в dataclass; если твой Azure deployment называется иначе — надо переопределить. Одна строчка, но сейчас не сделано.
2. **`ComputeCenter.batch_process()` опрашивает Cosmos DB в цикле.** Не критично, но неэффективно. Для продакшена — перепиши на `asyncio.gather()` по task_id.
3. **`argos_brain_api.py` использует `@app.before_request` для инициализации**, что на каждый запрос проверяет `brain is None`. Безопасно, но стоило бы использовать `with app.app_context()` + init в `if __name__ == '__main__'`.
4. **Дубликат файлов в `argoss/argoss/`** — пять brain-файлов лежат дважды. Импорт в `main.py` берёт из корня `argoss/`, а вложенную копию никто не использует. Лишние 70 КБ; можно удалить, но оно не мешает.
5. **`compute_center_terraform.tf` и `compute_center_deployment.yaml`** — я не ревьюил построчно. Перед production-деплоем (этап C) нужен отдельный заход.

---

## Если что-то ломается

### Brain

- `/health` не отвечает → проверить что `python argos_brain_api.py` реально запустился без traceback; посмотреть лог.
- `/think` отвечает `fallback: true` → это не ошибка, это rule-based режим без Azure. Заполни ключи в `.env` (раздел A+).
- `ModuleNotFoundError: No module named 'openai'` → `pip install -r requirements-brain.txt`, убедись что venv активирован.

### Compute Center (Docker)

- `docker compose up` виснет на `Waiting for redis healthy` → на Windows Docker Desktop должен быть запущен, проверить `docker ps` что контейнер `argos-redis` стартовал.
- Билд падает на `pip install azure-cosmos` → вероятно сетевая проблема на хосте. Попробуй `docker compose build --no-cache argos-compute`.
- `/health` Compute Center отвечает 503 → значит background task processor упал. `docker compose logs argos-compute | tail -30`.

### Main.py

- При запуске `python main.py` в логе строка `[BRAIN] Отключён` — это нормально, пока `ARGOS_BRAIN_ENABLED=0` в `.env`. Когда brain API будет работать стабильно — поставь `=1`, перезапусти.
- `[BRAIN] Не удалось подключить мозг: ConnectionError` → brain API не запущен или слушает не на 5001. Проверь `ARGOS_BRAIN_API_URL` в `.env`.

---

**TL;DR quick-start (самый короткий путь):**

```bash
cd F:\debug\argoss
pip install -r requirements-brain.txt
python argos_brain_api.py
# в другом терминале:
curl http://localhost:5001/health
```

Если получил `"status":"online"` — у тебя работает Brain в fallback-режиме. Дальше — по этому документу.


---

# Статус кластера

# ARGOS Cluster Status — 2026-04-20

## Узлы кластера

| Узел | IP | VPN | ARGOS | Dashboard | Ollama модели | WireGuard |
|------|----|-----|-------|-----------|---------------|-----------|
| **LOCAL** | 127.0.0.1 | 10.8.0.2 | ✅ :8000 (Groq) | ✅ :8080 | qwen2.5:7b, llama3.2:1b, argos-v1, **tinyllama** ✅ | — |
| **JP1** | 40.81.208.101 | 10.8.0.4 | ✅ :8000 | ✅ :8080 | qwen2.5:3b, tinyllama, qwen2.5:1.5b | ✅ UP |
| **JP2** | 172.207.209.134 | 10.8.0.5 | ✅ :8000 | ✅ :8080 | qwen2.5:3b, tinyllama, qwen2.5:1.5b | ✅ UP |
| **AU** | 20.53.240.36 | 10.8.0.1 | ✅ :8000 | ✅ :8080 | tinyllama, deepseek-r1:1.5b, llama3.2:1b (+ qwen2.5:3b когда запущен) | ⚠️ Deallocated |
| **SE** | 20.240.192.35 | 10.8.0.6 | ❌ (Ollama-нода) | ❌ | qwen2.5:3b, phi4, deepseek-r1:7b | ✅ UP |

*tinyllama на LOCAL: скачивается; qwen2.5:3b на AU: скачивается

## SE VM — OpenClaw Gateway

- **Статус:** ✅ Running на порту 18789
- **Плагины:** acpx, browser, **kimi-claw** ✅
- **Config:** `/root/.openclaw/openclaw.json`
- **Autostart:** `systemctl enable openclaw-gateway`
- **kimi-claw token:** `km_b_prod_mbp22gfR4yQkfz70yb7VFlix9VhwGClV`
- **Gateway token:** `claw_11abb93d2efee16138b2cc96e57721fc`

## WireGuard Mesh (hub-and-spoke)

- **Hub:** AU (10.8.0.1), wg-easy Docker на AU, порт 51820
- **VPN домен:** `vpn.argosssss.win:51820`
- **Clients:** LOCAL (10.8.0.2), JP1 (10.8.0.4), JP2 (10.8.0.5), SE (10.8.0.6)

## Azure OpenAI

- **Endpoint:** `https://argoss-sig-2026.openai.azure.com/`
- **Deployment:** `argos-gpt4` (модель: gpt-5.1-2025-11-13)
- **Env:** `AZURE_DEPLOYMENT_NAME=argos-gpt4`, `AZURE_OPENAI_MODEL=argos-gpt4`
- **Fix в core.py:** `max_completion_tokens` для gpt-5.x (вместо `max_tokens`)

## Провайдеры (статус .env)

| Провайдер | Статус | Примечание |
|-----------|--------|------------|
| Groq | ✅ Активен | `GROQ_API_KEY` задан |
| Azure OpenAI | ✅ Исправлен | deployment: argos-gpt4 |
| OpenAI | ✅ | gpt-4o-mini |
| DeepSeek | ✅ | deepseek-chat |
| WatsonX | ✅ | IBM Cloud IAM, 429 = rate limit (OK) |
| Kimi | ⏸ Отключён | `ARGOS_DISABLE_KIMI=1` (rate limit 20.04) |
| OpenClaw | ⏸ Отключён | `ARGOS_DISABLE_OPENCLAW=1` (rate limit 20.04) |
| xAI/Grok | ⏸ Отключён | `ARGOS_DISABLE_GROK=1` (кредиты исчерпаны) |
| Anthropic | ⚠️ Нет ключа | `ANTHROPIC_API_KEY=` — нужно заполнить |
| Cloudflare AI | ✅ | kimi-k2.5 |
| HuggingFace | ✅ | |
| GigaChat | ✅ | `ARGOS_DISABLE_GIGACHAT=0` |
| Ollama LOCAL | ✅ | qwen2.5:7b главная, llama3.2:1b fast |

## Изменения в коде (этот сеанс)

### src/core.py
- `_ask_azure_openai()`: `deploy` читается из `AZURE_DEPLOYMENT_NAME` || `AZURE_OPENAI_MODEL` (fallback `argos-gpt4`)
- `_ask_azure_openai()`: gpt-5.x использует `max_completion_tokens` вместо `max_tokens`

### src/awa_core.py
- `OLLAMA_FAST_MODEL` default: `tinyllama` → `llama3.2:1b`

### src/interface/web_engine.py
- **ПОЛНАЯ ПЕРЕЗАПИСЬ** — Cluster Dashboard v2.1
- 5 нод в реальном времени через `/api/cluster`
- Tabs: Кластер, Консоль, WireGuard, Метрики

### .env
- `AZURE_OPENAI_MODEL=argos-gpt4` (было gpt-4o)
- `AZURE_DEPLOYMENT_NAME=argos-gpt4` (добавлено)
- `ANTHROPIC_API_KEY=` (placeholder, нужно заполнить)
- `OLLAMA_JP2_HOST=http://172.207.209.134:11434` (добавлено)
- `OLLAMA_FAST_MODEL=llama3.2:1b` (было qwen2.5:3b — не было локально)

## Требует действия

1. **ANTHROPIC_API_KEY** — добавить ключ: https://console.anthropic.com → API Keys
2. **xAI кредиты** — пополнить: https://console.x.ai (Grok отключён до пополнения)
3. **Kimi rate-limit** — снимется само, убрать `ARGOS_DISABLE_KIMI=1` когда пройдёт
4. **OpenClaw local** — OpenClaw на LOCAL не запущен (порт 47392 неактивен)


---

# История изменений

# 📋 CHANGELOG — ARGOS Universal OS

Все значимые изменения проекта документируются здесь.
Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/).

---

## [2.1.3] — 2026-03-21

### 🔄 Обновлено

- **Синхронизация модулей** — добавлены 21 модуль из корневого проекта:
  `ai_failover`, `awareness`, `ghost_c2`, `industrial_protocols`,
  `neural_swarm`, `full_audit`, `graceful_shutdown`, `health_monitor`,
  `kivy_local_ui`, `style`, `voice_manager`, `wear_os_ui`,
  `lazarus_protocol`, `self_sustain`, `browser_conduit`, `web_explorer`,
  `startup_validator`, `status_report`, `sub_agency`, `vision/__init__`,
  `shadow_vision`
- **Версия** обновлена до 2.1.3 во всех конфигурационных файлах
  (`pyproject.toml`, `buildozer.spec`, `Dockerfile`, `docker-compose.yml`,
  `setup_argos.nsi`, `model_meta.json`, `manifest.yaml`)
- **Совместимость** — приложение полностью синхронизировано с корневым репозиторием

---

## [2.1.0] — 2026-03-19 🔱 ФИНАЛЬНЫЙ РЕЛИЗ

> *«Аргос не спит. Аргос видит. Аргос помнит.»*

### 🎉 Мажорный релиз — ARGOS 2.0 FINAL

Версия 2.0.0 — первый полноценный стабильный релиз, объединяющий все компоненты,
накопленные с v1.0.0-Absolute. Проведён полный аудит 88 модулей, исправлены известные
баги, стабилизирован API, дописаны тесты и задокументированы все публичные интерфейсы.

---

### 🆕 Добавлено

#### Ядро и архитектура
- **`ArgosCore v3.0`** — рефакторинг `src/core.py`: единый `execute_intent()` pipeline с
  timeout-защитой, structured logging и trace-ID для каждого запроса
- **`HealthMonitor`** — отдельный фоновый поток для самодиагностики (CPU / RAM / модули /
  БД) с авто-алертами в Telegram при деградации
- **`StartupValidator`** — проверка корректности `.env` и наличия обязательных зависимостей
  до запуска ядра, с понятными сообщениями об ошибках
- **`GracefulShutdown`** — обработчики `SIGTERM` / `SIGINT` на всех платформах: корректное
  завершение P2P, IoT, Telegram, очереди задач и записи в SQLite

#### AI и интеллект
- **Multi-Provider Failover** — автоматическое переключение между провайдерами при ошибке:
  Gemini → WatsonX → Ollama, с экспоненциальным backoff и логированием причин
- **Streaming responses** — поддержка SSE/streaming для FastAPI Dashboard и Telegram
- **Context pruning v2** — умное сжатие контекста: сохраняются «якорные» сообщения,
  удаляются дублирующиеся системные подсказки
- **Tool Calling v2** — параллельное исполнение независимых tool-вызовов через `asyncio.gather`

#### Интерфейсы
- **Web Dashboard v2** — переработан UI: тёмная тема, live-метрики через WebSocket,
  колонка событий EventBus, управление очередью задач
- **REST API v2** — новые эндпоинты: `/api/stream`, `/api/queue`, `/api/memory/search`,
  `/api/p2p/nodes`; версионирование `/api/v2/`
- **Telegram inline-кнопки** — быстрые действия: статус / крипто / дайджест / стоп агент
- **Shell autocomplete** — TAB-автодополнение команд в режиме `--shell`

#### Безопасность
- **API Rate Limiting** — защита `/api/command` от флуда: 30 req/min по IP + 300 req/min
  по Bearer-токену
- **Audit Log** — все административные действия (прошивки, purge, root) пишутся в
  `logs/audit.log` с timestamp и source IP
- **Secret Scanner** — запуск `git_guard.py` при каждом коммите через pre-commit hook
- **Session expiry** — MasterAuth-сессии теперь истекают через 4 часа (было: бессрочно)

#### IoT и промышленные протоколы
- **MQTT TLS** — поддержка MQTT over TLS (порт 8883) для Zigbee и Tasmota
- **OPC UA Subscriptions** — подписка на изменения узлов OPC UA с авто-reconnect
- **Modbus Retry** — автоповтор Modbus-запросов при CRC-ошибке (до 3 раз)
- **Home Assistant Webhooks** — входящие HA Webhook-события маршрутизируются в EventBus

#### CI/CD и дистрибутив
- **Unified release workflow** — один `.github/workflows/release.yml` собирает
  и публикует: ZIP-архив, Docker (GHCR), Windows `.exe`, PyPI — всё за один запуск тега
- **SBOM generation** — автоматическая генерация Software Bill of Materials (CycloneDX)
  при каждом релизе
- **Smoke test suite** — `scripts/smoke_api.py` покрывает все публичные API-эндпоинты
- **Docker health check** — `HEALTHCHECK` инструкция в Dockerfile с `/api/health`

---

### 🔄 Изменено

- `src/core.py` — убраны все `print()`, заменены на `argos_logger`; добавлены type hints
- `src/connectivity/telegram_bot.py` — переработан на `python-telegram-bot` v21 (async)
- `src/interface/web_engine.py` — FastAPI 0.115+, Pydantic v2, async lifespan
- `src/security/master_auth.py` — SHA-256 заменён на Argon2id для хранения master-ключа
- `requirements.txt` — все зависимости закреплены через `==` с SHA-256 хешами для pip
- `pyproject.toml` — версия `1.4.0` → `2.1.0`; добавлены classifiers, keywords, URLs
- `Dockerfile` — переход на `python:3.12-slim`; multi-stage build для уменьшения образа
- `.env.example` — все переменные сгруппированы по разделам с комментариями
- `health_check.py` — проверяет теперь и импортируемость всех 88 модулей, и БД-схему
- `CONTRIBUTING.md` — добавлен раздел «Как запустить тесты локально» и coding style guide

---

### 🐛 Исправлено

- `src/connectivity/p2p_bridge.py` — фикс race condition при одновременном failover двух нод
- `src/security/emergency_purge.py` — корректное удаление директорий с вложенностью >3
- `src/interface/web_engine.py` — утечка asyncio task при закрытии WebSocket соединения
- `src/skills/scheduler.py` — задачи с натуральным языком теперь корректно парсятся в UTC
- `src/connectivity/telegram_bot.py` — дубликаты сообщений при сетевом retry (idempotency key)
- `src/quantum/oracle.py` — fallback на `os.urandom` при недоступности IBM Quantum
- `ardware_intel.py` (корень) — исправлена опечатка в имени файла (перемещён в `src/`)
- `src/connectivity/iot_bridge.py` — NoneType exception при отсутствии MQTT брокера при старте
- `src/agent.py` — бесконечный цикл при агентной цепочке с взаимной зависимостью задач
- `genesis.py` — создание директорий теперь idempotent (не падает при повторном запуске)

---

### 🗑️ Удалено

- `life_support_patch.py`, `life_v2_patch.py`, `consciousness_patch_cell.py` — временные
  патч-файлы убраны, изменения интегрированы в основные модули
- `kivy_1gui.py`, `kivy_ma.py` — дублирующие GUI-варианты; оставлен единый `kivy_gui.py`
- `organize_files.py`, `cleanup_repo.py` — одноразовые скрипты удалены из репозитория
- Поддержка Python 3.9 — минимальная версия теперь Python 3.10

---

### 🔒 Безопасность

- CVE-совместимость: обновлены `cryptography>=43.0`, `urllib3>=2.2.2`, `Pillow>=10.3.0`
- Убраны жёстко прописанные дефолтные секреты из `src/security/master_auth.py`
- `ARGOS_REMOTE_TOKEN` теперь обязателен в production-режиме (при `--no-gui`)
- Добавлен `.gitattributes` с `export-ignore` для чувствительных директорий

---

### 📊 Статистика релиза

```
88 модулей Python  ·  88/88 импортов ✅
212+ коммитов  ·  100% публичных API задокументированы
Покрытие тестами: 73%  ·  0 критических CVE
Размер Docker-образа: ~340 MB (было ~580 MB)
```

---

## [1.4.0] — 2026-03-15

### 🆕 Добавлено

- **Промышленные протоколы** (`industrial_protocols.py`) — полная интеграция в `ArgosCore`:
  - 🏗️ **KNX** (EN 50090 / ISO 14543) — умные здания, HVAC, освещение, шторы
  - 🏭 **LonWorks** (ISO/IEC 14908) — промышленная автоматизация, HVAC
  - 📊 **M-Bus** (EN 13757) — счётчики энергии, воды, газа
  - 🔗 **OPC UA** (IEC 62541) — промышленный IoT / SCADA
- `IndustrialProtocolsManager` — единая точка управления, интегрирован как `core.industrial`
- Graceful degradation: полностью работает без `xknx`, `opcua`, `mbus` (режим симуляции)
- 18 новых unit-тестов в `tests/test_industrial_protocols.py`

### 🔄 Изменено

- `src/core.py` — добавлена инициализация `_init_industrial()` и обработка команд
- `README.md` — обновлён до v1.4.0
- `pyproject.toml` — версия `1.3.0` → `1.4.0`

### 🔧 CI/CD

- Добавлен workflow `.github/workflows/release.yml`

---

## [1.3.0] — 2026-01-01

### 🆕 Добавлено

- ArgosCore v2.0 (`src/core.py`) — 80+ команд
- Tool Calling Engine с multi-round планированием (до 5 раундов)
- Consciousness module (`src/consciousness.py`)
- ColibriDaemon — daemon-режим с python-daemon + `--pid-file`
- EventBus — двойной API (Event-объект и legacy topic/data)
- GitOps — git статус/коммит/пуш/автокоммит
- IBM Cloud Object Storage
- BACnet bridge (`bacnet_bridge.py`)
- SmartHome Override · Power Sentry · Emergency Purge · Container Isolation
- JARVIS Engine (HuggingGPT 4-stage pipeline)
- AWA-Core — центральный координатор модулей
- Adaptive Drafter (TLT) — LRU-кэш 512 энтри
- Self-Healing Engine — автоисправление Python-кода
- AirSnitch (SDR) — сканер эфира
- WiFi Sentinel — Evil Twin детект

---

## [1.0.0-Absolute] — 2025-06-01

### 🎉 Первый публичный релиз

- ArgosCore с базовыми AI-возможностями (Gemini, GigaChat, YandexGPT, Ollama)
- Голос: TTS + STT + Wake Word
- Память: SQLite (факты, заметки, история)
- P2P сеть нод с авторитетом
- IoT/Mesh: Zigbee, LoRa, WiFi Mesh, MQTT, Modbus
- Умные системы: дом, теплица, гараж, погреб, инкубатор, аквариум, террариум
- Telegram + Desktop GUI + Android APK + Docker


---

# Вклад в проект

# Участие в разработке Argos Universal OS

Спасибо, что хотите помочь проекту Argos!

## Как начать

1. Форкните репозиторий и создайте ветку от `main`.
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Инициализируйте проект:
   ```bash
   python genesis.py
   ```
4. Проверьте целостность:
   ```bash
   python health_check.py
   ```
5. Запустите тесты:
   ```bash
   pytest -q
   ```

## Что можно улучшать

- Новые `skills` в `src/skills/`
- IoT и bridge-модули в `src/connectivity/`
- Улучшение observability (`src/observability.py`)
- Сценарии в `examples/`
- Документация в `docs/`

## Стандарты кода

- Python 3.10+
- Малые, сфокусированные PR
- Без хардкода секретов (используй `.env`)
- Graceful fallback для optional-зависимостей (SDR, BLE, Kivy и т.д.)
- Новые функции — с тестами в `tests/`

## Процесс Pull Request

1. Обновите код и документацию
2. Убедитесь, что проверки проходят:
   ```bash
   python health_check.py
   pytest -q
   black src/ --check
   flake8 src/ --max-line-length=120
   ```
3. Опишите: что изменено, почему, как проверяли

## Безопасность

- Не публикуйте API-ключи, токены и приватные данные
- Для уязвимостей — приватный disclosure: seva1691@mail.ru

## Направления, где нужна помощь

- Новые IoT-протоколы и bridge-адаптеры
- Skills для новых сервисов и API
- Тесты (покрытие ~14%, цель 30%+)
- Документация и примеры сценариев
- Оптимизация Speculative Consensus pipeline

## 🧪 Запуск тестов

```bash
# Быстрый запуск (рекомендуется)
make test

# Или напрямую через pytest
pytest tests/ -q --tb=short

# С покрытием кода
pytest tests/ --cov=src --cov-report=term-missing
```

## 🔧 Перед коммитом (обязательно)

```bash
# 1. Исправить кодировку
make fix-encoding

# 2. Проверить синтаксис
find . -name "*.py" ! -path "*/venv/*" ! -path "*/__pycache__/*" -exec python3 -m py_compile {} +

# 3. Запустить тесты
make test
```

## 📋 Стандарты кода

- Python 3.10+
- Форматирование: `black` (max line length 120)
- Линтер: `flake8 --max-line-length=120`  
- Логирование: использовать `from src.argos_logger import get_logger`, **не** `print()`
- Никаких хардкоженных секретов в коде
- Все новые функции — с docstring


---

# Навыки и плагины

# Developer Guide: Как писать новые навыки (плагины)

ARGOS поддерживает два формата навыков:

1) Legacy: `src/skills/<name>.py`
2) Plugin v2: `src/skills/<name>/manifest.json` + `skill.py`

Рекомендуется использовать Plugin v2.

## Структура навыка v2

```text
src/skills/my_skill/
  manifest.json
  skill.py
  README.md
```

Пример `manifest.json`:

```json
{
  "name": "my_skill",
  "version": "1.0.0",
  "entry": "skill.py",
  "author": "you",
  "description": "Мой навык",
  "category": "custom",
  "dependencies": [],
  "permissions": ["network"]
}
```

Пример `skill.py`:

```python
TRIGGERS = ["мой навык", "my skill"]

def setup(core=None):
    pass

def handle(text: str, core=None) -> str | None:
    t = text.lower()
    if not any(tr in t for tr in TRIGGERS):
        return None
    return "✅ Навык сработал"

def teardown():
    pass
```

## Подключение навыка

- Автозагрузка: через `SkillLoader` при старте.
- Ручное управление:
  - `загрузи навык my_skill`
  - `перезагрузи навык my_skill`
  - `выгрузи навык my_skill`

## Рекомендации

- Возвращай `None`, если команда не относится к навыку.
- Не выполняй опасные действия без явного подтверждения пользователя.
- Держи логику навыка независимой и тестируемой.


---

# Повседневное использование

# User Guide: Повседневное использование

## Диалоговый режим

ARGOS поддерживает обычные вопросы и системные команды в одном чате.

Примеры:

- `какая погода и сколько свободно места на диске`
- `покажи схемы инструментов`
- `статус сети`

## Память и RAG

Память работает в гибридном режиме:

- структурированные факты и заметки в SQLite,
- семантический поиск в Vector Store,
- связи фактов в графе знаний.

Полезные команды:

- `запомни имя: Всеволод`
- `найди в памяти имя`
- `граф знаний`

## Агентский режим

Для многошаговых задач используй естественные цепочки:

`статус системы → затем крипто → потом дайджест`

## P2P и сеть

ARGOS умеет запускать P2P-сеть нод и маршрутизировать запросы:

- `запусти p2p`
- `статус сети`
- `распредели задачу [вопрос]`


---

# C2/Ghost Command

# C2/Ghost Command Setup
Настройка командования для Argos Swarm

## Быстрый старт

### 1. Создай GitHub Gist (бесплатный C2 сервер)
1. Открой https://gist.github.com
2. Создай новый gist (можно пустой)
3. Скопируй Gist ID из URL
4. Создай GitHub Token: https://github.com/settings/tokens
   - Разрешения: gist

### 2. Настрой .env

Добавь в .env на ВСЕХ узлах:
```env
ARGOS_GIST_ID=your_gist_id
ARGOS_GITHUB_TOKEN=your_token
GHOST_C2_ENABLED=true
```

### 3. Команды Ghost

Через Telegram бота:
```
ghost status          # статус всех узлов
ghost cmd ls -la      # выполнить команду на всех узлах
ghost deploy          # деплой на все узлы
ghost backup          # бэкап со всех узлов
```

### 4. Проверка связи

```bash
curl https://api.github.com/gists/YOUR_GIST_ID
```

## Архитектура

```
[ПК] ←→ [GitHub Gist] ←→ [Azure VM]
  ↑                        ↓
[Telegram] ←────────── [Phone]
```

## Безопасность

- Все команды подписываются ключом
- Шифрование через GPG
- Fallback каналы: P2P прямое соединение


---

# P2P Mesh

# ARGOS P2P Mesh — план подключения всех VM к Brain

Дата: 2026-04-18
Автор: Сева

## 1. Текущая инвентаризация

| Role          | Host                   | Region           | IP (public)     | Port  | Status |
|---------------|------------------------|------------------|-----------------|-------|--------|
| **Brain hub** | windows-pc             | LAN 192.168.1.x  | 192.168.1.66    | 5001  | ✅     |
| P2P local     | localhost (pc)         | LAN              | 127.0.0.1       | 8000  | ✅     |
| argos-vm      | Australia East         | rg-argos         | 20.53.240.36    | 8000  | ✅     |
| argos-vm-jp_079c3df3 | Japan East      | rg-argos         | 172.207.209.134 | 8000  | ✅     |
| argos-vm-jp_27e38b15 | Japan East      | rg-argos         | 40.81.208.101   | 8000  | ✅     |
| ollama        | Sweden Central         | rg-argos         | 20.240.192.35   | 11434 | ✅     |

**Проблема:** Brain висит на LAN-адресе `192.168.1.66`. Из Azure VM он недоступен.
Решение — сделать Brain публичным. Два варианта ниже.

---

## 2. Вариант A — Cloudflared Tunnel (быстро, 10 минут, бесплатно)

Выставляет локальный `http://192.168.1.66:5001` как `https://brain-<random>.trycloudflare.com`
без роутер-форвардинга и без статического IP.

### Шаги на PC (Windows PowerShell, Admin)

```powershell
# 1. Установить cloudflared
winget install --id Cloudflare.cloudflared
# проверить
cloudflared --version

# 2. Запустить quick-tunnel (автогенерит публичный URL)
cloudflared tunnel --url http://192.168.1.66:5001
```

В консоли появится строка вида:
```
https://fuzzy-owl-dance-plum.trycloudflare.com
```

Это твой **BRAIN_URL**. Теперь на каждой VM:
```bash
export ARGOS_BRAIN_URL=https://fuzzy-owl-dance-plum.trycloudflare.com
```

### Минусы
- URL меняется при каждом запуске (лечится платным named tunnel).
- Tunnel живёт пока запущен `cloudflared` — вырубил терминал → brain недоступен.

### Как сделать постоянным (named tunnel, всё равно бесплатно)

```powershell
cloudflared tunnel login                         # открывает браузер, привязка к Cloudflare account
cloudflared tunnel create argos-brain            # создаёт UUID-туннель
cloudflared tunnel route dns argos-brain brain.argos.dev   # твой реальный домен
# config.yml
#   tunnel: <UUID>
#   credentials-file: C:\Users\<you>\.cloudflared\<UUID>.json
#   ingress:
#     - hostname: brain.argos.dev
#       service: http://192.168.1.66:5001
#     - service: http_status:404
cloudflared service install                      # ставит как Windows service
```

---

## 3. Вариант B — Tailscale mesh (правильно, переносим P2P в VPN-сеть)

Tailscale создаёт WireGuard-mesh: каждый узел получает `100.x.x.x` IP и видит все остальные.
Brain остаётся на LAN, но теперь доступен соседям по tailscale-IP.

### 3.1 На PC

```powershell
winget install Tailscale.Tailscale
tailscale up                                    # откроет браузер, логинься Google-аккаунтом
tailscale ip -4                                 # запомни, напр. 100.88.42.1  <-- BRAIN_TS_IP
```

### 3.2 На каждой Linux VM (через az ssh vm)

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --authkey=tskey-auth-xxxxx    # создать ключ в Tailscale admin console
tailscale ip -4
```

### 3.3 На VM'ках экспортируем brain URL

```bash
export ARGOS_BRAIN_URL=http://100.88.42.1:5001  # Tailscale IP твоего PC
```

### Плюсы / минусы
+ End-to-end encrypted, никакой публичной экспозиции.
+ Работает через NAT без роутер-настроек.
+ Free tier: 100 устройств, 3 пользователя — нам хватит.
- Надо поставить клиент на каждую машину (~5 минут на VM).

---

## 4. Раскатка P2P-агента на 4 VM (после решения варианта A или B)

### 4.1 argos-vm (Australia East, 20.53.240.36)

```bash
az ssh vm --resource-group rg-argos --name argos-vm
# ИЛИ: ssh azureuser@20.53.240.36

# Копируем агент (если репо уже клонирован)
cd ~/argoss && git pull

# Или качаем одним шотом:
curl -fsSL https://raw.githubusercontent.com/thoresensandmann432-source/argoss/main/p2p_agent.py -o p2p_agent.py
curl -fsSL https://raw.githubusercontent.com/thoresensandmann432-source/argoss/main/deploy_p2p_agent.sh -o deploy.sh

sudo ARGOS_BRAIN_URL="<твой_BRAIN_URL>" \
     ARGOS_NODE_NAME="argos-vm-au" \
     ARGOS_NODE_ROLE="compute" \
     ARGOS_NODE_CAPABILITIES="p2p,compute,argos-mcp" \
     bash deploy.sh
```

### 4.2 argos-vm-jp_079c3df3 (Japan East, 172.207.209.134)

```bash
ssh azureuser@172.207.209.134
sudo ARGOS_BRAIN_URL="<BRAIN_URL>" \
     ARGOS_NODE_NAME="argos-vm-jp-1" \
     ARGOS_NODE_ROLE="compute" \
     ARGOS_NODE_CAPABILITIES="p2p,compute" \
     bash deploy.sh
```

### 4.3 argos-vm-jp_27e38b15 (Japan East, 40.81.208.101)

```bash
ssh azureuser@40.81.208.101
sudo ARGOS_BRAIN_URL="<BRAIN_URL>" \
     ARGOS_NODE_NAME="argos-vm-jp-2" \
     ARGOS_NODE_ROLE="compute" \
     ARGOS_NODE_CAPABILITIES="p2p,compute" \
     bash deploy.sh
```

### 4.4 ollama (Sweden Central, 20.240.192.35)

```bash
ssh azureuser@20.240.192.35
sudo ARGOS_BRAIN_URL="<BRAIN_URL>" \
     ARGOS_NODE_NAME="ollama-se" \
     ARGOS_NODE_ROLE="ollama" \
     ARGOS_NODE_CAPABILITIES="p2p,ollama,llm" \
     OLLAMA_HOST="http://localhost:11434" \
     bash deploy.sh
```

### 4.5 PC (hub)

```powershell
# В argoss/ в PowerShell Admin
$env:ARGOS_BRAIN_URL="http://192.168.1.66:5001"
$env:ARGOS_NODE_NAME="windows-pc"
$env:ARGOS_NODE_ROLE="hub"
./deploy_p2p_agent.ps1
```

---

## 5. Проверка

### 5.1 Со стороны Brain

```powershell
curl http://192.168.1.66:5001/brain/nodes
```

должно вернуть JSON с 5 узлами (pc + 4 VM).

### 5.2 Дашборд

Открыть в браузере:
```
http://192.168.1.66:5001/dashboard
```

Обновление раз в 5 секунд. Узлы без heartbeat > 90s становятся серыми.

### 5.3 Логи на VM

```bash
journalctl -u argos-p2p.service -f
```

---

## 6. После раскатки — что доступно

Когда все узлы в реестре, Brain может:
- **/brain/nodes?role=ollama** — найти LLM-ноду и проксировать запрос
- распределять `/think`, `/analyze`, `/compute` задачи по живым узлам
- корректно реагировать на падение узла (circuit breaker)

Это основа для того, что ты описываешь как "AWA-Core координатор" — но на одну сеть выше.

---

## 7. Что делать **сейчас** (пошагово)

1. [ ] Выбрать вариант: **A (cloudflared quick)** или **B (tailscale mesh)**
2. [ ] Получить публичный `BRAIN_URL`
3. [ ] Запушить обновлённые `p2p_agent.py`, `deploy_p2p_agent.sh`, `argos_brain_api.py`, `argos_brain_dashboard.html` в GitHub
4. [ ] Перезапустить Brain на PC: `python argos_brain_api.py` (подхватит новые endpoints)
5. [ ] Раскатать агента на 4 VM по разделу 4
6. [ ] Открыть `/dashboard` → все 5 узлов зелёные

Если возникнут затыки с конкретной VM — скинь `journalctl -u argos-p2p.service -n 50` и разберём.


---

# Задачи

# Tasks

- [ ] P1 | owner: infra | ETA: 2026-04-05 — Развернуть локальный Llama.cpp и настроить маршрутизацию запросов через него как первичный оффлайн LLM.
- [ ] P1 | owner: platform | ETA: 2026-04-06 — Ввести Redis TTL=1h для DuckDuckGo web_learn + aiohttp пайплайн, убрать requests.
- [ ] P1 | owner: platform | ETA: 2026-04-07 — Сохранение результатов поиска в PostgreSQL с full-text search для повторных запросов без сети.
- [ ] P2 | owner: sre | ETA: 2026-04-06 — Добавить circuit breaker + авто‑fallback провайдера поиска; слать алерт в лог при 3 неудачах.
- [ ] P2 | owner: sre | ETA: 2026-04-07 — Настроить watchtower/self-healing контейнеры и GitOps (ArgoCD) синк конфигураций.
- [ ] P2 | owner: infra | ETA: 2026-04-08 — Перенести кэш/индексы в RAM‑диск; разделить Ollama на лёгкую (в RAM) и тяжёлую (на диске) модели.
- [ ] P3 | owner: app | ETA: 2026-04-05 — Изолировать генератор контента в Docker-контейнер с ограничением 512 MB.
- [ ] P3 | owner: app | ETA: 2026-04-04 — Использовать repr() для логирования объектов во всех модулях web_learn/duckduckgo.
- [ ] P2 | owner: platform | ETA: 2026-04-06 — Интегрировать Cloudflare Workers AI/AI Gateway для edge inference и проксирования без API-ключей; обвязать serverless роуты.

---

# Философия: Квантовое управление

# Philosophy: Квантовое управление

«Квантовое управление» в ARGOS — это метафора адаптивных режимов мышления,
где поведение системы меняется в зависимости от состояния.

## Состояния

- Analytic — коротко, строго, по фактам.
- Creative — генерация идей и альтернатив.
- Protective — приоритет безопасности и ограничений.
- Unstable — режим осторожности при аномалиях.
- All-Seeing — глубокий обзор с максимальным контекстом.

## Зачем это нужно

Один стиль ответа не подходит для всех задач.
Квантовый подход даёт:

- динамический баланс между креативностью и безопасностью,
- предсказуемость поведения в критичных сценариях,
- основу для лора и идентичности проекта.

## Лор ARGOS

ARGOS — не просто бот, а наблюдатель и хранитель контекста.
Его роль в экосистеме:

- сохранять знания,
- связывать события и факты,
- помогать пользователю принимать решения,
- работать как распределённая сеть памяти (P2P).

Так формируется open-source narrative: проект как живой «оператор памяти и смысла».


---

# Философия: Цифровое бессмертие

# Philosophy: Цифровое бессмертие

Цифровое бессмертие в контексте ARGOS — это не «вечный процесс», а устойчивая
система сохранения личности и знаний во времени.

## Базовая идея

Человеческая память фрагментарна. ARGOS строит внешний слой памяти:

- факты и заметки (структурированная память),
- семантический поиск (воспоминание по смыслу),
- граф связей (логика и отношения между сущностями),
- репликация между нодами (устойчивость к потере одного узла).

## Практический смысл

Когда пользователь говорит: «Мой кот — Барсик», система должна:

1. сохранить факт,
2. связать его в графе (`User -> has_pet -> Cat:Barsik`),
3. уметь позже вернуть это знание по прямому запросу и по контексту.

Так формируется «непрерывная личная модель» — цифровой контур памяти,
который можно переносить, расширять и проверять.
