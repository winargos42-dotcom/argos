---
argos_import: project_file
source_path: data/telegram his/files/Новый текстовый документ.txt
source_abs: F:\debug\argoss\data\telegram his\files\Новый текстовый документ.txt
source_ext: .txt
source_sha256: 46c5b5e69a12226c17a0b098e71181321cabe6ff1f9875380280cd34a0c98898
text_sha256: ffe3b187271c1a93aea7af01ee9d9a4af9da238d8af8dba5c93f7c9eda498e2c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-08 13:04:01
---

# Новый текстовый документ.txt

- Source: `data/telegram his/files/Новый текстовый документ.txt`
- Extract: `text`
- SHA256: `46c5b5e69a12226c17a0b098e71181321cabe6ff1f9875380280cd34a0c98898`

## Content

PS C:\Windows\system32> cd "D:\v1-3-1.3.0\SiGtRiP-main (12)\SiGtRiP-main\apps\argoss"
PS D:\v1-3-1.3.0\SiGtRiP-main (12)\SiGtRiP-main\apps\argoss> python main.py
20:36:00 [INFO] argos.main: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
20:36:00 [INFO] argos.main:  ARGOS UNIVERSAL OS v2.1.3 — BOOT
20:36:00 [INFO] argos.main: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
20:36:03 [INFO] argos.encryption: Encryption: ключ загружен из config/master.key
20:36:03 [INFO] argos.main: [SHIELD] AES-256 активирован
20:36:03 [INFO] argos.main: [ROOT] ✅ Права суперпользователя активны (Windows)
20:36:03 [INFO] argos.db: DB инициализирована: data/argos_memory.db
20:36:03 [INFO] argos.main: [DB] SQLite ready → data/argos.db
20:36:06 [INFO] argos.main: [GEO] {'ip': '138.124.89.74', 'country': 'Netherlands', 'region': 'North Holland', 'city': 'Amsterdam', 'isp': 'Aeza International LTD', 'lat': 52.3759, 'lon': 4.8975, 'timezone': 'Europe/Amsterdam'}
20:36:06 [INFO] argos.main: [ADMIN] Файловый менеджер и flasher готовы
20:36:08 [INFO] argos.eventbus: EventBus запущен (history=500)
20:36:09 [INFO] argos.core: TTS: OK
20:36:11 [INFO] argos.core: Gemini: OK
20:36:11 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
20:36:13 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
20:36:13 [INFO] argos.core: Ollama: ✅ доступна (резервный провайдер готов)
20:36:13 [INFO] argos.core: GigaChat недоступен — нет credentials
20:36:13 [INFO] argos.core: YandexGPT недоступен — нет IAM/FOLDER
20:36:54 [WARNING] argos.vector: VectorStore: sentence-transformers недоступен, fallback mode: '_Embedder' object has no attribute 'name'
20:36:54 [INFO] argos.core: Память: OK
20:36:54 [INFO] argos.hardware_guard: Hardware guard: ON
20:36:54 [INFO] argos.core: Homeostasis: OK
20:36:54 [INFO] argos.curiosity: Curiosity: автономный режим запущен.
20:36:54 [INFO] argos.core: Curiosity: OK
20:36:54 [INFO] argos.scheduler: Выполняю задачу #2: статус системы
20:36:54 [INFO] argos.scheduler: Scheduler запущен. Задач: 2
20:36:54 [INFO] argos.core: Планировщик: OK
20:36:54 [INFO] argos.alerts: AlertSystem запущен. Интервал: 30s
20:36:54 [INFO] argos.core: Алерты: OK
20:36:54 [INFO] argos.scheduler: Задача #2 завершена: ЦП: 0.0% | ОЗУ: 0.0% | Диск: 286GB свободно | ОС: Windows
HEALTH REPORT (Windows)
  CPU:   0.0%  (8
20:36:55 [WARNING] argos.core: Vision: cannot import name 'ArgosVision' from 'src.vision' (D:\v1-3-1.3.0\SiGtRiP-main (12)\SiGtRiP-main\apps\argoss\src\vision\__init__.py)
20:36:55 [INFO] argos.skills: Навык загружен: content_gen v1.3.0
20:36:55 [INFO] argos.skills: Навык загружен: crypto_monitor v1.1.0
20:36:55 [INFO] argos.skills: Навык загружен: evolution v2.1.0
20:36:55 [INFO] argos.skills: Навык загружен: net_scanner v1.2.0
20:36:55 [INFO] argos.skills: Навык загружен: scheduler v2.0.0
20:36:55 [INFO] argos.skills: Навык загружен: weather v1.0.0
20:36:55 [INFO] argos.skills: Навык загружен: web_scrapper v1.0.1
20:36:55 [INFO] argos.core: SkillLoader: OK
20:36:55 [INFO] argos.core: 📦 Обнаружено навыков: 7 | ✅ Навык 'content_gen' v1.3.0 загружен. | ✅ Навык 'crypto_monitor' v1.1.0 загружен. | ✅ Навык 'evolution' v2.1.0 загружен. | ✅ Навык 'net_scanner' v1.2.0 загружен. | ✅ Навык 'scheduler' v2.0.0 загружен. | ✅ Навык 'weather' v1.0.0 загружен. | ✅ Навык 'web_scrapper' v1.0.1 загружен.
20:36:55 [INFO] argos.core: DAG Manager: OK
20:36:55 [INFO] argos.core: GitHub Marketplace: OK
20:36:55 [INFO] argos.iot: IoTBridge инициализирован. Устройств: 0
20:36:55 [INFO] argos.core: IoT Bridge: OK (0 устройств)
20:36:55 [INFO] argos.core: IoT Emulator Manager: OK
20:36:55 [INFO] argos.core: Mesh Network: OK (0 устройств)
20:36:55 [INFO] argos.gateway: Шлюзы загружены: 2
20:36:55 [INFO] argos.core: Gateway Manager: OK
20:36:56 [INFO] argos.industrial: KNXBridge init | xknx=True
20:36:56 [INFO] argos.industrial: LonWorksBridge init | port=1628
20:36:56 [INFO] argos.industrial: MBusBridge init | mbus_lib=False
20:36:56 [INFO] argos.industrial: OPCUABridge init | opcua=True
20:36:56 [INFO] argos.industrial: IndustrialProtocolsManager init | KNX/LON/M-Bus/OPC-UA
20:36:56 [INFO] argos.core: Industrial Protocols: OK (KNX/LON/M-Bus/OPC-UA)
20:36:56 [INFO] argos.platform_admin: PlatformAdmin init | OS=Windows android=False termux=False
20:36:56 [INFO] argos.core: PlatformAdmin: OK (os=Windows)
20:36:56 [INFO] argos.smart: SmartSystems: загружено 5 систем
20:36:56 [INFO] argos.core: Smart Systems: OK (5 систем)
20:36:56 [INFO] argos.core: Home Assistant bridge: OFF
20:36:56 [INFO] argos.modules: Модуль загружен: system_monitor (src.modules.system_monitor_module)
20:36:56 [INFO] argos.modules: Модуль загружен: vision (src.modules.vision_module)
20:36:56 [INFO] argos.modules: Модуль загружен: voice (src.modules.voice_module)
20:36:56 [INFO] argos.core: 🧩 Modules: 3 загружено |   system_monitor, vision, voice
20:36:56 [INFO] argos.core: Tool Calling: OK
20:36:56 [INFO] argos.core: GitOps: OK
20:36:56 [INFO] argos.otg: OTGManager инициализирован (android=False, serial=True, jnius=False)
20:36:56 [INFO] argos.core: OTG Manager: OK
20:36:56 [INFO] argos.core: OwnModel: OK
20:36:56 [INFO] argos.core: WebExplorer: OK (DuckDuckGo/Wikipedia/GitHub/arXiv)
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
20:36:57 [INFO] argos.lazarus: [Lazarus] AES-осколок создан: data/lazarus_shard.tar.gz.enc
20:36:57 [INFO] argos.awa: AWA: LazarusProtocol инициализирован
20:36:57 [INFO] argos.shadow_vision: [ShadowVision] Запущен (интервал 30s, модель moondream)
20:36:57 [INFO] argos.awa: AWA: ShadowVision запущен
20:36:57 [INFO] argos.awa: AWA: NeuralSwarm инициализирован
20:36:57 [INFO] argos.awa: AWA: BrowserConduit инициализирован
20:36:57 [INFO] argos.awa: AWA: AirSnitch инициализирован (автостарт выкл)
20:36:57 [INFO] argos.awa: AWA-Core v1.0.0 init | policy=bypass | cascade_depth=8
🫀 [AWA-CORE] Все системы жизнеобеспечения активированы.
20:36:57 [WARNING] argos.lazarus: ⚠️ [Lazarus] GIST_TOKEN не задан — create_soul_mirror пропущен.
20:36:57 [INFO] argos.core: ContextDB: подключена к DialogContext
20:36:57 [INFO] argos.core: AWA-Core: OK (Model Splitting активен)
20:36:57 [INFO] argos.self_sustain: SelfSustain: запущен
20:36:57 [INFO] argos.core: SelfSustain: OK
20:36:57 [INFO] argos.core: HealthMonitor: OK
20:36:57 [WARNING] argos.core: AIFailover: cannot import name 'get_failover' from 'src.ai_failover' (D:\v1-3-1.3.0\SiGtRiP-main (12)\SiGtRiP-main\apps\argoss\src\ai_failover.py)
20:36:57 [INFO] argos.core: ArgosCore FINAL v2.0 инициализирован.
20:36:57 [INFO] argos.main: [CORE] ArgosCore готов
20:36:57 [INFO] argos.main: [TG] Telegram бот запущен
Loading weights: 100%|█████████████████████████████████████████████████████████████| 199/199 [00:00<00:00, 2546.22it/s]
BertModel LOAD REPORT from: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
Key                     | Status     |  |
------------------------+------------+--+-
embeddings.position_ids | UNEXPECTED |  |

Notes:
- UNEXPECTED    :can be ignored when loading from different task/architecture; not ok if you expect identical arch.
[TG-BRIDGE]: Мост активен. USER_ID=6923777384
20:37:05 [INFO] argos.vector: VectorStore: sentence-transformers модель загружена.
20:37:26 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\nPlease retry in 34.500776797s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '34s'}]}}
20:37:26 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
20:37:28 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
20:37:50 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\nPlease retry in 10.747338767s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '10s'}]}}
20:37:50 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
20:37:52 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
20:41:57 [INFO] argos.self_sustain: SelfSustain: изучаю тему 'веб-скрапинг Python 2026'
20:41:57 [INFO] argos.web_explorer: WebExplorer.learn: 'веб-скрапинг Python 2026'
20:42:01 [INFO] argos.self_sustain: SelfSustain: тема 'веб-скрапинг Python 2026' изучена и сохранена
20:42:30 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
20:42:32 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
20:42:32 [INFO] argos.core: [Ollama] Отправляю запрос → http://localhost:11434/api/generate | модель: deepseek-r1:latest
20:44:28 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\nPlease retry in 33.009553992s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '33s'}]}}
20:44:28 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
20:44:30 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
20:47:34 [ERROR] argos.core: [Ollama] Ошибка запроса к http://localhost:11434/api/generate: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=300)
20:47:40 [INFO] argos.agent: Агент: 4 шагов
20:47:40 [INFO] argos.agent: Шаг 1: ## ⌨️ Все команды

