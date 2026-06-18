# ARGOS Root Cleanup Audit

Хранилище: `F:\debug\аргос`

## Контекст

В `F:\debug\argoss` подтверждена проблема с дублями между корнем репозитория и `src/`.
Проектовая упаковка, README, тесты и большинство импортов считают `src/` канонической зоной кода.

## Что найдено

- Найдено `35` пересечений root/src по имени Python-файла
- Среди них есть как минимум:
  - `core.py`
  - `ai_failover.py`
  - `cleanup_repo.py`
  - `graceful_shutdown.py`
  - `hardware_intel.py`
  - `health_monitor.py`
  - `life_support.py`
  - `life_support_v2.py`
  - `startup_validator.py`
  - `status_report.py`
  - `tool_calling.py`

## Отдельно по LifeSupport

Обнаружены 8 копий семейства `life_support*`:

- `F:\debug\argoss\life_support.py`
- `F:\debug\argoss\life_support_v2.py`
- `F:\debug\argoss\src\life_support.py`
- `F:\debug\argoss\src\life_support_v2.py`
- `F:\debug\argoss\argoss\life_support.py`
- `F:\debug\argoss\argoss\life_support_v2.py`
- `F:\debug\argoss\argos_deploy\life_support.py`
- `F:\debug\argoss\argos_deploy\life_support_v2.py`

### Фактическая картина по хэшам

- корень `life_support.py` == `argos_deploy/life_support.py`
- корень `life_support_v2.py` == `argos_deploy/life_support_v2.py`
- `src/life_support.py` отличается от корня и deploy
- `src/life_support_v2.py` отличается от корня и deploy
- `argoss/life_support.py` и `argoss/life_support_v2.py` — отдельная урезанная ветка

### Канонический путь использования

- `main.py` запускает `src.core`
- `src/core.py` импортирует `from src.life_support import ArgosLifeSupport`

Итог: каноническая активная ветка для основного проекта — `src/life_support.py`.
Удаление или перенос нельзя делать по одному только имени файла.

## Отдельно по hardware_intel

### Что проверено

- `src/core.py`
- `src/argos_patcher.py`
- `src/skills/hardware_intel.py`
- `src/hardware_intel.py`
- живые тесты в `tests/`

### Вывод

Активная ветка проекта уже использует только правильное имя `hardware_intel`.

Старое имя `ardware_intel` осталось в трёх ролях:

- как историческая запись в rename-логике (`src/bump_version.py`)
- как хвост совместимости в тестах
- как побочная старая копия в дереве `argoss/`

Это не активная поломка основного ядра, а миграционный хвост.
При cleanup его нужно учитывать отдельно от живого кода.

## Отдельно по ghost_c2

### Что найдено

- `src/connectivity/ghost_c2.py` существовал как маленький модуль без активных импортов в основном `src/` дереве
- По содержимому это был скрытый канал на базе GitHub Gist (`token`, `gist_id`, `requests.patch`)

### Решение

- Модуль обезврежен прямо в коде
- Имя файла и класс `GhostLink` сохранены для совместимости
- Метод `broadcast()` теперь явно поднимает `RuntimeError`
- Исходный текст сохранён отдельно как legacy-материал
- Создан `ghost_c2_legacy.py`
- Архивная копия вынесена в `duplicates_archive/ghost_c2_legacy_2026-05-03/`

### Почему

- такой скрытый канал опасен для публичных сборок
- имя `ghost_c2` и сама реализация создают ненужный репутационный и security-риск
- так как активных импортов не найдено, отключение безопаснее, чем оставлять канал живым

## Важное наблюдение

Не все дубли безопасно удалять:

- некоторые файлы отличаются по размеру
- некоторые явно расходятся по содержимому
- дерево git уже сильно грязное

Поэтому прямое удаление без сравнения было бы рискованным.

## Что уже перенесено в архив

В отдельную папку без удаления перенесены только побайтно идентичные root/src дубли:

- `argos_desktop.py`
- `status_report.py`

Папка архива:

- `F:\debug\argoss\duplicates_archive\root_identical_dupes_2026-05-03\`

Оставшиеся `33` пересечения по имени не были тронуты, потому что содержимое различается.

## Внутренние точные дубли корня

Отдельно внутри самого корня были найдены и архивированы точные дубли/неканоничные копии:

- `awareness (1).py`
- `z.py`
- `Python File (2).py`
- `12.py`
- `integrator_v25.py.py`

Папка архива:

- `F:\debug\argoss\duplicates_archive\root_internal_exact_dupes_2026-05-03\`

Пояснение:

- `awareness (1).py` — дубль `awareness.py`
- `z.py` — дубль `x.py`
- `Python File (2).py` — дубль `Python File.py`
- `12.py` и `integrator_v25.py.py` — две одинаковые копии странной заготовки, сохранены как исторический шум

## Что изменено

Обновлён скрипт:

- `F:\debug\argoss\cleanup_root.py`

Теперь он:

- работает в `dry-run` по умолчанию
- требует `--apply` для реальных изменений
- сравнивает root-файл и `src/`-копию по SHA-256
- не трогает файлы, если содержимое отличается
- архивирует идентичные дубли вместо удаления
- показывает дополнительные дубли вне жёсткого списка

## Следующий безопасный шаг

Когда рабочий Python снова будет доступен:

```bash
python cleanup_root.py
python cleanup_root.py --apply
```

Сначала только dry-run, потом точечное применение.

## Статус

- Аудит дублей: выполнен
- Безопасный cleanup-скрипт: подготовлен
- Автопроверка запуском: отложена, потому что в текущем окружении не найден рабочий Python runtime

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Projects Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Projects Hub]]
