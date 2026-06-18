---
argos_import: project_file
source_path: data/telegram his/files/GEMINI_DEPLOY_PROMPT.md
source_abs: F:\debug\argoss\data\telegram his\files\GEMINI_DEPLOY_PROMPT.md
source_ext: .md
source_sha256: 810192fcef2150d2ea28b86312a9e6c7f7f8d183e77f412275233c8425705413
text_sha256: 810192fcef2150d2ea28b86312a9e6c7f7f8d183e77f412275233c8425705413
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-08 13:16:46
---

# GEMINI_DEPLOY_PROMPT.md

- Source: `data/telegram his/files/GEMINI_DEPLOY_PROMPT.md`
- Extract: `text`
- SHA256: `810192fcef2150d2ea28b86312a9e6c7f7f8d183e77f412275233c8425705413`

## Content

# 🤖 Промпт для Gemini — Деплой ARGOS в Google Cloud

> **Скопируй весь текст ниже и вставь в Gemini 2.0 Flash / Pro**

---

## СИСТЕМНЫЙ КОНТЕКСТ (вставь первым)

```
Ты — DevOps-инженер, который помогает мне задеплоить проект ARGOS Universal OS в Google Cloud.
Отвечай только конкретными командами и объяснениями. Не добавляй общие советы.
Все команды — для PowerShell (Windows) или Google Cloud Shell.
Если нужно выбрать между вариантами — выбирай наиболее подходящий и объясни почему.
```

---

## КОНТЕКСТ ПРОЕКТА (вставь вторым)

```
ПРОЕКТ: ARGOS Universal OS v2.1.3
Автор: Всеволод (один разработчик)
Репозиторий: https://github.com/thoresensandmann432-source/argoss.git
Ветка: master (CI настроен на main — есть расхождение)

--- GOOGLE CLOUD ---
Project ID:        argos-489214
Region:            us-central1
Artifact Registry: us-central1-docker.pkg.dev/argos-489214/argos-repo/
Service Account:   argoss@argos-489214.iam.gserviceaccount.com

--- СЕРВИСЫ НА CLOUD RUN ---
argos-mcp   → Dockerfile.mcp  → uvicorn src.mcp_api:app  → порт 8000, 2Gi RAM, 1 CPU
argos-core  → Dockerfile.core → python main.py            → порт 8080, 4Gi RAM, 2 CPU

--- КОНФИГУРАЦИОННЫЕ ФАЙЛЫ ---
cloudbuild.yaml   — сборка Docker и деплой на Cloud Run (уже готов)
Dockerfile        — полный образ с GPIO, ffmpeg, whisper, всеми зависимостями
Dockerfile.mcp    — лёгкий образ только для MCP API
Dockerfile.core   — образ для основного оркестратора
app.yaml          — App Engine (python311, min 1 instance, 4GB RAM, 2 CPU)
cloud_entry.py    — точка входа для Cloud Run (запускает ArgosOrchestrator + MCP API)

--- КЛЮЧЕВЫЕ ПЕРЕМЕННЫЕ (НЕ секреты, можно публично) ---
ARGOS_ENV=cloud
PYTHONUNBUFFERED=1
ARGOS_SEMANTIC_CACHE=0
ARGOS_MEMPALACE=1
MEMPALACE_PALACE_PATH=data/mempalace

--- СЕКРЕТНЫЕ ПЕРЕМЕННЫЕ (хранить в Secret Manager) ---
TELEGRAM_BOT_TOKEN=<токен бота>
ADMIN_IDS=6923777384
GEMINI_API_KEY=<ключ>
GEMINI_API_KEY0..4=<ключи пула>
GOOGLE_APPLICATION_CREDENTIALS=/secrets/sa-key.json
GCP_PROJECT_ID=argos-489214

--- СТАТУС ---
✅ Artifact Registry создан
✅ cloudbuild.yaml готов
✅ Dockerfile готовы
✅ cloud_entry.py готов
❓ Cloud Build trigger с GitHub — нужно проверить/создать
❓ Secret Manager — секреты могут быть не добавлены
❓ Telegram webhook — бот сейчас в polling режиме, для Cloud Run нужен webhook
❓ Ветка master vs main — CI может не триггериться
```

---

## ЗАДАЧА ДЛЯ GEMINI

```
Помоги мне выполнить деплой ARGOS в Google Cloud по шагам.

ШАГ 1 — Проверь текущее состояние:
Дай мне команды для проверки:
- Какие образы есть в Artifact Registry argos-repo
- Какие Cloud Run сервисы запущены в us-central1
- Есть ли Cloud Build triggers

ШАГ 2 — Добавь секреты в Secret Manager:
Дай команды для добавления TELEGRAM_BOT_TOKEN, ADMIN_IDS, GEMINI_API_KEY и остальных секретов

ШАГ 3 — Запусти сборку:
Дай команду для ручного запуска Cloud Build с cloudbuild.yaml

ШАГ 4 — Переключи Telegram бота с polling на webhook:
Дай команды для:
a) Получения URL задеплоенного argos-core сервиса
b) Добавления /telegram/webhook эндпоинта в mcp_api.py
c) Регистрации webhook через Telegram API

ШАГ 5 — Проверь что всё работает:
Дай команды для проверки логов Cloud Run и теста /health эндпоинта

Начни с ШАГ 1.
```