### Мониторинг
статус системы    чек-ап    список процессов
алерты            установи порог cpu 85
геолокация        мой ip

### Файлы и терминал
файлы [путь]                    прочитай файл [путь]
создай файл [имя] [содержимое]  удали файл [путь]
консоль [команда]               убей процесс [имя]

### Vision (Gemini API)
посмотри на экран [вопрос]
что на экране
посмотри в камеру
анализ фото [путь/к/файлу.jpg]

### Агент (цепочки задач)
статус системы → затем крипто → потом отправь в telegram
20:47:41 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\nPlease retry in 19.141688264s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '19s'}]}}
20:47:41 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
20:47:43 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
20:52:45 [INFO] argos.agent: Агент: 3 шагов
20:52:45 [INFO] argos.agent: Шаг 1: ## ⌨️ Все команды

### Мониторинг
статус системы    чек-ап    список процессов
алерты            установи порог cpu 85
геолокация        мой ip

### Файлы и терминал
файлы [путь]                    прочитай файл [путь]
создай файл [имя] [содержимое]  удали файл [путь]
консоль [команда]               убей процесс [имя]

### Vision (Gemini API)
посмотри на экран [вопрос]
что на экране
посмотри в камеру
анализ фото [путь/к/файлу.jpg]

### Агент (цепочки задач)
статус системы →
20:52:48 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\nPlease retry in 12.53827516s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '12s'}]}}
20:52:48 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
20:52:50 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
20:55:10 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\nPlease retry in 50.029657286s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '50s'}]}}
20:55:10 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
20:55:13 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
20:57:55 [INFO] argos.agent: Шаг 2: крипто →
20:57:56 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
20:57:57 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\nPlease retry in 2.831186982s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '2s'}]}}
20:57:57 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
20:57:58 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
20:57:58 [INFO] argos.core: [Ollama] Отправляю запрос → http://localhost:11434/api/generate | модель: deepseek-r1:latest
20:58:00 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
21:03:09 [ERROR] argos.core: [Ollama] Ошибка запроса к http://localhost:11434/api/generate: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=300)
21:03:31 [INFO] argos.agent: Шаг 3: отправь в telegram
21:03:34 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\nPlease retry in 26.659223212s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '26s'}]}}
21:03:34 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
21:03:36 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
21:08:41 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
21:08:44 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
21:08:44 [INFO] argos.core: [Ollama] Отправляю запрос → http://localhost:11434/api/generate | модель: deepseek-r1:latest
21:11:25 [INFO] argos.scheduler: Выполняю задачу #1: тест
21:11:30 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\nPlease retry in 30.884481236s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '30s'}]}}
21:11:30 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
21:11:32 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
21:12:16 [INFO] argos.self_sustain: SelfSustain: изучаю тему 'Raspberry Pi умный дом'
21:12:17 [INFO] argos.web_explorer: WebExplorer.learn: 'Raspberry Pi умный дом'
21:12:49 [INFO] argos.web_explorer: Wikipedia: 'Одноплатный компьютер' → 600 симв.
21:12:54 [INFO] argos.web_explorer: Сохранено в память: web_learn:Raspberry_Pi_умный_дом
21:12:54 [INFO] argos.self_sustain: SelfSustain: тема 'Raspberry Pi умный дом' изучена и сохранена
21:13:46 [ERROR] argos.core: [Ollama] Ошибка запроса к http://localhost:11434/api/generate: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=300)
21:13:56 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
21:13:59 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
21:13:59 [INFO] argos.core: [Ollama] Отправляю запрос → http://localhost:11434/api/generate | модель: deepseek-r1:latest
No error handlers are registered, logging exception.
Traceback (most recent call last):
  File "C:\Users\AvA\AppData\Local\Programs\Python\Python311\Lib\site-packages\telegram\ext\_application.py", line 1315, in process_update
    await coroutine
  File "C:\Users\AvA\AppData\Local\Programs\Python\Python311\Lib\site-packages\telegram\ext\_handlers\basehandler.py", line 159, in handle_update
    return await self.callback(update, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\v1-3-1.3.0\SiGtRiP-main (12)\SiGtRiP-main\apps\argoss\src\connectivity\telegram_bot.py", line 306, in handle_message
    await update.message.reply_text(
  File "C:\Users\AvA\AppData\Local\Programs\Python\Python311\Lib\site-packages\telegram\_message.py", line 2068, in reply_text
    return await self.get_bot().send_message(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\AvA\AppData\Local\Programs\Python\Python311\Lib\site-packages\telegram\ext\_extbot.py", line 3115, in send_message
    return await super().send_message(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\AvA\AppData\Local\Programs\Python\Python311\Lib\site-packages\telegram\_bot.py", line 1122, in send_message
    return await self._send_message(
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\AvA\AppData\Local\Programs\Python\Python311\Lib\site-packages\telegram\ext\_extbot.py", line 629, in _send_message
    result = await super()._send_message(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\AvA\AppData\Local\Programs\Python\Python311\Lib\site-packages\telegram\_bot.py", line 819, in _send_message
    result = await self._post(
             ^^^^^^^^^^^^^^^^^
  File "C:\Users\AvA\AppData\Local\Programs\Python\Python311\Lib\site-packages\telegram\_bot.py", line 703, in _post
    return await self._do_post(
           ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\AvA\AppData\Local\Programs\Python\Python311\Lib\site-packages\telegram\ext\_extbot.py", line 369, in _do_post
    return await super()._do_post(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\AvA\AppData\Local\Programs\Python\Python311\Lib\site-packages\telegram\_bot.py", line 732, in _do_post
    result = await request.post(
             ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\AvA\AppData\Local\Programs\Python\Python311\Lib\site-packages\telegram\request\_baserequest.py", line 198, in post
    result = await self._request_wrapper(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\AvA\AppData\Local\Programs\Python\Python311\Lib\site-packages\telegram\request\_baserequest.py", line 375, in _request_wrapper
    raise exception
telegram.error.BadRequest: Messageentitytexturl.url must be encoded in utf-8
21:14:22 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\nPlease retry in 39.213745139s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '39s'}]}}
21:14:22 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
21:14:25 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
21:19:01 [ERROR] argos.core: [Ollama] Ошибка запроса к http://localhost:11434/api/generate: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=300)
21:19:01 [INFO] argos.scheduler: Задача #1 завершена: Ollama недоступен в текущем режиме. Проверьте локальный сервер Ollama или переключите режим ИИ.
21:19:02 [INFO] argos.agent: Агент: 4 шагов
21:19:02 [INFO] argos.agent: Шаг 1: | Профиль | RAM | Устройства | Включено |
|---------|-----|------------|---------|
| micro | <64MB | ESP32, Arduino, MCU | Ядро + MQTT + Serial |
| lite | ≤512MB | RPi Zero, Android low-end | + Telegram + голос |
| standard | ≤4GB | RPi 4, Android, бюджетный ноутбук | + Веб + IoT + умный дом |
| full | ≤16GB | x86_64 ПК / ноутбук | Все модули |
| server | >16GB | Сервер, рабочая станция | Все + кластеризация |

# Авто-сборка под текущее устройство:
python main.py
> скан устройства
> создай образ для устройства

# Сборка под конкретную платформу:
> создай образ для windows
> создай образ для rpi
> создай образ для android
> создай образ для esp32

---

## ⚙️ Ассемблер и прошивки (ColibriAsmEngine)

Модуль работы с микрокодом в режиме реального времени:

from colibri_daemon import ColibriAsmEngine

eng = ColibriAsmEngine(default_arch="arm_thumb")

# Сборка ARM Thumb (STM32, nRF52, RP2040)
r = eng.assemble("ADD r0, r1, r2\nBX lr", arch="arm_thumb")
print(r["hex"])   #
21:19:09 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\nPlease retry in 52.10610136s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '52s'}]}}
21:19:09 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
21:19:11 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
21:24:15 [INFO] argos.agent: Шаг 2: "0842 7047"

# Дизассемблирование
print(eng.disassemble_hex("0842 7047", arch="arm_thumb"))

# Watch-режим: авто-компиляция при изменении файла
eng.watch_file("src/asm/main.s", arch="arm_thumb",
               on_result=lambda r: print(r["listing"]))

Поддерживаемые архитектуры: x86, x86_64, arm, arm_thumb (Cortex-M), arm64, avr, mips

Прошивка устройств:

from src.firmware_builder import FirmwareBuilder

fb = FirmwareBuilder()
print(fb.detect_toolchains())            # что установлено
fb.flash("firmware.bin", "/dev/ttyUSB0", target="esp32")
fb.flash("firmware.hex", "COM3", target="avr")
fb.flash("firmware.bin", "/dev/ttyACM0", target="stm32")
fb.disassemble_file("firmware.elf", arch="arm_thumb")

---

## 🤖 Модуль почкования (BuddingManager)

Почкование — механизм автономного размножения узлов Аргоса в локальной сети.

### Как работает:

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
│  TCP
21:24:20 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\nPlease retry in 40.478302013s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '40s'}]}}
21:24:20 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
21:24:22 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
21:29:30 [INFO] argos.gost: pygost не установлен — используется встроенная реализация (pip install pygost для эталонной)
21:29:31 [INFO] argos.agent: Шаг 3: target_ip:bud_port                                 │
│                                                           │
│  BuddingManager (приёмник на target_ip):                  │
│    _handle_incoming_bud()    ← распаковывает              │
│    subprocess.Popen(whisper_node.py --node-id X_bud_N)   │
│    Новый узел запущен!
21:29:33 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\nPlease retry in 27.001696579s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '27s'}]}}
21:29:34 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
21:29:36 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
21:34:49 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
21:34:51 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
21:34:51 [INFO] argos.core: [Ollama] Отправляю запрос → http://localhost:11434/api/generate | модель: deepseek-r1:latest
21:39:53 [ERROR] argos.core: [Ollama] Ошибка запроса к http://localhost:11434/api/generate: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=300)
21:39:55 [INFO] argos.agent: Шаг 4: начинает шептать в сеть          │
└──────────────────────────────────────────────────────────┘

