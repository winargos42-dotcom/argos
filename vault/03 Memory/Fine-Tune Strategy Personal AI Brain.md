# Стратегия Fine-Tune: Личный ИИ-мозг на базе Obsidian

**Источник:** Telegram диалог с AI-консультантом  
**Дата:** 2026-05-07 (обновлено)
**Теги:** #finetune #vertex-ai #a100 #v100 #obsidian #mistral #unsloth #dataset

---

## ✅ Выполнено (2026-05-07)

### Датасет создан
- **Источник**: Obsidian vault (5,537 Markdown файлов)
- **Формат**: OpenAI chat (system/user/assistant)
- **Размер**: 18.73 MB
- **Примеров**: 5,537
- **Токенов**: ~12M
- **Файл**: `F:\debug\argoss\data\train.jsonl`
- **Конвертер**: `scripts/convert_to_train_jsonl.py`

### Категории данных
| Категория | Файлов | Доля |
|-----------|--------|------|
| 04 Project Mirror | 5,379 | 97.1% |
| 03 Memory | 40 | 0.7% |
| 06 Link Stubs | 39 | 0.7% |
| 05 SharedMemory Mirror | 33 | 0.6% |
| 02 Logs | 21 | 0.4% |
| Прочее | 25 | 0.5% |

### Конфигурации обучения
- **Vertex AI**: `config/vertex_job.json` (A100 40GB)
- **Kaggle**: `config/kaggle_finetune.ipynb` (T4x2, бесплатно)

### Системные параметры
| Параметр | Значение |
|----------|----------|
| Epochs | 3 |
| Batch size | 4 (Vertex) / 2 (Kaggle) |
| Learning rate | 2e-5 |
| Max seq length | 4,096 |
| Optimizer | AdamW |
| Precision | FP16 |
| Оценка времени (A100) | ~2-3 часа |
| Оценка времени (T4x2) | ~4-6 часов |
| Оценка стоимости | ~$6-12 (бонусы GCP) |

---

**Оригинальная дата:** 2026-05-06
**Теги:** #finetune #vertex-ai #a100 #v100 #obsidian #mistral #unsloth

---

## Архитектура решения

```
┌─────────────────────────────────────────┐
│  Подготовка данных (Claude/Kimi)        │
│  • Очистка Obsidian (80 MB)             │
│  • Форматирование в Instruction-Response│
│  • Синтез связей между заметками        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Google Cloud Vertex AI                 │
│  • A100 (обучение)                      │
│  • Managed Notebook / Custom Job        │
│  • Unsloth (ускорение 2x)               │
│  • Оплата: бонусный баланс $293.82      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Локальный inference                    │
│  • V100 16GB (дома)                     │
│  • GGUF 4-bit / EXL2                    │
│  • 40-70 tokens/sec                     │
│  • Полная приватность                   │
└─────────────────────────────────────────┘
```

---

## 1. Подготовка датасета (Claude/Kimi)

### Задачи для LLM

1. **Форматирование в Instruction-Response**
   ```json
   {
     "instruction": "Какие ключевые этапы настройки V100?",
     "context": "Текст заметки из Obsidian",
     "response": "Данные из заметки"
   }
   ```

2. **Очистка мусора**
   - Удалить Markdown-ссылки
   - Убрать дубликаты
   - Удалить пустые списки дел
   - Оставить только суть знаний

3. **Синтез связей**
   - Найти пересекающиеся темы в 80 MB заметок
   - Создать примеры, объединяющие информацию из разных файлов

### Промпт для подготовки данных

```
Ты — эксперт по подготовке обучающих данных для LLM.

Задача: Преврати мои Obsidian-заметки в качественный датасет для fine-tuning.

Правила:
1. Извлеки ключевые факты и сформулируй как пары "Вопрос — Ответ"
2. Удали Markdown-ссылки, дубликаты, пустые списки
3. Создай обучающие примеры, объединяющие информацию из разных файлов
4. Используй формат: {"instruction": "...", "context": "...", "response": "..."}
5. Сохрани JSONL в файл train.jsonl

Модель для обучения: Mistral NeMo 12B
```

---

## 2. Обучение на Vertex AI (A100)

### Вариант A: Managed Notebook (для экспериментов)

**Настройка:**
- Тип машины: `a2-highgpu-1g` (1x A100 40GB)
- Предустановленная среда: PyTorch / TensorFlow
- Idle shutdown: 30-60 минут

