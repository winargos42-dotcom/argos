# Telegram → Obsidian Chat Logger

## Дата настройки: 2026-05-06

---

## Что реализовано

Автоматическое сохранение ВСЕХ сообщений из Telegram-чатов в Obsidian vault в структурированном виде.

### Структура сохранения

```
📁 03 Memory/Telegram Chats/
  📁 chat_123456789/
    📄 _index.md          # Индекс всех дней
    📄 2026-05-06.md      # Сообщения за день
    📄 2026-05-07.md
```

### Формат сообщения

```markdown
## 15:30:45 — 👤 Всеволод

Привет, ARGOS!

<!-- msg_id: 12345 | user_id: 987654321 -->
---

## 15:31:02 — 🤖 ARGOS

ARGOS [Auto]

Привет! Чем могу помочь?

<!-- msg_id: -1 | user_id: bot -->
---
```

---

## Конфигурация (.env)

```bash
# Включить логирование
ARGOS_TG_CHAT_LOG_ENABLED=true

# Папка в Obsidian vault
ARGOS_TG_CHAT_LOG_FOLDER=03 Memory/Telegram Chats

# Путь к vault
ARGOS_OBSIDIAN_VAULT_PATH=F:/debug/аргос
```

---

## Файлы

- `src/connectivity/telegram_chat_logger.py` — модуль логирования
- `src/connectivity/telegram_bot.py` — интеграция (строки ~636-642, ~2567-2582, ~2960-2975)

---

## Возможности

✅ Сохранение входящих сообщений (с timestamp, именем, ID)  
✅ Сохранение ответов бота (с пометкой "ARGOS")  
✅ Группировка по дням (отдельный файл на каждый день)  
✆ Автоматический индекс (_index.md ссылками на все дни)  
✅ Thread/reply context (сохраняется текст оригинального сообщения)  
✅ Markdown форматирование  

---

## Тестирование

После перезапуска ARGOS:
1. Отправь сообщение боту в Telegram
2. Проверь папку `03 Memory/Telegram Chats/`
3. Должен появиться файл с текущей датой

---

## Связи
- [[ARGOS Unified State 2026-05-06]]
- [[Telegram Bot Configuration]]

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
