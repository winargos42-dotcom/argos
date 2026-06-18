# ARGOS Fine-Tuning на доступных GPU — Практическое руководство

**Дата**: 2026-05-07
**Альтернатива A100**: ✅ Реализована
**Статус**: Готово к запуску

---

## Почему не A100?

Квота A100 = 0 во всех регионах (ожидание 24-48ч).
Но у нас есть **T4** и **L4** с лимитом 1 — ими можно пользоваться прямо сейчас!

---

## Сравнение GPU

| GPU | VRAM | Скорость | Стоимость | Подходит для 12B? |
|-----|------|----------|-----------|-------------------|
| **A100** | 40GB | 🔥🔥🔥 | ~$3.7/ч | ✅ Полный fine-tuning |
| **L4** | 24GB | 🔥🔥 | ~$0.8/ч | ✅ QLoRA (рекомендуем) |
| **T4** | 16GB | 🔥 | ~$0.4/ч | ✅ QLoRA (экономия) |
| **V100** | 16GB | 🔥🔥 | ~$1.2/ч | ✅ QLoRA (устаревший) |

### Что такое QLoRA?

**Q**uantized **Lo**w-Rank **A**daptation — обучение только "адаптеров" (маленьких матриц), а не всей модели.

- Вместо 12B параметров → обучаем ~0.5% (60M параметров)
- VRAM: вместо 24GB → 8-12GB
- Качество: 95-98% от полного fine-tuning
- Скорость: быстрее за счёт меньших вычислений

---

## Конфигурации

### Option 1: L4 (24GB) ⭐ Рекомендуем

**Файл**: `config/vertex_job_l4.json`

```json
{
  "machine_type": "g2-standard-4",
  "accelerator_type": "NVIDIA_L4",
  "accelerator_count": 1
}
```

**Параметры обучения**:
- Batch size: 2
- Gradient accumulation: 8 (эффективный batch = 16)
- LoRA r: 16, alpha: 32
- Max sequence: 2048
- Время: ~3-4 часа на 5537 примеров
- Стоимость: ~$2.5-3.5 за полный run

### Option 2: T4 (16GB) 💰 Экономия

**Файл**: `config/vertex_job_t4.json`

```json
{
  "machine_type": "n1-standard-4",
  "accelerator_type": "NVIDIA_TESLA_T4",
  "accelerator_count": 1
}
```

**Параметры обучения**:
- Batch size: 1
- Gradient accumulation: 16 (эффективный batch = 16)
- LoRA r: 8, alpha: 16 (меньше адаптеров)
- Max sequence: 1024 (экономия VRAM)
- Gradient checkpointing: ✅ Включен
- Время: ~5-7 часов
- Стоимость: ~$2-3 за полный run

---

## Как запустить

### Шаг 1: Подготовка

```bash
cd F:\debug\argoss
. .venv\Scripts\Activate.ps1
```

### Шаг 2: Загрузка данных

```bash
# Создать bucket (один раз)
gsutil mb -l us-central1 gs://argos-training-data

# Загрузить датасет
gsutil cp data/train.jsonl gs://argos-training-data/
```

### Шаг 3: Запуск (L4)

```bash
# Через gcloud CLI
gcloud ai custom-jobs create \
  --region=us-central1 \
  --display-name=argos-finetune-l4-$(date +%Y%m%d) \
  --config=config/vertex_job_l4.json
```

**Или через скрипт**:
```bash
bash scripts/launch_vertex_training.sh
```

### Шаг 4: Мониторинг

```bash
# Смотреть логи в реальном времени
gcloud ai custom-jobs stream-logs [JOB_ID] --region=us-central1

# Или в Console:
# https://console.cloud.google.com/vertex-ai/training/custom-jobs
```

### Шаг 5: Скачивание модели

```bash
# После завершения
gsutil cp -r gs://argos-training-data/output-l4/ ./models/

# Модель в GGUF формате (для llama.cpp)
gsutil cp gs://argos-training-data/output-l4/gguf/*.gguf ./models/
```

---

## Интеграция с ARGOS

### После обучения

1. **Скачать GGUF**:
   ```bash
   gsutil cp gs://argos-training-data/output-l4/gguf/argos-mistral-nemo-q4_k_m.gguf F:\debug\argoss\models\
   ```

2. **Добавить в GPU кластер**:
   ```bash
   # Запустить на новом порту
   llama-server \
     -m models/argos-mistral-nemo-q4_k_m.gguf \
     -c 32768 \
     -ngl 35 \
     --host 0.0.0.0 \
     --port 8085
   ```

3. **Обновить AI Router**:
   - Добавить endpoint `:8085` в список провайдеров
   - Приоритет: fine-tuned > base model

---

## Ожидаемые результаты

### Качество
- **Base model**: Общие знания, не знает о твоих проектах
- **Fine-tuned**: Понимает контекст ARGOS, твои проекты, код

### Примеры улучшений
```
Вопрос: "Как настроить GPU кластер в ARGOS?"

Base: "GPU кластер — это группа видеокарт..." (общий ответ)
Fine-tuned: "В ARGOS используется llama-server с Vulkan. 
  RX 580 (:8082) и RX 560 (:8084) запускаются автоматически 
  при старте системы. Проверка: curl http://localhost:8082/health" 
  (конкретный ответ)
```

---

## Бюджет

| GPU | Время | Стоимость/час | Итого |
|-----|-------|---------------|-------|
| L4 | 3-4ч | $0.80 | **$2.4-3.2** |
| T4 | 5-7ч | $0.40 | **$2.0-2.8** |
| A100 | 1.5-2ч | $3.67 | **$5.5-7.3** |

**Доступно**: $293.82 (бонусы GCP)
**Можно запустить**: ~90-120 тренировок на L4

---

## Fallback цепочка

```
1. A100 (ждем квоту) → 2x быстрее
2. L4 (доступен сейчас) ← РЕКОМЕНДУЕМ
3. T4 (доступен сейчас) ← Дешевле
4. Kaggle T4x2 (бесплатно) ← Без GCP
```

---

## Файлы

| Файл | Описание |
|------|----------|
| `config/vertex_job_l4.json` | Конфиг для L4 |
| `config/vertex_job_t4.json` | Конфиг для T4 |
| `scripts/train_unsloth.py` | Скрипт обучения (Unsloth) |
| `scripts/launch_vertex_training.sh` | Запуск тренировки |
| `data/train.jsonl` | Датасет (18.73 MB) |

---

## Следующие шаги

1. ✅ Конфиги созданы
2. ⏳ Загрузить данные на GCS
3. ⏳ Запустить первую тренировку (L4)
4. 📋 Скачать и протестировать модель
5. 📋 Интегрировать в ARGOS GPU кластер

---

*Создано: 2026-05-07*
*Статус: Готово к запуску*

## Связанные документы

- [[ARGOS Train Dataset v1.0]] — Датасет для обучения
- [[GCP A100 Quota Status 2026-05-07]] — Статус квот GCP
- [[Fine-Tune Strategy Personal AI Brain]] — Стратегия обучения
- [[ARGOS System Architecture 2026-05-07]] — Архитектура системы
- [[ARGOS Next Steps 2026-05-07]] — План действий
- [[ARGOS Unified State 2026-05-06]] — Текущее состояние

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
