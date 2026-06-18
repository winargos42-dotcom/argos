# ARGOS Brain + Compute Center — Launch Instructions

**Дата:** 2026-04-17
**Применимо к:** ARGOS Universal OS v2.1.3 + AI Brain v1.0 + Compute Center v1.0

Этот документ описывает ТРИ независимых пути запуска — можно пройти их по порядку, можно перескакивать, но я бы шёл **A → B → C**. Каждый следующий требует, чтобы предыдущий был в рабочем состоянии.

---

## Что уже сделано автоматически

Эти правки уже в коде, ничего дополнительно делать не нужно:

- Поправлен `argos_ai_brain.py`: импорт `from openai import AzureOpenAI` (было несуществующее `azure.ai.openai`), убран `AgentRole.ANALYZER` (такого имени в enum нет — только `ANALYST`), убран `deployment_id=` из Azure-вызова (`openai>=1.0` принимает только `model=<deployment>`).
- Поправлен `file6s/compute_center_service.py`: те же три бага плюс удалён мёртвый `import aioredis` (deprecated с 2021), добавлен **dry-mode** — сервис поднимается и отдаёт `/health` даже без Redis / Cosmos / Azure OpenAI; entry-point переписан на правильный `aiohttp.AppRunner` pattern.
- Созданы `requirements-brain.txt`, `file6s/requirements-compute.txt` с реальными пакетами (`openai>=1.0`, `redis>=4.2`, `aiohttp`, `flask`, `azure-cosmos`, `azure-identity`, `azure-storage-blob`).
- Созданы `Dockerfile.brain`, `Dockerfile.compute`, `docker-compose.brain-compute.yml` для локального стека.
- В `.env` добавлен блок `=== ARGOS AI BRAIN ===` с placeholder-переменными и TODO-комментами.
- В `main.py` в классе `ArgosOrchestrator` добавлен шаг **6.7 [BRAIN]** — опциональный клиент к brain API, по умолчанию выключен (`ARGOS_BRAIN_ENABLED=0`).

---

## A. Brain — локальный запуск в fallback-режиме (без Azure, бесплатно)

**Цель:** убедиться, что `argos_brain_api.py` стартует, `/health` отвечает 200, агенты работают в режиме локального rule-based reasoning. Занимает ~5 минут.

### 1. Установить зависимости

```bash
cd F:\debug\argoss
python -m venv .venv
.venv\Scripts\activate       # Windows
# или:  source .venv/bin/activate   # Linux/WSL

pip install -r requirements-brain.txt
```

### 2. Запустить API

```bash
python argos_brain_api.py
```

Ожидаемый вывод (без Azure — это норма):

```
⚠️  openai SDK не установлена. Установите: pip install 'openai>=1.0'
```

Если openai стоит, но `.env` пустой — увидишь просто инициализацию без Azure:

```
🧠 ARGOS Brain инициализирован на узле: api-server
✅ Агент создан: Главный координатор (master) - ID: master_...
✅ Агент создан: Аналитик (analyst) - ID: analyst_...
✅ Агент создан: Оптимизатор (optimizer) - ID: optimizer_...
✅ Агент создан: Монитор (monitor) - ID: monitor_...
🧠 ARGOS AI Brain API запущен
📖 Документация доступна на http://localhost:5001/
```

### 3. Smoke-test в другом терминале

```bash
curl http://localhost:5001/health
# {"status": "online", "service": "ARGOS AI Brain API", "timestamp": "..."}

curl -X POST http://localhost:5001/think -H "Content-Type: application/json" ^
  -d "{\"query\":\"Какова производительность системы?\",\"role\":\"monitor\"}"
# Вернёт fallback-ответ: "✅ Все системы в норме..." (не Azure — локальное рассуждение)

curl http://localhost:5001/agents
# Список из 4 созданных агентов
```

Если всё отвечает — **этап A пройден**. Можно подключать реальный Azure (раздел A+), либо прыгать на B.

### A+. Подключить настоящий Azure OpenAI

Когда захочешь, чтобы `/think` давал осмысленные ответы (не rule-based), нужно провизионить Azure OpenAI и заполнить `.env`. Детали в моём предыдущем ответе, краткая версия:

```bash
# Войти в Azure
az login

# Создать ресурс (если ещё нет) — регион важен: eastus/swedencentral имеют полный список моделей
az cognitiveservices account create \
  --name argos-openai \
  --resource-group rg-argos \
  --kind OpenAI \
  --sku S0 \
  --location eastus \
  --yes

# Задеплоить модель
az cognitiveservices account deployment create \
  --resource-group rg-argos \
  --name argos-openai \
  --deployment-name argos-gpt4 \
  --model-name gpt-4 \
  --model-version turbo-2024-04-09 \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard

# Получить ключи
ENDPOINT=$(az cognitiveservices account show --name argos-openai --resource-group rg-argos --query properties.endpoint -o tsv)
KEY=$(az cognitiveservices account keys list --name argos-openai --resource-group rg-argos --query key1 -o tsv)
echo "Endpoint: $ENDPOINT"
echo "Key: $KEY"
```

