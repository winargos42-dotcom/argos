---
argos_import: project_file
source_path: reports/2026-05-10_training_autopilot_upgrade.md
source_abs: F:\debug\argoss\reports\2026-05-10_training_autopilot_upgrade.md
source_ext: .md
source_sha256: cf3024c1dbb2beeb3be85543ea3a140bf3ff8c3f5acc4192977e4fd28e21e0f1
text_sha256: cf3024c1dbb2beeb3be85543ea3a140bf3ff8c3f5acc4192977e4fd28e21e0f1
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-11 15:48:31
---

# 2026-05-10_training_autopilot_upgrade.md

- Source: `reports/2026-05-10_training_autopilot_upgrade.md`
- Extract: `text`
- SHA256: `cf3024c1dbb2beeb3be85543ea3a140bf3ff8c3f5acc4192977e4fd28e21e0f1`

## Content

# 2026-05-10 Training Autopilot Upgrade

## Что сделано

- Усилен экспорт тренировочного датасета из Obsidian:
  - include/exclude фильтры по папкам vault
  - фильтр по свежести (`recent_days`)
  - приоритет новых заметок
- Усилен Colab bundle pipeline:
  - параметры фильтрации пробрасываются из pipeline в export
  - отчеты расширены параметрами фильтрации
- MCP команды обучения обновлены:
  - `argoss dataset_build_obsidian`
  - `argoss colab_pipeline`
  - теперь используют `ARGOS_TRAIN_*` ENV и показывают их в ответе

## Новые ENV

- `ARGOS_TRAIN_INCLUDE_ROOTS`
- `ARGOS_TRAIN_EXCLUDE_ROOTS`
- `ARGOS_TRAIN_RECENT_DAYS`

## Проверка

- `python -m py_compile scripts/export_obsidian_training_dataset.py scripts/prepare_colab_finetune_bundle.py src/mcp_api.py`
- `pytest tests/test_obsidian_training_export.py -q` → `2 passed`
- `python scripts/prepare_colab_finetune_bundle.py --max-examples 2500 --max-chars 1800 --recent-days 30`

## Результат прогонки

- Obsidian rows: `455`
- Evolver rows: `3938`
- Merged rows: `2500`
- Bundle: `artifacts/colab_finetune_bundle_20260510_120818.zip`
- Dataset: `data/colab_finetune_dataset.jsonl`
- Reports:
  - `reports/obsidian_training_dataset_report.md`
  - `reports/colab_finetune_bundle_report.md`

## MCP smoke-check

- `ArgosMCPServer._argoss_command('dataset_build_obsidian')`:
  - notes_scanned: `159`
  - examples: `455`
  - include/exclude фильтры отображаются корректно
- `ArgosMCPServer._argoss_command('colab_pipeline')`:
  - merged_rows: `2000`
  - bundle: `artifacts/colab_finetune_bundle_20260510_121120.zip`
  - include/exclude: `(script default)` отображается корректно

## Примечание по проверке

- Разовая ошибка `py_compile` по `mcp_api.py` из-за lock на `.pyc` (`WinError 5`) не воспроизвелась в runtime:
  MCP smoke-команды отработали успешно.

## Исправление тренера (TRL API mismatch)

- Исправлен `src/argos_lora_trainer.py`:
  - динамическая проверка параметров `SFTTrainer.__init__`
  - безопасная передача `max_seq_length / dataset_text_field / packing` только если поддерживаются текущей версией `trl`
  - устранён крэш: `TypeError: SFTTrainer.__init__() got an unexpected keyword argument 'max_seq_length'`

## Текущий запуск обучения

- Установлен пакет: `trl==1.4.0`
- Запущен quick-train в фоне:
  - PID: `15368`
  - Команда: `python src/argos_lora_trainer.py --quick`
  - Логи:
    - `logs/lora_quick_20260510_122012.out.log`
    - `logs/lora_quick_20260510_122012.err.log`
- Статус по логу: этап LoRA train стартовал (`Начинаю LoRA обучение...`).

## Следующий шаг

1. В Colab: распаковать bundle и прогнать quick train:
   - `python src/argos_lora_trainer.py --quick`
2. После валидации — full train на том же датасете.

## Stability Patch (MCP/Telegram AI Response)

