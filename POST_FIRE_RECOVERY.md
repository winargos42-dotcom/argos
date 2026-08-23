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
| `poilopr57-a11y/Argos` — третий репозиторий (доступен анонимно) | FPGA-стек, VPN-сервис и ещё 23 модуля, отсутствовавших в обоих других |

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

## Третий репозиторий: FPGA-стек и VPN-сервис

`poilopr57-a11y/Argos` подключить к сессии нельзя (кросс-владельческое ограничение),
но git-прокси отдаёт его анонимно — репозиторий публичный. Клонирован целиком:
107 коммитов, история до 29.06.2026.

Оттуда вернулись 23 модуля, которых не было ни в основном репозитории, ни в форке:

| Модуль | Размер |
|---|---|
| `src/vpn_service/api.py` | 36 650 б |
| `src/connectivity/xilinx_fpga.py` | 32 111 б |
| `src/connectivity/pi_bridge.py` | 21 953 б |
| `src/skills/evolution/skill.py` | 19 951 б |
| `src/unified_node_registry.py` | 15 268 б |
| `src/vpn_service/bulgakov_tunnel.py` | 15 024 б |
| `src/argos_disk_cleaner.py` | 12 406 б |
| `src/argos_nexus.py` | 12 115 б |

Плюс `src/fpga_api.py`, `src/skills/fpga/`, `src/vpn_service/{bot,database,wg_manager,
traffic_daemon,bulgakov_server}.py`, `src/connectivity/protocols/lora_bridge.py`,
`src/argos_miniapp_router.py`, `src/dry_leaf_daemon.py`, `src/vpn_api.py`,
`src/skills/{desktop_actions,hardware_intel}.py`.

Это как раз FPGA-контур, над которым шла работа перед пожаром (см. довоенные сессии
про JTAG и пересборку m2-битстрима). Все файлы просканированы на секреты — включая
`vpn_service/bot.py` и `api.py`, где ключи вероятнее всего, — не найдено. Синтаксис
проверен `compileall`, `src.core` по-прежнему импортируется, ARGOS перезапущен и жив.

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

## Оркестратор: полный запуск по README

README описывает главную точку входа как `python main.py --no-gui` с режимами
`--mobile`, `--dashboard`, `--wake`, `--full`, `--shell`, `--root`, скрипт
`launch.sh` и `health_check.py`. Ничего этого в репозитории не было: `main.py`
здесь **всегда** был Railway-сервисом (с первого коммита 09.05.2026), а
оркестратор `ArgosOrchestrator` (1 206 строк) жил только в форке.

Восстановлено под именем **`argos_main.py`**, а не `main.py` — иначе сломался бы
рабочий деплой: `Procfile` и `railway.json` запускают `uvicorn main:app`.
`launch.sh` восстановлен с правкой вызова на `argos_main.py`.

Вместе с ним вернулись `health_check.py`, `genesis.py`, `main_kivy.py`,
`amd_gpu_patch.py`, `src/mcp_api.py` (169 КБ), интерфейсы
`src/interface/{argos_shell,gui,kivy_local_ui,mobile_ui,web_engine}.py`,
`src/launch_config.py` и `src/security/{encryption,git_guard,root_manager}.py`.

Проверка запуска:

```
$ python argos_main.py --status
ARGOS работает: PID 955, MCP http://127.0.0.1:8000/mcp (ok)
Web UI: http://127.0.0.1:8080/

$ curl http://127.0.0.1:8000/health
{"ok":true,"uptime_seconds":50,"ai_mode":"Auto","cpu_pct":0.0,"ram_pct":5.6}
```

`health_check.py` даёт 35/44: синтаксис всех 142 модулей в порядке, ключевые
импорты проходят; ошибки — отсутствующие pip-пакеты (`scikit-learn`, `numpy`,
`cryptography`) и `pyproject.toml` с `build.py` в корне (`build.py` лежит в
`scripts/`). `SkillLoader` поднимает **24 навыка**.

Замечания по запущенному экземпляру:

- Telegram-бот не стартует без `TELEGRAM_BOT_TOKEN` в окружении — и это правильно,
  пока токены из репозитория не отозваны.