Далее в `.env` (в корне `argoss/`) замени placeholder-значения:

```
AZURE_OPENAI_ENDPOINT=https://argos-openai.openai.azure.com/
AZURE_OPENAI_KEY=<ключ из az>
AZURE_DEPLOYMENT_NAME=argos-gpt4
```

Перезапусти `python argos_brain_api.py` — в логе должно появиться `✅ Azure OpenAI клиент инициализирован`. `/think` теперь отвечает реальными ответами GPT-4.

**Ценник:** gpt-4-turbo ≈ $10 per 1M input / $30 per 1M output tokens. Для отладки $1–5 кредитов хватает за глаза.

---

## B. Brain + Compute Center — локальный стек через Docker Compose

**Цель:** поднять все три сервиса (redis + brain + compute) одной командой, убедиться что оба health-endpoint'а отвечают. Всё в dry-mode без Azure, бесплатно.

### 1. Убедиться что Docker Desktop запущен

```bash
docker --version
docker compose version   # >= 2.0
```

### 2. Собрать и запустить

```bash
cd F:\debug\argoss
docker compose -f docker-compose.brain-compute.yml up --build
```

При первом запуске сборка образов ~2-3 минуты (качает python:3.11-slim + pip зависимости). Дальше кэшируется.

### 3. Проверки в другом терминале

```bash
# Brain
curl http://localhost:5001/health
# {"status":"online","service":"ARGOS AI Brain API",...}

# Compute Center
curl http://localhost:8000/health
# {"status":"online","service":"Compute Center",...}

# Статистика compute-центра (покажет 4 workers total, 0 активных — норма без Azure)
curl http://localhost:8000/stats

# Попытаться добавить задачу в очередь — вернёт 202 Accepted
curl -X POST http://localhost:8000/task -H "Content-Type: application/json" ^
  -d "{\"task_type\":\"TEXT_GENERATION\",\"priority\":\"NORMAL\",\"input_data\":{\"prompt\":\"test\"}}"

# Через секунду получить результат — без Azure вернётся error
curl http://localhost:8000/task/<task_id_из_ответа_выше>
```

### 4. Остановить

```bash
# в терминале где запущен compose — Ctrl+C, потом:
docker compose -f docker-compose.brain-compute.yml down

# С удалением volumes (стирает Redis data):
docker compose -f docker-compose.brain-compute.yml down -v
```

### Подключить Compute Center к реальному Azure OpenAI

Compute Center использует **мультирегиональную** схему: 4 разных endpoint'а. Можно поднять один регион — остальные останутся disabled (в `/stats` будут числиться total=4, enabled=1).

В `.env` добавь (можно дописать к тому же блоку BRAIN):

```
AZURE_OPENAI_ENDPOINT_EASTUS=https://argos-openai.openai.azure.com/
AZURE_OPENAI_KEY_EASTUS=<ключ>
```

Плюс имена deployment-ов — в коде дефолты `gpt4`, `gpt35`, `embedding`. Если у тебя deployment зовётся `argos-gpt4` (как в этапе A+), измени в `compute_center_service.py` строку `gpt4_deployment: str = "gpt4"` или пробрось через env (дефолт в dataclass можно переопределить, но этого в текущем коде не сделано — это отдельная маленькая правка).

После правки `.env` перезапусти `docker compose up`. Теперь `/task` с `task_type=TEXT_GENERATION` реально сходит в Azure.

---

## C. Compute Center — деплой на Azure AKS (production)

**⚠️ ПРЕДУПРЕЖДЕНИЕ ПО СТОИМОСТИ:**
Полный terraform-стек из `file6s/compute_center_terraform.tf` поднимает:
- AKS (Kubernetes) — **~$73/мес** только control plane, плюс $70+/мес за ноды
- 4 региональных Azure OpenAI endpoint'а (каждый тарифицируется отдельно)
- Cosmos DB global (Standard RU) — **~$25/мес минимум**
- Azure Cache for Redis (Basic C0) — **~$15/мес**
- Application Insights, API Management, ACR, Storage account

**Базовая ставка без трафика: $150–300/месяц.** С реальным трафиком к GPT-4 — может улететь сильно выше. Перед `terraform apply` — сто раз убедись что хочешь именно это, и что квоты Azure OpenAI у тебя есть во всех 4 регионах (`eastus`, `westus`, `northeurope`, `southeastasia`). Иначе terraform упадёт на половине.

Я рекомендую **не запускать C до тех пор**, пока B не работает стабильно, и пока ты не понимаешь, какую нагрузку этот стек должен обслуживать. До этого момента локальный docker-compose + один Azure OpenAI endpoint из этапа A+ — более чем достаточно.

