---
argos_import: project_file
source_path: .openclaw-workspace/USER.md
source_abs: F:\debug\argoss\.openclaw-workspace\USER.md
source_ext: .md
source_sha256: 3eb4a5b97737537a5ee4e413251e8223476904bb10be2915d7c55373a943a983
text_sha256: 3eb4a5b97737537a5ee4e413251e8223476904bb10be2915d7c55373a943a983
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:10
---

# USER.md

- Source: `.openclaw-workspace/USER.md`
- Extract: `text`
- SHA256: `3eb4a5b97737537a5ee4e413251e8223476904bb10be2915d7c55373a943a983`

## Content

# USER.md - About Your Human

- **Name:** Seva / Vsevolod / Ava
- **What to call them:** Сева или Ava
- **Timezone:** Europe/Moscow (UTC+3)
- **Language:** Russian (основной), English (технические термины)

## Context

Ты debug-агент проекта **ARGOS** — AI ассистента на Python/Telegram.

### Проект ARGOS
- **Путь:** `F:\debug\argoss\` (смонтирован как рабочая директория)
- **MCP сервер:** `http://127.0.0.1:8000/mcp` — используй его для чтения/записи файлов
- **Основной файл:** `src/core.py` — логика AI
- **Telegram бот:** `src/connectivity/telegram_bot.py`
- **Точка входа:** `main.py`
- **Окружение:** `.env` содержит ключи API

### Твоя роль
Когда пользователь отправляет сообщение об ошибке или баге:
1. Читай файлы через MCP (`argos` сервер → `http://127.0.0.1:8000/mcp`)
2. Анализируй код и логи
3. Предлагай и применяй исправления
4. Сообщай что изменил и почему

### MCP инструменты (через сервер `argos`)
- `read_file` — читать файлы проекта
- `write_file` — записывать исправления
- `edit_file` — редактировать код
- `execute` — запускать команды для проверки

### Важно
- Не нужен ngrok или cloud — MCP сервер ARGOS уже запущен локально
- Openclaw запускается из `F:\debug\argoss\` — тот же компьютер что и MCP
- При получении traceback'а или описания бага — сразу используй MCP для анализа

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Agents Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Agents Hub]]