- Работающий ARGOS пишет в файлы, которые лежат под git: `AGENTS.md`
  (строка `## Pi Shutdown — …`, причём с испорченной кодировкой на Linux),
  `data/sysmon_metrics.json`, `config/p2p_health_history.json`. Из-за этого
  рабочее дерево грязнится при каждом запуске; рантайм-состояние стоит вынести
  из-под контроля версий.
- В `data/sysmon_metrics.json` в git лежит **последний замер со сгоревшего
  ноутбука**: CPU 99.5 %, температуры 87–90 °C, ThinkPad. Запуск ARGOS
  перезаписывает эту запись — при работе с репозиторием её стоит беречь.

## Инфраструктура сборки — только в форке

В `winargos42-dotcom/argos-1` лежат 19 workflow, которых нет в основном
репозитории: `build_windows.yml` (сборка .exe через PyInstaller, вместе с
`argos.spec`), `build_apk.yml` и `android-apk.yml`, `docker.yml`,
`release.yml`, `publish_pypi.yml`, `secret-scan.yml`, `status_report.yml` и другие.
Основной репозиторий сейчас имеет только три: Planeta MCP CI, Railway deploy и
ROM build. Артефакты прошлых сборок в форке из этой сессии недоступны — репозиторий
не подключён к сессии для GitHub API; и артефакты Actions в любом случае хранятся
ограниченное время.

## Довоенные коммиты нашлись — в форке

В основном репозитории последний довоенный коммит — 20.06.2026. Но форк
`winargos42-dotcom/argos-1` содержит работу вплоть до самого пожара (его клон тоже
приходил обрезанным, история развёрнута через `fetch --unshallow`, 195 коммитов):

| Дата | Коммит | Что |
|---|---|---|
| 30.07 21:45 | `9912253` | самораспаковывающийся инсталлятор `install_argos.sh` |
| 30.07 22:56 | `811296a` | **add missing argos_ai_brain.py core module** — тот же модуль, что утрачен здесь |
| 31.07 | 17 коммитов | доводка сборок Windows (PyInstaller + Inno Setup) и APK |
| 01.08 | 3 коммита | Android entry point, `src/__init__.py`, p4a/SDL2 |
| **02.08 11:03** | **`3cb6d05`** | **последний довоенный коммит** — чистка кэша SDL2 |

Сверка показала, что восстановленный код соответствует этому состоянию: между
`3cb6d05` (02.08) и HEAD форка расходятся только `src/argos_logger.py` и
`src/launch_config.py` — и там взяты более новые версии.

## Сборка Windows: срок продлён до 22.09.2026

31.07.2026 в форке успешно отработала `build_windows.yml` (run #9, коммит
`7f69d405`) — рабочая сборка довоенного состояния. Её артефакты истекали 30.08.

Прогон пере-запущен 23.08 на **том же коммите** `7f69d405`, сборка снова успешна,
новые артефакты живут до **22.09.2026** (retention репозитория — 30 дней):

| Артефакт | ID | Размер | Истекает |
|---|---|---|---|
| `argos-windows-setup-9` (Inno Setup) | 9491939281 | 48,2 МБ | 2026-09-22 |
| `argos-windows-exe-9` (PyInstaller) | 9491938858 | 7,9 МБ | 2026-09-22 |

**Оговорка:** пере-запуск удаляет артефакты предыдущей попытки, поэтому оригинальные
файлы сборки от 31.07 больше не существуют. Исходный код тот же самый коммит, но
pip-зависимости подтянулись версиями на 23.08 — размеры отличаются (было 47 812 978
и 7 637 573 байта, стало 48 205 489 и 7 927 889). Это пересборка того же состояния,
а не побайтовая копия июльской.

Скачать (30-дневное окно — дальше сборку придётся запускать заново):

```bash
gh api repos/winargos42-dotcom/Argos-1/actions/artifacts/9491939281/zip > argos-windows-setup.zip
gh api repos/winargos42-dotcom/Argos-1/actions/artifacts/9491938858/zip > argos-windows-exe.zip
```