- Исправлен loop-flood в `src/core.py`:
  - `Ollama (Argoss)` больше не включается в `auto_providers`, если провайдер на cooldown.
  - Добавлен ранний guard в `_ask_ollama()` на cooldown.
- Улучшен анти-флуд по квоте Gemini:
  - `RESOURCE_EXHAUSTED / 429` теперь ставит `Gemini` на cooldown через `_disable_provider_temporarily`.
- Ускорен консенсус:
  - `ARGOS_AUTO_COLLAB_MAX_MODELS` default: `4` (было `8`).
  - Добавлен `ARGOS_CONSENSUS_EARLY_STOP` (default `on`) — ранний выход после `consensus_n`.
- Расширен fast-path статуса провайдеров:
  - `src/mcp_api.py` и `src/connectivity/telegram_bot.py` теперь мгновенно обрабатывают
    формулировки вида `статус ai провайдеров`.

### Проверка

- `python -m py_compile src/core.py src/mcp_api.py src/connectivity/telegram_bot.py` → OK
- `pytest tests/test_core_provider_resilience.py tests/test_mcp_fast_ai_status.py -q` → `3 passed`
- MCP smoke:
  - `command: "расскажи статус ai провайдеров кратко"` → `~2.0s`, стабильный direct-ответ.

### Наблюдение

- Свободные чат-запросы (не system/fast command) по MCP всё ещё могут доходить до `MCP timeout`
  при высокой загрузке/недоступных провайдерах. Функциональный контур диагностики и управления
  (status/providers/skills/argoss commands) стабилен и быстрый.

## Mini LoRA Run (после патчей)

- Выполнен контрольный train:
  - `python src/argos_lora_trainer.py --step train --steps 3 --examples 16`
- Результат:
  - `train_loss: 2.892`
  - `train_runtime: ~69s`
  - адаптер сохранён: `models/argos-lora-adapter`
- Ограничение:
  - предупреждение HF Hub об unauthenticated запросах остаётся (`HF_TOKEN` не подхвачен рантаймом тренера).

## Behavior Logic Upgrade (MCP/Telegram actions)

- Исправлена логика аудита ответов (`scripts/audit_argos_behavior.py`):
  - убрано ложное срабатывание `error` по строкам формата `❌ 0`
  - добавлена строгая классификация по JSON-RPC и явным сигнатурам ошибок
- Усилен warmup-контур GPU (`main.py`):
  - добавлены ретраи старта GPU-провайдеров:
    - `ARGOS_GPU_WARMUP_RETRIES=2` (default)
    - `ARGOS_GPU_WARMUP_RETRY_DELAY_SEC=2.0` (default)
  - снижены ложные предупреждения на старте (GPU может подняться со 2-й попытки)

### Контроль

- `python -m py_compile main.py scripts/audit_argos_behavior.py` → OK
- `pytest tests/test_mcp_fast_ai_status.py tests/test_core_provider_resilience.py -q` → `4 passed`
- Behavioral audit:
  - `reports/argos_behavior_audit_20260510_133635.md` → `ok=11, errors=1` (до)
  - `reports/argos_behavior_audit_20260510_133844.md` → `ok=12, errors=0` (после)

## MCP Training Pipeline Runtime Args

- Обновлён `src/mcp_api.py`:
  - `argoss_dataset_build_obsidian` и `argoss_colab_pipeline` теперь принимают runtime-аргументы:
    - `include_roots`, `exclude_roots`, `recent_days`, `max_examples`, `max_chars`
  - `tools/list` inputSchema расширен для этих двух инструментов
- Проверка:
  - `argoss_colab_pipeline` с аргументами
    - `{recent_days:30, max_examples:1234, max_chars:900}`
  - результат:
    - `merged_rows: 1234`
    - `recent_days: 30`
    - `max_examples: 1234`
    - `max_chars: 900`
    - bundle: `artifacts/colab_finetune_bundle_20260510_135714.zip`

## GPU Starter Hardening

- Обновлён `scripts/three_gpu_start.ps1`:
  - безопасный поиск `llama-server.exe` (ENV/PATH/локальная сборка/legacy path)
  - фильтрация только runnable бинарников
  - безопасный `Start-LlamaInstance` с понятными сообщениями
  - устранён шум `Test-Path Access denied`
- Поведение:
  - если валидный бинарник не найден/недоступен, скрипт завершается чисто с диагностикой, без stacktrace.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Training Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Training Hub]]
