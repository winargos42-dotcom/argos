---
type: error-audit
date: 2026-05-15
scope: telegram-history + runtime-logs
severity: critical
tags: [argos, errors, audit, telegram, bugfix, p0]
---

# 🐛 ARGOS — Отчёт об ошибках (15.05.2026)

> Полный аудит истории Telegram (1680+ сообщений, 3–12 мая) + логов работающих сервисов

## 📊 Сводка по категориям

| Категория | Кол-во | Серьёзность |
|-----------|--------|-------------|
| Timeout (нет ответа AI) | 30+ | 🔴 Critical |
| Офлайн (все провайдеры недоступны) | 15+ | 🔴 Critical |
| Ollama/GPU не отвечает | 7+ | 🔴 Critical |
| Gemini geo-blocked | 4+ | 🟡 High |
| CPU 100% / перегрев 86°C | 3+ | 🟡 High |
| Polling conflict (дубль бота) | 2+ | 🟡 High |
| Fake .env ключ перезаписал реальный | 1 | 🔴 Critical |
| Curiosity garbage insights | 1 | 🟠 Medium |
| ShadowVision AttributeError | 1 | 🟠 Medium |
| Photo analysis NoneType crash | 1 | 🟠 Medium |
| Vulkan GPU OOM | 3+ | 🟠 High |
| LoRA training TypeError | 1 | 🟠 Medium |
| Ngrok auth failure | 1 | 🟡 Medium |
| Unclosed SSL/file handles | 2 | 🟢 Low |

## 🔴 КРИТИЧЕСКИЕ ОШИБКИ

### 1. Провайдерный каскадный таймаут
**Что**: Когда DeepSeek/Gemini/Groq не отвечают, система последовательно ждёт 10с на каждом → 30с пустого ожидания → `⚡ Офлайн-режим`

**Где**: `src/ai_failover.py` — `_DEFAULT_ORDER = ["kimi", "deepseek"]` (всего 2 провайдера!)
**Когда**: 7–12 мая, каждый день

**Почему**: Нет circuit breaker на уровне Telegram bridge. Dead провайдеры не отключаются автоматически.

### 2. Fake .env ключ перезаписал реальный
**Что**: Строка 68 `.env`: `DEEPSEEK_API_KEY=your_key_here` перезаписала реальный ключ на строке 270. `ARGOS_AI_MODE` дублировался 3 раза.

**Где**: `/home/ava/Projects/argoss/.env`
**Влияние**: DeepSeek полностью не работал, пока placeholder был первым

### 3. Нет автозапуска GPU серверов
**Что**: После перезагрузки Ollama GPU серверы не стартуют. Результат: `No API provider registered for api: ollama` × 7

**Где**: `scripts/argos_start_all.sh` — нет `ollama_three.py`

### 4. Системные ресурсы на пределе
**Что**: CPU 100%, RAM 90%, диск 94.7% (5GB свободно), температура 86°C

**Где**: `argos.log` — health alerts
**Влияние**: Таймауты, OOM, крашы

## 🟡 ВЫСОКИЕ ОШИБКИ

### 5. Gemini geo-blocked + 5 мёртвых ключей
**Что**: `400 FAILED_PRECONDITION: User location is not supported` — Россия/Хабаровск. 5 истёкших ключей не удалены.

**Где**: `.env` — `GEMINI_API_KEY_*` (5 штук), `ai_router.py`

### 6. Telegram Bot 409 Conflict
**Что**: `terminated by other getUpdates request` — два экземпляра бота конкурируют за polling

**Где**: `bot_stderr.log`, `src/connectivity/telegram_bot.py`
**Решение**: PID file + lock при старте

### 7. Две версии telegram_bot.py
**Что**: `src/telegram_bot.py` (старая) и `src/connectivity/telegram_bot.py` (новая с патчами). Старая НЕ имеет FastPath, TimeoutFallback, Vision adapter.

**Риск**: Если запущена старая — все патчи 10–11 мая не работают