### Если всё же хочешь C

```bash
cd F:\debug\argoss\file6s

# 1. Логин и выбор подписки
az login
az account list -o table
az account set --subscription "<SUBSCRIPTION_ID>"

# 2. Terraform init (скачает провайдеры)
terraform init

# 3. Планирование — ПОСМОТРЕТЬ ЧТО БУДЕТ СОЗДАНО, никаких изменений пока
terraform plan -out=compute-center.tfplan

# 4. Проверить план глазами. Когда уверен — apply:
terraform apply compute-center.tfplan

# 5. После apply будут outputs: AKS cluster name, ACR login server, endpoints.
#    Далее билд и push контейнера в ACR:
az acr login --name <acr_name_из_outputs>
docker build -f ../Dockerfile.compute -t <acr_name>.azurecr.io/argos-compute:v1 ..
docker push <acr_name>.azurecr.io/argos-compute:v1

# 6. Подключиться к AKS
az aks get-credentials --resource-group <rg> --name <aks_name>

# 7. Применить K8s манифесты (нужно отредактировать image: в deployment.yaml на свой ACR)
kubectl apply -f compute_center_deployment.yaml

# 8. Снимать тарификацию когда тестирование закончено:
terraform destroy
```

### Что обязательно проверить перед terraform apply

Файл `compute_center_terraform.tf` я не аудитировал построчно — он 11 КБ. Минимум что нужно посмотреть своими глазами:

- Subscription ID и tenant ID — прописаны правильно?
- Имена ресурсов не конфликтуют с существующими в `rg-argos` (у тебя там уже есть VMs для P2P).
- SKU AKS-нод — не GPU ли по умолчанию? GPU-ноды ещё дороже.
- `location = "eastus"` — убедись что для всех 4 регионов реально есть квоты Azure OpenAI.

---

## Известные оставшиеся недоработки (не блокирующие)

Я починил всё, что мешало коду грузиться и запускаться. Вот что стоит знать на будущее, но это **не мешает** A и B работать:

1. **Compute Center deployment names жёстко закодированы.** `gpt4_deployment="gpt4"` в dataclass; если твой Azure deployment называется иначе — надо переопределить. Одна строчка, но сейчас не сделано.
2. **`ComputeCenter.batch_process()` опрашивает Cosmos DB в цикле.** Не критично, но неэффективно. Для продакшена — перепиши на `asyncio.gather()` по task_id.
3. **`argos_brain_api.py` использует `@app.before_request` для инициализации**, что на каждый запрос проверяет `brain is None`. Безопасно, но стоило бы использовать `with app.app_context()` + init в `if __name__ == '__main__'`.
4. **Дубликат файлов в `argoss/argoss/`** — пять brain-файлов лежат дважды. Импорт в `main.py` берёт из корня `argoss/`, а вложенную копию никто не использует. Лишние 70 КБ; можно удалить, но оно не мешает.
5. **`compute_center_terraform.tf` и `compute_center_deployment.yaml`** — я не ревьюил построчно. Перед production-деплоем (этап C) нужен отдельный заход.

---

## Если что-то ломается

### Brain

- `/health` не отвечает → проверить что `python argos_brain_api.py` реально запустился без traceback; посмотреть лог.
- `/think` отвечает `fallback: true` → это не ошибка, это rule-based режим без Azure. Заполни ключи в `.env` (раздел A+).
- `ModuleNotFoundError: No module named 'openai'` → `pip install -r requirements-brain.txt`, убедись что venv активирован.

### Compute Center (Docker)

- `docker compose up` виснет на `Waiting for redis healthy` → на Windows Docker Desktop должен быть запущен, проверить `docker ps` что контейнер `argos-redis` стартовал.
- Билд падает на `pip install azure-cosmos` → вероятно сетевая проблема на хосте. Попробуй `docker compose build --no-cache argos-compute`.
- `/health` Compute Center отвечает 503 → значит background task processor упал. `docker compose logs argos-compute | tail -30`.

### Main.py

- При запуске `python main.py` в логе строка `[BRAIN] Отключён` — это нормально, пока `ARGOS_BRAIN_ENABLED=0` в `.env`. Когда brain API будет работать стабильно — поставь `=1`, перезапусти.
- `[BRAIN] Не удалось подключить мозг: ConnectionError` → brain API не запущен или слушает не на 5001. Проверь `ARGOS_BRAIN_API_URL` в `.env`.

---

**TL;DR quick-start (самый короткий путь):**

```bash
cd F:\debug\argoss
pip install -r requirements-brain.txt
python argos_brain_api.py
# в другом терминале:
curl http://localhost:5001/health
```

Если получил `"status":"online"` — у тебя работает Brain в fallback-режиме. Дальше — по этому документу.
