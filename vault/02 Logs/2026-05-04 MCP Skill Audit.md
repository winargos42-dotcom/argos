📄 **02 Logs/2026-05-04 MCP Skill Audit.md**

# 2026-05-04 MCP Skill Audit

- Старт аудита MCP-инструментов ARGOS
- Endpoint: http://localhost:8001/mcp
- Фаза 1: initialize и 	ools/list
- Результат: сервер rgos v2.1.3 отвечает, список инструментов получен
- Найден конфиг-дрейф: локальный .mcp.json всё ещё указывает на 127.0.0.1:8000/mcp

## Инструменты к тесту

- providers
- skills
- limits
- status
- image_generate
- cloudflare_models
- cloudflare_chat
- npm
- porphyry
- orangepi_gadget
- orangepi_bridge
- ollama_vision
- pi_bridge
- command
## Фаза 2 — Fast tools on 8000

- Endpoint переключён на `http://localhost:8000/mcp`, так как именно он реально поднят по текущему `.env`
- `initialize` и `tools/list` ранее отработали успешно
- Реальный результат первой серии `tools/call`:
  - `status` — timeout ~15.4s
  - `providers` — timeout ~20.0s
  - `skills` — timeout ~20.0s
  - `limits` — connection closed on receive
  - все последующие (`npm`, `porphyry`, `orangepi_gadget`, `orangepi_bridge`, `ollama_vision`, `pi_bridge`, `command`) — `Unable to connect to the remote server` 
- Вывод: MCP сервер принимает handshake, но на первой же рабочей серии `tools/call` зависает или падает
- Артефакты отчёта:
  - `F:\debug\argoss\reports\mcp_phase_fast_2026-05-04.md`
  - `F:\debug\argoss\reports\mcp_phase_fast_2026-05-04.json`


## Фаза 3 - Стабильный mcp-only на 8000

- Поднят отдельный mcp-only процесс для чистого аудита на http://localhost:8000/mcp
- Точечный tools/call status подтвердил живой MCP после перезапуска

## Фаза 4 - Fast tools (повторный прогон на свежем MCP)

Работают с реальным ответом:
- status - OK, uptime/CPU/RAM возвращаются
- providers - OK, длинный отчёт по AI-провайдерам возвращается
- skills - OK, список загруженных навыков возвращается
- limits - OK, лимиты и pool-статус возвращаются
- npm - OK, список npm-пакетов проекта возвращается
- porphyry - OK, статус модуля возвращается
- orangepi_gadget - OK, статус возвращается (неактивен)
- orangepi_bridge - OK, статус железа возвращается
- ollama_vision 
## MCP Fast Contour Update (2026-05-04 12:53:46)
- Добавлен новый MCP tool: rgoss_dataset_build_obsidian
- Добавлен быстрый action: dataset_build_obsidian в rgoss_command
- Исправлен fallback для iot протоколы: больше не падает при отсутствии _iot_protocols_help
- Живой тест MCP: rgoss_dataset_build_obsidian => OK (data/obsidian_training_dataset.jsonl, 2554779 bytes)
- Живой тест MCP: command: iot протоколы => OK (выведен полный список протоколов)
- Живой тест MCP: rgoss_finetune target=colab => OK (возвращает актуальный Colab prep)

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
