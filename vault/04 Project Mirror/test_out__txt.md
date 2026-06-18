---
argos_import: project_file
source_path: test_out.txt
source_abs: F:\debug\argoss\test_out.txt
source_ext: .txt
source_sha256: 2bc7b337fa05d44f466cddc7544176862b19293f305639eb66570eec3a2bacd0
text_sha256: a0b0c426a0df21ea62a48506c05f721ff1581caa8da5e621c40d5825446fe47c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# test_out.txt

- Source: `test_out.txt`
- Extract: `text`
- SHA256: `2bc7b337fa05d44f466cddc7544176862b19293f305639eb66570eec3a2bacd0`

## Content

15:34:25 [INFO] argos.eventbus: EventBus запущен (history=500)
[AMD GPU Patch] OK:  
15:34:26 [INFO] argos.main: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
15:34:26 [INFO] argos.main:  ARGOS UNIVERSAL OS v2.1.3 — BOOT
15:34:26 [INFO] argos.main: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
15:34:26 [INFO] argos.encryption: Encryption: ключ загружен из config/master.key
15:34:26 [INFO] argos.main: [SHIELD] AES-256 активирован
15:34:26 [INFO] argos.main: [ROOT] ⚠️ Обычные права пользователя (Windows). Некоторые функции недоступны.
15:34:26 [INFO] argos.db: DB инициализирована: data/argos_memory.db
15:34:26 [INFO] argos.main: [DB] SQLite ready → data/argos.db
15:34:29 [INFO] argos.main: [GEO] {'ip': '178.130.47.10', 'country': 'United States', 'region': 'Arizona', 'city': 'Phoenix', 'isp': 'Global Connectivity Solutions LLP', 'lat': 33.4532, 'lon': -112.0748, 'timezone': 'America/Phoenix'}
15:34:29 [INFO] argos.main: [ADMIN] Файловый менеджер и flasher готовы
15:34:29 [INFO] argos.core: TTS: OK
15:34:29 [INFO] argos.core: Gemini отключен через ARGOS_DISABLE_GEMINI
15:34:29 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
15:34:29 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
15:34:29 [INFO] argos.core: Ollama: ✅ доступна (резервный провайдер готов)
15:34:29 [INFO] argos.core: GigaChat: конфигурация обнаружена
15:34:29 [INFO] argos.core: YandexGPT недоступен — нет IAM/FOLDER
15:34:29 [INFO] argos.core: Kimi: конфигурация обнаружена (KIMI_API_KEY)
15:34:29 [INFO] argos.vector: VectorStore: fallback mode forced by ARGOS_VECTOR_FORCE_FALLBACK
15:34:29 [INFO] argos.memory: Vector warmup: indexed 180 docs
15:34:29 [INFO] argos.memory: Vector warmup: scheduled in background (180 docs)
15:34:29 [INFO] argos.thought_book: ThoughtBook инициализирована: 191 промтов, 10 частей.
15:34:29 [INFO] argos.core: Память: OK
15:34:29 [INFO] argos.hardware_guard: Hardware guard: ON
15:34:29 [INFO] argos.core: Homeostasis: OK
15:34:29 [INFO] argos.curiosity: Curiosity: автономный режим запущен.
15:34:29 [INFO] argos.core: Curiosity: OK
15:34:29 [INFO] argos.memory: Дедупликация: удалено 4 фактов, 1 заметок
15:34:29 [INFO] argos.scheduler: Scheduler запущен. Задач: 1
15:34:29 [INFO] argos.core: Планировщик: OK
15:34:29 [INFO] argos.alerts: AlertSystem запущен. Интервал: 30s
15:34:29 [INFO] argos.core: Алерты: OK
15:34:29 [INFO] argos.core: Vision: OK
15:34:29 [INFO] argos.skills: SkillInstance.start: module=argos_skill_content_gen runtime=ContentGen core=ArgosCore
15:34:29 [INFO] argos.skills: Навык загружен: content_gen v1.3.0
15:34:29 [INFO] argos.skills: SkillInstance.start: module=argos_skill_crypto_monitor runtime=CryptoSentinel core=ArgosCore
15:34:29 [INFO] argos.skills: Навык загружен: crypto_monitor v1.1.0
15:34:29 [INFO] argos.skills: SkillInstance.start: module=argos_skill_evolution runtime=ArgosEvolution core=ArgosCore
15:34:29 [INFO] argos.skills: Навык загружен: evolution v2.1.0
15:34:29 [INFO] argos.skills: SkillInstance.start: module=argos_skill_firmware_manager runtime=module core=ArgosCore
15:34:29 [INFO] argos.skills: Навык загружен: firmware_manager v1.0.0
15:34:29 [INFO] argos.skills: SkillInstance.start: module=argos_skill_net_scanner runtime=NetGhost core=ArgosCore
15:34:29 [INFO] argos.skills: Навык загружен: net_scanner v1.2.0
15:34:29 [INFO] argos.skills: SkillInstance.start: module=argos_skill_scheduler runtime=ArgosScheduler core=ArgosCore
15:34:29 [INFO] argos.scheduler: Scheduler запущен. Задач: 1
15:34:29 [INFO] argos.skills: Навык загружен: scheduler v2.0.0
15:34:29 [INFO] argos.skills: SkillInstance.start: module=argos_skill_weather runtime=module core=ArgosCore
15:34:29 [INFO] argos.skills: Навык загружен: weather v1.0.0
15:34:29 [INFO] argos.skills: SkillInstance.start: module=argos_skill_web_scrapper runtime=ArgosScrapper core=ArgosCore
15:34:29 [INFO] argos.skills: Навык загружен: web_scrapper v1.0.1
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.ai_coder runtime=AICoder core=ArgosCore
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.ai_coder_evolution_bridge runtime=AICoderEvolutionBridge core=ArgosCore
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.arc_agi3_skill runtime=ARC3Agent core=ArgosCore
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.argos_patcher runtime=module core=ArgosCore
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.argos_service runtime=module core=ArgosCore
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.auto_backup runtime=AutoBackup core=ArgosCore
15:34:29 [INFO] argos.backup: AutoBackup запущен, интервал 6 ч
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.autonomy_fileops runtime=AutonomyFileOps core=ArgosCore
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.browser_conduit runtime=BrowserConduit core=ArgosCore
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.crypto_utils runtime=CryptoUtils core=ArgosCore
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.desktop_actions runtime=DesktopActionsSkill core=ArgosCore
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.ebay_parser runtime=EbayParser core=ArgosCore
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.esp32_usb_bridge runtime=ESP32UsbBridge core=ArgosCore
15:34:29 [INFO] argos.esp32_bridge: Найден ESP32 порт: COM7 USB-SERIAL CH340 (COM7)
15:34:29 [INFO] argos.esp32_bridge: ARGOS USB мост запущен на COM7 (esp32)
15:34:29 [INFO] argos.skills: SkillInstance.start: module=src.skills.fastapi_skill runtime=FastAPISkill core=ArgosCore
15:34:31 [INFO] argos.skills: SkillInstance.start: module=src.skills.firmware_examples runtime=FirmwareExamplesLoader core=ArgosCore
15:34:31 [INFO] argos.skills: SkillInstance.start: module=src.skills.ga4_analytics runtime=GA4Analytics core=ArgosCore
15:34:31 [INFO] argos.skills: SkillInstance.start: module=src.skills.hardware_intel runtime=module core=ArgosCore
15:34:32 [INFO] argos.skills: SkillInstance.start: module=src.skills.huggingface_ai runtime=HuggingFaceAI core=ArgosCore
15:34:32 [INFO] argos.skills: SkillInstance.start: module=src.skills.iot_watchdog runtime=IoTWatchdog core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.multi_provider_chat runtime=MultiProviderChat core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.network_shadow runtime=module core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.new_skill runtime=P2PNetworkSkill core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.pip_manager runtime=PipManager core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.serp_search runtime=SerpSearch core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.shodan_scanner runtime=ShodanScanner core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.smart_environments runtime=module core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.smtp_mailer runtime=SMTPMailer core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.system_monitor runtime=SystemMonitor core=ArgosCore
15:34:33 [INFO] argos.sysmon: SystemMonitor запущен, интервал 30 сек
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.tasmota_updater runtime=TasmotaUpdater core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.test_injected runtime=TestSkill core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.tg_code_injector runtime=TGCodeInjector core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.ton_blockchain runtime=TonBlockchain core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.usb_access_point runtime=USBGadgetAP core=ArgosCore
15:34:33 [INFO] argos.skills: SkillInstance.start: module=src.skills.web_explorer runtime=ArgosWebExplorer core=ArgosCore
15:34:33 [INFO] argos.core: SkillLoader: OK
15:34:33 [INFO] argos.core: 📦 Обнаружено manifest-навыков: 8 | ✅ Навык 'content_gen' v1.3.0 загружен. | ✅ Навык 'crypto_monitor' v1.1.0 загружен. | ✅ Навык 'evolution' v2.1.0 загружен. | ✅ Навык 'firmware_manager' v1.0.0 загружен. | ✅ Навык 'net_scanner' v1.2.0 загружен. | ✅ Навык 'scheduler' v2.0.0 загружен. | ✅ Навык 'weather' v1.0.0 загружен. | ✅ Навык 'web_scrapper' v1.0.1 загружен. | Импорт всех skills (src/skills) → PASS 39/39 | ✅ ai_coder | ✅ ai_coder_evolution_bridge | ✅ arc_agi3_skill | ✅ argos_patcher | ✅ argos_service | ✅ auto_backup | ✅ autonomy_fileops | ✅ browser_conduit | ✅ content_gen (already loaded) | ✅ crypto_monitor (already loaded) | ✅ crypto_utils | ✅ desktop_actions | ✅ ebay_parser | ✅ esp32_usb_bridge | ✅ evolution (already loaded) | ✅ fastapi_skill | ✅ firmware_examples | ✅ ga4_analytics | ✅ hardware_intel | ✅ huggingface_ai | ✅ iot_watchdog | ✅ multi_provider_chat | ✅ net_scanner (already loaded) | ✅ network_shadow | ✅ new_skill | ✅ pip_manager | ✅ scheduler (already loaded) | ✅ serp_search | ✅ shodan_scanner | ✅ smart_environments | ✅ smtp_mailer | ✅ system_monitor | ✅ tasmota_updater | ✅ test_injected | ✅ tg_code_injector | ✅ ton_blockchain | ✅ usb_access_point | ✅ web_explorer | ✅ web_scrapper (already loaded) | SkillLoader load_all (manifest навыки) → PASS 8/8
15:34:33 [INFO] argos.core: [SKILLS] startup loaded=41 | import_all=39/39 | manifest=8/8
15:34:33 [INFO] argos.core: DAG Manager: OK
15:34:33 [INFO] argos.core: GitHub Marketplace: OK
15:34:33 [INFO] argos.core: OPi GPIO patch: GPIO=False I2C=False
15:34:33 [INFO] argos.iot: IoTBridge инициализирован. Устройств: 0
15:34:33 [INFO] argos.core: IoT Bridge: OK (0 устройств)
15:34:33 [INFO] argos.core: IoT Emulator Manager: OK
15:34:33 [INFO] argos.core: Mesh Network: OK (0 устройств)
15:34:33 [INFO] argos.gateway: Шлюзы загружены: 2
15:34:33 [INFO] argos.core: Gateway Manager: OK
15:34:33 [INFO] argos.industrial: KNXBridge init | xknx=True
15:34:33 [INFO] argos.industrial: LonWorksBridge init | port=2
15:34:33 [INFO] argos.industrial: MBusBridge init | mbus_lib=False
15:34:33 [INFO] argos.industrial: OPCUABridge init | opcua=True
15:34:33 [INFO] argos.industrial: IndustrialProtocolsManager init | KNX/LON/M-Bus/OPC-UA
15:34:33 [INFO] argos.core: Industrial Protocols: OK (KNX/LON/M-Bus/OPC-UA)
15:34:33 [INFO] argos.platform_admin: PlatformAdmin init | OS=Windows android=False termux=False
15:34:33 [INFO] argos.core: PlatformAdmin: OK (os=Windows)
15:34:33 [INFO] argos.smart: SmartSystems: загружено 5 систем
15:34:33 [INFO] argos.core: Smart Systems: OK (5 систем)
15:34:33 [INFO] argos.core: Home Assistant bridge: OFF
15:34:33 [INFO] argos.modules: Модуль загружен: system_monitor (src.modules.system_monitor_module)
15:34:33 [INFO] argos.modules: Модуль загружен: vision (src.modules.vision_module)
15:34:33 [INFO] argos.modules: Модуль загружен: voice (src.modules.voice_module)
15:34:33 [INFO] argos.core: 🧩 Modules: 3 загружено |   system_monitor, vision, voice
15:34:33 [INFO] argos.core: ToolCalling: OK (6 инструментов)
15:34:33 [INFO] argos.core: Awareness: OK
15:34:33 [INFO] argos.eventbus: EventBus запущен (history=500)
15:34:33 [INFO] argos.core: EventBus: OK
15:34:33 [INFO] argos.core: IoTHub: OK
15:34:33 [INFO] argos.life_support: ExpenseMonitor init
15:34:33 [INFO] argos.life_support: EarningEngine init
15:34:33 [INFO] argos.life_support: ArgosLifeSupport init ✅
15:34:33 [INFO] argos.core: LifeSupport: OK
15:34:42 [INFO] argos.watsonx: WatsonX: OK (meta-llama/llama-3-3-70b-instruct)
15:34:42 [INFO] argos.core: WatsonX: OK (meta-llama/llama-3-3-70b-instruct)
15:34:42 [INFO] argos.core: IBM Quantum: токен задан
15:34:42 [INFO] argos.core: Slack: SLACK_BOT_TOKEN не задан
15:34:42 [INFO] argos.core: SerpSearch: backend=serpapi
15:34:44 [INFO] argos.core: GitOps: OK
15:34:44 [INFO] argos.otg: OTGManager инициализирован (android=False, serial=True, jnius=False)
15:34:44 [INFO] argos.core: [WinBridge] 🚀 Запущен (PID 1600, порт 5000)
15:34:44 [INFO] argos.core: OTG Manager: OK
15:34:47 [INFO] argos.core: OwnModel: OK
15:34:47 [INFO] argos.evolver: ArgossEvolver готов (модель=qwen2.5:7b v1)
15:34:47 [INFO] argos.core: ArgossEvolver: OK (модель: qwen2.5:7b, версия: v1)
15:34:47 [INFO] argos.orangepi: OrangePiBridge init (I2C=bus0 UART=/dev/ttyS3 RS485=/dev/ttyS2)
15:34:47 [INFO] argos.core: OrangePiBridge: OK (платформа=Windows)
15:34:47 [INFO] argos.core: WebExplorer: OK (DuckDuckGo/Wikipedia/GitHub/arXiv)
15:34:51 [INFO] argos.awa: AWA: LazarusProtocol инициализирован
15:34:51 [INFO] argos.shadow_vision: [ShadowVision] Запущен (интервал 5s, модель yolov8n)
15:34:51 [INFO] argos.awa: AWA: ShadowVision запущен
15:34:51 [INFO] argos.awa: AWA: NeuralSwarm инициализирован
15:34:51 [INFO] argos.browser_conduit: BrowserConduit: stub mode (playwright не установлен)
15:34:51 [INFO] argos.awa: AWA: BrowserConduit инициализирован
15:34:51 [INFO] argos.awa: AWA: AirSnitch инициализирован (автостарт выкл)
15:34:51 [INFO] argos.awa: AWA-Core v1.0.0 init | policy=auto | cascade_depth=3
15:34:51 [INFO] argos.awa: AWA-CORE: Все системы жизнеобеспечения активированы.
15:34:55 [INFO] argos.core: ContextDB: подключена к DialogContext
15:34:55 [INFO] argos.core: AWA-Core: OK (Model Splitting активен)
15:34:55 [INFO] argos.self_sustain: SelfSustain: запущен
15:34:55 [INFO] argos.core: SelfSustain: OK
15:34:55 [INFO] argos.core: HealthMonitor: OK
15:34:55 [INFO] argos.core: AIFailover: OK
15:34:55 [INFO] argos.integrator: ╔══════════════════════════════════════════════════════════╗
15:34:55 [INFO] argos.integrator: ║             ARGOS UNIVERSAL INTEGRATOR v3.0              ║
15:34:55 [INFO] argos.integrator: ╚══════════════════════════════════════════════════════════╝
15:34:55 [INFO] argos.encryption: Encryption: ключ загружен из config/master.key
15:34:55 [WARNING] argos.integrator: Stub for LazarusProtocol: LazarusProtocol.__init__() missing 1 required positional argument: 'core'
15:34:55 [INFO] argos.integrator: ✅ security: 5 loaded
15:34:55 [INFO] argos.gost: pygost не установлен — используется встроенная реализация (pip install pygost для эталонной)
15:34:55 [INFO] argos.gost_p2p: GostP2PSecurity: шифр=Кузнечик pygost=False
15:34:56 [INFO] argos.orangepi: OrangePiBridge init (I2C=bus0 UART=/dev/ttyS3 RS485=/dev/ttyS2)
15:34:56 [INFO] argos.iot: IoTBridge инициализирован. Устройств: 0
15:34:56 [WARNING] argos.integrator: Stub for Any: Any cannot be instantiated
15:34:56 [INFO] argos.integrator: ✅ connectivity: 19 loaded
15:34:56 [INFO] argos.vector: VectorStore: fallback mode forced by ARGOS_VECTOR_FORCE_FALLBACK
15:34:56 [INFO] argos.grist: Grist: отключен через ARGOS_DISABLE_GRIST
15:34:56 [INFO] argos.integrator: ✅ knowledge: 2 loaded
15:34:56 [INFO] argos.integrator: ✅ factory: 3 loaded
15:34:56 [INFO] argos.evolution: Evolution: загружено 10 записей
15:34:56 [INFO] argos.self_model_v2: SelfModelV2 инициализирована
15:34:56 [INFO] argos.integrator: ✅ mind: 3 loaded
15:34:56 [INFO] argos.integrator: ✅ quantum: 4 loaded
15:34:56 [INFO] argos.integrator: ✅ vision: 2 loaded
15:34:56 [INFO] argos.skills: SkillInstance.start: module=argos_skill_content_gen runtime=ContentGen core=ArgosCore
15:34:56 [INFO] argos.skills: Навык загружен: content_gen v1.3.0
15:34:56 [INFO] argos.skills: SkillInstance.start: module=argos_skill_crypto_monitor runtime=CryptoSentinel core=ArgosCore
15:34:56 [INFO] argos.skills: Навык загружен: crypto_monitor v1.1.0
15:34:56 [INFO] argos.skills: SkillInstance.start: module=argos_skill_evolution runtime=ArgosEvolution core=ArgosCore
15:34:56 [INFO] argos.skills: Навык загружен: evolution v2.1.0
15:34:56 [INFO] argos.skills: SkillInstance.start: module=argos_skill_firmware_manager runtime=module core=ArgosCore
15:34:56 [INFO] argos.skills: Навык загружен: firmware_manager v1.0.0
15:34:56 [INFO] argos.skills: SkillInstance.start: module=argos_skill_net_scanner runtime=NetGhost core=ArgosCore
15:34:56 [INFO] argos.skills: Навык загружен: net_scanner v1.2.0
15:34:56 [INFO] argos.skills: SkillInstance.start: module=argos_skill_scheduler runtime=ArgosScheduler core=ArgosCore
15:34:56 [INFO] argos.scheduler: Scheduler запущен. Задач: 1
15:34:56 [INFO] argos.skills: Навык загружен: scheduler v2.0.0
15:34:56 [INFO] argos.skills: SkillInstance.start: module=argos_skill_weather runtime=module core=ArgosCore
15:34:56 [INFO] argos.skills: Навык загружен: weather v1.0.0
15:34:56 [INFO] argos.skills: SkillInstance.start: module=argos_skill_web_scrapper runtime=ArgosScrapper core=ArgosCore
15:34:56 [INFO] argos.skills: Навык загружен: web_scrapper v1.0.1
15:34:56 [INFO] argos.integrator: ✅ skills: 8 loaded
15:34:56 [INFO] argos.modules: Модуль загружен: system_monitor (src.modules.system_monitor_module)
15:34:56 [INFO] argos.modules: Модуль загружен: vision (src.modules.vision_module)
15:34:56 [INFO] argos.modules: Модуль загружен: voice (src.modules.voice_module)
15:34:56 [INFO] argos.integrator: ✅ modules: 3 loaded
15:34:56 [INFO] argos.integrator: ✅ interfaces: 4 loaded
15:34:56 [INFO] argos.claude-templates: ╔══════════════════════════════════════════════════════════╗
15:34:56 [INFO] argos.claude-templates: ║               CLAUDE TEMPLATES INTEGRATOR                ║
15:34:56 [INFO] argos.claude-templates: ╚══════════════════════════════════════════════════════════╝
15:34:56 [INFO] argos.claude-templates: 📦 Обнаружено компонентов: 0
15:34:56 [INFO] argos.claude-templates: 🤖 Адаптация агентов: 0
15:34:56 [INFO] argos.claude-templates: ⌨️ Адаптация команд: 0
15:34:56 [INFO] argos.claude-templates: 🪝 Адаптация хуков: 0
15:34:56 [INFO] argos.claude-templates: 🔗 Адаптация MCP: 0
15:34:56 [INFO] argos.claude-templates: 
════════════════════════════════════════════════════════════
15:34:56 [INFO] argos.claude-templates: ══════════════ ИНТЕГРАЦИЯ ШАБЛОНОВ ЗАВЕРШЕНА ═══════════════
15:34:56 [INFO] argos.claude-templates: ════════════════════════════════════════════════════════════
15:34:56 [INFO] argos.claude-templates: 🤖 Агенты:    0
15:34:56 [INFO] argos.claude-templates: ⌨️ Команды:   0
15:34:56 [INFO] argos.claude-templates: 🪝 Хуки:      0
15:34:56 [INFO] argos.claude-templates: 🔗 MCP:       0
15:34:56 [INFO] argos.claude-templates: ════════════════════════════════════════════════════════════
15:34:56 [INFO] argos.integrator: 
════════════════════════════════════════════════════════════
15:34:56 [INFO] argos.integrator: ═══════════════════ ИНТЕГРАЦИЯ ЗАВЕРШЕНА ═══════════════════
15:34:56 [INFO] argos.integrator: ════════════════════════════════════════════════════════════
15:34:56 [INFO] argos.integrator: ✅ security     —  5 loaded
15:34:56 [INFO] argos.integrator: ✅ connectivity — 19 loaded
15:34:56 [INFO] argos.integrator: ✅ knowledge    —  2 loaded
15:34:56 [INFO] argos.integrator: ✅ factory      —  3 loaded
15:34:56 [INFO] argos.integrator: ✅ mind         —  3 loaded
15:34:56 [INFO] argos.integrator: ✅ quantum      —  4 loaded
15:34:56 [INFO] argos.integrator: ✅ vision       —  2 loaded
15:34:56 [INFO] argos.integrator: ✅ skills       —  8 loaded
15:34:56 [INFO] argos.integrator: ✅ modules      —  3 loaded
15:34:56 [INFO] argos.integrator: ✅ interfaces   —  4 loaded
15:34:56 [INFO] argos.integrator: ✅ claude-templates —  3 loaded
15:34:56 [INFO] argos.integrator: ────────────────────────────────────────────────────────────
15:34:56 [INFO] argos.integrator: Итого: 11/11 подсистем OK, 0 ошибок
15:34:56 [INFO] argos.integrator: ════════════════════════════════════════════════════════════
15:34:56 [INFO] argos.core: Integrator: 12 категорий подключено
15:34:56 [INFO] argos.core:   └─ security: shield, gitguard, bootloader, lazarusprotocol, zkp
15:34:56 [INFO] argos.core:   └─ connectivity: p2p, telegram, whatsapp, slack, email...
15:34:56 [INFO] argos.core:   └─ protocol: modbus, ble, lora, zigbee, nfc
15:34:56 [INFO] argos.core:   └─ knowledge: vector, grist
15:34:56 [INFO] argos.core:   └─ factory: flasher, replicator, firmware
15:34:56 [INFO] argos.core:   └─ mind: dreamer, evolution, self_model
15:34:56 [INFO] argos.core:   └─ quantum: ibm, watson, logic, oracle
15:34:56 [INFO] argos.core:   └─ vision: shadow, vision
15:34:56 [INFO] argos.core:   └─ skill: content_gen, crypto_monitor, evolution, firmware_manager, net_scanner...
15:34:56 [INFO] argos.core:   └─ module: system_monitor, vision, voice
15:34:56 [INFO] argos.core:   └─ interface: gui, web, fastapi, shell
15:34:56 [INFO] argos.core:   └─ claude: agents, commands, hooks
15:34:56 [WARNING] argos.constitution: ARGOS mode => normal
15:34:56 [INFO] argos.core: Constitution: ARGOS Constitution Report
15:34:56 [WARNING] argos.core: C2 System: GistC2.__init__() got an unexpected keyword argument 'core'
15:34:56 [INFO] argos.self_model_v2: SelfModelV2 инициализирована
15:34:56 [INFO] argos.core: SelfModelV2: OK
15:34:56 [INFO] argos.dreamer: Dreamer запущен (интервал=3600s)
15:34:56 [INFO] argos.core: Dreamer: OK
15:34:56 [INFO] argos.evolution: Evolution: загружено 10 записей
15:34:56 [INFO] argos.core: EvolutionEngine: OK
15:34:56 [INFO] argos.consciousness: [Consciousness] Загружено: 140 мыслей, 0 синтезов
15:34:56 [INFO] argos.consciousness: CollectiveConsciousness v1.0.0 инициализировано
15:34:56 [INFO] argos.consciousness: [Consciousness] Фоновый цикл: интервал 120s
15:34:56 [INFO] argos.consciousness: [Consciousness] Фоновый цикл запущен
15:34:56 [INFO] argos.core: CollectiveConsciousness: OK
15:34:56 [INFO] argos.core: ArgosCore FINAL v2.0 инициализирован.
15:34:56 [INFO] argos.main: [CORE] ArgosCore готов
15:34:56 [INFO] argos.gost_p2p: GostP2PSecurity: шифр=Кузнечик pygost=False
15:34:56 [INFO] argos.core: P2P: 🌐 P2P-мост запущен
15:34:56 [INFO] argos.main: [P2P] Автозапуск: 🌐 P2P-мост запущен
15:34:56 [INFO] argos.integrator: ╔══════════════════════════════════════════════════════════╗
15:34:56 [INFO] argos.integrator: ║             ARGOS UNIVERSAL INTEGRATOR v3.0              ║
15:34:56 [INFO] argos.integrator: ╚══════════════════════════════════════════════════════════╝
15:34:56 [INFO] argos.encryption: Encryption: ключ загружен из config/master.key
15:34:56 [WARNING] argos.integrator: Stub for LazarusProtocol: LazarusProtocol.__init__() missing 1 required positional argument: 'core'
15:34:57 [INFO] argos.integrator: ✅ security: 5 loaded
15:34:57 [INFO] argos.gost_p2p: GostP2PSecurity: шифр=Кузнечик pygost=False
15:34:57 [INFO] argos.orangepi: OrangePiBridge init (I2C=bus0 UART=/dev/ttyS3 RS485=/dev/ttyS2)
15:34:57 [INFO] argos.iot: IoTBridge инициализирован. Устройств: 0
15:34:57 [WARNING] argos.integrator: Stub for Any: Any cannot be instantiated
15:34:57 [INFO] argos.integrator: ✅ connectivity: 19 loaded
15:34:57 [INFO] argos.vector: VectorStore: fallback mode forced by ARGOS_VECTOR_FORCE_FALLBACK
15:34:57 [INFO] argos.grist: Grist: отключен через ARGOS_DISABLE_GRIST
15:34:57 [INFO] argos.integrator: ✅ knowledge: 2 loaded
15:34:57 [INFO] argos.integrator: ✅ factory: 3 loaded
15:34:57 [INFO] argos.evolution: Evolution: загружено 10 записей
15:34:57 [INFO] argos.self_model_v2: SelfModelV2 инициализирована
15:34:57 [INFO] argos.integrator: ✅ mind: 3 loaded
15:34:57 [INFO] argos.integrator: ✅ quantum: 4 loaded
15:34:57 [INFO] argos.integrator: ✅ vision: 2 loaded
15:34:57 [INFO] argos.skills: SkillInstance.start: module=argos_skill_content_gen runtime=ContentGen core=ArgosCore
15:34:57 [INFO] argos.skills: Навык загружен: content_gen v1.3.0
15:34:57 [INFO] argos.skills: SkillInstance.start: module=argos_skill_crypto_monitor runtime=CryptoSentinel core=ArgosCore
15:34:57 [INFO] argos.skills: Навык загружен: crypto_monitor v1.1.0
15:34:57 [INFO] argos.skills: SkillInstance.start: module=argos_skill_evolution runtime=ArgosEvolution core=ArgosCore
15:34:57 [INFO] argos.skills: Навык загружен: evolution v2.1.0
15:34:57 [INFO] argos.skills: SkillInstance.start: module=argos_skill_firmware_manager runtime=module core=ArgosCore
15:34:57 [INFO] argos.skills: Навык загружен: firmware_manager v1.0.0
15:34:57 [INFO] argos.skills: SkillInstance.start: module=argos_skill_net_scanner runtime=NetGhost core=ArgosCore
15:34:57 [INFO] argos.skills: Навык загружен: net_scanner v1.2.0
15:34:57 [INFO] argos.skills: SkillInstance.start: module=argos_skill_scheduler runtime=ArgosScheduler core=ArgosCore
15:34:57 [INFO] argos.scheduler: Scheduler запущен. Задач: 1
15:34:57 [INFO] argos.skills: Навык загружен: scheduler v2.0.0
15:34:57 [INFO] argos.skills: SkillInstance.start: module=argos_skill_weather runtime=module core=ArgosCore
15:34:57 [INFO] argos.skills: Навык загружен: weather v1.0.0
15:34:57 [INFO] argos.skills: SkillInstance.start: module=argos_skill_web_scrapper runtime=ArgosScrapper core=ArgosCore
15:34:57 [INFO] argos.skills: Навык загружен: web_scrapper v1.0.1
15:34:57 [INFO] argos.integrator: ✅ skills: 8 loaded
15:34:57 [INFO] argos.modules: Модуль загружен: system_monitor (src.modules.system_monitor_module)
15:34:57 [INFO] argos.modules: Модуль загружен: vision (src.modules.vision_module)
15:34:57 [INFO] argos.modules: Модуль загружен: voice (src.modules.voice_module)
15:34:57 [INFO] argos.integrator: ✅ modules: 3 loaded
15:34:57 [INFO] argos.integrator: ✅ interfaces: 4 loaded
15:34:57 [INFO] argos.claude-templates: ╔══════════════════════════════════════════════════════════╗
15:34:57 [INFO] argos.claude-templates: ║               CLAUDE TEMPLATES INTEGRATOR                ║
15:34:57 [INFO] argos.claude-templates: ╚══════════════════════════════════════════════════════════╝
15:34:57 [INFO] argos.claude-templates: 📦 Обнаружено компонентов: 0
15:34:57 [INFO] argos.claude-templates: 🤖 Адаптация агентов: 0
15:34:57 [INFO] argos.claude-templates: ⌨️ Адаптация команд: 0
15:34:57 [INFO] argos.claude-templates: 🪝 Адаптация хуков: 0
15:34:57 [INFO] argos.claude-templates: 🔗 Адаптация MCP: 0
15:34:57 [INFO] argos.claude-templates: 
════════════════════════════════════════════════════════════
15:34:57 [INFO] argos.claude-templates: ══════════════ ИНТЕГРАЦИЯ ШАБЛОНОВ ЗАВЕРШЕНА ═══════════════
15:34:57 [INFO] argos.claude-templates: ════════════════════════════════════════════════════════════
15:34:57 [INFO] argos.claude-templates: 🤖 Агенты:    0
15:34:57 [INFO] argos.claude-templates: ⌨️ Команды:   0
15:34:57 [INFO] argos.claude-templates: 🪝 Хуки:      0
15:34:57 [INFO] argos.claude-templates: 🔗 MCP:       0
15:34:57 [INFO] argos.claude-templates: ════════════════════════════════════════════════════════════
15:34:57 [INFO] argos.integrator: 
════════════════════════════════════════════════════════════
15:34:57 [INFO] argos.integrator: ═══════════════════ ИНТЕГРАЦИЯ ЗАВЕРШЕНА ═══════════════════
15:34:57 [INFO] argos.integrator: ════════════════════════════════════════════════════════════
15:34:57 [INFO] argos.integrator: ✅ security     —  5 loaded
15:34:57 [INFO] argos.integrator: ✅ connectivity — 19 loaded
15:34:57 [INFO] argos.integrator: ✅ knowledge    —  2 loaded
15:34:57 [INFO] argos.integrator: ✅ factory      —  3 loaded
15:34:57 [INFO] argos.integrator: ✅ mind         —  3 loaded
15:34:57 [INFO] argos.integrator: ✅ quantum      —  4 loaded
15:34:57 [INFO] argos.integrator: ✅ vision       —  2 loaded
15:34:57 [INFO] argos.integrator: ✅ skills       —  8 loaded
15:34:57 [INFO] argos.integrator: ✅ modules      —  3 loaded
15:34:57 [INFO] argos.integrator: ✅ interfaces   —  4 loaded
15:34:57 [INFO] argos.integrator: ✅ claude-templates —  3 loaded
15:34:57 [INFO] argos.integrator: ────────────────────────────────────────────────────────────
15:34:57 [INFO] argos.integrator: Итого: 11/11 подсистем OK, 0 ошибок
15:34:57 [INFO] argos.integrator: ════════════════════════════════════════════════════════════
15:34:57 [INFO] argos.main: [INTEGRATOR] Подключено подсистем: 56
15:34:58 [ERROR] argos.core: GigaChat: HTTP 402 {"status":402,"message":"Payment Required"}

