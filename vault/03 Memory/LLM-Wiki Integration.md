# LLM-Wiki Интеграция в ARGOS

**Дата:** 2026-05-07 (обновлено)
**Версия:** v1.1
**Статус:** ✅ Внедрено и протестировано

---

## Что такое LLM-Wiki в ARGOS

Автоматическая система управления знаниями на базе Obsidian + LLM.

### Архитектура

```
Obsidian Vault (F:\debug\аргос)
├── 03 Memory/
│   ├── Telegram Chats/     # Raw sources (сырые логи)
│   └── Wiki/               # Переработанные знания
│       ├── concepts/       # Концепты и термины
│       ├── people/         # Люди и контакты
│       ├── topics/         # Темы
│       ├── sessions/       # Сессии
│       └── index.md        # Карта знаний
├── 04 Project Mirror/      # Исходники проекта
└── AGENTS.md / CLAUDE.md   # Schema (правила для агента)
```

---

## MCP Инструменты

### 1. wiki_ingest

Инжест Telegram чата в wiki-формат.

**Использование:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "wiki_ingest",
    "arguments": {
      "chat_id": "6923777384"
    }
  }
}
```

**Что делает:**
- Читает логи из `03 Memory/Telegram Chats/chat_<id>/`
- Создает wiki-страницы в `03 Memory/Wiki/sessions/telegram_<id>/`
- Извлекает концепты (технические термины)
- Создает связи между страницами (`[[wikilinks]]`)
- Обновляет глобальный `index.md`

### 2. wiki_lint

Проверка целостности Obsidian vault.

**Использование:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "wiki_lint",
    "arguments": {}
  }
}
```

**Проверки:**
- 🔴 Битые `[[wikilinks]]`
- 🟡 Устаревшие страницы (>180 дней)
- 🟠 Orphan-страницы (нет входящих ссылок)
- 🔵 Дубликаты заголовков

**Отчет сохраняется в:** `02 Logs/lint_report_YYYYMMDD_HHMM.md`

### 3. wiki_query

Запрос к базе знаний на естественном языке.

**Использование:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "wiki_query",
    "arguments": {
      "question": "Какие AI провайдеры использует ARGOS?"
    }
  }
}
```

**Алгоритм:**
1. Извлекает ключевые слова из вопроса
2. Ищет релевантные страницы (score-based)
3. Собирает контекст из топ-5 страниц
4. Отправляет вопрос + контекст в LLM
5. Возвращает ответ с источниками (`[[wiki-link]]`)

---

## Файлы модуля

```
src/llm_wiki/
├── __init__.py              # Экспорт классов
├── telegram_ingest.py       # Auto-ingest
├── obsidian_lint.py         # Lint checker
└── wiki_query.py            # LLM-query engine
```

---

## Примеры использования

### Через MCP API

```bash
# Инжест чата
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"wiki_ingest","arguments":{"chat_id":"6923777384"}}}'

# Проверка vault
# curl ... wiki_lint

# Запрос к базе знаний
# curl ... wiki_query
```

### Через Telegram

```
wiki_ingest 6923777384
wiki_lint
wiki_query Какие GPU использует ARGOS?
```

---

## Интеграция с AutoGPT

Phase P2 (Memory → Dataset) теперь использует LLM-Wiki:

1. **Ingest** (04:00 AM): Авто-обработка новых Telegram-логов
2. **Lint** (еженедельно): Проверка целостности vault
3. **Query**: Ответы на вопросы из базы знаний

---

## Ссылки

- Оригинал LLM-Wiki: https://habr.com/ru/articles/1031970/
- Andrej Karpathy: https://karpathy.ai/

---

*Внедрено автоматически ARGOS*

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
