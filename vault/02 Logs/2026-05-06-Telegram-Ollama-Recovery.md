# 2026-05-06 — Telegram/Ollama Recovery (Codex)

## Контекст
- Симптом в Telegram: `No API provider registered for api: ollama`.
- Дополнительно: нестабильный запуск из-за конфликтов портов и дублей Python-процессов.

## Что изменено
1. `src/connectivity/telegram_bot.py`
- Усилен `_run_core_with_timeout`: теперь ловит любые исключения ядра и не отдаёт сырой traceback/текст провайдера в Telegram.
- Усилен `_normalize_core_result`: нормализует даже не-dict ответы; при маркере `No API provider...` переводит в recovery/offline-safe ответ.

2. `src/telegram_bot.py`
- Добавлены `_normalize_core_result()` и `_run_core_with_timeout()` с таким же защитным поведением.
- `handle_message`, `handle_voice`, `handle_audio` переведены на единый безопасный вызов ядра.

3. `.env`
- `OLLAMA_ENABLED=true`
- `OLLAMA_GPU_ENABLED=true`

4. `scripts/start_argos_telegram_stable.ps1`
- Расширена очистка дублей перед стартом: учитываются `telegram_bot.py` и `src\\telegram_bot.py`.
- Добавлена зачистка осиротевших python-listener’ов на портах `8080` и `8090` (иначе падение bind и конфликт polling).

## Диагностика/проверки
- В логе подтверждено: `Ollama: ✅ доступна (резервный провайдер готов)`.
- После очистки конфликтного процесса ARGOS поднят:
  - health: `http://127.0.0.1:8000/health` -> `ok=true`
  - MCP endpoint активен: `http://0.0.0.0:8000/mcp`
  - Telegram: `polling lock acquired` + `Telegram бот запущен`
- MCP ручная проверка команды `Argos Win <winargos42@gmail.com>`: возвращается нормальный ответ (без raw `No API provider...`).

## Замечания
- Есть внешний конфликт `getUpdates` в отдельные моменты (возможен второй бот/узел вне текущего процесса).
- GCP quota monitor: клиент не инициализирован (отдельный вопрос зависимостей/credentials).

## Статус
- Критичный баг с сырым `No API provider...` закрыт в коде.
- ARGOS в текущем запуске отвечает и держит MCP/Telegram контур.

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