[ERR]    : HTTPConnectionPool(host='localhost', port=5010): Max retries exceeded with url: /health (Caused by NewConnectionError("HTTPConnection(host='localhost', port=5010): Failed to establish a new connection: [WinError 10061]   , ..      "))
15:35:01 [INFO] argos.main: [BRAIN] Brain API не отвечает — запускаю автоматически...
15:35:01 [INFO] argos.main: [BRAIN] Запускаю Brain API: C:\Users\AvA\AppData\Local\Programs\Python\Python311\python.exe F:\debug\argoss\argos_brain_api.py
15:35:03 [INFO] argos.memory: Запомнил [dreamer] insight_1776749703_0 = 1. Пользователь ценит четкие и пошаговые инструкции по установке и настройке программного обеспечения.
15:35:03 [INFO] argos.memory: Запомнил [dreamer] insight_1776749703_1 = 2. Я мог ответить лучше, предоставив более подробные объяснения по каждому этапу установки.
15:35:03 [INFO] argos.memory: Запомнил [dreamer] insight_1776749703_2 = 3. Я узнал, что пользователь интересуется улучшением функциональности поиска с помощью API.
15:35:07 [INFO] argos.main: [BRAIN] ✅ Brain API запущен (PID 18364): http://localhost:5010
15:35:07 [INFO] argos.main: [WARMUP] Прогрев Ollama модели qwen2.5:7b...
15:35:07 [INFO] argos.main: [SERVER] Headless режим — только Telegram + P2P
[CLUSTER DASH]   http://0.0.0.0:808015:35:07 [INFO] argos.main: [SERVER] Dashboard: http://localhost:8080