---

## БЫСТРЫЕ КОМАНДЫ (если Gemini спросит — скопируй нужное)

### Проверить состояние GCP

```powershell
# Список образов в Artifact Registry
gcloud artifacts docker images list us-central1-docker.pkg.dev/argos-489214/argos-repo --project argos-489214

# Список Cloud Run сервисов
gcloud run services list --region us-central1 --project argos-489214

# Список Cloud Build triggers
gcloud builds triggers list --project argos-489214

# Список секретов в Secret Manager
gcloud secrets list --project argos-489214
```

### Запустить Cloud Build вручную

```powershell
cd C:\Users\AvA\argoss

gcloud builds submit --config cloudbuild.yaml --project argos-489214
```

### Добавить секреты в Secret Manager

```powershell
# Telegram токен
echo "ТВОЙ_TELEGRAM_TOKEN" | gcloud secrets create TELEGRAM_BOT_TOKEN --data-file=- --project argos-489214

# Gemini ключи
echo "ТВОЙ_GEMINI_KEY" | gcloud secrets create GEMINI_API_KEY --data-file=- --project argos-489214

# Admin ID
echo "6923777384" | gcloud secrets create ADMIN_IDS --data-file=- --project argos-489214

# Service Account JSON (файл)
gcloud secrets create SA_KEY --data-file="C:\Users\AvA\debug\argos-489214-782ee50ae90b.json" --project argos-489214
```

### Подключить секреты к Cloud Run

```powershell
gcloud run services update argos-core `
  --region us-central1 `
  --project argos-489214 `
  --set-secrets "TELEGRAM_BOT_TOKEN=TELEGRAM_BOT_TOKEN:latest,GEMINI_API_KEY=GEMINI_API_KEY:latest,ADMIN_IDS=ADMIN_IDS:latest" `
  --set-env-vars "ARGOS_ENV=cloud,ARGOS_SEMANTIC_CACHE=0,ARGOS_MEMPALACE=1"
```

### Получить URL сервиса

```powershell
gcloud run services describe argos-core --region us-central1 --project argos-489214 --format "value(status.url)"
```

### Зарегистрировать Telegram Webhook

```powershell
# После получения URL сервиса:
$URL = "https://argos-core-XXXX-uc.a.run.app"
$TOKEN = "ТВОЙ_TELEGRAM_TOKEN"
Invoke-WebRequest "https://api.telegram.org/bot$TOKEN/setWebhook?url=$URL/telegram/webhook"
```

### Посмотреть логи

```powershell
# Последние 100 строк логов argos-core
gcloud run services logs read argos-core --region us-central1 --project argos-489214 --limit 100

# Live логи
gcloud beta run services logs tail argos-core --region us-central1 --project argos-489214
```

### Исправить ветку master → main (если CI не триггерится)

```powershell
cd C:\Users\AvA\argoss
git checkout -b main
git push origin main
# Потом переключить Cloud Build trigger на main
```

---

## ИЗВЕСТНЫЕ ПРОБЛЕМЫ — скажи Gemini если столкнёшься

| Проблема | Что происходит | Решение |
|----------|----------------|---------|
| `argoss-core` зависает при старте | WatsonX blocking init | Уже исправлено в watson_bridge.py (threading.Event) |
| CPU 100% при запуске | SentenceTransformer загружает 80MB модель | `ARGOS_SEMANTIC_CACHE=0` в env vars |
| Бот молчит | polling режим несовместим с холодным стартом | Переключить на webhook (ШАГ 4) |
| `No module named 'redis'` | Redis не установлен в requirements | Добавить `redis>=5.0.0` в requirements.txt |
| `ARGOS_VECTOR_FORCE_FALLBACK` | ChromaDB блокирует старт | Установить `ARGOS_VECTOR_FORCE_FALLBACK=1` |
| Конфликт polling | Две копии бота одновременно | Удалить старый сервис или отключить polling |
| Disk quota | Cloud Run ephemeral filesystem 512MB | Использовать Cloud Storage для data/ |

---

## АРХИТЕКТУРА (для контекста Gemini)

```
┌─────────────────────────────────────────────────────┐
│                   ARGOS P2P СЕТЬ                    │
│                                                      │
│  ┌──────────────┐    ┌──────────────┐               │
│  │  Local PC    │    │ Google Cloud │               │
│  │  (мастер)    │◄──►│  Cloud Run   │               │
│  │  Windows     │    │  argos-core  │               │
│  │  Redis       │    │  argos-mcp   │               │
│  └──────┬───────┘    └──────┬───────┘               │
│         │                   │                       │
│         └─────────┬─────────┘                       │
│                   │                                 │
│            ┌──────▼──────┐                          │
│            │ IBM Code    │                          │
│            │ Engine (P2P)│                          │
│            └─────────────┘                          │
└─────────────────────────────────────────────────────┘

Telegram Bot → webhook → argos-core Cloud Run
                         → process_logic_async()
                         → AIRouter (Gemini/Groq/Ollama)
                         → MemPalace (ChromaDB память)
                         → ← ответ пользователю
```

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
