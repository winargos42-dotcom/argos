# 2026-05-11 ARGOS Telegram Plus FastPath

## Что проверено
- MCP health: `http://127.0.0.1:8000/health` отвечает `200`, `ok=true`.
- Живой процесс: `python.exe main.py --no-gui`.
- Активные порты: `8000` MCP, `8080` dashboard, `8082/8084` GPU llama-server, `8090` cluster dashboard, `11434` Ollama, `47291` Telegram lock, `47392` OpenClaw.
- Регрессии: `pytest tests/test_telegram_bot_history_scope.py tests/test_web_learn_routing.py tests/test_telegram_can_start.py tests/test_core_provider_resilience.py -q` -> `23 passed`.

## Найденная причина молчания
- Telegram polling реально получил входящее `+` от администратора.
- До исправления `+` не был Direct ping-командой и уходил в тяжёлый AI/SkillLoader/consensus путь.
- Из-за тяжёлого пути пользователь видел отсутствие ответа, а task-log позже показал `ARGOS exited with code -1`.

## Исправлено
- `src/connectivity/telegram_bot.py`: `+` и `++` добавлены в мгновенный Direct ping path без LLM/consensus.
- `start-argoss.ps1`: перед запуском добавлена зачистка stale `main.py --no-gui`, `web_server.py`, `telegram_bot.py`, чтобы после ребута не оставались полуживые дубли.
- `tests/test_telegram_bot_history_scope.py`: добавлена регрессия, что `+` отвечает Direct и не вызывает `core.process_logic_async`.
- `tests/test_telegram_bot_history_scope.py`: test helper явно отключает `TG_ALLOW_ALL_USERS`, чтобы тесты авторизации не зависели от `.env`.

## Важное наблюдение
- `Start Argos on Logon` сейчас в состоянии `Ready`, но живой ARGOS есть через отдельный `main.py --no-gui`.
- Если после ребута снова будет `Ready` при живом ARGOS, проверить внешний one-shot launcher, который запускает `Get-Process pythonw,python | Stop-Process` и может сбивать task-start.

## Следующая проверка
- Написать `+` в Telegram.
- Ожидаемый ответ: `ARGOS [Direct]`, текст о том, что Telegram bridge жив и принимает updates.