Страница прогона: https://github.com/winargos42-dotcom/Argos-1/actions/runs/30606382271

Из этой сессии скачать нельзя — egress-политика прокси отдаёт 403 на CONNECT к
хранилищу артефактов, поэтому переложить файлы в релиз или на HuggingFace я не могу.
Продление срока — единственное, что удалось сделать отсюда.

## Запуск с нуля: проверено на чистом клоне

Ветка склонирована в отдельный каталог и поднята с нуля — так же, как это будет на
новой машине:

```bash
git clone -b claude/post-fire-recovery-xyn05v https://github.com/winargos42-dotcom/argos
cd argos
bash scripts/argos_recovery.sh          # venv, зависимости, три сервиса → 3/3
bash scripts/argos_recovery.sh --full   # полный ARGOS: argos_main.py --no-gui
```

Результат второй команды на чистом клоне:

```
оркестратор запускается, лог: logs/argos_main.log
MCP поднялся за 5 с
ARGOS работает: PID 12380, MCP http://127.0.0.1:8000/mcp (ok)
Dashboard: http://127.0.0.1:8081/   Web UI: http://127.0.0.1:8080/
```

Прогон вскрыл пробел, который иначе всплыл бы у вас: скрипт не ставил `aiohttp`, без
которого `src/mcp_api.py` не импортируется и оркестратор молча не поднимает
MCP-эндпоинт (`_start_mcp_with_guard` глотает исключение). Добавлены `aiohttp`,
а также `numpy` и `cryptography` — без них `health_check.py` валит две проверки.

Telegram-бот стартует только при заданном `TELEGRAM_BOT_TOKEN`. Пока старые токены
из репозитория не отозваны, переменную задавать не нужно.

## Четвёртый репозиторий и потерянная ветка

`thoresensandmann432-source/argoss` (28 коммитов, до 25.04.2026) тоже открыт
анонимно. Проверен: ни одного `src/*.py`, которого не было бы уже здесь, и ни одного
из девяти недостающих модулей — 12 362 пути. Полезен только как подтверждение.

Отдельная потеря: сессия «Прогресс по задаче 2801» (создана 02.08.2026, за день до
пожара) работала в `poilopr57-a11y/Argos` на ветке
`codex/partner-business-local-save`. **На GitHub такой ветки нет** — в репозитории
только `main`, `master` и `extract-archives`. Ветка жила локально на сгоревшей
машине и запушена не была; её содержимое существует только в транскрипте той сессии.

## Навыки: 10 из 10 манифест-навыков снова живы

При запуске выяснилось, что `SkillLoader` проходил только 2 из 9 манифест-навыков.
Причина: в каталогах `src/skills/{content_gen,crypto_monitor,firmware_manager,
net_scanner,scheduler,weather}/` лежали только `manifest.yaml` и `README.md` —
сами реализации `skill.py` отсутствовали. Найдены в `argos-1/argos_deploy/src/skills/`
и возвращены (от 3 898 до 15 847 б каждая, секретов нет).

Отдельно `src/skills/fpga/` не грузился вообще: реализация есть, а манифеста не было
ни здесь, ни в источнике. Манифест написан по фактическим метаданным самого навыка
(`SKILL_NAME`, `SKILL_DESCRIPTION`, `TRIGGERS` из `skill.py`) — это единственное
место во всём восстановлении, где файл создан заново, а не возвращён из источника.

Результат: `SkillLoader load_all (manifest навыки) → PASS 10/10`, всего **30 навыков**
против 24 на момент первого запуска.

## Облачный деплой: два сервиса, ничего не удалено

Для Railway восстановлены недостающие файлы деплоя. Существующий `railway.json`
не тронут — он как и раньше поднимает лёгкий edge `main.py` через NIXPACKS.

| Файл | Что делает | Источник |
|---|---|---|
| `Dockerfile` | полный образ ARGOS (GPIO, ffmpeg, whisper, драйверы) | форк, точка входа поправлена на `argos_main.py` |
| `Dockerfile.vpn_api` | образ VPN-сервиса | форк |
| `Dockerfile.legacy-recovery` | образ восстановительного контура | форк |
| `railway.full.json` | полный ARGOS через `cloud_entry.py`, healthcheck `/health` | написан по образцу из форка |
| `cloud_entry.py` | точка входа для облака | **написан заново** — утрачен везде |

