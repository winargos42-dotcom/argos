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