15:35:08 [INFO] argos.main: [MCP] Endpoint доступен: http://0.0.0.0:8000/mcp
15:35:08 [INFO] argos.main: [MCP] Watchdog активен: check каждые 10s
15:35:08 [INFO] argos.main: [TG] Telegram бот запущен
15:35:08 [INFO] argos.main: [SERVER] Argos running. Press Ctrl+C to stop.
[TG] polling started
15:35:11 [INFO] argos.main: [OpenClaw] Запускаю Gateway (local): node dist/index.js gateway --port 18789
15:35:12 [INFO] argos.skills: Dispatch checking skill: content_gen
15:35:12 [INFO] argos.skills: Dispatch checking skill: crypto_monitor
15:35:12 [INFO] argos.skills: Dispatch checking skill: evolution
15:35:12 [INFO] argos.skills: Dispatch checking skill: firmware_manager
15:35:12 [INFO] argos.skills: Dispatch checking skill: net_scanner
15:35:12 [INFO] argos.skills: Dispatch checking skill: scheduler
15:35:12 [INFO] argos.skills: Dispatch checking skill: weather
15:35:12 [INFO] argos.skills: Dispatch checking skill: web_scrapper
15:35:12 [INFO] argos.skills: Dispatch checking skill: ai_coder
15:35:12 [INFO] argos.skills: Dispatch checking skill: ai_coder_evolution_bridge
15:35:12 [INFO] argos.skills: Dispatch checking skill: arc_agi3_skill
15:35:12 [INFO] argos.skills: Dispatch checking skill: argos_patcher
15:35:12 [INFO] argos.skills: Dispatch checking skill: argos_service
15:35:12 [INFO] argos.skills: Dispatch checking skill: auto_backup
15:35:12 [INFO] argos.skills: Dispatch checking skill: autonomy_fileops
15:35:12 [INFO] argos.skills: Dispatch checking skill: browser_conduit
15:35:12 [INFO] argos.skills: Dispatch checking skill: crypto_utils
15:35:12 [INFO] argos.skills: Dispatch checking skill: desktop_actions
15:35:12 [INFO] argos.skills: Dispatch checking skill: ebay_parser
15:35:12 [INFO] argos.skills: Dispatch checking skill: esp32_usb_bridge
15:35:12 [INFO] argos.skills: Dispatch checking skill: fastapi_skill
15:35:12 [INFO] argos.skills: Dispatch checking skill: firmware_examples
15:35:12 [INFO] argos.skills: Dispatch checking skill: ga4_analytics
15:35:12 [INFO] argos.skills: Dispatch checking skill: hardware_intel
15:35:12 [INFO] argos.skills: Dispatch checking skill: huggingface_ai
15:35:12 [INFO] argos.skills: Dispatch checking skill: iot_watchdog
15:35:12 [INFO] argos.skills: Dispatch checking skill: multi_provider_chat
15:35:12 [INFO] argos.skills: Dispatch checking skill: network_shadow
15:35:12 [INFO] argos.skills: Dispatch checking skill: new_skill
15:35:12 [INFO] argos.skills: Dispatch checking skill: pip_manager
15:35:12 [INFO] argos.skills: Dispatch checking skill: serp_search
15:35:12 [INFO] argos.skills: Dispatch checking skill: shodan_scanner
15:35:12 [INFO] argos.skills: Dispatch checking skill: smart_environments
15:35:12 [INFO] argos.skills: Dispatch checking skill: smtp_mailer
15:35:12 [INFO] argos.skills: Dispatch checking skill: system_monitor
15:35:12 [INFO] argos.skills: Dispatch checking skill: tasmota_updater
15:35:12 [INFO] argos.skills: Dispatch checking skill: test_injected
15:35:12 [INFO] argos.skills: Dispatch checking skill: tg_code_injector
15:35:12 [INFO] argos.skills: Dispatch checking skill: ton_blockchain
15:35:12 [INFO] argos.skills: Dispatch checking skill: usb_access_point
15:35:12 [INFO] argos.skills: Dispatch checking skill: web_explorer
15:35:13 [WARNING] argos.core: [WinBridge] Не ответил за 8с
15:35:20 [WARNING] argos.main: [OpenClaw] Gateway не отвечает: HTTPConnectionPool(host='localhost', port=18789): Max retries exceeded with url: /health (Caused by NewConnectionError("HTTPConnection(host='localhost', port=18789): Failed to establish a new connection: [WinError 10061] Подключение не установлено, т.к. конечный компьютер отверг запрос на подключение"))
15:35:21 [INFO] argos.main: [WARMUP] ✅ Ollama qwen2.5:7b готова к работе
15:35:29 [INFO] argos.backup: AutoBackup: создаём плановый бэкап...
15:35:41 [INFO] argos.backup: Бэкап создан: argos_backup_20260421_153529_auto.zip (4378 файлов, 61649.7 КБ)
15:35:41 [INFO] argos.backup: Удалён старый бэкап: argos_backup_20260420_191759_auto.zip
15:35:41 [INFO] argos.backup: AutoBackup: ✅ Бэкап создан
15:37:04 [ERROR] argos.core: GigaChat: HTTP 402 {"status":402,"message":"Payment Required"}

