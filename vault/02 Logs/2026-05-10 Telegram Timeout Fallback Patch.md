# 2026-05-10 Telegram Timeout Fallback Patch

- Время: 2026-05-10 11:32:15
- Статус: applied

## Что сделано

1. Патч Telegram timeout fallback в коде:
   - src/connectivity/telegram_bot.py
   - src/telegram_bot.py
2. Новая логика при Timeout:
   - сначала пробует execute_intent (быстрые system/direct команды)
   - если нет результата, отдаёт _offline_answer
   - больше нет пустого технического timeout-ответа как единственного варианта
3. Валидация:
   - python -m py_compile src/connectivity/telegram_bot.py
   - python -m py_compile src/telegram_bot.py

## Ожидаемый эффект

- Telegram-бот отвечает полезно даже при перегрузе ядра/провайдеров
- Снижение «молчит/завис» по пользовательскому каналу

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
