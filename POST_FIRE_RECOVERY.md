# ARGOS — восстановление после пожара 03.08.2026

Отчёт о фактически выполненном восстановлении ядра. Всё, что здесь описано,
проверено запуском, а не предположением.

## Итог одной строкой

Ядро ARGOS восстановлено и запускается: **119 Python-файлов, 41 041 строка
(1,73 МБ)** возвращены в репозиторий, `ArgosCore` импортируется, три сервиса
поднимаются одной командой и отвечают на запросы.

---

## Ключевая находка: истории было больше, чем видно

Рабочая копия была **shallow-клоном** (`git rev-parse --is-shallow-repository` →
`true`), и история обрывалась на 10.08.2026 — через неделю после пожара.
Это артефакт клона, а не реальное состояние репозитория.

После `git fetch --unshallow`:

- реальная история начинается **09.05.2026**, довоенная работа идёт до **20.06.2026**;
- довоенное дерево (11 312 файлов) **цело**: `git diff --diff-filter=D` между
  последним довоенным коммитом и HEAD показывает **0 удалённых файлов**;
- разрыв в истории — с 20.06 по 10.08.2026: локальная работа этого периода
  в git не попадала.

## Источники, из которых восстановлен код

| Источник | Что дал |
|---|---|
| `winargos42-dotcom/argos-1` — форк, каталог `argos_deploy/src/` | основную массу модулей ядра |
| `argos_deploy/backups/auto_20260411_*` — 10 авто-снимков в том же форке | модули, отсутствовавшие в основном дереве форка |
| `scripts/build.py` в этом репозитории | генератор, содержащий исходники `src/quantum/*` и `src/argos_logger.py` дословно |
| `LAUNCH_INSTRUCTIONS.md`, `ARGOS_BRAIN_*.md`, `README.md` | контракт Brain API, таблица квантовых состояний, поведение fallback-режима |

Проверено: `argos_ai_brain.py` **никогда не был в git этого репозитория** —
поиск по деревьям всех коммитов всех веток пуст. Оригинал (25 903 б, что
совпадает с «24 KB» из `ARGOS_BRAIN_SUMMARY.md`) найден в форке и возвращён.

## Что восстановлено

**Ядро мозга**

- `argos_ai_brain.py` — `ARGOSBrain`, `ARGOSAgent`, `AgentRole` (5 ролей),
  `AzureAIClient`, `AgentMemoryDB`. Без него `argos_brain_api.py` не стартовал вообще.

**Пакеты `src/`, отсутствовавшие целиком** — `factory`, `interface`, `knowledge`,
`mind`, `modules`, `quantum`, `security`.

**Крупнейшие возвращённые модули**

| Модуль | Размер |
|---|---|
| `src/thought_book.py` | 73 582 б |
| `src/consciousness.py` | 73 062 б |
| `src/life_support.py` | 55 550 б |
| `src/skills/huggingface_ai.py` | 50 533 б |
| `src/kolibri_os_builder.py` | 46 556 б |
| `src/platform_admin.py` | 44 136 б |
| `src/telegram_bot.py` | 43 871 б |
| `src/device_scanner.py` | 37 767 б |
| `src/argos_model.py` | 34 592 б |
| `src/factory/flasher.py` | 31 842 б |

Плюс `src/quantum/{logic,oracle,ibm_bridge,watson_bridge,quantum_ml}.py`,
`src/security/{gost_cipher,bootloader_manager,autostart}.py`,
`src/mind/{dreamer,evolution_engine,self_model_v2}.py`,
`src/interface/{web_dashboard,fastapi_dashboard}.py`, 18 модулей
`src/connectivity/*`, 17 навыков `src/skills/*`.

Все восстановленные файлы проверены на секреты (токены Telegram, ключи OpenAI /
Google / GitHub / HuggingFace, приватные ключи) — **не найдено**.

## Что запущено и проверено

`bash scripts/argos_recovery.sh` поднимает с нуля:

| Сервис | Порт | Проверка |
|---|---|---|
| Brain API (`argos_brain_api.py`) | 5001 | `/health` 200, 4 агента созданы, `/think`, `/coordinate` отвечают |
| MCP API (`src/mcp_api_standalone.py`) | 8000 | `/health` → `{"ok":true}` |
| Edge API (`main.py`, тот же код, что на Railway) | 8080 | `/` → `{"name":"ARGOS","version":"2.1.5","status":"online"}` |

Проверка мышления через восстановленное ядро:

```
POST /think {"query":"Статус системы","role":"monitor"}
→ source: ArgosCore
  📊 АРГОС СТАТУС:
    CPU: 0.0%   RAM: 5.9%   DISK: 21.3%
    AI: нет     Задач планировщика: 0
```

`source: ArgosCore` означает, что отвечает именно восстановленное ядро, а не
заглушка.

## Артефакты пожара в конфигурации