### 8. Kimi/K2P5 таймауты
**Что**: Каждый запрос к Kimi K2P5 → таймаут 30с → fallback на `surface_error`

**Где**: `kimi_bridge.py` — 60с таймаут, нет streaming

### 9. Vulkan GPU OOM
**Что**: `ErrorOutOfDeviceMemory` при загрузке DeepSeek-Coder-V2-Lite, phi4-mini

**Где**: `llama-server.err`, `gpu2_debug_err.log`

## 🟠 СРЕДНИЕ ОШИБКИ

### 10. Curiosity module — garbage insights
**Что**: `insight_insight_insight_insight_...` × 44 — рекурсивная конкатенация ключей

**Где**: `src/curiosity.py`
**Влияние**: Memory pollution, мусор в Obsidian

### 11. ShadowVision.look_at_screen() — AttributeError
**Что**: `core.py:6231` вызывает `self.vision.look_at_screen()`, но метод не существует

**Где**: `src/core.py`
**Решение**: Добавить метод или `hasattr` guard

### 12. Photo analysis — NoneType crash
**Что**: `'NoneType' object is not subscriptable` при анализе фото

**Где**: `src/connectivity/telegram_bot.py` — `handle_photo`
**Решение**: `_analyze_photo_file()` adapter (патч от 11 мая, только в connectivity версии)

### 13. LoRA training — SFTTrainer TypeError
**Что**: `SFTTrainer.__init__() got an unexpected keyword argument 'max_seq_length'`

**Где**: `lora_training_err.log`

### 14. Ngrok — ERR_NGROK_4018
**Что**: Туннель не работает без authtoken

**Где**: `.ngrok.err.log`

## 🕐 Хронология инцидентов

| Дата | Инцидент | Решение |
|------|----------|---------|
| 3–6 мая | Ollama не отвечает (GPU не стартуют) | Ручной запуск `ollama_three.py` |
| 6 мая | Raw error leak в Telegram | `_normalize_core_result()` + `_run_core_with_timeout()` |
| 7 мая | **100% timeout** — бот не отвечает | CPU 100%, все провайдеры down |
| 8 мая | **0 ответов за весь день** | Fine-tuning запросы зависли |
| 9 мая | Частичное восстановление, Gemini geo-blocked | — |
| 10 мая | **Root cause найден**: dead провайдеры в начале маршрута, fake .env ключ | Переупорядочен `ai_router.py`, убран placeholder, таймауты 30→10с |
| 10 мая | Timeout Fallback Patch | `_offline_answer()` fallback для Direct команд |
| 11 мая | Stale PID 19032, 409 Conflict | Kill + restart, `+`/`++` FastPath |
| 11 мая | Photo analysis crash | `_analyze_photo_file()` adapter |
| 12 мая | Офлайн продолжается | Только `?` (help) работает |

## 🛠️ План исправлений

### P0 — Немедленно
- [ ] Валидация `.env` при старте: детектить `your_key_here`, пустые ключи, дубликаты
- [ ] Автозапуск GPU серверов в `argos_start_all.sh`
- [ ] Унифицировать `telegram_bot.py` — слить патчи из `connectivity/` в `src/`
- [ ] `asyncio.wait_for` timeout 30s в `handle_message`

### P1 — Скоро
- [ ] Удалить 5 мёртвых Gemini ключей + добавить health-check провайдеров
- [ ] Расширить `ai_failover._DEFAULT_ORDER` — все доступные провайдеры
- [ ] Починить Curiosity `insight_insight_` рекурсию
- [ ] Добавить `ShadowVision.look_at_screen()` или `hasattr` guard
- [ ] Exponential backoff: 30с → 60с → 120с → 300с

### P2 — Потом
- [ ] Ограничить Kimi `_messages` (max 20 turns)
- [ ] PID file + stale process detection
- [ ] WebLearn quality gate (не создавать skill при 0 chars context)
- [ ] Evolution skill auto-review feedback loop
- [ ] Почистить диск (94.7% занято)

---

_Отчёт сгенерирован автоматически на основе анализа 1680+ сообщений Telegram и логов ARGOS._