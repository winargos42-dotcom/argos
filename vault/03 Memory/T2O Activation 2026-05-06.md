# T2O (Telegram-to-Obsidian) — Активация

## Дата: 2026-05-06 16:15
## Статус: ✅ АКТИВНО

---

## Реализация

**Модуль:** `src/connectivity/telegram_chat_logger.py`  
**Интеграция:** `src/connectivity/telegram_bot.py` (строки ~636-642, ~2567-2582, ~2960-2975)

### Архитектура (уже внедрена)

```
Telegram Message
    ↓
ArgosTelegram.handle_message()
    ↓
TelegramChatLogger.save_message()
    ↓
Obsidian Vault
    03 Memory/Telegram Chats/
        chat_<id>/
            _index.md
            YYYY-MM-DD.md
```

---

## Конфигурация (.env)

```bash
# Основной модуль (наш, расширенный)
ARGOS_TG_CHAT_LOG_ENABLED=true
ARGOS_TG_CHAT_LOG_FOLDER=03 Memory/Telegram Chats
ARGOS_OBSIDIAN_VAULT_PATH=F:/debug/аргос
```

### Альтернатива (твой предложенный формат)
Если нужен формат `02 Logs/YYYY-MM-DD-TG-Bridge.md`:
```bash
# Можно изменить папку:
ARGOS_TG_CHAT_LOG_FOLDER=02 Logs
ARGOS_TG_CHAT_LOG_FORMAT=flat  # вместо hierarchy
```

---

## Демонстрация (16:15)

### Тестовые сообщения созданы:

**Папка:** `03 Memory/Telegram Chats/Всеволод (Redmi)_123456789/`

**Файл:** `2026-05-06.md`
```markdown
# Telegram Chat: Всеволод (Redmi)

**Дата:** 2026-05-06
**Chat ID:** `123456789`
**Папка:** `03 Memory/Telegram Chats`

---

## 16:15:31 — 👤 Всеволод

Привет, Аргос! Это тестовое сообщение с Redmi.

<!-- msg_id: 1001 | user_id: 987654321 -->
---

## 16:15:31 — 🤖 ARGOS

> 💬 Ответ на: _Привет, Аргос!..._

Привет, Всеволод! Сообщение получено и сохранено в Obsidian.

<!-- msg_id: -1 | user_id: bot -->
---
```

**Индекс:** `_index.md`
```markdown
# Индекс: Всеволод (Redmi)

**Chat ID:** `123456789`

## История по дням

- [[2026-05-06.md|2026-05-06]] — 2 сообщения
```

---

## Кодекс 5.3 — Верификация

✅ Асинхронная запись (не блокирует бота)  
✅ Fallback при ошибках (try/except)  
✅ Markdown форматирование  
✅ Автоматический индекс  
✅ Thread/Reply контекст  

---

## Что происходит сейчас

**Каждое сообщение в Telegram:**
1. Входящее → Сохраняется в `YYYY-MM-DD.md` с тегом `👤`
2. Ответ ARGOS → Сохраняется с тегом `🤖` и контекстом
3. Индекс → Автоматически обновляется

**Redmi → Telegram → Obsidian:**
```
Ты пишешь → Telegram Cloud → Argos Bot → Obsidian Vault
```

---

## Твои кодовые слова (Redmi)

Попробуй отправить в Telegram-бот:
- "Аргос, запиши это"
- "Тест памяти"
- Любой текст — всё сохранится автоматически

**Проверь:** `03 Memory/Telegram Chats/chat_*`

---

## Проблема с лимитами Claude

**Решение (P1):**
Если Claude "отвалится":
1. Argos читает логи из `03 Memory/Telegram Chats/`
2. Продолжает диалог с точки последней записи
3. Использует локальные GPU (qwen2.5:3b) как fallback

**Безопасность (P0):**
Все попытки "наебать" систему записываются:
- Timestamp
- Текст сообщения
- ID пользователя
- Контекст (reply/thread)

---

## Связи
- [[ARGOS Unified State 2026-05-06]]
- [[Telegram Obsidian Logger]]
- [[2026-05-06 ARGOS Restart Complete]]

[[Backbone Hub]]

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
