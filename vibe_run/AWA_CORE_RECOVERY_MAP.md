# ARGOS-VIBE: карта восстановления ядра (сверено с X230, 14.11.2026)

## Различие версий

В GitHub `winargos42-dotcom/argos` на коммите `617de117` файл `src/core.py` содержит класс **ArgosCore**, а не `AwaCore`. В действующей версии X230 также присутствует отдельный файл `src/awa_core.py` с классом **AWACore**. Его нет в проверенном GitHub-коммите.

Не исправлять это ложным переименованием классов. Сначала получить совместимые исходники и определить контракт инициализации.

## Проверено на X230

Оригиналы:
- `/home/argos-data/recovery/argos_ai_brain.py` (660 строк, syntax OK)
- `/home/argos-data/recovery/argos_brain_api.py` (794 строки, syntax OK)
- `/home/argos-data/runtime/app/src/core.py` (класс ArgosCore)
- `/home/argos-data/runtime/app/src/awa_core.py` (класс AWACore)
- `/home/argos-data/runtime/app/src/argos_logger.py` (оригинальный логгер; **не заменять shim**)

Все перечисленные Vibe зависимости найдены в каталоге `/home/argos-data/runtime/app/src/`:
- `quantum/logic.py`, `factory/replicator.py`, `connectivity/sensor_bridge.py`
- `skill_loader.py`, `dag_agent.py`, `github_marketplace.py`
- **`modules/__init__.py` + `modules/module_loader.py`** (пакет, не `modules.py`)
- `context_manager.py`, `agent.py`, `argos_integrator.py`
- `agent_guard.py`, `rollback_manager.py`, `telegram_direct_commands.py`

Это подтверждение наличия файлов, **не подтверждение совместимости импортов или рабочего запуска** в Vibe. Для `src.modules` оригинальный `__init__.py` экспортирует `ModuleLoader`.

## Безопасный порядок восстановления

1. Сохранить исходный коммит `617de117` и работающие процессы Vibe без изменений.
2. Создать изолированную ветку/рабочее дерево; не копировать .env, токены, базы и модели.
3. Перенести оригиналы Brain API и зависимости как отдельный набор, сверить их SHA256.
4. Сначала проверить `python -m compileall`, затем импорт `ArgosCore`, отдельно `AWACore`, отдельно `ARGOSBrain`.
5. Запускать `pytest vibe_run/test_brain_api_integration.py -v` с установленными Flask/pytest и только оригинальным Brain API. SKIP не считать успешным тестом.
6. Проверить `/health`, `/brain/status`, `/agents`, создание агента и read-back.
7. После прохождения тестов пробовать защищённое объединение узлов. Публичный ingress не включать.

## Замечание по исходным тестам Vibe

Тест создания агента из переданного патча ошибочно ищет `agent_id` в корне ответа. В оригинальном API он находится по пути `agent.id` внутри JSON, а HTTP статус — 201. Исправлено в файле `test_brain_api_integration.py` этой ветки.

Оригинальный патч Vibe целиком ещё не подтверждён побайтовой сверкой с SHA256 `7d7ae8309f54253bcff386cd3dfa574a97b97f6a5ef62dcc7eeeb876a9b5087c`. Эта ветка содержит **проверенные исправления, а не побайтовое применение патча**.
