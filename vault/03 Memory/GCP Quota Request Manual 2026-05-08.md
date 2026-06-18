# GCP GPU Quota Request Guide (Manual Required)

## Status: API Blocked

**Error**: `consumer override value can only be set between 0 to 0`

**Reason**: После отказа в A100 Google Cloud заблокировал автоматические запросы через API. Требуется ручной запрос через веб-консоль.

## Action Required: Cloud Console

### Step 1: Открыть Quotas
1. Перейти: https://console.cloud.google.com/iam-admin/quotas
2. Включить фильтр: **Service = Vertex AI API**

### Step 2: Найти метрики
Найти и отметить (чекбокс) следующие квоты:
- `custom_model_training_nvidia_t4_gpus` (us-central1, us-east1)
- `custom_model_training_nvidia_l4_gpus` (us-central1, us-east1)
- `nvidia_a100_gpus` (us-central1)

### Step 3: Edit Quotas
1. Нажать **EDIT QUOTAS** (сверху)
2. Для каждой метрики:
   - **New limit**: 2 (для T4/L4), 1 (для A100)
   - **Request description**: 
     ```
     ARGOS project — AI assistant fine-tuning using Mistral NeMo 12B.
     Previous request was denied due to new project status.
     Project now has billing history and active usage.
     Please approve GPU quota for model training.
     ```
3. Нажать **NEXT** → **SUBMIT REQUEST**

### Step 4: Ждать ответа
- **T4/L4**: Обычно 24-48 часов
- **A100**: Может потребовать больше времени или будет отклонён снова

## Alternative: Preemptible VMs
Если regular квоты отклонены, попробовать:
- `preemptible_nvidia_t4_gpus` — дешевле, но могут прерываться
- Запросить через ту же форму

## After Approval
После подтверждения по email:
```powershell
cd F:\debug\argoss
python scripts\check_gcp_quota.py
# или
powershell scripts\resume.ps1 -GCP
```

## Current Status
- **T4 API quota**: 0/0 (blocked, need console request)
- **L4 API quota**: 0/0 (blocked, need console request)
- **A100**: 0/0 (denied, can retry after 2026-05-09)
- **Compute quota**: 0/1 available but exhausted

## Fallback
Пока GCP не одобрит — использовать **Kaggle** (T4 x2 бесплатно).

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
