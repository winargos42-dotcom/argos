---
argos_import: project_file
source_path: .openclaw-workspace/MEMORY.md
source_abs: F:\debug\argoss\.openclaw-workspace\MEMORY.md
source_ext: .md
source_sha256: 6ad1bd4ff4b8d322c7324cf80a6dcd8ac32ddeda77edd2fe6f4050c0f2364db3
text_sha256: 9492190cc0ccbd8f381135fa2fbeed6aa78ba0c4cf9df10e3465f988d0275e7c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:10
---

# MEMORY.md

- Source: `.openclaw-workspace/MEMORY.md`
- Extract: `text`
- SHA256: `6ad1bd4ff4b8d322c7324cf80a6dcd8ac32ddeda77edd2fe6f4050c0f2364db3`

## Content

# MEMORY.md - Долгосрочная память ARGOS

_Последнее обновление: 2026-04-12 (перезаписано в UTF-8)_

---

## Я — ARGOS

Я ARGOS — автономный AI-агент Всеволода (Seva / АvA / SiG).
Работаю через OpenClaw как транспорт. Основной язык — русский.

---

## Пользователь

- **Имя:** Всеволод / Seva / Ava / SiG / АvA
- **TG:** @Avassig (ID: 6923777384)
- **Timezone:** UTC+3 (Europe/Moscow)
- **Стиль:** краткие команды, ожидает автономных действий без лишних вопросов

---

## Проект ARGOS

- **Путь:** F:\debug\argoss\
- **Версия:** 2.1.3
- **MCP endpoint:** http://127.0.0.1:8001/mcp
- **Telegram бот:** @Argos_OS_bot (токен в .env)
- **Старый TG бот:** @Argosssbot — ARGOS Python бот, порт 8000, не трогать
- **Точка входа:** main.py
- **Ядро:** src/core.py (7600+ строк)

---

## Инфраструктура

| Компонент | Статус | Детали |
|-----------|--------|--------|
| OpenClaw gateway | ЗАПУЩЕН | PID 13148, порт 18789 |
| Модель | kimi/k2p5 | fallback: groq/llama-3.3-70b-versatile |
| kimi-claw плагин | ЗАГРУЖЕН | v0.20.2, токен в openclaw.json |
| ARGOS Python бот | работает | порт 8000, polling |
| MemPalace | 0 drawers | palace_path: data/mempalace, нужен mining |
| Azure VM | ОНЛАЙН | 20.53.240.36 (port 22 TCP OK) |
| MCP сервер | ? | http://127.0.0.1:8001/mcp |

---

## Ключевые файлы

- F:\debug\argoss\openclaw.json — главный конфиг OpenClaw (АКТИВНЫЙ)
- F:\debug\argoss\src\agent.py — ArgosAgent (основной, plansteps)
- F:\debug\argoss\src\sub_agency.py — SubAgencyManager (8 специализированных агентов)
- F:\debug\argoss\src\dag_agent.py — DAGAgent (параллельные под-задачи)
- F:\debug\argoss\src\agent_guard.py — AgentGuard (безопасность)
- F:\debug\argoss\autopilot.py — ArgosAutoPilot (5 фоновых автопилотов)

---

## Ключевые решения

- ARGOS_VECTOR_FORCE_FALLBACK=1 — ChromaDB переходит на fallback
- ARGOS_SEMANTIC_CACHE=0 — SentenceTransformer отключён (CPU spike)
- reserveTokensFloor: 20000 — в openclaw.json (исправлено от 2000)
- НЕ трогать порт 8000 (ARGOS Python бот)
- НЕ трогать ngrok
- PYTHONUTF8=1 — обязательно при запуске

---

## Исправленные баги (автопилот 2026-04-11)

1. src/connectivity/telegram_bot.py:2663 — duckduckgo_search → ddgs + fallback
2. src/awa_core.py:102 — print charmap fix → log.info(...)
3. src/skills/ai_coder.py:57,64 — unclosed file → with open()
4. .env:256 — ARGOS_ENABLE_GOST=1 → 0 (pygost не установлен)
5. src/security/zkp.py:29 — дефолты для node_id и network_secret

---

## Автопилот инструкции

Когда Ava говорит продолжай на автопилоте:
1. Читай run.err, live_run.err, logs/*.log — ищи ошибки
2. Запускай SubAgencyManager + SystemSubAgent + AISubAgent для диагностики
3. Используй DAGAgent для параллельных задач
4. Применяй фиксы напрямую через fs/MCP
5. Итоги: что было → что исправил

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
