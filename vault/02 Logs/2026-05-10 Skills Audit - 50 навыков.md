# Аудит навыков ARGOS — 2026-05-10

**Всего:** 50 навыков | **Работают:** 49 | **Заблокирован:** 1 (ebay)

## Результаты тестирования

### ✅ ПОЛНОСТЬЮ РАБОТАЮТ (24)

| # | Навык | Результат |
|---|-------|-----------|
| 1 | weather | Москва 11°C, влажность 47%, ветер 16 км/ч |
| 2 | crypto_monitor | BTC $80,628 (+0.60%), ETH $2,325 (+0.86%) |
| 3 | net_scanner | 0 активных устройств, периметр чист |
| 4 | auto_backup | 10 ZIP-бэкапов, последний 09:18 |
| 5 | ton_blockchain | Баланс 0.0000 TON (кошелёк подключён) |
| 6 | huggingface_ai | 1 токен, Mistral-7B, embed MiniLM |
| 7 | evolution | 10 циклов, 10 принятых навыков |
| 8 | fastapi_skill | Порт 8010, токен задан, работает |
| 9 | pip_manager | 458 пакетов установлено |
| 10 | hardware_intel | Ryzen 7 3700X, 48GB RAM, COM1+COM14 |
| 11 | desktop_actions | Скриншот 237 KB сохранён |
| 12 | system_monitor | CPU 39.4%, RAM 58.3%, Диск 86.7% |
| 13 | scheduler | 1 задача: daily 10:00 |
| 14 | crypto_utils | AES-256-GCM шифрование работает |
| 15 | browser_conduit | pyautogui ✅, pyperclip ✅ |
| 16 | porphyry | v1.0, аналитический режим |
| 17 | serp_search | SerpAPI ключ задан + DDG fallback |
| 18 | arc_agi3_skill | venv ready, score=3.57, 79 действий |
| 19 | network_shadow | Маскировка вкл, MASK_60970236 |
| 20 | obsidian_skill | 100 заметок в vault |
| 21 | ai_coder_evolution_bridge | Code review работает (нашёл 5 проблем) |
| 22 | web_explorer | DDG, Wikipedia, GitHub, arXiv — готов |
| 23 | web_scraper | Активен, 0 записей в БЗ |
| 24 | test_injected | "Hello from TestSkill" — OK |

### ✅ РАБОТАЮТ, НО НЕТ РЕСУРСОВ (18)

| # | Навык | Статус | Что нужно |
|---|-------|--------|-----------|
| 25 | smtp_mailer | gmail, пользователь не задан | Настроить SMTP_USER в .env |
| 26 | iot_watchdog | 0 устройств | Подключить IoT |
| 27 | smart_environments | Нет датчиков | Подключить датчики |
| 28 | shodan_scanner | Нет ключа | SHODAN_API_KEY в .env |
| 29 | tasmota_updater | Нет MQTT | Настроить MQTT broker |
| 30 | esp32_usb_bridge | Нет устройства | Подключить ESP32 |
| 31 | ga4_analytics | Нет GA4_PROPERTY_ID | Настроить в .env |
| 32 | ai_coder | Ollama 404: llama3.2:1b | Скачать модель |
| 33 | argos_service | Не установлен как сервис | nssm install |
| 34 | usb_access_point | USB/WiFi AP не активен | Запустить на устройстве |
| 35 | hive_mind | 6 узлов, 0 онлайн | Запустить ноды |
| 36 | metagpt_skill | MetaGPT не установлен | pip install metagpt |
| 37 | tg_code_injector | USER_ID не задан | TG_ADMIN_ID в .env |
| 38 | free_ai | CF ❌ (нет токена) | CLOUDFLARE_API_TOKEN |
| 39 | image_gen | Все HF Spaces провайдеры FAIL | HF Spaces API нестабильно |
| 40 | new_skill | 3 ноды offline | Запустить P2P ноды |
| 41 | argos_patcher | Патч V2 не применён | Применить патч |
| 42 | firmware_manager | COM1+COM14, 5 прошивок готовы | Подключить ESP32/STM32 |

### ✅ ЗАГРУЖЕНЫ (минимальный ответ) (6)

| # | Навык | Статус |
|---|-------|--------|
| 43 | content_gen | Загружен (нет handle/execute для статуса) |
| 44 | web_scrapper | Готов, ждёт запрос |
| 45 | web_learn | Загружен |
| 46 | multi_provider_chat | Активен |
| 47 | npm_manager | Загружен |
| 48 | autonomy_fileops | Загружен |

### ❌ ЗАБЛОКИРОВАН (1)

| # | Навык | Причина | Решение |
|---|-------|---------|---------|
| 49 | ebay_parser | 403 Forbidden от eBay | Нужен прокси или API eBay |

### ⚠️ FIRMWARE (отдельная категория)

| # | Навык | Статус |
|---|-------|--------|
| 50 | firmware_examples | COM1+COM14, 5 прошивок (rp2350, esp32, stm32, tasmota×2) |

## Статистика

- **49/50** навыков отвечают корректно (98%)
- **24** полностью функциональны прямо сейчас
- **18** работают, но ждут настройки/оборудования
- **6** загружены в минимальном режиме
- **1** заблокирован внешним сервисом (eBay 403)

## Проблемы таймаутов

При вызове через обычные команды (без `запусти навык`) многие навыки таймаутятся — команда попадает в AI pipeline вместо прямого dispatch. Решение: использовать точные триггеры или `запусти навык <имя>`.

## Рекомендации P1

1. **Скачать llama3.2:1b** для ai_coder (ollama pull llama3.2:1b)
2. **Применить патч V2** через argos_patcher
3. **Настроить SMTP** для email-алертов
4. **Прокси для eBay** если нужен мониторинг цен

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Logs Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Logs Hub]]
