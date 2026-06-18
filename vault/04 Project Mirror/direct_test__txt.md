---
argos_import: project_file
source_path: direct_test.txt
source_abs: F:\debug\argoss\direct_test.txt
source_ext: .txt
source_sha256: 0533c0bcc93bf95e0bb519d169753ca34192cdee3b5bee82bbf2eae119f85b50
text_sha256: e3d4126b20074dbfe3b77aea0e0a1e67facf8e8fa20c98456904ae33d6f3eb10
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# direct_test.txt

- Source: `direct_test.txt`
- Extract: `text`
- SHA256: `0533c0bcc93bf95e0bb519d169753ca34192cdee3b5bee82bbf2eae119f85b50`

## Content

00:01:07 [INFO] argos.eventbus: EventBus запущен (history=500)
00:01:07 [INFO] argos.core: TTS: OK
00:01:11 [INFO] argos.core: Gemini: OK
00:01:11 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
00:01:14 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
00:01:14 [INFO] argos.core: Ollama: ✅ доступна (резервный провайдер готов)
00:01:14 [INFO] argos.core: GigaChat недоступен — нет credentials
00:01:14 [INFO] argos.core: YandexGPT недоступен — нет IAM/FOLDER
00:01:14 [INFO] argos.core: Kimi: конфигурация обнаружена (KIMI_API_KEY)
00:01:14 [INFO] argos.vector: VectorStore: fallback mode forced by ARGOS_VECTOR_FORCE_FALLBACK
00:01:14 [INFO] argos.memory: Vector warmup: indexed 180 docs
00:01:14 [INFO] argos.memory: Vector warmup: scheduled in background (180 docs)
00:01:14 [INFO] argos.thought_book: ThoughtBook инициализирована: 191 промтов, 10 частей.
00:01:14 [INFO] argos.core: Память: OK
00:01:14 [INFO] argos.hardware_guard: Hardware guard: ON
00:01:14 [INFO] argos.core: Homeostasis: OK
00:01:14 [INFO] argos.curiosity: Curiosity: автономный режим запущен.
00:01:14 [INFO] argos.core: Curiosity: OK
00:01:14 [INFO] argos.scheduler: Scheduler запущен. Задач: 1
00:01:14 [INFO] argos.core: Планировщик: OK
00:01:14 [INFO] argos.alerts: AlertSystem запущен. Интервал: 30s
00:01:14 [INFO] argos.core: Алерты: OK
00:01:14 [INFO] argos.core: Vision: OK
00:01:14 [INFO] argos.skills: SkillInstance.start: module=argos_skill_content_gen runtime=ContentGen core=ArgosCore
00:01:14 [INFO] argos.skills: Навык загружен: content_gen v1.3.0
00:01:14 [INFO] argos.skills: SkillInstance.start: module=argos_skill_crypto_monitor runtime=CryptoSentinel core=ArgosCore
00:01:14 [INFO] argos.skills: Навык загружен: crypto_monitor v1.1.0
00:01:14 [INFO] argos.skills: SkillInstance.start: module=argos_skill_evolution runtime=ArgosEvolution core=ArgosCore
00:01:14 [INFO] argos.skills: Навык загружен: evolution v2.1.0
00:01:14 [INFO] argos.skills: SkillInstance.start: module=argos_skill_firmware_manager runtime=module core=ArgosCore
00:01:14 [INFO] argos.skills: Навык загружен: firmware_manager v1.0.0
00:01:14 [INFO] argos.skills: SkillInstance.start: module=argos_skill_net_scanner runtime=NetGhost core=ArgosCore
00:01:14 [INFO] argos.skills: Навык загружен: net_scanner v1.2.0
00:01:14 [INFO] argos.skills: SkillInstance.start: module=argos_skill_scheduler runtime=ArgosScheduler core=ArgosCore
00:01:14 [INFO] argos.scheduler: Scheduler запущен. Задач: 1
00:01:14 [INFO] argos.skills: Навык загружен: scheduler v2.0.0
00:01:14 [INFO] argos.skills: SkillInstance.start: module=argos_skill_weather runtime=module core=ArgosCore
00:01:14 [INFO] argos.skills: Навык загружен: weather v1.0.0
00:01:14 [INFO] argos.skills: SkillInstance.start: module=argos_skill_web_scrapper runtime=ArgosScrapper core=ArgosCore
00:01:14 [INFO] argos.skills: Навык загружен: web_scrapper v1.0.1
00:01:14 [INFO] argos.skills: SkillInstance.start: module=src.skills.ai_coder runtime=AICoder core=ArgosCore
00:01:14 [INFO] argos.skills: SkillInstance.start: module=src.skills.ai_coder_evolution_bridge runtime=AICoderEvolutionBridge core=ArgosCore
00:01:14 [INFO] argos.skills: SkillInstance.start: module=src.skills.arc_agi3_skill runtime=ARC3Agent core=ArgosCore
00:01:14 [INFO] argos.skills: SkillInstance.start: module=src.skills.argos_patcher runtime=module core=ArgosCore
00:01:14 [INFO] argos.skills: SkillInstance.start: module=src.skills.argos_service runtime=module core=ArgosCore
00:01:14 [INFO] argos.skills: SkillInstance.start: module=src.skills.auto_backup runtime=AutoBackup core=ArgosCore
00:01:14 [INFO] argos.backup: AutoBackup запущен, интервал 6 ч
00:01:14 [INFO] argos.skills: SkillInstance.start: module=src.skills.autonomy_fileops runtime=AutonomyFileOps core=ArgosCore
00:01:16 [INFO] argos.skills: SkillInstance.start: module=src.skills.browser_conduit runtime=BrowserConduit core=ArgosCore
00:01:16 [INFO] argos.skills: SkillInstance.start: module=src.skills.crypto_utils runtime=CryptoUtils core=ArgosCore
00:01:16 [INFO] argos.skills: SkillInstance.start: module=src.skills.desktop_actions runtime=DesktopActionsSkill core=ArgosCore
00:01:16 [INFO] argos.skills: SkillInstance.start: module=src.skills.ebay_parser runtime=EbayParser core=ArgosCore
00:01:16 [INFO] argos.skills: SkillInstance.start: module=src.skills.esp32_usb_bridge runtime=ESP32UsbBridge core=ArgosCore
00:01:16 [INFO] argos.esp32_bridge: Найден ESP32 порт: COM7 USB-SERIAL CH340 (COM7)
00:01:16 [INFO] argos.skills: SkillInstance.start: module=src.skills.fastapi_skill runtime=FastAPISkill core=ArgosCore
00:01:18 [INFO] argos.skills: SkillInstance.start: module=src.skills.firmware_examples runtime=FirmwareExamplesLoader core=ArgosCore
00:01:18 [INFO] argos.skills: SkillInstance.start: module=src.skills.free_ai runtime=FreeAIProvider core=ArgosCore
00:01:18 [INFO] argos.skills: SkillInstance.start: module=src.skills.ga4_analytics runtime=GA4Analytics core=ArgosCore
00:01:18 [INFO] argos.skills: SkillInstance.start: module=src.skills.hardware_intel runtime=module core=ArgosCore
00:01:19 [INFO] argos.skills: SkillInstance.start: module=src.skills.huggingface_ai runtime=HuggingFaceAI core=ArgosCore
00:01:19 [INFO] argos.skills: SkillInstance.start: module=src.skills.image_gen runtime=module core=ArgosCore
00:01:19 [INFO] argos.skills: SkillInstance.start: module=src.skills.iot_watchdog runtime=IoTWatchdog core=ArgosCore
00:01:20 [INFO] argos.skills: SkillInstance.start: module=src.skills.multi_provider_chat runtime=MultiProviderChat core=ArgosCore
00:01:20 [INFO] argos.skills: SkillInstance.start: module=src.skills.network_shadow runtime=module core=ArgosCore
00:01:20 [INFO] argos.skills: SkillInstance.start: module=src.skills.new_skill runtime=P2PNetworkSkill core=ArgosCore
00:01:20 [INFO] argos.skills: SkillInstance.start: module=src.skills.pip_manager runtime=PipManager core=ArgosCore
00:01:20 [INFO] argos.skills: SkillInstance.start: module=src.skills.serp_search runtime=SerpSearch core=ArgosCore
00:01:20 [INFO] argos.skills: SkillInstance.start: module=src.skills.shodan_scanner runtime=ShodanScanner core=ArgosCore
00:01:20 [INFO] argos.skills: SkillInstance.start: module=src.skills.smart_environments runtime=module core=ArgosCore
00:01:21 [INFO] argos.skills: SkillInstance.start: module=src.skills.smtp_mailer runtime=SMTPMailer core=ArgosCore
00:01:21 [INFO] argos.skills: SkillInstance.start: module=src.skills.system_monitor runtime=SystemMonitor core=ArgosCore
00:01:21 [INFO] argos.sysmon: SystemMonitor запущен, интервал 30 сек
00:01:21 [INFO] argos.skills: SkillInstance.start: module=src.skills.tasmota_updater runtime=TasmotaUpdater core=ArgosCore
00:01:21 [INFO] argos.skills: SkillInstance.start: module=src.skills.test_injected runtime=TestSkill core=ArgosCore
00:01:21 [INFO] argos.skills: SkillInstance.start: module=src.skills.tg_code_injector runtime=TGCodeInjector core=ArgosCore
00:01:21 [INFO] argos.skills: SkillInstance.start: module=src.skills.ton_blockchain runtime=TonBlockchain core=ArgosCore
00:01:21 [INFO] argos.skills: SkillInstance.start: module=src.skills.usb_access_point runtime=USBGadgetAP core=ArgosCore
00:01:21 [INFO] argos.skills: SkillInstance.start: module=src.skills.web_explorer runtime=ArgosWebExplorer core=ArgosCore
00:01:21 [INFO] argos.skills: SkillInstance.start: module=src.skills.web_scraper runtime=module core=ArgosCore
00:01:21 [INFO] argos.core: SkillLoader: OK
00:01:21 [INFO] argos.core: 📦 Обнаружено manifest-навыков: 8 | ✅ Навык 'content_gen' v1.3.0 загружен. | ✅ Навык 'crypto_monitor' v1.1.0 загружен. | ✅ Навык 'evolution' v2.1.0 загружен. | ✅ Навык 'firmware_manager' v1.0.0 загружен. | ✅ Навык 'net_scanner' v1.2.0 загружен. | ✅ Навык 'scheduler' v2.0.0 загружен. | ✅ Навык 'weather' v1.0.0 загружен. | ✅ Навык 'web_scrapper' v1.0.1 загружен. | Импорт всех skills (src/skills) → PASS 42/43 | ✅ ai_coder | ✅ ai_coder_evolution_bridge | ✅ arc_agi3_skill | ✅ argos_patcher | ✅ argos_service | ✅ auto_backup | ✅ autonomy_fileops | ✅ browser_conduit | ✅ content_gen (already loaded) | ✅ crypto_monitor (already loaded) | ✅ crypto_utils | ✅ desktop_actions | ✅ ebay_parser | ✅ esp32_usb_bridge | ✅ evolution (already loaded) | ✅ fastapi_skill | ✅ firmware_examples | ✅ free_ai | ✅ ga4_analytics | ✅ hardware_intel | ❌ hive_mind: ModelNode.__init__() missing 5 required positional arguments: 'name', 'host', 'port', 'model_type', and 'model_name' | ✅ huggingface_ai | ✅ image_gen | ✅ iot_watchdog | ✅ multi_provider_chat | ✅ net_scanner (already loaded) | ✅ network_shadow | ✅ new_skill | ✅ pip_manager | ✅ scheduler (already loaded) | ✅ serp_search | ✅ shodan_scanner | ✅ smart_environments | ✅ smtp_mailer | ✅ system_monitor | ✅ tasmota_updater | ✅ test_injected | ✅ tg_code_injector | ✅ ton_blockchain | ✅ usb_access_point | ✅ web_explorer | ✅ web_scraper | ✅ web_scrapper (already loaded) | SkillLoader load_all (manifest навыки) → PASS 8/8
00:01:21 [INFO] argos.core: [SKILLS] startup loaded=44 | import_all=42/43 | manifest=8/8
00:01:21 [INFO] argos.core: DAG Manager: OK
00:01:21 [INFO] argos.core: GitHub Marketplace: OK
00:01:21 [INFO] argos.core: OPi GPIO patch: GPIO=False I2C=False
00:01:21 [INFO] argos.iot: IoTBridge инициализирован. Устройств: 0
00:01:21 [INFO] argos.core: IoT Bridge: OK (0 устройств)
00:01:21 [INFO] argos.core: IoT Emulator Manager: OK
00:01:21 [INFO] argos.core: Mesh Network: OK (0 устройств)
00:01:21 [INFO] argos.gateway: Шлюзы загружены: 2
00:01:21 [INFO] argos.core: Gateway Manager: OK
00:01:22 [INFO] argos.industrial: KNXBridge init | xknx=True
00:01:22 [INFO] argos.industrial: LonWorksBridge init | port=2
00:01:22 [INFO] argos.industrial: MBusBridge init | mbus_lib=False
00:01:22 [INFO] argos.industrial: OPCUABridge init | opcua=True
00:01:22 [INFO] argos.industrial: IndustrialProtocolsManager init | KNX/LON/M-Bus/OPC-UA
00:01:22 [INFO] argos.core: Industrial Protocols: OK (KNX/LON/M-Bus/OPC-UA)
00:01:22 [INFO] argos.platform_admin: PlatformAdmin init | OS=Windows android=False termux=False
00:01:22 [INFO] argos.core: PlatformAdmin: OK (os=Windows)
00:01:22 [INFO] argos.smart: SmartSystems: загружено 5 систем
00:01:22 [INFO] argos.core: Smart Systems: OK (5 систем)
00:01:22 [INFO] argos.core: Home Assistant bridge: OFF
00:01:22 [INFO] argos.modules: Модуль загружен: system_monitor (src.modules.system_monitor_module)
00:01:22 [INFO] argos.modules: Модуль загружен: vision (src.modules.vision_module)
00:01:22 [INFO] argos.modules: Модуль загружен: voice (src.modules.voice_module)
00:01:22 [INFO] argos.core: 🧩 Modules: 3 загружено |   system_monitor, vision, voice
00:01:22 [INFO] argos.core: ToolCalling: OK (6 инструментов)
00:01:22 [INFO] argos.core: Awareness: OK
00:01:22 [INFO] argos.eventbus: EventBus запущен (history=500)
00:01:22 [INFO] argos.core: EventBus: OK
00:01:22 [INFO] argos.core: IoTHub: OK
00:01:22 [INFO] argos.life_support: ExpenseMonitor init
00:01:22 [INFO] argos.life_support: EarningEngine init
00:01:22 [INFO] argos.life_support: ArgosLifeSupport init ✅
00:01:22 [INFO] argos.core: LifeSupport: OK
00:01:28 [WARNING] argos.watsonx: WatsonX: 403 Forbidden — Service ID не добавлен в проект IBM Cloud.
  Исправление:
  1. Открой https://dataplatform.cloud.ibm.com/projects/196146fe-d674-475b-9a1b-4d02f5a77f56/manage
  2. Раздел 'Access Control' → 'Add collaborators'
  3. Добавь ServiceId из WATSONX_API_KEY с ролью Editor
  Или замени WATSONX_API_KEY на IAM-ключ владельца проекта.