Конфигурация всё ещё указывает на сгоревшее железо — это ломает работу тихо,
поэтому вынесено отдельно:

- `argos_brain_api.py` → `_llama_servers()` по умолчанию ходит на
  `192.168.1.72:8083/8085/8082` (llama-server на сгоревшем ПК). Каждый `/think`
  ждал 45 с × 3 сервера. Обходится переменной `ARGOS_MODEL_ROUTER`, которую
  выставляет `scripts/argos_recovery.sh`.
- `config/p2p_health_history.json`, P2P-монитор → узлы `192.168.1.10`,
  `192.168.1.11`, `192.168.1.53`, `192.168.1.66` — сгоревшая домашняя сеть.
- `scripts/argos_start_all.sh` рассчитан на путь `/home/ava/Projects/argoss`,
  systemd, mosquitto и SSH-туннель к ПК — на новой машине неприменим как есть.

## Что ещё не восстановлено

**9 модулей не найдены ни в одном доступном источнике:**

```
src/integrations/anomaly_detector.py     src/principles/audit_procedure.py
src/integrations/circuit_breaker.py      src/principles/convergent_fsm.py
src/integrations/conflict_aggregator.py  src/principles/open_loop_ctl.py
src/integrations/esports_tracker.py      src/principles/topology_id.py
src/mcp/cache_layer.py
```

Все они импортируются лениво внутри `try/except`, поэтому ядро работает без них —
недоступны только соответствующие функции.

**Файлы, упомянутые в документации, но отсутствующие везде:**
`argos_brain_examples.py`, `ARGOS_BRAIN_SETUP.sh`, `Dockerfile.brain`,
`Dockerfile.compute`, `file6s/compute_center_service.py`,
`scripts/ARGOS_EMERGENCY_RESTORE.py`, `ARGOS_RESTORE_PART2..7.py`,
`ARGOS_RESTORE_{MODULES,GUI,FINAL}.py`. Последние — семейство скриптов-генераторов,
которые вызывает `scripts/build.py`; без них `build.py` восстанавливает только то,
что содержит внутри себя.

**Данные:** веса локальных моделей (`models/mini-tron-50/` — только конфиг и
токенайзер), исходные `data/*.jsonl` (в `.gitignore`; на HuggingFace лежит только
очищенный `AvaSiG/argos-canonical`). Разрыв состояния 20.06 → 03.08 ничем не покрыт.

## Облачный контур

Проверить HTTP из этой сессии нельзя — исходящий доступ закрыт политикой прокси
(403 на CONNECT). Что удалось установить косвенно:

- DNS всех адресов живой: `argosssss.win` и `api.argosssss.win` → Cloudflare
  (`2606:4700:3031::ac43:b17c`), `reboot-static-production`, `argos-v2-production`,
  `planeta-mcp-v4-production` → Railway (`69.46.46.x`),
  `argos-core-508337926357.us-central1.run.app` → Google Cloud Run;
- GitHub Actions «Deploy to Railway» успешно отработал 20.08.2026, Planeta MCP CI
  зелёный (114 тестов) — значит, Railway подключён к репозиторию и деплоит с каждого
  пуша в `main`.

Проверить со своей машины:

```bash
for u in https://reboot-static-production.up.railway.app \
         https://argos-v2-production.up.railway.app/health \
         https://planeta-mcp-v4-production.up.railway.app/health \
         https://api.argosssss.win/health; do
  echo -n "$u → "; curl -s -o /dev/null -w "%{http_code}\n" -m 10 "$u"
done
```

## Требует действий: секреты в публичном репозитории

Эти файлы лежат в открытом репозитории и переживают любое восстановление —
их нельзя переиспользовать, только отозвать и перевыпустить:

| Файл | Что внутри |
|---|---|
| `argos-489214-782ee50ae90b.json` | приватный ключ сервис-аккаунта GCP (проект `argos-489214`) |
| `data/entity_bot_tokens.json` | токены Telegram-ботов открытым текстом |
| `config/phase3/swarm_tokens.txt` | docker swarm join-token |
| `config/master.key`, `config/node_id`, `config/node_birth` | ключ и идентичность узла (закоммичены вопреки `.gitignore`) |

Порядок: отозвать ключ GCP → перевыпустить токены ботов через BotFather →
перевыпустить swarm-token → сгенерировать новые `master.key` и `node_id` →
убрать файлы из индекса и вычистить историю.

## Как запустить

```bash
bash scripts/argos_recovery.sh          # venv, зависимости, запуск, health-check
bash scripts/argos_recovery.sh --check  # только проверка
bash scripts/argos_recovery.sh --stop   # остановить
```

Для осмысленных ответов вместо rule-based режима нужен LLM-бэкенд: либо
`AZURE_OPENAI_ENDPOINT` и `AZURE_OPENAI_KEY` в `.env`, либо локальный
llama-server / Ollama и `ARGOS_MODEL_ROUTER="http://<host>:<port>|<модель>|<приоритет>"`.
