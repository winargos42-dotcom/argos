# GCP A100 Quota Status — 2026-05-07

**Дата проверки**: 2026-05-07 ~18:30 MSK
**Проект**: `argos-489214`
**Регионы проверены**: us-central1, us-east1, us-west1, europe-west4, asia-southeast1

---

## Текущий статус квот

### NVIDIA A100 GPUs

| Регион | Лимит | Использование | Статус |
|--------|-------|---------------|--------|
| us-central1 | 0 | 0 | ❌ Нет доступа |
| us-east1 | 0 | 0 | ❌ Нет доступа |
| us-west1 | 0 | 0 | ❌ Нет доступа |
| europe-west4 | 0 | 0 | ❌ Нет доступа |
| asia-southeast1 | 0 | 0 | ❌ Нет доступа |

### Другие GPU (для справки)

| Тип | Лимит | Примечание |
|-----|-------|------------|
| NVIDIA T4 | 1 | ✅ Доступен ( downgrade ) |
| NVIDIA L4 | 1 | ✅ Доступен (базовый) |
| NVIDIA V100 | 1 | ✅ Доступен (устаревший) |
| NVIDIA P100 | 1 | ✅ Доступен (устаревший) |

---

## Что было сделано

### 1. Проверка квот (gcloud CLI)
**Команда**: `gcloud compute regions describe [REGION] --project=argos-489214`

**Результат**: Во всех проверенных регионах лимит A100 = 0

**Вывод**: Квота не выделена, требуется запрос

### 2. Запрос квоты (ручной)
**Статус**: ❌ ОТКЛОНЕНО
**Дата ответа**: 2026-05-07 ~22:39 MSK
**Ответ Google Cloud**:
> "К сожалению, в данный момент мы не можем предоставить вам дополнительную квоту. Если это новый проект, пожалуйста, подождите 48 часов, прежде чем повторно отправлять запрос или пока в вашем платежном аккаунте не появится дополнительная история."

**Причина отказа**: Новый проект, нет платежной истории
**Рекомендация Google**: Подождать 48 часов или связаться с менеджером по продажам

### 3. Повторный запрос
**Возможен через**: 48 часов (2026-05-09 ~22:39)
**Альтернатива**: Связаться с командой продаж https://cloud.google.com/contact/

---

## ⚠️ ВАЖНО: Используем L4/T4 (fallback)

Пока A100 недоступен, запускаем fine-tuning на доступных GPU:
- **L4 (24GB)**: `config/vertex_job_l4.json` — РЕКОМЕНДУЕМ
- **T4 (16GB)**: `config/vertex_job_t4.json` — экономия

Инструкция: [[ARGOS Fine-Tuning L4 T4 Guide]]

---

## Инструкция по запросу (ручная)

### Шаг 1: Открыть Console
```
https://console.cloud.google.com/iam-admin/quotas?project=argos-489214
```

### Шаг 2: Фильтр
- В поиске ввести: `Custom model training NVIDIA A100 GPUs`
- Или найти вручную в списке

### Шаг 3: Edit Quotas
- Нажать иконку карандаша (Edit Quotas)
- Выбрать метрику: `Custom model training NVIDIA A100 GPUs`

### Шаг 4: Заполнить форму
```
New limit: 1
Request description: 
  Research project for personal AI fine-tuning.
  Training Mistral NeMo 12B on private knowledge base.
  Expected usage: 2-3 hours per run, 1-2 runs/month.
  Budget limit: $50/month.

Contact email: [doppol85@gmail.com]
Phone: [указать номер]
```

### Шаг 5: Submit
- Нажать Submit Request
- Ожидать ответа 24-48 часов

---

## Обоснование (Justification)

```
Research project for personal AI fine-tuning.
Training a personalized assistant model (Mistral NeMo 12B) 
on private Obsidian knowledge base (5,537 documents, 12M tokens).

Expected usage:
- 2-3 hours per training run
- 1-2 runs per month
- Total budget: $50/month

Purpose: Personal AI assistant with long-term memory
and knowledge of software engineering workflows.
```

---

## Альтернативы

### Option A: Kaggle (Immediate)
- **GPU**: T4 x2 (бесплатно)
- **Лимит**: 30 часов/неделю
- **Готовность**: Можно начать сегодня
- **Файл**: `F:\debug\argoss\config\kaggle_finetune.ipynb`

### Option B: Vertex AI L4/T4
- **GPU**: L4 или T4 (1 шт. доступен)
- **Стоимость**: ~$0.5-1/час
- **Медленнее**: A100 в 8-10 раз быстрее
- **Можно начать**: Сразу

### Option C: Локальное обучение
- **GPU**: RX 580 8GB (не подходит для 12B)
- **Статус**: Невозможно (недостаточно VRAM)

---

## Рекомендация

### Сейчас (L4/T4 fallback)
1. ✅ **Запустить fine-tuning на L4**: `config/vertex_job_l4.json`
2. ✅ **Запустить fine-tuning на T4**: `config/vertex_job_t4.json` (если L4 занят)
3. ✅ **Kaggle fallback**: Бесплатно, без GCP

### Позже (A100)
4. ⏳ **Повторный запрос**: 2026-05-09 (через 48 часов)
5. 📞 **Или связаться с продажами**: https://cloud.google.com/contact/
6. 🚀 **Когда одобрят**: Перенести на A100 для скорости

---

## Связанные документы
- [[ARGOS Fine-Tuning L4 T4 Guide]] — Руководство по обучению
- [[ARGOS Train Dataset v1.0]] — готовый датасет
- [[Fine-Tune Strategy Personal AI Brain]] — стратегия обучения
- [[ARGOS Next Steps 2026-05-07]] — приоритеты

---

*Записано: 2026-05-07*
*Обновлено: 2026-05-07 (ответ получен — отказ)*
*Следующее обновление: 2026-05-09 (повторный запрос)*

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
