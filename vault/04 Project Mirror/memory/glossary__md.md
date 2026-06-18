---
argos_import: project_file
source_path: memory/glossary.md
source_abs: F:\debug\argoss\memory\glossary.md
source_ext: .md
source_sha256: c50304937077502af273fb337a50b7e73659ec45bee6c0ac8f7b0ebe450b1676
text_sha256: c50304937077502af273fb337a50b7e73659ec45bee6c0ac8f7b0ebe450b1676
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# glossary.md

- Source: `memory/glossary.md`
- Extract: `text`
- SHA256: `c50304937077502af273fb337a50b7e73659ec45bee6c0ac8f7b0ebe450b1676`

## Content

# Glossary — ARGOS Project

## Acronyms & Tools
| Term | Meaning |
|------|---------|
| ARGOS | Autonomous Realtime General-purpose Operating System — Argos Universal OS |
| AWA-Core | Центральный координатор модулей, capability-routing, cascade pipelines |
| ColibriAsmEngine | Ассемблер/дизассемблер: x86, ARM Thumb, AVR, ARM64, MIPS |
| LLM | Large Language Model |
| TTS | Text-to-Speech |
| STT | Speech-to-Text |
| VAD | Voice Activity Detection |
| IoT | Internet of Things |
| P2P | Peer-to-Peer |
| TTL | Time To Live (Redis cache expiry) |
| ArgoCD | GitOps continuous delivery tool |
| SRE | Site Reliability Engineering |
| CI/CD | Continuous Integration / Continuous Delivery |

## Modules & Internal Terms
| Term | Meaning |
|------|---------|
| `web_learn` | Модуль веб-поиска через DuckDuckGo |
| `web_learn/duckduckgo` | Подмодуль DuckDuckGo поиска в web_learn |
| circuit breaker | Паттерн: при 3+ неудачах → авто-переключение на fallback провайдер |
| watchtower | Docker-утилита для авто-обновления контейнеров |
| self-healing | Самовосстановление контейнеров при сбоях |
| Speculative Consensus v2 | Параллельные Drafter-ы + структурированный Verifier |
| Batch Idle Learning | Пакетное alignment до 8 уроков в idle-режиме |

## Priority Scale
| Level | Meaning |
|-------|---------|
| P1 | Критично — блокирует основной функционал |
| P2 | Важно — влияет на стабильность/производительность |
| P3 | Низкий приоритет — улучшения и clean-up |

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
