# Запуск ARGOS Universal OS в песочнице (Vibe)

Минимальный воспроизводимый запуск **оригинального кода** репозитория `argos`
без Docker, секретов и внешних сервисов.

## Что запускается

| Компонент | Файл (оригинал) | Порт |
|---|---|---|
| Test LLM adapter (явно помечен, не модуль ARGOS) | `vibe_run/test_llm_adapter.py` | 11434 |
| MCP API v2.1.4 | `src/mcp_api_standalone.py` | 8000 |
| ARGOS API gateway v2.1.6 | `main.py` | 8080 |

Внешние пиров (Cloudflare `argosssss.win`, Telegram, Gist) переопределяет
пустыми env-переменными: узел работает в standalone-режиме, только loopback.

## Запуск

```bash
./vibe_run/run_argos.sh
```

Скрипт создаёт venv в `/workspace/argos-runtime/venv` (если нет), ставит
`fastapi uvicorn httpx requests python-dotenv`, стартует три процесса и
делает health-проверки. PID-файлы и логи: `/workspace/argos-runtime/logs/`.

## Проверка

```bash
curl -s http://127.0.0.1:8080/health
curl -s http://127.0.0.1:8080/p2p/nodes      # mcp-пир должен быть ok:true
curl -s -X POST http://127.0.0.1:8080/ask \
     -H 'Content-Type: application/json' \
     -d '{"prompt":"ping"}'                  # gateway -> MCP -> test adapter
```

## Память и оркестрация (оригинальные модули)

`src/swarm/argos_master_core.py` (ArgosMasterCore: SQLite-память, NeuralNexus,
ACL, execute) и `src/cognitive_memory.py` (CognitiveMemory: события, знания,
цели, рефлексия) запускаются напрямую из исходников — см. отчёт развёртывания.

## Реальная LLM (этап 2+)

`vibe_run/local_llm_server.py` — настоящий инференс Qwen2.5-0.5B-Instruct Q4_K_M
через llama-cpp-python на loopback :11434 (Ollama- и OpenAI-совместимые формы).
`run_argos.sh` автоматически выбирает реальную модель, если GGUF найден, иначе
явно помеченный тестовый адаптер.

## Автономный цикл, диагностика, восстановление (этап 4)

```bash
# Диагностика: сервисы, cgroup, диск, ускорители (честно), SQLite-память
ARGOS_DIAG_PATH=/workspace/argos-runtime/diagnostics.json \
  python vibe_run/diagnostics.py

# Целевой цикл агента: goals из CognitiveMemory -> ArgosMasterCore.execute
# (ACL) -> shell/remember/recall напрямую, остальное -> NeuralNexus -> Qwen.
ARGOS_LOOP_MAX=3 ARGOS_LOOP_IDLE_EXIT=1 python vibe_run/agent_loop.py
# Цель добавляется оригинальным API:
#   cm = CognitiveMemory(prefer_pg=False); cm.add_goal("shell echo hi", priority=1)

# Восстановление оригинальных модулей с X230 (после ручного переноса файлов
# в staging-каталог с layout recovery/ + runtime/app/src/):
./vibe_run/restore_from_x230.sh <staging_dir>
# Проверяет наличие всех 19 файлов, делает бэкап перезаписываемых, сверяет
# SHA256 источник<->назначение, затем импорт-проверки ArgosCore/AWACore и pytest.
```

## Параллельный пул, peering, изолированные сессии (этап 5)

```bash
# Пул воркеров: атомарный захват целей (UPDATE goals WHERE state='active'),
# watchdog на задачу, метрики в JSON. Двойное выполнение исключено.
ARGOS_POOL_WORKERS=3 ARGOS_POOL_IDLE_EXIT=1 python vibe_run/agent_pool.py
#
# Восстановление после падения воркера — строго однократно: задача с маркером
# task_done закрывается как done без перезапуска; незавершённая помечается
# interrupted:<worker> и НЕ перезапускается автоматически (её побочный эффект
# мог уже произойти). Явный перезапуск таких задач — только с
# ARGOS_POOL_REQUEUE_INTERRUPTED=1 (риск дубля принимается оператором).

# Готовность peering: локальные сервисы + пиры ТОЛЬКО из env; публичные
# argosssss.win жёстко запрещены; link_state=OPERATIONAL только при реальном
# ответе пира в этом запуске.
ARGOS_X230_MCP_URL=http://127.0.0.1:18000 python vibe_run/peering_check.py

# Бенчмарк изолированных сессий: N отдельных процессов, свои SQLite,
# синтетические сообщения, замеры задержек (память/shell/LLM, p95).
ARGOS_ISO_SESSIONS=3 ARGOS_ISO_ROUNDS=2 python vibe_run/session_isolation_test.py

# Восстановление из ZIP-снапшота X230 (проверка SHA256 архива обязательна):
./vibe_run/restore_from_x230.sh --archive <snapshot.zip>
# Ожидаемый SHA256 архива: 6b1a60237cca2bfd2b202457da24043eb6cca3de59da9baeaf0d4da73347606e
# Отсутствующие модули REPORTУЮТСЯ, не имитируются; частичное восстановление —
# только с ALLOW_MISSING=1.
```

Подробности восстановления и карта 13 недостающих модулей:
`vibe_run/AWA_CORE_RECOVERY_MAP.md`.

## Известные ограничения

- `argos_ai_brain` (Brain API, агенты) и ~14 модулей `src/core.py` (AwaCore)
  **отсутствуют в репозитории** — восстановить их из оригинала невозможно.
- `src/argos_logger.py` отсутствовал; добавлен минимальный shim на stdlib
  (только логирование), чтобы оригинальные модули запускались без правок.
- Тестовый адаптер `[TEST-ADAPTER]` используется ТОЛЬКО если GGUF-модель не
  найдена; при наличии модели работает реальный Qwen2.5-0.5B (61 tok/s, 4 потока).
- Оборудование (P100, SPR2801S, Coral Edge TPU, FPGA) недоступно и не
  имитируется.

## Постоянный узел (этап 7): демон

```bash
# Фоновая обработка очереди: 2 воркера (жёсткий лимит), heartbeat в SQLite и
# daemon_heartbeat.json, опрос GitHub (коммиты main + открытые issues) раз в
# 15 минут — только чтение; новые issues ставятся в очередь ТОЛЬКО как
# "analyze:" (через локальную LLM), shell-цели из непроверенных источников
# не ставятся никогда.
nohup python vibe_run/daemon.py > "$ARGOS_RUNTIME/logs/stage7/daemon.out" 2>&1 &

# Состояние: daemon_heartbeat.json (ts, boot_id, сервисы, очередь),
# daemon_state.json (boot_id, последний коммит, виденные issues),
# logs/stage7/daemon_results.jsonl (результат каждой задачи).
# После перезапуска песочницы демон сравнивает boot_id, логирует
# sandbox_restart и восстанавливает очередь строго однократно.
```
