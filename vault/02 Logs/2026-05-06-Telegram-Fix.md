# ARGOS Telegram Fix — 2026-05-06

- Проведена диагностика runtime, GPU и Telegram polling.
- Устранены дубли процессов `main.py --no-gui` и `web_server.py`.
- Проверено: MCP health `ok`, Telegram lock `127.0.0.1:47291` у единственного main-процесса.
- Обновлён `.env` для стабильных ответов:
  - `OPENCLAW_ENABLED=false`
  - `ARGOS_AUTO_COLLAB=off`
  - `ARGOS_CONSENSUS_MODE=off`
  - `ARGOS_AUTO_COLLAB_MAX_MODELS=1`
  - `ARGOS_CONSENSUS_N=1`
  - `TG_CORE_TIMEOUT_SEC=20`
  - `TG_CORE_MAX_INFLIGHT=1`
  - `ARGOS_DISABLE_OPENCLAW=1`
- Исправлен `scripts/three_gpu_start.ps1`:
  - автоподбор валидной модели для RX560 (игнор битого `phi4-mini-3.8b-q4_k_m.gguf`)
  - fallback-профиль для GPU0 (RX580), если 8082 не поднялся.
- Добавлен скрипт `scripts/start_argos_telegram_stable.ps1` для безопасного единого запуска без дублей.
- Контрольный тест через MCP: запрос `привет` отвечает без таймаута.

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
