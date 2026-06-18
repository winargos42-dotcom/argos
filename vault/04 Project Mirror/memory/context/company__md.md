---
argos_import: project_file
source_path: memory/context/company.md
source_abs: F:\debug\argoss\memory\context\company.md
source_ext: .md
source_sha256: d408507662b7adf05838747ed771f53fff930a5c317459cd80c56f81c693b491
text_sha256: d408507662b7adf05838747ed771f53fff930a5c317459cd80c56f81c693b491
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# company.md

- Source: `memory/context/company.md`
- Extract: `text`
- SHA256: `d408507662b7adf05838747ed771f53fff930a5c317459cd80c56f81c693b491`

## Content

# Context — ARGOS Project

## Author
- **Всеволод** (Seva / АvA / SiG) — единственный разработчик / owner проекта

## Team Roles (Task Owners)
Все роли — это Сева. Один разработчик, носит разные "шляпы" в зависимости от контекста задачи.
- **infra** — Инфраструктура (LLM-движки, дисковые структуры)
- **platform** — Платформенные сервисы (кэш, БД, внешние API)
- **sre** — Надёжность и мониторинг (circuit breaker, self-healing)
- **app** — Приложение (контейнеры, логирование, UX)

## Tools & Services Used
| Tool | Purpose |
|------|---------|
| Redis | Кэширование (TTL=1h для web_learn) |
| PostgreSQL | Хранение результатов поиска, full-text search |
| Docker | Контейнеризация модулей |
| Ollama | Локальный запуск LLM-моделей |
| Llama.cpp | Оффлайн LLM inference |
| ArgoCD | GitOps синк конфигураций |
| Watchtower | Авто-обновление контейнеров |
| Cloudflare Workers AI | Edge inference без API-ключей |
| GitHub Actions | CI/CD пайплайны |

## Language
Рабочий язык задач и документации: **русский**.

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