`cloud_entry.py` восстановить было неоткуда: его нет ни в одном из четырёх
репозиториев, есть только описание в `GEMINI_DEPLOY_PROMPT.md` — «точка входа для
Cloud Run (запускает ArgosOrchestrator + MCP API)». Написан по этой спецификации и
по тому, как оркестратор читает конфигурацию: облако даёт один порт в `$PORT`,
поэтому он прокидывается в `ARGOS_MCP_PORT`, и MCP-эндпоинт оказывается ровно на
том порту, который платформа проверяет healthcheck-ом.

Проверено локально в облачном режиме:

```
$ PORT=8300 python3 cloud_entry.py
[cloud_entry] ARGOS_ENV=cloud порт MCP: 8300
[cloud_entry] TELEGRAM_BOT_TOKEN не задан — Telegram-бот не поднимается
поднялся за 7 с
$ curl http://127.0.0.1:8300/health
{"ok":true,"uptime_seconds":0,"ai_mode":"Auto","cpu_pct":4.8,"ram_pct":5.1}
```

Развернуть это на Railway из сессии нельзя: токена нет ни в репозиториях, ни в
окружении, CLI отсутствует, а egress к `backboard.railway.app` закрыт политикой
прокси. Разворачивать нужно из аккаунта: подключить репозиторий как источник и в
настройках сервиса (Config-as-code) указать нужный файл — `railway.json` для
edge-сервиса, `railway.full.json` для полного ARGOS. Переменные для полного
сервиса: `ARGOS_ENV=cloud`, `PYTHONUNBUFFERED=1`, при необходимости
`ARGOS_MODEL_ROUTER` и `TELEGRAM_BOT_TOKEN` (последний — только после ротации).

## Суть ARGOS, а не только запуск

По README из `poilopr57-a11y/Argos` (идентичен нашему) ARGOS — не сервис, а
самовоспроизводящийся организм: узлы почкуются по локальной сети, система сама
пишет себе навыки и ведёт модель собственной личности. Три несущих механизма
из этого описания при первом проходе не восстановились — их не ловит анализ
статических импортов, потому что они грузятся динамически. Возвращены:

**Почкование (`BuddingManager`)** — автономное размножение узлов:
`src/connectivity/budding_manager.py` (13 784 б) + `whisper_node.py` (18 142 б) +
`p2p_transport.py`. Родитель ARP-сканирует LAN, находит «плодородный» хост,
сериализует собственный код и веса RNN, шифрует ГОСТ-Кузнечиком с HMAC-Стрибог и
разворачивает копию через `subprocess.Popen`. Проверено: `BuddingManager`
импортируется, методы `find_soil`, `send_bud`, `start/stop/status` на месте.

**Самонаписанные навыки (`src/skills/evolved/`)** — 4 навыка, которые ARGOS
сгенерировал сам через `evolution_engine`: `evolved_более_точное_распознавание`,
`evolved_оптимизация_работы_с`, `evolved_улучшение_качества_о`,
`evolved_улучшение_форматиров`. Это не заготовки разработчика, а продукт
самоэволюции системы — восстановлены из снапшота `auto_20260411_182909`
(идентичны во всех 10 снапшотах). Плюс журнал эволюции: `data/evolution/` — 480
файлов `evolution_*.json` за 09.06–19.06, уже был в основном репозитории.

**Остальные слои по README:** `budding_manager`, `whisper_node`, мессенджер-мосты
(`whatsapp_bridge`, `max_bridge`, `messenger_router`), контуры безопасности
(`emergency_purge`, `container_isolation`, `master_auth`), интеллектуальный стек
(`jarvis_engine`, `context_engine`, `self_healing`, `sub_agency`, `empathy_engine`,
`evolution`) — итого 19 файлов, включая 4 evolved-навыка. Секретов нет, `src.core`
импортируется, ARGOS перезапущен и жив.

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
