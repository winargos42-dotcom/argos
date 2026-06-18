# ARGOS Unified State 2026-05-05

Обновлено: `2026-05-05 03:42`
Оператор: `Всеволод (Seva / AvA / SiG)`
Режим: `production`

## Канонические точки

- Проект: `F:\debug\argoss`
- Vault: `F:\debug\аргос`
- SharedMemory: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory`
- Рабочая память ARGOS DB: `F:\debug\argoss\data\memory.db`
- MCP endpoint: `http://127.0.0.1:8000/mcp`

## Текущее положение дел

- ARGOS v2.1.3, MCP :8000 -- **ПЕРЕЗАПУЩЕН 2026-05-05**
- Навыки: 50+ загружено (включая content_gen, crypto_monitor, evolution, firmware_manager)
- AI-провайдеры: **5+ рабочих** (DeepSeek, OpenAI, Azure, Kimi, Gemini) + GPU
- Эволюция: приоритет evolution, 10+ принятых циклов
- Память: 6172 факта, 603 заметки, 9798 рёбер знаний
- MCP: 30 tools OK
- TTS: pyttsx3 активен
- Obsidian: vault F:\debug\аргос, 100+ заметок

## AI Провайдеры (проверены 2026-05-05)

| Провайдер | Статус | Примечание |
|-----------|--------|------------|
| **DeepSeek** | ✅ OK | v4-flash, v4-pro |
| **OpenAI** | ✅ OK | 70+ моделей |
| **Azure OpenAI** | ✅ OK | gpt-4 |
| **Kimi** | ✅ **ПОЧИНЕН** | api.moonshot.ai, k2.6, k2.5 |
| **Gemini** | ✅ **ВКЛЮЧЁН** | 6 ключей готовы |
| **HuggingFace** | ✅ **РАБОТАЕТ** | Fine-Grained, датасеты OK |
| **Cloudflare** | ✅ **ОБНОВЛЁН** | Workers AI доступен |
| **GigaChat** | ⚠️ Отключён | Нет необходимости |
| **YandexGPT** | ⚠️ Отключён | Пустой IAM |
| **Grok** | ❌ Заблокирован | Нужен новый ключ (низкий приоритет) |
| **SERPAPI** | ❌ Закончились запросы | Пополнить баланс |

### HuggingFace детали
- **Токены:** Оба невалидны (Invalid username/password)
- **Inference API:** Не работает без авторизации
- **Space AvaSiG:** Build Error (Docker cache miss)
- **Модели:** Поиск работает, модели доступны

## 3x GPU (llama-server Vulkan)

| Порт | GPU | Vulkan | VRAM | Модель | Роль |
|------|-----|--------|------|--------|------|
| 8082 | RX 580 | Vulkan0 | 4GB | qwen2.5:3b | smart |
| 8083 | Vega 11 | Vulkan2 | 2GB | tinyllama | fast |
| 8084 | RX 560 | Vulkan1 | 4GB | qwen2.5:3b | code |

## Изменения за сегодня

- [03:20-03:42] Полный аудит AI-провайдеров
- [03:30] Kimi исправлен: api.moonshot.cn → api.moonshot.ai
- [03:35] Gemini включён: ARGOS_DISABLE_GEMINI=0
- [03:40] Создан отчёт в Obsidian: 2026-05-05 AI Providers Audit

## Изменения за сегодня (2026-05-05)

- [03:20-03:45] Полный аудит AI-провайдеров
- [03:30] Kimi исправлен: api.moonshot.cn → api.moonshot.ai
- [03:35] Gemini включён: ARGOS_DISABLE_GEMINI=0
- [03:40] Cloudflare токен обновлён (рабочий)
- [03:42] HF токен проверен — Fine-Grained, доступ к датасетам OK
- [03:45] ARGOS перезапущен с обновлённой конфигурацией
- [03:50] TTS (pyttsx3) активен, новые навыки загружены

## Известные риски

- CPU ~100% при тяжёлых прогонах
- RX 580 VRAM = 4GB, требует очистки перед стартом
- Grok key заблокирован — заменить (низкий приоритет)
- SERPAPI запросы исчерпаны — пополнить баланс

## Infrastructure Reconnaissance (анализ 2026-05-05)

### Подтверждённые наблюдения
- **DNS Latency** (`argosssss.win`): TTL propagation delay → 404 при первом обращении
- **JSON-валидация**: Сырой ASM без escaping в `src/self_healing.py:144`
- **SSH-обрывы**: Нестабильные узлы при передаче дампов БД
- **Time Sync Error**: Δt = 8 минут, ломает JWT и цепочки команд
- **Grist recursion**: P2P-узел синхронизирует таблицу саму с собой

### Реальные угрозы
- Colab T4 side-channel (cache timing) — теоретически возможен
- WireGuard mesh уже дает сетевой доступ к нодам

### Нереальные угрозы
- Container escape в Colab (VM isolation)
- Shodan не даёт внутренней топологии
- "Паразитарное слияние" — VPN ≠ ядро

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Human Sessions Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Human Sessions Hub]]
