# Запрос увеличения GPU квот в GCP

**Дата**: 2026-05-08
**Проект**: argos-489214

---

## Что запрашивать

### 1. L4 GPU (приоритет)
- **Метрика**: `Custom model training NVIDIA L4 GPUs`
- **Текущий лимит**: 1
- **Запросить**: 1 (или 2 для параллельных jobs)

### 2. T4 GPU (fallback)
- **Метрика**: `Custom model training NVIDIA T4 GPUs`
- **Текущий лимит**: 1
- **Запросить**: 1-2

### 3. A100 GPU (опционально)
- **Метрика**: `Custom model training NVIDIA A100 GPUs`
- **Текущий лимит**: 0
- **Запросить**: 1

---

## Инструкция

### Шаг 1: Открыть Quotas
```
https://console.cloud.google.com/iam-admin/quotas?project=argos-489214
```

### Шаг 2: Фильтр
- В поле фильтра ввести: `Custom model training`
- Или найти вручную нужные метрики

### Шаг 3: Выбрать метрику
- Найти: `Custom model training NVIDIA L4 GPUs`
- Найти: `Custom model training NVIDIA T4 GPUs`
- (Опционально) `Custom model training NVIDIA A100 GPUs`

### Шаг 4: Edit Quotas
- Выбрать метрику
- Нажать карандаш (Edit Quotas)
- Указать новый лимит

### Шаг 5: Заполнить форму
```
New limit: 1 (или 2)

Request description:
Personal AI research project. Training Mistral NeMo 12B 
for autonomous assistant using private knowledge base.
Expected usage: 2-3 hours per run, 2-3 runs per month.
Budget limit: $50/month.

Contact email: doppol85@gmail.com
Phone: [указать номер телефона]
```

### Шаг 6: Submit
- Нажать Submit Request
- Ждать email подтверждения (24-48 часов)

---

## Обоснование (Justification)

```
Research project for personal AI fine-tuning.

Project: ARGOS - autonomous AI assistant with long-term memory
Model: Mistral NeMo 12B Instruct
Dataset: 5,537 examples from personal Obsidian knowledge base
Method: QLoRA (4-bit quantization)

Expected usage:
- Training time: 2-3 hours per run
- Frequency: 2-3 runs per month
- Budget: $50/month maximum

Purpose: Create personalized AI assistant that understands
software engineering workflows and project context.

No commercial use. Research and education only.
```

---

## Статус запросов

| GPU | Статус | Дата запроса | Результат |
|-----|--------|-------------|-----------|
| A100 | ❌ Отклонен | 2026-05-07 | Нет платежной истории |
| L4 | ⏳ Ожидает | - | - |
| T4 | ⏳ Ожидает | - | - |

---

## Альтернатива (пока ждем)

**Kaggle**: https://www.kaggle.com/code
- T4 x2 (бесплатно)
- 30 часов/неделю
- Ноутбук: `config/kaggle_finetune.ipynb`

---

*Создано: 2026-05-08*

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