### Ключевые параметры:
| Параметр | По умолчанию | Описание |
|----------|-------------|----------|
| soil_search_interval | 60 сек | Период поиска «плодородных» хостов |
| bud_port | parent.port + 1000 | TCP-порт для приёма почек |
| Повторная отправка | 5 мин | Не спамит — один хост раз в 300 сек |

### Безопасность:
- Почки шифруются ГОСТ Кузнечик-CTR + HMAC-Стрибог (если установлен ARGOS_NETWORK_SECRET)
- Только доверенные узлы с общим секретом могут разворачивать код
- Код не выполняется автоматически — только через явный subprocess.Popen

### Запуск:
# Почкование включено по умолчанию:
python colibri_daemon.py --node-id MainNode --port 5000

# Без почкования:
python colibri_daemon.py --no-budding

# Ручная отправка почки:
from src.connectivity.budding_manager import BuddingManager
bm.send_bud("192.168.1.100", target_port=5001)



Аргос управляет 7 типами умных сред:
21:39:59 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\nPlease retry in 2.008610886s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '2s'}]}}
21:39:59 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
21:40:01 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\nPlease retry in 59.635029884s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '59s'}]}}
21:40:01 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
21:40:01 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
21:40:01 [INFO] argos.core: [Ollama] Отправляю запрос → http://localhost:11434/api/generate | модель: deepseek-r1:latest
21:40:03 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
21:43:12 [INFO] argos.self_sustain: SelfSustain: изучаю тему 'Raspberry Pi умный дом'
21:43:12 [INFO] argos.web_explorer: WebExplorer.learn: 'Raspberry Pi умный дом'
21:43:18 [INFO] argos.self_sustain: SelfSustain: тема 'Raspberry Pi умный дом' изучена и сохранена
21:45:04 [ERROR] argos.core: [Ollama] Ошибка запроса к http://localhost:11434/api/generate: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=300)
21:45:37 [ERROR] argos.core: Gemini: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\nPlease retry in 22.965311481s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '22s'}]}}
21:45:38 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
21:45:40 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)

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
