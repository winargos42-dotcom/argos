# 2026-05-11 ARGOS MCP Debug Hardening

## Причина
Пользователь запросил развивать и дебажить MCP. Быстрые MCP tools работали, но `command` мог уводить короткие проверки в тяжёлый AI pipeline.

## Исправлено
- `src/mcp_api.py`: добавлен `_mcp_debug()` — быстрый debug-снимок без AI pipeline:
  - uptime, ai_mode, CPU/RAM
  - `MCP_COMMAND_TIMEOUT_SEC`
  - открытые локальные порты `8000/8080/8082/8084/8090/11434/47291/47392`
  - состояние core/admin/p2p/vision/skill_loader
- `src/mcp_api.py`: добавлен MCP tool `mcp_debug`.
- `src/mcp_api.py`: `_run_command()` получил Direct fast-path для `+`, `++`, `ping/пинг`, `test/тест`, `э/эй`, `на связи`.
- `src/mcp_api.py`: короткие числовые команды до 12 цифр отвечают Direct (`Получил число/код`) без AI pipeline.
- `src/mcp_api.py`: `mcp debug` / `debug mcp` / `mcp статус` через `command` тоже возвращают `_mcp_debug()`.
- `tests/test_mcp_fast_ai_status.py`: добавлены регрессии для `mcp_debug`, `command +`, `command 89385`.

## Проверка
- `py_compile src/mcp_api.py src/connectivity/telegram_bot.py` -> OK.
- `pytest tests/test_mcp_fast_ai_status.py tests/test_mcp_gcp_quota_tool.py tests/test_telegram_bot_history_scope.py tests/test_web_learn_routing.py tests/test_core_provider_resilience.py -q` -> `22 passed`.
- Перезапуск через `Start Argos on Logon`: task `Running`, новый MCP PID `7980`.
- MCP health -> `200`, `ok=true`.
- `mcp_debug` -> OK за `426ms`.
- `command +` -> OK за `110ms`, Direct.
- `command 89385` -> OK за `2ms`, Direct.
- Активные порты: `8000`, `8080`, `8082`, `8084`, `8090`, `11434`, `47291`, `47392`.

## Новый протокол диагностики
1. `mcp_debug`
2. `command +`
3. `status`
4. `providers`
5. `gpu_status`
6. `obsidian_status`