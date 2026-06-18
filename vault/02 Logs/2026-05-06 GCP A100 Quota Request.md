# Запрос квоты NVIDIA A100 GPUs в GCP

## Статус
**Дата:** 2026-05-06  
**Проект:** argos-489214  
**Запрашиваемая квота:** NVIDIA A100 GPUs = 1 (us-central1)  
**Текущая квота:** 0 (во всех регионах)  
**Статус запроса:** ✅ ЗАПРОШЕНО (ожидание ответа Google 24-48ч)

---

## Почему нельзя через CLI

API `cloudsupport.googleapis.com` возвращает **PERMISSION_DENIED** для текущего аккаунта. Бесплатный/триальный tier требует ручного запроса через веб-интерфейс.

---

## Инструкция (3 минуты)

### Шаг 1: Открыть страницу квот
[Прямая ссылка → Quotas](https://console.cloud.google.com/iam-admin/quotas?project=argos-489214&metric=compute.googleapis.com%2Fnvidia_a100_gpus)

### Шаг 2: Найти метрику
В фильтре сверху выбрать:  
- **Service:** Compute Engine API  
- **Metric:** NVIDIA A100 GPUs  
- **Location:** us-central1

### Шаг 3: Запросить увеличение
1. Поставить галочку на строке с `us-central1`
2. Нажать **EDIT QUOTAS** (кнопка сверху)
3. В форме указать:
   - **New limit:** `1`
   - **Justification:** 
     ```
     Fine-tuning large language models for autonomous AI agent research project (ARGOS). 
     A100 GPU required for training with large context windows (>8K tokens).
     Expected usage: 20-40 hours/week for model experimentation.
     Contact: doppol85@gmail.com
     ```

### Шаг 4: Подтвердить
Нажать **SUBMIT REQUEST**.  
Обычно одобряют в течение **24-48 часов**.

---

## Альтернатива (если A100 не дадут)

| Машина | GPU | Память GPU | Стоимость/час | Статус квоты |
|--------|-----|-----------|---------------|-------------|
| `a2-highgpu-1g` | A100 40GB | 40 GB | ~$3.67 | ❌ 0 |
| `n1-standard-4` + T4 | T4 | 16 GB | ~$0.35 | ⚠️ 1 |
| `g2-standard-4` | L4 | 24 GB | ~$0.80 | ⚠️ 1 |

Если A100 отклонят — запросить **L4** (достаточно для fine-tune 7B моделей).

---

## Что делать после одобрения

```bash
# Автоматический деплой A100-ноды
gcloud compute instances create argos-a100-node \
  --zone=us-central1-a \
  --machine-type=a2-highgpu-1g \
  --image-family=pytorch-latest-gpu \
  --image-project=deeplearning-platform-release \
  --boot-disk-size=100GB \
  --metadata="install-nvidia-driver=True"
```

---

## Связи
- [[ARGOS Unified State 2026-05-05]]
- [[2026-05-05 Infrastructure Reconnaissance]]
- [[GCP Quota Monitoring]]

[[Backbone Hub]]

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Logs Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Logs Hub]]
