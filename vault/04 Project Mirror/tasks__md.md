---
argos_import: project_file
source_path: tasks.md
source_abs: F:\debug\argoss\tasks.md
source_ext: .md
source_sha256: 279ecd86b1bdc52317ab28b6d2b6efa6ec2c31a4227ac52275c36c5c067d31a4
text_sha256: bb66d663502936f3c1eda9216c45644d4513ae6aec62c5c7d9a92231d6f12657
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# tasks.md

- Source: `tasks.md`
- Extract: `text`
- SHA256: `279ecd86b1bdc52317ab28b6d2b6efa6ec2c31a4227ac52275c36c5c067d31a4`

## Content

# Tasks

- [ ] P1 | owner: infra | ETA: 2026-04-05 — Развернуть локальный Llama.cpp и настроить маршрутизацию запросов через него как первичный оффлайн LLM.
- [ ] P1 | owner: platform | ETA: 2026-04-06 — Ввести Redis TTL=1h для DuckDuckGo web_learn + aiohttp пайплайн, убрать requests.
- [ ] P1 | owner: platform | ETA: 2026-04-07 — Сохранение результатов поиска в PostgreSQL с full-text search для повторных запросов без сети.
- [ ] P2 | owner: sre | ETA: 2026-04-06 — Добавить circuit breaker + авто‑fallback провайдера поиска; слать алерт в лог при 3 неудачах.
- [ ] P2 | owner: sre | ETA: 2026-04-07 — Настроить watchtower/self-healing контейнеры и GitOps (ArgoCD) синк конфигураций.
- [ ] P2 | owner: infra | ETA: 2026-04-08 — Перенести кэш/индексы в RAM‑диск; разделить Ollama на лёгкую (в RAM) и тяжёлую (на диске) модели.
- [ ] P3 | owner: app | ETA: 2026-04-05 — Изолировать генератор контента в Docker-контейнер с ограничением 512 MB.
- [ ] P3 | owner: app | ETA: 2026-04-04 — Использовать repr() для логирования объектов во всех модулях web_learn/duckduckgo.
- [ ] P2 | owner: platform | ETA: 2026-04-06 — Интегрировать Cloudflare Workers AI/AI Gateway для edge inference и проксирования без API-ключей; обвязать serverless роуты.

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
