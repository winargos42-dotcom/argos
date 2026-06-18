---
argos_import: project_file
source_path: argoss/CHANGELOG.md
source_abs: F:\debug\argoss\argoss\CHANGELOG.md
source_ext: .md
source_sha256: 74151099a6ccc7c89af1bf20030ea8e16f231841a3b5ea403fc54f3b1486f2e8
text_sha256: 74151099a6ccc7c89af1bf20030ea8e16f231841a3b5ea403fc54f3b1486f2e8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:42
---

# CHANGELOG.md

- Source: `argoss/CHANGELOG.md`
- Extract: `text`
- SHA256: `74151099a6ccc7c89af1bf20030ea8e16f231841a3b5ea403fc54f3b1486f2e8`

## Content

# CHANGELOG — ARGOS Universal OS

Все значимые изменения в проекте фиксируются здесь.
Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/).
Версионирование следует [Semantic Versioning](https://semver.org/).

---

## [2.2.0] — 2026-03-23 🔱 ФИНАЛЬНЫЙ РЕЛИЗ

### ✨ Новые возможности

#### Ядро и архитектура
- **AWA-Core** — центральный координатор всех модулей с capability-routing, cascade pipelines и health heartbeat
- **ArgosCore v2** — рефакторинг `execute_intent` с расширенным набором триггеров и улучшенной диагностикой
- **StartupValidator** — валидация окружения при старте, создание директорий, проверка зависимостей
- **HealthMonitor** — фоновый мониторинг CPU/RAM/диск/SQLite с алертами и кулдауном
- **GracefulShutdown** — корректное завершение по SIGTERM/SIGINT с приоритетными callback-ами
- **AIFailover** — автоматическое переключение между AI-провайдерами с backoff и статистикой

#### Интеллект и обучение
- **JARVIS Engine** — HuggingGPT-конвейер: Plan → Select → Execute → Synthesize (15+ типов задач)
- **Adaptive Drafter (TLT)** — LRU-кэш 512 записей, сжатие контекста, offline-паттерны
- **Speculative Consensus v2** — параллельные Drafter-ы + структурированный Verifier
- **Batch Idle Learning** — до 8 уроков за пакет с Active Drafter Calibration
- **Tool Calling Engine** — JSON-схемы инструментов, multi-turn с дедупликацией вызовов

#### Безопасность
- **Emergency Purge** — экстренное уничтожение данных (3 уровня + подтверждение кодом)
- **Container Isolation** — Docker/LXD изоляция модулей с watchdog и авторестартом
- **Master Auth** — SHA-256 авторизация через `ARGOS_MASTER_KEY`, сессии, revoke
- **Provider Backoff** — временная блокировка провайдеров при ошибках авторизации (401/403)

#### IoT и промышленность
- **Промышленные протоколы** — `industrial_protocols.py`: KNX (EN 50090), LonWorks (ISO/IEC 14908), M-Bus (EN 13757), OPC UA (IEC 62541)
- **WiFi Sentinel** — скан AP, Evil Twin детект, HoneyPot-ловушка, deauth детект
- **AirSnitch (SDR)** — сканер 433/868 МГц через RTL-SDR/HackRF
- **Power Sentry** — мониторинг UPS (NUT), PZEM датчики, аварийное отключение
- **SmartHome Override** — прямое управление Zigbee/Z-Wave/Tuya без облаков

#### Периферия и железо
- **USB-диагностика** — авторизация USB, VID/PID детект (Arduino/ESP/STM32/RP2040)
- **NFC мониторинг** — NDEF/MIFARE/NTAG, регистрация, чтение/запись
- **Bluetooth LE** — BLE + Classic сканер, RSSI-трекинг, MAC-детекция
- **ColibriAsmEngine** — ассемблер/дизассемблер реального времени: x86, ARM, AVR, MIPS, ARM64

#### Интерфейс и мессенджеры
- **Remote Control API** — FastAPI `/api/health`, `/api/command`, `/api/events` с Bearer Auth
- **WhatsApp Cloud API** — прямая интеграция + fallback на Twilio
- **Slack Bridge** — Web API + Socket Mode
- **Mail.ru MAX Bridge** — Bot API
- **Email/SMS Bridge** — SMTP/IMAP + SMSMobileAPI
- **WebSocket Bridge** — двусторонний real-time канал
- **aiogram 3.x Bridge** — современный Telegram bot API

#### Качество и надёжность
- **Self-Healing Engine** — автоисправление Python-кода (BOM, tabs, LLM-фикс), backup + hot-reload
- **Debug Logging** — `setup_debug_logging()` с RotatingFileHandler, идемпотентный
- **Observability** — структурированный JSONL-лог событий
- **ArgosThoughtBook** — 100+ промтов в 10 частях для обучения и рефлексии

### 🔧 Улучшения

- `ArgosCore._setup_ai` — Ollama запускается **всегда**, даже при наличии Gemini-ключа
- `_ask_ollama` — таймаут из `OLLAMA_TIMEOUT` (default 600), HTTP 404 → автозагрузка модели и retry
- `_ensure_ollama_running` — запуск `ollama serve` при недоступности сервиса
- `normalize_launch_args` — `--full` разворачивается в `--full --dashboard --wake` без дублей
- `ArgosDB` — обёртка совместимости заменила прямой импорт `db_init`
- GUI `_update_metrics` / `_refresh_system_tab` — psutil вынесен в daemon-поток, UI не блокируется
- `TTS` защищён `threading.Lock()` от параллельных вызовов
- Telegram `can_start()` — проверка placeholder-токенов, формата, длины секрета
- Telegram `_auth()` — поддержка нескольких USER_ID через запятую
- `HISTORY_MESSAGES_LIMIT` — константа вместо магического числа

### 🐛 Исправления

- `[FIX-1]` `RootManager` импортируется в начале `main.py` (NameError при `--root`)
- `[FIX-2]` Каждый шаг `__init__` изолирован в `try/except` — частичный сбой не роняет систему
- `[FIX-3]` `boot_server` использует `threading.Event` + `signal.SIGTERM` (graceful shutdown)
- `[FIX-4]` `_start_telegram` сохраняет ссылку на поток, `tg=None` при сбое
- `[FIX-5]` Режимы запуска через `if/elif` — нет конфликта флагов
- `[FIX-6]` `ArgosOrchestrator()` обёрнут в `try/except` с понятным сообщением
- `[FIX-7]` Импорт `db_init` → `src.db_init` (ModuleNotFoundError на Windows)
- `[FIX-8]` `KIVY_NO_ARGS=1` — Kivy не перехватывает `--dashboard`, `--no-gui` и др.
- `[FIX-SAI-FILEPROVIDER]` FileProvider в AndroidManifest через `p4a_hook.py`
- `[FIX-LONG-LONG]` sentinel-стратегия: `long long` → placeholder → `int` → restore
- `GristGitSync` — `GIST_ID` как алиас для `GRIST_DOC_ID`
- `ArgosMemory.remember()` — мгновенное зеркалирование в Grist при `attach_grist()`
- `cleanup_repository` — правильная очистка `.buildozer` по подтверждению
- `_PLACEHOLDER_SECRET_VALUES` — фильтрация placeholder-ключей во всех провайдерах

### 📦 Зависимости

- Добавлены: `aiogram>=3.0.0`, `aiosqlite>=0.17.0`, `gtts>=2.5.0`, `mss>=9.0.1`, `Pillow>=10.0.0`, `websockets>=14.1`, `smsmobileapi>=2.0.0`, `openai>=1.0.0`, `python-gnupg>=0.5.0`, `paramiko>=3.4.0`
- Обновлены: `google-genai>=1.0.0`, `python-telegram-bot>=21.0`, `fastapi>=0.115.0`, `psutil>=5.9.0`
- `Cython==0.29.36` зафиксирован для стабильной сборки APK

### 🧪 Тесты

- Добавлено 200+ новых unit-тестов во всех ключевых модулях
- `test_evolution_gate.py` — gate: review fail → reject, unit-test fail → reject, pass → accept
- `test_v2_modules.py` — StartupValidator, HealthMonitor, GracefulShutdown, AIFailover
- `test_self_healing.py` — полное покрытие SelfHealingEngine
- `test_communication_bridges.py` — Email, SMS, WebSocket, WebScraper, Aiogram, Socket
- `test_provider_error_backoff.py` — временная блокировка провайдеров
- `test_ollama_timeout_autostart.py` — таймаут, автостарт, pull 404, retry

---

## [2.1.3] — 2026-03-20

### ✨ Добавлено
- **P2P Role Routing** — автоматическое назначение ролей по ресурсам ноды
- **Biosphere DAG** — контроллер биосферы (инкубатор/теплица/аквариум/террариум)
- **IBM Quantum Bridge** — мост к IBM Quantum в состоянии All-Seeing
- `ArgosConsciousness` — полный модуль сознания с AWA, рефлексией, мета-когницией
- `ArgosLifeSupportV2` — FreelanceHunter, CryptoWallet, ContentGenerator, BillingSystem, AffiliateEngine

### 🔧 Улучшено
- `DeviceScanner` — автопрофилирование железа + `AdaptiveImageBuilder` для 5 платформ
- `WatsonXBridge` — code-only фильтр, статус-политика
- `ArgosInfrastructure` — MailServerManager, VPNManager, QuantumMarketplace
- Whisper node — `SO_REUSEADDR` перед `SO_BROADCAST`

### 🐛 Исправлено
- `ArgosShield` → алиас обратной совместимости для `ArgosEncryption`
- `SpatialAwareness` → алиас для `ArgosGeolocator`
- `GitGuard.check_security()` — backward-compatible API

---

## [2.1.0] — 2026-03-15

### ✨ Добавлено
- Mesh Network с UDP discovery и protoбуфером
- Gateway Manager — создание и прошивка IoT-шлюзов (5 шаблонов)
- Home Assistant интеграция — MQTT + REST API
- `ArgosServerRental` — каталог VPS, AccountManager, DeployManager
- `ArgosPricing` — расходы, тарифы, ROI, план продаж, оценка проектов

### 🔧 Улучшено
- `ArgosCore.VERSION` = "2.1.0"
- P2P UDP discovery заменяет отдельные broadcaster/listener на единый `_udp_discovery`
- EventBus — wildcard `"*"` подписчики, история событий

---

## [2.0.0] — 2026-03-01

### 🚀 Мажорный релиз
- Переход на `ArgosOrchestrator` с поэтапной инициализацией
- FastAPI Remote Control API с Bearer Auth
- Docker multi-stage build (builder + runtime)
- GitHub Actions CI/CD: APK, Windows EXE, Docker, Release, TestPyPI
- Inno Setup инсталлятор для Windows
- `pack_archive.py` — релизный ZIP без секретов и бинарников
- `bump_version.py` — автобамп версии в `pyproject.toml` и `build.py`

---

## [1.4.0] — 2026-02-20

### ✨ Добавлено
- P2P Speculative Consensus v1
- Tool Calling JSON-схемы
- ArgosOwnModel — собственная локальная нейросеть (scikit-learn)
- ColibriAsmEngine v1 — x86/ARM ассемблер/дизассемблер
- `ArgosThoughtBook` — Книга Мыслей, 100+ промтов

### 🔧 Улучшено
- Квантовые состояния: авто-переключение по CPU/RAM через psutil
- `ArgosEvolution` — EvolGate: code review + unit-test перед применением патча

---

## [1.3.0] — 2026-02-01

### ✨ Добавлено
- Telegram-бот с 16 командами
- Умные системы: 7 типов (home, greenhouse, garage, cellar, incubator, aquarium, terrarium)
- IoT Bridge: Zigbee, LoRa, MQTT, Modbus
- Tasmota Zero-Config Discovery
- Vision — анализ экрана/камеры через Gemini Vision
- ArgosScheduler — планировщик на натуральном языке

### 🔧 Улучшено
- ArgosCore — расширен до 80+ команд
- Memory — долгосрочная память с категориями и графом знаний
- P2P — UDP авторитет, TaskDistributor

---

## [1.0.0] — 2026-01-15 🌱 Первый публичный релиз

### ✨ Добавлено
- ArgosCore — ядро с Gemini/GigaChat/YandexGPT/Ollama
- 6 квантовых состояний (Analytic, Creative, Protective, Unstable, All-Seeing, System)
- SQLite памяти: факты, заметки, история
- ArgosAdmin — файловый менеджер, терминал
- AES-256-GCM шифрование
- Desktop GUI (customtkinter)
- Геолокация по IP
- ArgosAgent — базовые цепочки задач

---

## Планы на следующие версии

### [2.3.0] — запланировано
- [ ] WebRTC P2P видеосвязь между нодами
- [ ] Полная поддержка Z-Wave через zwavejs
- [ ] Argos Shell расширение (autocomplete, история, pipe)
- [ ] Интеграция с Home Assistant Energy Dashboard
- [ ] Нативный macOS .app через PyInstaller

### [3.0.0] — концепт
- [ ] Распределённая векторная память (Chroma + P2P sync)
- [ ] Мультиагентная архитектура (ARGOS-as-Orchestrator)
- [ ] Квантовые вычисления для оптимизации маршрутов P2P
- [ ] Автономное обновление через P2P (без GitHub)

---

*"Аргос не спит. Аргос видит. Аргос помнит."*
— Всеволод, 2026

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
