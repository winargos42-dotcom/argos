# AwaCore / Brain API — карта восстановления (ARGOS-VIBE, этап 2)

Проверено прямым импортом в рантайме Vibe (Python 3.12), а не только чтением
кода. Оригинал `src/core.py` (8504 строки, `AwaCore`) и `argos_brain_api.py`
находятся в репозитории, но их зависимости частично отсутствуют.

## 1. Источники восстановления (X230, предоставлены владельцем)

| Файл на X230 | Куда положить в репозитории |
|---|---|
| `/home/argos-data/recovery/argos_ai_brain.py` | `argos_ai_brain.py` (корень репо) |
| `/home/argos-data/recovery/argos_brain_api.py` | `argos_brain_api.py` (сверить с версией в репо) |
| `/home/argos-data/runtime/app/src/core.py` | `src/core.py` (сверить) |

## 1а. Две реализации ядра — не смешивать

| Реализация | Файл | Класс | Статус в репо |
|---|---|---|---|
| Ядро репозитория | `src/core.py` (8504 строки) | `ArgosCore` | есть, но 13 зависимостей отсутствуют |
| Ядро действующей X230 | `src/awa_core.py` | `AWACore` | **в репозитории отсутствует** — восстановить отдельным файлом с X230 |

План: `src/awa_core.py` копируется с X230 как отдельный модуль рядом с `src/core.py`;
импорты и точки входа двух классов не объединять. Проверка раздельно:
`python -c "from src.core import ArgosCore"` и
`python -c "from src.awa_core import AWACore"`. Какой класс использует
`mcp_api_standalone`/`main.py` — сверить по фактическому коду X230 перед
подключением к API.

## 2. Требуемые символы

- `argos_brain_api.py` импортирует из `argos_ai_brain`:
  `ARGOSBrain, ARGOSAgent, AgentRole, AgentConfig, AzureAIClient`
- `src/core.py` импортирует из 16 модулей `src/*` (см. таблицу ниже)
- Дополнительно: `python-dotenv` (установлен в Vibe-venv)

## 3. Недостающие модули для AwaCore (13, подтверждено импортом)

| # | Модуль | Символы, нужные `src/core.py` | Отметка |
|---|---|---|---|
| 1 | `src/quantum/__init__.py` + `src/quantum/logic.py` | `ArgosQuantum` | пакет отсутствует целиком |
| 2 | `src/factory/__init__.py` + `src/factory/replicator.py` | `Replicator` | пакет отсутствует целиком |
| 3 | `src/connectivity/sensor_bridge.py` | `ArgosSensorBridge` | |
| 4 | `src/skill_loader.py` | `SkillLoader` | |
| 5 | `src/dag_agent.py` | `DAGManager` | |
| 6 | `src/github_marketplace.py` | `GitHubMarketplace` | |
| 7 | `src/modules.py` | `ModuleLoader` | |
| 8 | `src/context_manager.py` | `DialogContext` | |
| 9 | `src/agent.py` | `ArgosAgent` | |
| 10 | `src/argos_integrator.py` | `ArgosIntegrator` | |
| 11 | `src/agent_guard.py` | `AgentGuard` | |
| 12 | `src/rollback_manager.py` | `RollbackManager` | |
| 13 | `src/telegram_direct_commands.py` | `handle_direct_telegram` | |

Присутствуют и работают: `src/argos_logger.py` (восстановлен минимальным shim),
`src/skills/web_scrapper` (пакет — импортируется успешно),
`src/connectivity/p2p_bridge.py` (импортируется).

## 4. Порядок импорта `src/core.py` (порядок = порядок восстановления)

```
1. src.argos_logger          (shim готов)
2. src.skills.web_scrapper   (есть)
3. src.quantum.logic         ← блокер №1
4. src.factory.replicator    ← блокер №2
5. src.connectivity.sensor_bridge
6. src.connectivity.p2p_bridge (есть)
7. src.skill_loader
8. src.dag_agent
9. src.github_marketplace
10. src.modules
11. src.context_manager
12. src.agent
13. src.argos_integrator
14. src.agent_guard
15. src.rollback_manager
16. src.telegram_direct_commands
```

Любой отсутствующий модуль на пути рвёт весь импорт `AwaCore` — восстанавливать
нужно все 13 файлов одним набором, затем повторять
`python -c "from src.core import AwaCore"` до успеха.

## 5. Проверка после восстановления

```bash
# 1. Brain API (Flask, порт 5001)
python argos_brain_api.py &
curl -s http://127.0.0.1:5001/health
# 2. Интеграционные тесты оригинального Brain API
python -m pytest vibe_run/test_brain_api_integration.py -v
# 3. AwaCore
python -c "from src.core import AwaCore; c = AwaCore(); print(type(c))"
```

Тесты `vibe_run/test_brain_api_integration.py` сейчас корректно SKIPP с
указанием причины; после восстановления `argos_ai_brain` они прогоняются по
настоящему Flask-приложению без изменений.
