# 2026-05-09 Hardware Upgrade + Obsidian Commands

## Апгрейд железа
- CPU: Ryzen 7 3700X (8c/16t, 4.05 GHz) — заменён APU с Vega 11
- RAM: 48 GB
- GPU: 2x дискретных (RX 580 + RX 560), Vega 11 убрана

## GPU перенастроен (v4)
| Порт | GPU | Vulkan | Модель | tok/s |
|------|-----|--------|--------|-------|
| 8082 | RX 580 4GB | Vulkan0 | qwen2.5:3b (smart) | 29.4 |
| 8084 | RX 560 4GB | Vulkan1 | qwen2.5:3b (code) | 20.8 |

## Файлы обновлены
- `src/ollama_three.py` → v4 (2 GPU, убрана Vega 11)
- `scripts/two_gpu_start.ps1` — новый скрипт запуска
- `src/mcp_api.py` — gpu_status описание
- `src/core.py` — добавлены Obsidian команды в ядро
- `.env` — исправлен OBSIDIAN_VAULT_PATH (был Linux-путь)

## Obsidian команды добавлены в ядро ARGOS
Теперь работают из Telegram:
- `обсидиан статус` — статус vault
- `обсидиан сегодня` — daily note
- `обсидиан заметки` — список заметок
- `обсидиан найди <запрос>` — поиск
- `обсидиан читай <путь>` — чтение заметки
- `обсидиан запиши <путь>\n<текст>` — запись

## Исправленные баги
- `.env` содержал Linux-путь `/home/ava/...` → заменён на `F:\debug\аргос`
- `self.obsidian_mcp` не сохранялся в core → теперь сохраняется при инициализации

[[Backbone Hub]]
[[ARGOS Memory Web]]

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Logs Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Logs Hub]]
