---
argos_import: project_file
source_path: CONTRIBUTING.md
source_abs: F:\debug\argoss\CONTRIBUTING.md
source_ext: .md
source_sha256: acdcf8d8084dbb5e019a6f2bf2837c71889d570752b78f57576bc9e4b3387693
text_sha256: acdcf8d8084dbb5e019a6f2bf2837c71889d570752b78f57576bc9e4b3387693
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# CONTRIBUTING.md

- Source: `CONTRIBUTING.md`
- Extract: `text`
- SHA256: `acdcf8d8084dbb5e019a6f2bf2837c71889d570752b78f57576bc9e4b3387693`

## Content

# Участие в разработке Argos Universal OS

Спасибо, что хотите помочь проекту Argos!

## Как начать

1. Форкните репозиторий и создайте ветку от `main`.
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Инициализируйте проект:
   ```bash
   python genesis.py
   ```
4. Проверьте целостность:
   ```bash
   python health_check.py
   ```
5. Запустите тесты:
   ```bash
   pytest -q
   ```

## Что можно улучшать

- Новые `skills` в `src/skills/`
- IoT и bridge-модули в `src/connectivity/`
- Улучшение observability (`src/observability.py`)
- Сценарии в `examples/`
- Документация в `docs/`

## Стандарты кода

- Python 3.10+
- Малые, сфокусированные PR
- Без хардкода секретов (используй `.env`)
- Graceful fallback для optional-зависимостей (SDR, BLE, Kivy и т.д.)
- Новые функции — с тестами в `tests/`

## Процесс Pull Request

1. Обновите код и документацию
2. Убедитесь, что проверки проходят:
   ```bash
   python health_check.py
   pytest -q
   black src/ --check
   flake8 src/ --max-line-length=120
   ```
3. Опишите: что изменено, почему, как проверяли

## Безопасность

- Не публикуйте API-ключи, токены и приватные данные
- Для уязвимостей — приватный disclosure: seva1691@mail.ru

## Направления, где нужна помощь

- Новые IoT-протоколы и bridge-адаптеры
- Skills для новых сервисов и API
- Тесты (покрытие ~14%, цель 30%+)
- Документация и примеры сценариев
- Оптимизация Speculative Consensus pipeline

## 🧪 Запуск тестов

```bash
# Быстрый запуск (рекомендуется)
make test

# Или напрямую через pytest
pytest tests/ -q --tb=short

# С покрытием кода
pytest tests/ --cov=src --cov-report=term-missing
```

## 🔧 Перед коммитом (обязательно)

```bash
# 1. Исправить кодировку
make fix-encoding

# 2. Проверить синтаксис
find . -name "*.py" ! -path "*/venv/*" ! -path "*/__pycache__/*" -exec python3 -m py_compile {} +

# 3. Запустить тесты
make test
```

## 📋 Стандарты кода

- Python 3.10+
- Форматирование: `black` (max line length 120)
- Линтер: `flake8 --max-line-length=120`  
- Логирование: использовать `from src.argos_logger import get_logger`, **не** `print()`
- Никаких хардкоженных секретов в коде
- Все новые функции — с docstring

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
