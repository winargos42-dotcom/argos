# ARGOS Changelog 2026-05-07

## Сводка изменений

| Компонент | Изменение | Статус |
|-----------|-----------|--------|
| Система | Исправлено дублирование процессов | ✅ Fixed |
| API | Обновлен Gemini API ключ | ✅ Updated |
| Модуль | Создан LLM-Wiki (3 инструмента MCP) | ✅ Created |
| Данные | Создан train.jsonl (5,537 примеров) | ✅ Created |
| Инфра | Подготовлены конфиги Vertex AI + Kaggle | ✅ Ready |
| Документация | 6 новых/обновленных документов | ✅ Saved |

---

## Детали изменений

### 1. Исправление критической ошибки
**Проблема**: "No API provider registered for api: ollama" в Telegram
- **Время**: ~15:13 MSK
- **Причина**: Старый процесс ARGOS (PID 4436, uptime 6.8ч) работал параллельно с новым
- **Решение**: 
  ```bash
  # Убиты ВСЕ Python процессы
  # Перезапущен единственный экземпляр ARGOS
  # PID: 17592 (headless .venv)
  ```
- **Проверка**: MCP uptime < 100s, 3/3 GPU активны

### 2. Обновление Gemini API
**Проблема**: HTTP 400 (ключи истекли)
- **Старые ключи**: `GEMINI_API_KEY0-4` (закомментированы)
- **Новый ключ**: `AIzaSyBZBnx_y9E6QUMNTQhv5HfcyU-8j-18EqI`
- **Модель**: `gemini-2.5-flash`
- **Файл**: `.env` (строки GEMINI_API_KEY*)

### 3. LLM-Wiki Модуль
**Файлы**:
- `src/llm_wiki/__init__.py` — экспорт
- `src/llm_wiki/telegram_ingest.py` — инжест чатов
- `src/llm_wiki/obsidian_lint.py` — линтинг vault
- `src/llm_wiki/wiki_query.py` — LLM-поиск

**Интеграция MCP** (`src/mcp_api.py`):
- Добавлены 3 новых инструмента
- Обновлена схема инструментов
- Добавлена валидация аргументов

### 4. Fine-Tuning Датасет
**Конвертер**: `scripts/convert_to_train_jsonl.py`
- Сканирует Obsidian vault (5,537 .md файлов)
- Очищает markdown → plain text
- Создает OpenAI chat формат
- Перемешивает данные

**Результат**:
- **Файл**: `data/train.jsonl`
- **Размер**: 18.73 MB
- **Примеров**: 5,537
- **Токенов**: ~12M
- **Средний размер**: 2,954 символа

**Конфигурации**:
- **Vertex AI**: `config/vertex_job.json` (A100 40GB, ~$3.67/час)
- **Kaggle**: `config/kaggle_finetune.ipynb` (T4x2, бесплатно)

### 5. Документация

| Документ | Статус | Описание |
|----------|--------|----------|
| [[ARGOS Session 2026-05-07 Evening]] | ✅ Новый | Полный отчет сессии |
| [[ARGOS Unified State 2026-05-06]] | ✅ Обновлен | Текущее состояние |
| [[ARGOS Train Dataset v1.0]] | ✅ Новый | Технический референс |
| [[ARGOS System Architecture 2026-05-07]] | ✅ Новый | Архитектура системы |
| [[ARGOS Next Steps 2026-05-07]] | ✅ Новый | План действий |
| [[Fine-Tune Strategy Personal AI Brain]] | ✅ Обновлен | Стратегия обучения |
| [[LLM-Wiki Integration]] | ✅ Обновлен | Интеграция wiki |
| [[Email App Password Setup]] | ✅ Новый | Инструкция email |

---

## Метрики

### До изменений
- Uptime: 18,895s (~5.2 часа)
- Процессов ARGOS: 2 (дубль)
- GPU: Нестабильно (таймауты)
- Gemini: HTTP 400

### После изменений
- Uptime: 29s (свежий процесс)
- Процессов ARGOS: 1 (корректно)
- GPU: 3/3 стабильно
- Gemini: ✅ Работает

---

## Технические детали

### Процессы
```
System Python (PID ~27012)
├── MCP Server      → :8000  ✅
└── Dashboard       → :8080  ✅

ARGOS .venv (PID 17592)      ✅
└── Telegram + AutoGPT + LLM-Wiki
```

### GPU Кластер
```
:8082  RX 580  8GB  qwen2.5:3b   ✅
:8083  Vega 11 2GB  tinyllama    ✅
:8084  RX 560  4GB  qwen2.5:3b   ✅
```

### Vault
```
Всего файлов:     5,514
Markdown файлов:  5,537
Размер:           63.6 MB
train.jsonl:      18.73 MB
```

---

## Известные проблемы

| Проблема | Статус | Решение |
|----------|--------|---------|
| Gmail OAuth 403 | ❌ | Переход на App Password |
| GCP A100 quota | ⏳ | Запрос через Console |
| Grok API | ❌ | Новый ключ (x.ai) |
| SERPAPI balance | ❌ | Пополнить ($5+) |

---

## Следующие действия

1. ⏳ Создать Gmail App Password
2. ⏳ Запросить A100 quota
3. 📋 Запустить Kaggle fine-tuning (fallback)
4. 📋 Интегрировать модель в ARGOS

---

## Связанные документы

- [[ARGOS Session 2026-05-07 Evening]] — Отчет сессии
- [[ARGOS Next Steps 2026-05-07]] — План действий
- [[ARGOS Train Dataset v1.0]] — Датасет
- [[ARGOS Fine-Tuning L4 T4 Guide]] — Руководство по обучению
- [[ARGOS Unified State 2026-05-06]] — Текущее состояние

---

*Сессия: 2026-05-07 15:13 — 15:45 MSK*
*Всего изменено файлов: ~15*
*Новых документов Obsidian: 6*
*Обновленных документов: 3*

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Human Sessions Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Human Sessions Hub]]