**Команды:**
```bash
# Установка Unsloth
pip install unsloth

# Запуск обучения
python train.py --model mistral-nemo-12b \
  --dataset train.jsonl \
  --output model.gguf \
  --quantization q4_k_m
```

### Вариант B: Custom Job (для продакшена)

**Преимущества:**
- Авто-отключение после завершения
- Экономия средств
- Масштабируемость

**Конфигурация:**
```yaml
workerPoolSpecs:
  machineSpec:
    machineType: a2-highgpu-1g
    acceleratorType: NVIDIA_TESLA_A100
    acceleratorCount: 1
  replicaCount: 1
  containerSpec:
    imageUri: gcr.io/argos-489214/unsloth-trainer:latest
```

### Квоты

**Необходимо запросить:**
1. IAM & Admin > Quotas
2. Vertex AI API > Custom model training NVIDIA A100 GPUs
3. Edit Quotas → запросить 1 GPU

---

## 3. Локальный inference (V100 16GB)

### Спецификации

| Параметр | Значение |
|----------|----------|
| Модель | Mistral NeMo 12B |
| Квантование | Q4_K_M (4-bit) |
| VRAM | ~8-10 GB |
| Скорость | 40-70 tokens/sec |
| Контекст | До 128K tokens |

### Интеграция с ARGOS

**Варианты использования:**
1. **LM Studio / Ollama** — простой чат
2. **Smart Connections** — плагин для Obsidian
3. **Telegram-бот** — доступ с телефона
4. **ARGOS Core** — интеграция в систему

### Конфигурация llama-server

```bash
# Запуск fine-tuned модели
llama-server \
  -m models/mistral-nemo-personalized.gguf \
  -c 32768 \
  -ngl 35 \
  --host 0.0.0.0 \
  --port 8085
```

---

## 4. Инструменты

### Unsloth

**Преимущества:**
- Обучение в 2x быстрее
- Меньше расход бонусных долларов
- Прямой экспорт в GGUF

**Установка:**
```bash
pip install unsloth
```

### llmfit

**Репозиторий:** https://github.com/AlexsJones/llmfit

**Назначение:** Инструмент для fine-tuning LLM

---

## 5. Экономия средств

### Стратегии

1. **Custom Job вместо Managed Notebook**
   - Нет платы за простой
   - Авто-отключение

2. **Idle Shutdown**
   - 30-60 минут простоя → авто-стоп
   - Настройка в Managed Notebook

3. **Удаление дисков**
   - После завершения проекта
   - Диски стоят недорого, но накапливаются

### Бюджет

- **Доступно:** $293.82 (бонусы)
- **Стоимость A100:** ~$3/час
- **Время обучения:** ~2-4 часа (Unsloth)
- **Итого:** ~$6-12 за полный цикл

---

## 6. Риски и решения

### Галлюцинации

**Проблема:** Модель придумывает то, чего нет в заметках

**Решения:**
- Хорошо перемешать данные с General Purpose
- Использовать качественный скрипт подготовки
- Добавить системный промпт: "Отвечай ТОЛЬКО на основе предоставленного контекста"

### Приватность

**Гарантии:**
- Данные не покидают компьютер после обучения
- Локальный inference на V100
- Нет зависимости от OpenAI/Anthropic

---

## 7. План внедрения

### Phase 1: Подготовка (неделя 1) ✅ ВЫПОЛНЕНО
- [x] Создать промпт для Claude/Kimi
- [x] Очистить Obsidian (убрать мусор)
- [x] Сгенерировать train.jsonl (5,537 примеров)
- [x] Проверить качество данных (средний размер: 2,954 chars)
- [x] Создать конвертер `convert_to_train_jsonl.py`
- [x] Сохранить конфиги Vertex AI и Kaggle

### Phase 2: Обучение (неделя 2)
- [ ] Получить квоту A100
- [ ] Настроить Vertex AI
- [ ] Запустить Custom Job
- [ ] Экспортировать GGUF

### Phase 3: Интеграция (неделя 3)
- [ ] Настроить llama-server на V100
- [ ] Интегрировать в ARGOS
- [ ] Тестирование и дебаг
- [ ] Оптимизация скорости

---

## Ссылки

- llama.cpp server: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- llmfit: https://github.com/AlexsJones/llmfit
- Unsloth: https://github.com/unsloth/unsloth
- Vertex AI: https://cloud.google.com/vertex-ai

---

*Сохранено из Telegram*

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