15:37:08 [INFO] argos.memory: Запомнил [dreamer] insight_1776749828_0 = 1. Пользователь ценит четкие и пошаговые инструкции по установке и настройке программного обеспечения.
15:37:08 [INFO] argos.memory: Запомнил [dreamer] insight_1776749828_1 = 2. Я мог ответить лучше, предоставив более подробные объяснения по каждому шагу установки.
15:37:08 [INFO] argos.memory: Запомнил [dreamer] insight_1776749828_2 = 3. Я узнал, что пользователь интересуется улучшением функциональности поиска и использует API для этого.
15:37:59 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
15:37:59 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
15:38:59 [ERROR] argos.core: [argos-v1] Ошибка: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=60)
15:38:59 [WARNING] argos.core: argos-v1 временно отключен на 300 сек: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=60)
15:39:04 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
15:39:04 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
15:39:04 [INFO] argos.core: [Ollama] Запрос: модель=qwen2.5:7b
15:39:55 [INFO] argos.self_sustain: SelfSustain: изучаю тему 'веб-скрапинг Python 2026'
15:39:55 [INFO] argos.web_explorer: WebExplorer.learn: 'веб-скрапинг Python 2026'
15:39:58 [WARNING] argos.web_explorer: SerpAPI AI Overview error: Your account has run out of searches.
15:39:59 [WARNING] argos.web_explorer: SerpAPI DDG error: Your account has run out of searches.
15:40:02 [INFO] argos.web_explorer: DuckDuckGo: 'веб-скрапинг Python 2026' → 3 результатов
15:40:02 [INFO] argos.memory: Запомнил [web_knowledge] web_learn:веб-скрапинг_Python_2026 = [Поиск DuckDuckGo]
  • Веб-скрапинг с parsel в python 2026: гайд по архитектуре: Гайд по Веб-скрапинг с parsel в python 2026 : как ускорить сбор данных на 40%, избежать ошибок и настроить XPath селекторы.
  • Веб-скрапинг на Python с Beautiful Soup: пошаговое руководство с ...: Она значительно упрощает работу с веб-страницами, позволяя легко получать их HTML-код. Beautiful Soup 4 (bs4): Основной инструмент для парсинга HTML и XML документов.
  • Руководство по веб-скрейпингу на Python / Хабр: Один из самых волшебных аспектов веб-скрейпинга при помощи Python -библиотеки BeautifulSoup — это применение CSS-селекторов для извлечения нужного контента из HTML-страниц.