00:01:28 [WARNING] argos.core: WatsonX: ключи заданы, но инициализация не удалась — смотри лог выше
00:01:28 [INFO] argos.core: IBM Quantum: токен задан
00:01:28 [INFO] argos.core: Slack: SLACK_BOT_TOKEN не задан
00:01:28 [INFO] argos.core: SerpSearch: backend=serpapi
00:01:32 [INFO] argos.core: GitOps: OK
00:01:32 [INFO] argos.otg: OTGManager инициализирован (android=False, serial=True, jnius=False)
00:01:32 [INFO] argos.core: [WinBridge] 🚀 Запущен (PID 2920, порт 5000)
00:01:32 [INFO] argos.core: OTG Manager: OK
00:01:36 [INFO] argos.core: OwnModel: OK
00:01:36 [INFO] argos.evolver: ArgossEvolver готов (модель=llama3.2:1b v1)
00:01:36 [INFO] argos.core: ArgossEvolver: OK (модель: llama3.2:1b, версия: v1)
00:01:36 [INFO] argos.orangepi: OrangePiBridge init (I2C=bus0 UART=/dev/ttyS3 RS485=/dev/ttyS2)
00:01:36 [INFO] argos.core: OrangePiBridge: OK (платформа=Windows)
00:01:36 [INFO] argos.core: WebExplorer: OK (DuckDuckGo/Wikipedia/GitHub/arXiv)
00:01:41 [INFO] argos.awa: AWA: LazarusProtocol инициализирован
00:01:41 [INFO] argos.shadow_vision: [ShadowVision] Запущен (интервал 5s, модель yolov8n)
00:01:41 [INFO] argos.awa: AWA: ShadowVision запущен
00:01:41 [INFO] argos.awa: AWA: NeuralSwarm инициализирован
00:01:41 [INFO] argos.browser_conduit: BrowserConduit: stub mode (playwright не установлен)
00:01:41 [INFO] argos.awa: AWA: BrowserConduit инициализирован
00:01:41 [INFO] argos.awa: AWA: AirSnitch инициализирован (автостарт выкл)
00:01:41 [INFO] argos.awa: AWA-Core v1.0.0 init | policy=auto | cascade_depth=3
00:01:41 [INFO] argos.awa: AWA-CORE: Все системы жизнеобеспечения активированы.
00:01:47 [INFO] argos.core: ContextDB: подключена к DialogContext
00:01:47 [INFO] argos.core: AWA-Core: OK (Model Splitting активен)
00:01:47 [INFO] argos.self_sustain: SelfSustain: запущен
00:01:47 [INFO] argos.core: SelfSustain: OK
00:01:47 [INFO] argos.core: HealthMonitor: OK
00:01:47 [INFO] argos.core: AIFailover: OK
00:01:47 [INFO] argos.integrator: ╔══════════════════════════════════════════════════════════╗
00:01:47 [INFO] argos.integrator: ║             ARGOS UNIVERSAL INTEGRATOR v3.0              ║
00:01:47 [INFO] argos.integrator: ╚══════════════════════════════════════════════════════════╝
00:01:47 [INFO] argos.encryption: Encryption: ключ загружен из config/master.key
00:01:47 [WARNING] argos.integrator: Stub for LazarusProtocol: LazarusProtocol.__init__() missing 1 required positional argument: 'core'
00:01:47 [INFO] argos.gost: pygost не установлен — используется встроенная реализация (pip install pygost для эталонной)
00:01:47 [WARNING] argos.integrator: Stub for GostKuznyechik: GostKuznyechik.__init__() missing 1 required positional argument: 'key'
00:01:47 [INFO] argos.integrator: ✅ security: 6 loaded
00:01:48 [INFO] argos.gost_p2p: GostP2PSecurity: шифр=Кузнечик pygost=False
00:01:50 [INFO] argos.orangepi: OrangePiBridge init (I2C=bus0 UART=/dev/ttyS3 RS485=/dev/ttyS2)
00:01:50 [INFO] argos.iot: IoTBridge инициализирован. Устройств: 0
00:01:50 [WARNING] argos.integrator: Stub for Any: Any cannot be instantiated
00:01:51 [INFO] argos.integrator: ✅ connectivity: 19 loaded
00:01:51 [INFO] argos.vector: VectorStore: fallback mode forced by ARGOS_VECTOR_FORCE_FALLBACK
00:01:51 [INFO] argos.grist: Grist: отключен через ARGOS_DISABLE_GRIST
00:01:51 [INFO] argos.integrator: ✅ knowledge: 2 loaded
00:01:51 [INFO] argos.integrator: ✅ factory: 3 loaded
00:01:51 [INFO] argos.evolution: Evolution: загружено 10 записей
00:01:51 [INFO] argos.self_model_v2: SelfModelV2 инициализирована
00:01:51 [INFO] argos.integrator: ✅ mind: 3 loaded
00:01:51 [INFO] argos.integrator: ✅ quantum: 4 loaded
00:01:51 [INFO] argos.integrator: ✅ vision: 2 loaded
00:01:51 [INFO] argos.skills: SkillInstance.start: module=argos_skill_content_gen runtime=ContentGen core=ArgosCore
00:01:51 [INFO] argos.skills: Навык загружен: content_gen v1.3.0
00:01:51 [INFO] argos.skills: SkillInstance.start: module=argos_skill_crypto_monitor runtime=CryptoSentinel core=ArgosCore
00:01:51 [INFO] argos.skills: Навык загружен: crypto_monitor v1.1.0
00:01:51 [INFO] argos.skills: SkillInstance.start: module=argos_skill_evolution runtime=ArgosEvolution core=ArgosCore
00:01:51 [INFO] argos.skills: Навык загружен: evolution v2.1.0
00:01:51 [INFO] argos.skills: SkillInstance.start: module=argos_skill_firmware_manager runtime=module core=ArgosCore
00:01:51 [INFO] argos.skills: Навык загружен: firmware_manager v1.0.0
00:01:51 [INFO] argos.skills: SkillInstance.start: module=argos_skill_net_scanner runtime=NetGhost core=ArgosCore
00:01:51 [INFO] argos.skills: Навык загружен: net_scanner v1.2.0
00:01:51 [INFO] argos.skills: SkillInstance.start: module=argos_skill_scheduler runtime=ArgosScheduler core=ArgosCore
00:01:51 [INFO] argos.scheduler: Scheduler запущен. Задач: 1
00:01:51 [INFO] argos.skills: Навык загружен: scheduler v2.0.0
00:01:51 [INFO] argos.skills: SkillInstance.start: module=argos_skill_weather runtime=module core=ArgosCore
00:01:51 [INFO] argos.skills: Навык загружен: weather v1.0.0
00:01:51 [INFO] argos.skills: SkillInstance.start: module=argos_skill_web_scrapper runtime=ArgosScrapper core=ArgosCore
00:01:51 [INFO] argos.skills: Навык загружен: web_scrapper v1.0.1
00:01:51 [INFO] argos.integrator: ✅ skills: 8 loaded
00:01:51 [INFO] argos.modules: Модуль загружен: system_monitor (src.modules.system_monitor_module)
00:01:51 [INFO] argos.modules: Модуль загружен: vision (src.modules.vision_module)
00:01:51 [INFO] argos.modules: Модуль загружен: voice (src.modules.voice_module)
00:01:51 [INFO] argos.integrator: ✅ modules: 3 loaded
00:01:51 [INFO] argos.integrator: ✅ interfaces: 4 loaded
00:01:51 [INFO] argos.claude-templates: ╔══════════════════════════════════════════════════════════╗
00:01:51 [INFO] argos.claude-templates: ║               CLAUDE TEMPLATES INTEGRATOR                ║
00:01:51 [INFO] argos.claude-templates: ╚══════════════════════════════════════════════════════════╝
00:01:52 [INFO] argos.claude-templates: 📦 Обнаружено компонентов: 695
00:01:52 [INFO] argos.claude-templates:   └─ agents: 417
00:01:52 [INFO] argos.claude-templates:   └─ commands: 276
00:01:52 [INFO] argos.claude-templates:   └─ hooks: 0
00:01:52 [INFO] argos.claude-templates:   └─ mcps: 0
00:01:52 [INFO] argos.claude-templates:   └─ settings: 0
00:01:52 [INFO] argos.claude-templates:   └─ skills: 2
00:01:52 [INFO] argos.claude-templates: 🤖 Адаптация агентов: 417
00:01:52 [INFO] argos.claude-templates: ⌨️ Адаптация команд: 276
00:01:52 [INFO] argos.claude-templates: 🪝 Адаптация хуков: 0
00:01:52 [INFO] argos.claude-templates: 🔗 Адаптация MCP: 0
00:01:52 [INFO] argos.claude-templates: 
════════════════════════════════════════════════════════════
00:01:52 [INFO] argos.claude-templates: ══════════════ ИНТЕГРАЦИЯ ШАБЛОНОВ ЗАВЕРШЕНА ═══════════════
00:01:52 [INFO] argos.claude-templates: ════════════════════════════════════════════════════════════
00:01:52 [INFO] argos.claude-templates: 🤖 Агенты:    417
00:01:52 [INFO] argos.claude-templates: ⌨️ Команды:   274
00:01:52 [INFO] argos.claude-templates: 🪝 Хуки:      0
00:01:52 [INFO] argos.claude-templates: 🔗 MCP:       0
00:01:52 [INFO] argos.claude-templates: ════════════════════════════════════════════════════════════
00:01:52 [INFO] argos.integrator: 
════════════════════════════════════════════════════════════
00:01:52 [INFO] argos.integrator: ═══════════════════ ИНТЕГРАЦИЯ ЗАВЕРШЕНА ═══════════════════
00:01:52 [INFO] argos.integrator: ════════════════════════════════════════════════════════════
00:01:52 [INFO] argos.integrator: ✅ security     —  6 loaded
00:01:52 [INFO] argos.integrator: ✅ connectivity — 19 loaded
00:01:52 [INFO] argos.integrator: ✅ knowledge    —  2 loaded
00:01:52 [INFO] argos.integrator: ✅ factory      —  3 loaded
00:01:52 [INFO] argos.integrator: ✅ mind         —  3 loaded
00:01:52 [INFO] argos.integrator: ✅ quantum      —  4 loaded
00:01:52 [INFO] argos.integrator: ✅ vision       —  2 loaded
00:01:52 [INFO] argos.integrator: ✅ skills       —  8 loaded
00:01:52 [INFO] argos.integrator: ✅ modules      —  3 loaded
00:01:52 [INFO] argos.integrator: ✅ interfaces   —  4 loaded
00:01:52 [INFO] argos.integrator: ✅ claude-templates —  3 loaded
00:01:52 [INFO] argos.integrator: ────────────────────────────────────────────────────────────
00:01:52 [INFO] argos.integrator: Итого: 11/11 подсистем OK, 0 ошибок
00:01:52 [INFO] argos.integrator: ════════════════════════════════════════════════════════════
00:01:52 [INFO] argos.core: Integrator: 12 категорий подключено
00:01:52 [INFO] argos.core:   └─ security: shield, gitguard, bootloader, lazarusprotocol, gostcipher...
00:01:52 [INFO] argos.core:   └─ connectivity: p2p, telegram, whatsapp, slack, email...
00:01:52 [INFO] argos.core:   └─ protocol: modbus, ble, lora, zigbee, nfc
00:01:52 [INFO] argos.core:   └─ knowledge: vector, grist
00:01:52 [INFO] argos.core:   └─ factory: flasher, replicator, firmware
00:01:52 [INFO] argos.core:   └─ mind: dreamer, evolution, self_model
00:01:52 [INFO] argos.core:   └─ quantum: ibm, watson, logic, oracle
00:01:52 [INFO] argos.core:   └─ vision: shadow, vision
00:01:52 [INFO] argos.core:   └─ skill: content_gen, crypto_monitor, evolution, firmware_manager, net_scanner...
00:01:52 [INFO] argos.core:   └─ module: system_monitor, vision, voice
00:01:52 [INFO] argos.core:   └─ interface: gui, web, fastapi, shell
00:01:52 [INFO] argos.core:   └─ claude: agents, commands, hooks
00:01:52 [WARNING] argos.constitution: ARGOS mode => normal
00:01:52 [INFO] argos.core: Constitution: ARGOS Constitution Report
00:01:52 [WARNING] argos.core: C2 System: GistC2.__init__() got an unexpected keyword argument 'core'
00:01:52 [INFO] argos.self_model_v2: SelfModelV2 инициализирована
00:01:52 [INFO] argos.core: SelfModelV2: OK
00:01:52 [INFO] argos.dreamer: Dreamer запущен (интервал=3600s)
00:01:52 [INFO] argos.core: Dreamer: OK
00:01:52 [INFO] argos.evolution: Evolution: загружено 10 записей
00:01:52 [INFO] argos.core: EvolutionEngine: OK
00:01:52 [INFO] argos.consciousness: [Consciousness] Загружено: 195 мыслей, 0 синтезов
00:01:52 [INFO] argos.consciousness: CollectiveConsciousness v1.0.0 инициализировано
00:01:52 [INFO] argos.consciousness: [Consciousness] Фоновый цикл: интервал 120s
00:01:52 [INFO] argos.consciousness: [Consciousness] Фоновый цикл запущен
00:01:52 [INFO] argos.core: CollectiveConsciousness: OK
00:01:52 [INFO] argos.core: ArgosCore FINAL v2.0 инициализирован.
00:02:09 [INFO] argos.core: [LocalGPU] Ответ от GPU0-RX580 (localhost:8082)
============================================================
ПРЯМАЯ ПРОВЕРКА GPU
============================================================

AI Mode: local-gpu
Label: Local GPU (Vulkan)

GPU серверы:
  GPU0-RX580: localhost:8082 - ONLINE
  GPU1-Vega11: localhost:8083 - ONLINE
  GPU2-RX560: localhost:8084 - ONLINE

Отправка запроса...

[OK] Ответ получен (225 символов):
Мой статус - я постоянно доступен для общения и выполнения задач. Я могу отвечать на вопросы и помогать с различными задачами, используя информацию и знания, полученные за время своей эволюции. Как я могу помочь тебе сегодня?

============================================================

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
