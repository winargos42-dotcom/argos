# ARGOS Claude Templates — фикс кодировки + проверка — 2026-06-04

## Контекст
Интеграция Claude Code Templates в ARGOS (695 компонентов: 417 agents, 276 commands,
2 skills). Файлы: `src/claude_templates_integrator.py`, `argos-claude.py`,
`src/argos_integrator.py`, `src/event_bus.py` (событие COMPONENT_LOADED).

## Проверка реальности (до фикса)
Проверено фактически, не на слово:
- Файлы существуют: claude_templates_integrator.py (21KB), argos-claude.py (9.7KB),
  argos_integrator.py (27KB), event_bus.py (COMPONENT_LOADED ✓).
- claude-code-templates на диске: 473 agents .md, 391 commands .md.
- Рантайм: EventBus стартует, 695 компонентов загружаются, кеш 402 агента/274 команды,
  поиск "python" → 9 агентов. РАБОТАЕТ.

## БАГ (найден)
`argos-claude.py search ...` падал с:
`UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f50d'` (эмодзи 🔍).
Причина: консоль Windows в cp1251 не кодирует эмодзи/юникод. Вывод падал → выглядело
как "не работает", хотя интеграция исправна. (Та же болезнь, что валила idf monitor.)

## ФИКС (применён)
`argos-claude.py` — после импортов добавлено:
```python
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
```
Теперь скрипт печатает эмодзи/кириллицу без PYTHONIOENCODING.

## Статус
- [x] Фикс применён в argos-claude.py
- [x] Проверка после фикса — ПРОЙДЕНА

## ПРОВЕРКА после фикса (чистый запуск БЕЗ PYTHONIOENCODING)
Запуск как у пользователя: `python argos-claude.py <cmd>` (без env-префикса).

| Команда | Результат |
|---------|-----------|
| `search python`   | ✅ эмодзи 🤖 печатаются, выдал python-pro, python-mcp-expert и др., exit 0 |
| `search security` | ✅ найдено 22 агента, exit 0 |
| `stats`           | ✅ agents:417, commands:276 (кеш 402/274), эмодзи ок, exit 0 |

UnicodeEncodeError 'charmap' БОЛЬШЕ НЕ ВОЗНИКАЕТ. Вывод читаемый.

## ИТОГ
Интеграция Claude Templates реальна и работает (695 компонентов, поиск/stats/адаптация).
Единственный баг — кодировка вывода — устранён одной вставкой в argos-claude.py
(reconfigure stdout/stderr на utf-8). Чистый софт, рантайм-логика не тронута.

## Заметка на будущее
Та же болезнь cp1251 встречается в проекте повсеместно (idf monitor, прочие CLI с
эмодзи). Универсальный приём: `sys.stdout.reconfigure(encoding="utf-8")` в начале
скрипта ИЛИ `PYTHONIOENCODING=utf-8` / `chcp 65001` в окружении.

*Подход: сначала проверка реальности (не на слово), потом точечный фикс, потом
повторная проверка. Урок после провала с ESP усвоен.*
