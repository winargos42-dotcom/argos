# GCP GPU Quota Status — 2026-05-08

**Дата**: 2026-05-08
**Статус**: ❌ Все квоты исчерпаны

---

## Результаты попыток запуска

### L4 (24GB)
- **Регионы проверены**: us-central1, us-east1, us-west1, europe-west4, asia-southeast1
- **Статус**: ❌ RESOURCE_EXHAUSTED (429)
- **Ошибка**: `aiplatform.googleapis.com/custom_model_training_nvidia_l4_gpus`

### T4 (16GB)
- **Регионы проверены**: us-central1
- **Статус**: ❌ RESOURCE_EXHAUSTED (429)
- **Ошибка**: `aiplatform.googleapis.com/custom_model_training_nvidia_t4_gpus`

### A100 (40GB)
- **Статус**: ❌ Квота 0 (отклонена 2026-05-07)

---

## Причина

Квоты на training GPU (L4/T4) исчерпаны для проекта `argos-489214`.

Возможные причины:
1. Другие jobs выполняются в этом проекте
2. Лимит 1 GPU уже используется
3. Необходимо запросить увеличение квоты

---

## Альтернативы

### Option 1: Kaggle (Рекомендуется)
- **GPU**: T4 x2 (бесплатно)
- **Лимит**: 30 часов/неделю
- **Готовность**: Можно начать сейчас
- **Файл**: `config/kaggle_finetune.ipynb`
- **Время**: ~4-6 часов

### Option 2: Ожидание освобождения
- Непредсказуемо по времени
- Может занять часы или дни

### Option 3: Запрос увеличения квоты
- **URL**: https://console.cloud.google.com/iam-admin/quotas
- **Метрики**:
  - `Custom model training NVIDIA L4 GPUs`
  - `Custom model training NVIDIA T4 GPUs`
- **Время рассмотрения**: 24-48 часов

---

## Следующие шаги

1. **Сейчас**: Использовать Kaggle для fine-tuning
2. **Параллельно**: Запросить увеличение квот L4/T4
3. **Потом**: Перенести на Vertex AI когда квоты будут доступны

---

## Файлы

| Файл | Описание |
|------|----------|
| `config/kaggle_finetune.ipynb` | Ноутбук для Kaggle |
| `config/vertex_job_l4.yaml` | Конфиг L4 (Vertex AI) |
| `config/vertex_job_t4.yaml` | Конфиг T4 (Vertex AI) |
| `data/train.jsonl` | Датасет (18.73 MB) |

---

*Дата обновления: 2026-05-08*
*Следующее обновление: после освобождения квот или запуска на Kaggle*

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
