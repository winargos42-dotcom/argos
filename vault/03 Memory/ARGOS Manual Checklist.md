# Чеклист ручных действий

## 1. Kaggle (критично — блокирует fine-tuning)
- [ ] Открыть https://www.kaggle.com
- [ ] Account → Phone Verification
- [ ] Ввести номер телефона → подтвердить SMS
- [ ] Вернуться сюда → выполнить: `powershell scripts/resume.ps1 -Kaggle`

## 2. GCP Quota (через 1 день 21 час)
- [ ] 2026-05-09 после 22:39 открыть https://console.cloud.google.com
- [ ] IAM → Quotas → filter "nvidia_a100_gpus"
- [ ] Нажать Edit Quotas → запросить 1 A100 в us-central1
- [ ] Выполнить: `powershell scripts/resume.ps1 -GCP`

## 3. API Keys
- [ ] Gmail App Password: https://myaccount.google.com/apppasswords
  - Обновить `SMTP_PASSWORD` в `.env`
- [ ] Grok API: https://x.ai → получить новый ключ
  - Обновить `XAI_API_KEY` в `.env`
- [ ] SERPAPI: https://serpapi.com/dashboard → пополнить баланс

## 4. Запуск обучения (после п.1)
- [ ] Открыть https://www.kaggle.com/code/poldop/argos-finetune-v2
- [ ] Нажать Edit → включить GPU T4 x2 (справа)
- [ ] Нажать Run All
- [ ] Ждать 4-6 часов
- [ ] Скачать output (GGUF файл)

## Автоматизация уже работает:
- ✅ Бэкап vault: каждый день в 02:00
- ✅ Проверка квот GCP: каждые 6 часов
- ✅ Мониторинг GPU кластера: watchdog active

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
