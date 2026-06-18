---
argos_import: project_file
source_path: argos_restart_out.txt
source_abs: F:\debug\argoss\argos_restart_out.txt
source_ext: .txt
source_sha256: 4e0edd68ccd99205b181fd66d10f6df22cefc5b97d19aed0a05a6e43f15fe011
text_sha256: d15a5d2acee5fef06b4a5c9eefbd119d0fd3afee0dc03f008ca6f9c9645bfa68
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-06 12:50:07
---

# argos_restart_out.txt

- Source: `argos_restart_out.txt`
- Extract: `text`
- SHA256: `4e0edd68ccd99205b181fd66d10f6df22cefc5b97d19aed0a05a6e43f15fe011`

## Content

12:46:01 [INFO] argos.eventbus: EventBus запущен (history=500)
12:46:01 [INFO] argos.main: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12:46:01 [INFO] argos.main:  ARGOS UNIVERSAL OS v2.1.3 — BOOT
12:46:01 [INFO] argos.main: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12:46:02 [INFO] argos.encryption: Encryption: ключ загружен из config/master.key
12:46:02 [INFO] argos.main: [SHIELD] AES-256 активирован
12:46:02 [INFO] argos.main: [ROOT] ⚠️ Обычные права пользователя (Windows). Некоторые функции недоступны.
12:46:02 [INFO] argos.db: DB инициализирована: data/argos_memory.db
12:46:02 [INFO] argos.main: [DB] SQLite ready → data/argos.db
12:46:04 [INFO] argos.main: [GEO] {'ip': '178.130.47.10', 'country': 'United States', 'region': 'Arizona', 'city': 'Phoenix', 'isp': 'Global Connectivity Solutions LLP', 'lat': 33.4532, 'lon': -112.0748, 'timezone': 'America/Phoenix'}
12:46:04 [INFO] argos.main: [ADMIN] Файловый менеджер и flasher готовы
12:46:04 [INFO] argos.core: TTS: OK
12:46:07 [INFO] argos.core: Gemini: OK
12:46:07 [INFO] argos.core: [Ollama] Проверяю доступность: http://localhost:11434/api/tags
12:46:07 [INFO] argos.core: [Ollama] ✅ Уже запущен (http://localhost:11434/api/tags)
12:46:07 [INFO] argos.core: Ollama: ✅ доступна (резервный провайдер готов)
12:46:07 [INFO] argos.core: GigaChat недоступен — нет credentials
12:46:07 [INFO] argos.core: YandexGPT недоступен — нет IAM/FOLDER
12:46:07 [INFO] argos.core: Kimi: конфигурация обнаружена (KIMI_API_KEY)
12:46:07 [INFO] argos.vector: VectorStore: fallback mode forced by ARGOS_VECTOR_FORCE_FALLBACK
12:46:07 [INFO] argos.memory: Vector warmup: indexed 180 docs
12:46:07 [INFO] argos.memory: Vector warmup: scheduled in background (180 docs)
12:46:09 [INFO] argos.thought_book: ThoughtBook инициализирована: 191 промтов, 10 частей.
12:46:09 [INFO] argos.core: Память: OK
12:46:09 [INFO] argos.hardware_guard: Hardware guard: ON
12:46:09 [INFO] argos.core: Homeostasis: OK
12:46:09 [INFO] argos.curiosity: Curiosity: автономный режим запущен.
12:46:09 [INFO] argos.core: Curiosity: OK
12:46:09 [INFO] argos.scheduler: Scheduler запущен. Задач: 1
12:46:09 [INFO] argos.core: Планировщик: OK
12:46:09 [INFO] argos.alerts: AlertSystem запущен. Интервал: 30s
12:46:09 [INFO] argos.core: Алерты: OK
12:46:09 [INFO] argos.core: Vision: OK
12:46:09 [INFO] argos.skills: SkillInstance.start: module=argos_skill_content_gen runtime=ContentGen core=ArgosCore
12:46:09 [INFO] argos.skills: Навык загружен: content_gen v1.3.0
12:46:09 [INFO] argos.skills: SkillInstance.start: module=argos_skill_crypto_monitor runtime=CryptoSentinel core=ArgosCore
12:46:09 [INFO] argos.skills: Навык загружен: crypto_monitor v1.1.0
12:46:09 [INFO] argos.skills: SkillInstance.start: module=argos_skill_evolution runtime=ArgosEvolution core=ArgosCore
12:46:09 [INFO] argos.skills: Навык загружен: evolution v2.1.0
12:46:09 [INFO] argos.skills: SkillInstance.start: module=argos_skill_firmware_manager runtime=module core=ArgosCore
12:46:09 [INFO] argos.skills: Навык загружен: firmware_manager v1.0.0
12:46:09 [INFO] argos.skills: SkillInstance.start: module=argos_skill_net_scanner runtime=NetGhost core=ArgosCore
12:46:09 [INFO] argos.skills: Навык загружен: net_scanner v1.2.0
12:46:09 [INFO] argos.skills: SkillInstance.start: module=argos_skill_scheduler runtime=ArgosScheduler core=ArgosCore
12:46:09 [INFO] argos.scheduler: Scheduler запущен. Задач: 1
12:46:09 [INFO] argos.skills: Навык загружен: scheduler v2.0.0
12:46:09 [INFO] argos.skills: SkillInstance.start: module=argos_skill_weather runtime=module core=ArgosCore
12:46:09 [INFO] argos.skills: Навык загружен: weather v1.0.0
12:46:09 [INFO] argos.skills: SkillInstance.start: module=argos_skill_web_scrapper runtime=ArgosScrapper core=ArgosCore
12:46:09 [INFO] argos.skills: Навык загружен: web_scrapper v1.0.1
12:46:09 [INFO] argos.skills: SkillInstance.start: module=src.skills.ai_coder runtime=AICoder core=ArgosCore
12:46:09 [INFO] argos.skills: SkillInstance.start: module=src.skills.ai_coder_evolution_bridge runtime=AICoderEvolutionBridge core=ArgosCore
12:46:10 [INFO] argos.skills: SkillInstance.start: module=src.skills.arc_agi3_skill runtime=ARC3Agent core=ArgosCore
12:46:10 [INFO] argos.skills: SkillInstance.start: module=src.skills.argos_patcher runtime=module core=ArgosCore
12:46:10 [INFO] argos.skills: SkillInstance.start: module=src.skills.argos_service runtime=module core=ArgosCore
12:46:10 [INFO] argos.skills: SkillInstance.start: module=src.skills.auto_backup runtime=AutoBackup core=ArgosCore
12:46:10 [INFO] argos.backup: AutoBackup запущен, интервал 6 ч
12:46:10 [INFO] argos.skills: SkillInstance.start: module=src.skills.autonomy_fileops runtime=AutonomyFileOps core=ArgosCore
12:46:10 [INFO] argos.skills: SkillInstance.start: module=src.skills.browser_conduit runtime=BrowserConduit core=ArgosCore
12:46:10 [INFO] argos.skills: SkillInstance.start: module=src.skills.crypto_utils runtime=CryptoUtils core=ArgosCore
12:46:10 [INFO] argos.skills: SkillInstance.start: module=src.skills.desktop_actions runtime=DesktopActionsSkill core=ArgosCore
12:46:10 [INFO] argos.skills: SkillInstance.start: module=src.skills.ebay_parser runtime=EbayParser core=ArgosCore
12:46:10 [INFO] argos.skills: SkillInstance.start: module=src.skills.esp32_usb_bridge runtime=ESP32UsbBridge core=ArgosCore
12:46:10 [INFO] argos.skills: SkillInstance.start: module=src.skills.fastapi_skill runtime=FastAPISkill core=ArgosCore
12:46:12 [INFO] argos.skills: SkillInstance.start: module=src.skills.firmware_examples runtime=FirmwareExamplesLoader core=ArgosCore
12:46:12 [INFO] argos.skills: SkillInstance.start: module=src.skills.free_ai runtime=FreeAIProvider core=ArgosCore
12:46:12 [INFO] argos.skills: SkillInstance.start: module=src.skills.ga4_analytics runtime=GA4Analytics core=ArgosCore
12:46:12 [INFO] argos.skills: SkillInstance.start: module=src.skills.hardware_intel runtime=module core=ArgosCore
12:46:12 [INFO] argos.skills: SkillInstance.start: module=src.skills.hive_mind runtime=module core=ArgosCore
12:46:13 [INFO] argos.skills: SkillInstance.start: module=src.skills.huggingface_ai runtime=HuggingFaceAI core=ArgosCore
12:46:14 [INFO] argos.skills: SkillInstance.start: module=src.skills.image_gen runtime=ImageGenSkill core=ArgosCore
12:46:14 [INFO] argos.skills: SkillInstance.start: module=src.skills.iot_watchdog runtime=IoTWatchdog core=ArgosCore
12:46:14 [INFO] argos.skills: SkillInstance.start: module=src.skills.metagpt_skill runtime=MetaGPTSkill core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.multi_provider_chat runtime=MultiProviderChat core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.network_shadow runtime=module core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.new_skill runtime=P2PNetworkSkill core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.npm_manager runtime=NpmManager core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.obsidian_skill runtime=ObsidianSkill core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.pip_manager runtime=PipManager core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.porphyry runtime=PorphyryTriad core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.serp_search runtime=SerpSearch core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.shodan_scanner runtime=ShodanScanner core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.smart_environments runtime=module core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.smtp_mailer runtime=SMTPMailer core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.system_monitor runtime=SystemMonitor core=ArgosCore
12:46:15 [INFO] argos.sysmon: SystemMonitor запущен, интервал 30 сек
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.tasmota_updater runtime=TasmotaUpdater core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.test_injected runtime=TestSkill core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.tg_code_injector runtime=TGCodeInjector core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.ton_blockchain runtime=TonBlockchain core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.usb_access_point runtime=USBGadgetAP core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.web_explorer runtime=ArgosWebExplorer core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.web_learn runtime=WebLearn core=ArgosCore
12:46:15 [INFO] argos.skills: SkillInstance.start: module=src.skills.web_scraper runtime=WebScraper core=ArgosCore
12:46:15 [INFO] argos.core: SkillLoader: OK
12:46:15 [INFO] argos.core: 📦 Обнаружено manifest-навыков: 8 | ✅ Навык 'content_gen' v1.3.0 загружен. | ✅ Навык 'crypto_monitor' v1.1.0 загружен. | ✅ Навык 'evolution' v2.1.0 загружен. | ✅ Навык 'firmware_manager' v1.0.0 загружен. | ✅ Навык 'net_scanner' v1.2.0 загружен. | ✅ Навык 'scheduler' v2.0.0 загружен. | ✅ Навык 'weather' v1.0.0 загружен. | ✅ Навык 'web_scrapper' v1.0.1 загружен. | Импорт всех skills (src/skills) → PASS 48/48 | ✅ ai_coder | ✅ ai_coder_evolution_bridge | ✅ arc_agi3_skill | ✅ argos_patcher | ✅ argos_service | ✅ auto_backup | ✅ autonomy_fileops | ✅ browser_conduit | ✅ content_gen (already loaded) | ✅ crypto_monitor (already loaded) | ✅ crypto_utils | ✅ desktop_actions | ✅ ebay_parser | ✅ esp32_usb_bridge | ✅ evolution (already loaded) | ✅ fastapi_skill | ✅ firmware_examples | ✅ free_ai | ✅ ga4_analytics | ✅ hardware_intel | ✅ hive_mind | ✅ huggingface_ai | ✅ image_gen | ✅ iot_watchdog | ✅ metagpt_skill | ✅ multi_provider_chat | ✅ net_scanner (already loaded) | ✅ network_shadow | ✅ new_skill | ✅ npm_manager | ✅ obsidian_skill | ✅ pip_manager | ✅ porphyry | ✅ scheduler (already loaded) | ✅ serp_search | ✅ shodan_scanner | ✅ smart_environments | ✅ smtp_mailer | ✅ system_monitor | ✅ tasmota_updater | ✅ test_injected | ✅ tg_code_injector | ✅ ton_blockchain | ✅ usb_access_point | ✅ web_explorer | ✅ web_learn | ✅ web_scraper | ✅ web_scrapper (already loaded) | SkillLoader load_all (manifest навыки) → PASS 8/8
12:46:15 [INFO] argos.core: [SKILLS] startup loaded=50 | import_all=48/48 | manifest=8/8
12:46:15 [INFO] argos.core: DAG Manager: OK
12:46:15 [INFO] argos.core: GitHub Marketplace: OK
12:46:15 [INFO] argos.core: OPi GPIO patch: GPIO=False I2C=False
12:46:15 [INFO] argos.iot: IoTBridge инициализирован. Устройств: 0
12:46:15 [INFO] argos.core: IoT Bridge: OK (0 устройств)
12:46:15 [INFO] argos.core: IoT Emulator Manager: OK
12:46:15 [INFO] argos.core: Mesh Network: OK (0 устройств)
12:46:15 [INFO] argos.gateway: Шлюзы загружены: 2
12:46:15 [INFO] argos.core: Gateway Manager: OK
12:46:16 [INFO] argos.industrial: KNXBridge init | xknx=True
12:46:16 [INFO] argos.industrial: LonWorksBridge init | port=2
12:46:16 [INFO] argos.industrial: MBusBridge init | mbus_lib=False
12:46:16 [INFO] argos.industrial: OPCUABridge init | opcua=False
12:46:16 [INFO] argos.industrial: IndustrialProtocolsManager init | KNX/LON/M-Bus/OPC-UA
12:46:16 [INFO] argos.core: Industrial Protocols: OK (KNX/LON/M-Bus/OPC-UA)
12:46:16 [INFO] argos.platform_admin: PlatformAdmin init | OS=Windows android=False termux=False
12:46:16 [INFO] argos.core: PlatformAdmin: OK (os=Windows)
12:46:16 [INFO] argos.smart: SmartSystems: загружено 5 систем
12:46:16 [INFO] argos.core: Smart Systems: OK (5 систем)
12:46:16 [INFO] argos.core: Home Assistant bridge: OFF
12:46:16 [INFO] argos.modules: Модуль загружен: system_monitor (src.modules.system_monitor_module)
12:46:16 [INFO] argos.modules: Модуль загружен: vision (src.modules.vision_module)
12:46:16 [INFO] argos.modules: Модуль загружен: voice (src.modules.voice_module)
12:46:16 [INFO] argos.core: 🧩 Modules: 3 загружено |   system_monitor, vision, voice
12:46:16 [INFO] argos.core: ToolCalling: OK (6 инструментов)
12:46:16 [INFO] argos.core: Awareness: OK
12:46:16 [INFO] argos.eventbus: EventBus запущен (history=500)
12:46:16 [INFO] argos.core: EventBus: OK
12:46:16 [INFO] argos.core: IoTHub: OK
12:46:16 [INFO] argos.life_support: ExpenseMonitor init
12:46:16 [INFO] argos.life_support: EarningEngine init
12:46:16 [INFO] argos.life_support: ArgosLifeSupport init ✅
12:46:16 [INFO] argos.core: LifeSupport: OK

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