15:40:02 [INFO] argos.web_explorer: Сохранено в память: web_learn:веб-скрапинг_Python_2026
15:40:02 [INFO] argos.self_sustain: SelfSustain: тема 'веб-скрапинг Python 2026' изучена и сохранена
15:40:04 [WARNING] argos.core: [Ollama] Таймаут (60s) — отключаю на 5 минут, fallback на облако
15:40:04 [WARNING] argos.core: Ollama (Argoss) временно отключен на 300 сек: timeout 60s
15:40:04 [INFO] argos.memory: Запомнил [dialogue] last_user_query = sk-kimi-L8P6bTKOVDIwfgF44yERMuaw38qIhQFfi3Gtb1j806TVvdqRKzEvJ8rELYc38DE7
15:40:04 [INFO] argos.memory: Запомнил [dialogue] last_argos_response = Я не могу выполнить эти команды, так как они предназначены для Linux-систем, а я работаю на Windows. Если у вас есть другие задачи или вопросы, дайте знать.
15:40:08 [INFO] argos.skills: Dispatch checking skill: content_gen
15:40:08 [INFO] argos.skills: Dispatch checking skill: crypto_monitor
15:40:08 [INFO] argos.skills: Dispatch checking skill: evolution
15:40:08 [INFO] argos.skills: Dispatch checking skill: firmware_manager
15:40:08 [INFO] argos.skills: Dispatch checking skill: net_scanner
15:40:08 [INFO] argos.skills: Dispatch checking skill: scheduler
15:40:08 [INFO] argos.skills: Dispatch checking skill: weather
15:40:08 [INFO] argos.skills: Dispatch checking skill: web_scrapper
15:40:08 [INFO] argos.skills: Dispatch checking skill: ai_coder
15:40:08 [INFO] argos.skills: Dispatch checking skill: ai_coder_evolution_bridge
15:40:08 [INFO] argos.skills: Dispatch checking skill: arc_agi3_skill
15:40:08 [INFO] argos.skills: Dispatch checking skill: argos_patcher
15:40:08 [INFO] argos.skills: Dispatch checking skill: argos_service
15:40:08 [INFO] argos.skills: Dispatch checking skill: auto_backup
15:40:08 [INFO] argos.skills: Dispatch checking skill: autonomy_fileops
15:40:08 [INFO] argos.skills: Dispatch checking skill: browser_conduit
15:40:08 [INFO] argos.skills: Dispatch checking skill: crypto_utils
15:40:08 [INFO] argos.skills: Dispatch checking skill: desktop_actions
15:40:08 [INFO] argos.skills: Dispatch checking skill: ebay_parser
15:40:08 [INFO] argos.skills: Dispatch checking skill: esp32_usb_bridge
15:40:08 [INFO] argos.skills: Dispatch checking skill: fastapi_skill
15:40:08 [INFO] argos.skills: Dispatch checking skill: firmware_examples
15:40:08 [INFO] argos.skills: Dispatch checking skill: ga4_analytics
15:40:08 [INFO] argos.skills: Dispatch checking skill: hardware_intel
15:40:08 [INFO] argos.skills: Dispatch checking skill: huggingface_ai
15:40:08 [INFO] argos.skills: Dispatch checking skill: iot_watchdog
15:40:08 [INFO] argos.skills: Dispatch checking skill: multi_provider_chat
15:40:08 [INFO] argos.skills: Dispatch checking skill: network_shadow
15:40:08 [INFO] argos.skills: Dispatch checking skill: new_skill
15:40:08 [INFO] argos.skills: Dispatch checking skill: pip_manager
15:40:08 [INFO] argos.skills: Dispatch checking skill: serp_search
15:40:08 [INFO] argos.skills: Dispatch checking skill: shodan_scanner
15:40:08 [INFO] argos.skills: Dispatch checking skill: smart_environments
15:40:08 [INFO] argos.skills: Dispatch checking skill: smtp_mailer
15:40:08 [INFO] argos.skills: Dispatch checking skill: system_monitor
15:40:08 [INFO] argos.skills: Dispatch checking skill: tasmota_updater
15:40:08 [INFO] argos.skills: Dispatch checking skill: test_injected
15:40:08 [INFO] argos.skills: Dispatch checking skill: tg_code_injector
15:40:08 [INFO] argos.skills: Dispatch checking skill: ton_blockchain
15:40:08 [INFO] argos.skills: Dispatch checking skill: usb_access_point
15:40:08 [INFO] argos.skills: Dispatch checking skill: web_explorer
15:43:19 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
15:43:19 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
15:43:19 [INFO] argos.core: [Ollama] Запрос: модель=qwen2.5:7b
15:44:19 [WARNING] argos.core: [Ollama] Таймаут (60s) — отключаю на 5 минут, fallback на облако
15:44:19 [INFO] argos.memory: Запомнил [dialogue] last_user_query = Иии
15:44:23 [INFO] argos.skills: Dispatch checking skill: content_gen
15:44:23 [INFO] argos.skills: Dispatch checking skill: crypto_monitor
15:44:23 [INFO] argos.skills: Dispatch checking skill: evolution
15:44:23 [INFO] argos.skills: Dispatch checking skill: firmware_manager
15:44:23 [INFO] argos.skills: Dispatch checking skill: net_scanner
15:44:23 [INFO] argos.skills: Dispatch checking skill: scheduler
15:44:23 [INFO] argos.skills: Dispatch checking skill: weather
15:44:23 [INFO] argos.skills: Dispatch checking skill: web_scrapper
15:44:23 [INFO] argos.skills: Dispatch checking skill: ai_coder
15:44:23 [INFO] argos.skills: Dispatch checking skill: ai_coder_evolution_bridge
15:44:23 [INFO] argos.skills: Dispatch checking skill: arc_agi3_skill
15:44:23 [INFO] argos.skills: Dispatch checking skill: argos_patcher
15:44:23 [INFO] argos.skills: Dispatch checking skill: argos_service
15:44:23 [INFO] argos.skills: Dispatch checking skill: auto_backup
15:44:23 [INFO] argos.skills: Dispatch checking skill: autonomy_fileops
15:44:23 [INFO] argos.skills: Dispatch checking skill: browser_conduit
15:44:23 [INFO] argos.skills: Dispatch checking skill: crypto_utils
15:44:23 [INFO] argos.skills: Dispatch checking skill: desktop_actions
15:44:23 [INFO] argos.skills: Dispatch checking skill: ebay_parser
15:44:23 [INFO] argos.skills: Dispatch checking skill: esp32_usb_bridge
15:44:23 [INFO] argos.skills: Dispatch checking skill: fastapi_skill
15:44:23 [INFO] argos.skills: Dispatch checking skill: firmware_examples
15:44:23 [INFO] argos.skills: Dispatch checking skill: ga4_analytics
15:44:23 [INFO] argos.skills: Dispatch checking skill: hardware_intel
15:44:23 [INFO] argos.skills: Dispatch checking skill: huggingface_ai
15:44:23 [INFO] argos.skills: Dispatch checking skill: iot_watchdog
15:44:23 [INFO] argos.skills: Dispatch checking skill: multi_provider_chat
15:44:23 [INFO] argos.skills: Dispatch checking skill: network_shadow
15:44:23 [INFO] argos.skills: Dispatch checking skill: new_skill
15:44:23 [INFO] argos.skills: Dispatch checking skill: pip_manager
15:44:23 [INFO] argos.skills: Dispatch checking skill: serp_search
15:44:23 [INFO] argos.skills: Dispatch checking skill: shodan_scanner
15:44:23 [INFO] argos.skills: Dispatch checking skill: smart_environments
15:44:23 [INFO] argos.skills: Dispatch checking skill: smtp_mailer
15:44:23 [INFO] argos.skills: Dispatch checking skill: system_monitor
15:44:23 [INFO] argos.skills: Dispatch checking skill: tasmota_updater
15:44:23 [INFO] argos.skills: Dispatch checking skill: test_injected
15:44:23 [INFO] argos.skills: Dispatch checking skill: tg_code_injector
15:44:23 [INFO] argos.skills: Dispatch checking skill: ton_blockchain
15:44:23 [INFO] argos.skills: Dispatch checking skill: usb_access_point
15:44:23 [INFO] argos.skills: Dispatch checking skill: web_explorer
15:47:10 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
15:47:10 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)

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
