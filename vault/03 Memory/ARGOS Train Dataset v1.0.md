# ARGOS Train Dataset — Technical Reference

Дата создания: `2026-05-07`
Версия датасета: `v1.0`

## Статистика

| Параметр | Значение |
|----------|----------|
| **Всего примеров** | 5,537 |
| **Размер файла** | 18.73 MB |
| **Формат** | JSON Lines (OpenAI chat) |
| **Оценка токенов** | ~12M |
| **Средний размер примера** | 2,954 символа |
| **Мин/Макс** | 329 / 4,172 символа |

## Структура

```json
{
  "messages": [
    {"role": "system", "content": "You are ARGOS, a software engineer..."},
    {"role": "user", "content": "Tell me about: README.txt"},
    {"role": "assistant", "content": "This is a stand-alone library..."}
  ],
  "metadata": {
    "source": "04 Project Mirror/.../README.txt",
    "category": "04 Project Mirror",
    "created": "2026-05-07T15:25:00"
  }
}
```

## Категории данных

| Категория | Файлов | Описание |
|-----------|--------|----------|
| **04 Project Mirror** | 5,379 | Код, документация проектов, README |
| **03 Memory** | 40 | Архивные заметки, инструкции |
| **06 Link Stubs** | 39 | Ссылки и референсы |
| **05 SharedMemory Mirror** | 33 | Shared данные |
| **02 Logs** | 21 | Логи системы |
| **00 Memory Web** | 14 | Веб-скрапинг |
| **01 Projects** | 4 | Текущие проекты |
| **Daily** | 1 | Ежедневные заметки |
| **(root)** | 6 | Корневые файлы |

## Процесс создания

### 1. Сканирование vault
- Рекурсивный обход `F:\debug\аргос`
- Фильтрация: только `.md` файлы
- Всего найдено: 5,537 Markdown файлов

### 2. Очистка markdown
- Удаление YAML frontmatter
- Удаление wiki-ссылок `[[...]]`
- Удаление markdown-ссылок `[...](...)`
- Удаление изображений `![...](...)`
- Замена код-блоков на `[CODE]`
- Удаление inline code
- Удаление заголовков `#`
- Удаление bullet points
- Удаление таблиц
- Сжатие пустых строк

### 3. Создание примеров
- System prompt зависит от категории:
  - `03 Memory` → ARGOS с long-term memory
  - `04 Project Mirror` → Software engineer
  - `02 Logs` → System analyst
  - `Telegram` → Conversational assistant
  - Default → General assistant

- User prompt: `Tell me about: {title}`
- Assistant: очищенный контент (обрезан до 4,000 символов)

### 4. Перемешивание
- Random shuffle для предотвращения переобучения
- Сохранение в `data/train.jsonl`

## Файлы

| Файл | Путь | Описание |
|------|------|----------|
| Датасет | `data/train.jsonl` | 18.73 MB |
| Конвертер | `scripts/convert_to_train_jsonl.py` | Python скрипт |
| Vertex Config | `config/vertex_job.json` | Vertex AI CustomJob |
| Kaggle Notebook | `config/kaggle_finetune.ipynb` | Kaggle fallback |

## Fine-Tuning цели

### Модель: Mistral NeMo 12B Instruct
- **Параметры**: 12B
- **Контекст**: 128K токенов
- **Формат**: Instruct (chat template)
- **Лицензия**: Apache 2.0

### Гиперпараметры

| Параметр | Значение |
|----------|----------|
| Epochs | 3 |
| Batch size | 4 (Vertex) / 2 (Kaggle) |
| Learning rate | 2e-5 |
| Max seq length | 4,096 |
| Optimizer | AdamW |
| Precision | FP16 |

## Платформы

### Option A: Vertex AI (рекомендуется)
- **Машина**: `a2-highgpu-1g` (1x A100 40GB)
- **Стоимость**: ~$3.67/час
- **Время обучения**: ~2-3 часа (5,537 примеров)
- **Требование**: Квота A100

### Option B: Kaggle (fallback)
- **GPU**: T4 x2 (бесплатно)
- **Лимит**: 30 часов/неделю
- **Время обучения**: ~4-6 часов
- **Преимущество**: Бесплатно, доступно сразу

## Дальнейшие шаги

1. **Загрузка на GCS**: `gsutil cp data/train.jsonl gs://argos-bucket/`
2. **Fine-tuning**: Запуск Vertex AI CustomJob
3. **Экспорт модели**: Сохранение в GCS
4. **Интеграция**: Подключение к ARGOS через MCP

## Валидация качества

Перед запуском:
- [ ] Проверить 10 случайных примеров на корректность
- [ ] Убедиться в отсутствии PII (персональных данных)
- [ ] Проверить баланс категорий
- [ ] Замерить perplexity на hold-out set

---

*Создано: 2026-05-07*
*Версия: 1.0*
*Следующее обновление: после первого fine-tuning*

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

## Связанные документы

- [[ARGOS Fine-Tuning L4 T4 Guide]] — Руководство по обучению
- [[GCP A100 Quota Status 2026-05-07]] — Статус квот GCP
- [[Fine-Tune Strategy Personal AI Brain]] — Стратегия обучения
- [[ARGOS Session 2026-05-07 Evening]] — Отчет сессии
- [[ARGOS Changelog 2026-05-07]] — Изменения
