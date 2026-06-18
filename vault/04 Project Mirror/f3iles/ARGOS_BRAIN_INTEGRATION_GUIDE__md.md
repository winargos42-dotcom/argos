---
argos_import: project_file
source_path: f3iles/ARGOS_BRAIN_INTEGRATION_GUIDE.md
source_abs: F:\debug\argoss\f3iles\ARGOS_BRAIN_INTEGRATION_GUIDE.md
source_ext: .md
source_sha256: 319c6f8439fcd40913ed3b7317005445bb866bd5f9d0090ce2fc00d211597cb0
text_sha256: 319c6f8439fcd40913ed3b7317005445bb866bd5f9d0090ce2fc00d211597cb0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# ARGOS_BRAIN_INTEGRATION_GUIDE.md

- Source: `f3iles/ARGOS_BRAIN_INTEGRATION_GUIDE.md`
- Extract: `text`
- SHA256: `319c6f8439fcd40913ed3b7317005445bb866bd5f9d0090ce2fc00d211597cb0`

## Content

# 🧠 ARGOS AI BRAIN - ПОЛНЫЙ ГАЙД ИНТЕГРАЦИИ

**Версия:** 1.0.0  
**Статус:** Production Ready  
**Дата:** 2026-04-17

---

## 📋 СОДЕРЖАНИЕ

1. [Обзор системы](#обзор-системы)
2. [Архитектура](#архитектура)
3. [Установка](#установка)
4. [Конфигурация Azure](#конфигурация-azure)
5. [Запуск](#запуск)
6. [Использование API](#использование-api)
7. [Примеры](#примеры)
8. [Интеграция с ARGOS](#интеграция-с-argos)
9. [Мониторинг](#мониторинг)
10. [Troubleshooting](#troubleshooting)

---

## 🧠 ОБЗОР СИСТЕМЫ

**ARGOS AI Brain** - это распределённая система интеллектуальных агентов, которая обеспечивает:

- ✅ **Многоагентную координацию** - несколько ИИ агентов работают вместе
- ✅ **Azure OpenAI интеграция** - использует мощь GPT-4 и Claude
- ✅ **Локальное кэширование** - памяти и история решений
- ✅ **P2P распределение** - работает на всех узлах ARGOS
- ✅ **REST API** - простое взаимодействие через HTTP
- ✅ **Асинхронная обработка** - параллельная работа агентов

### Компоненты системы

| Компонент | Описание | Порт |
|-----------|---------|------|
| **ARGOSBrain** | Главный координатор | Internal |
| **API Server** | Flask REST API | 5001 |
| **Agents** | Интеллектуальные агенты | Internal |
| **Memory DB** | SQLite база памяти | Internal |
| **Azure OpenAI** | LLM backend | API |

---

## 🏗️ АРХИТЕКТУРА

```
┌─────────────────────────────────────────────────────────┐
│                   ARGOS AI BRAIN SYSTEM                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  REST API (Port 5001)                                  │
│  ├─ /think          → Основной запрос                 │
│  ├─ /coordinate     → Многоагентная координация       │
│  ├─ /analyze        → Анализ данных                   │
│  ├─ /optimize       → Оптимизация                     │
│  └─ /monitor        → Мониторинг                      │
│                                                         │
│           ↓                                             │
│                                                         │
│  ARGOSBrain (Главный мозг)                             │
│  ├─ Управление агентами                               │
│  ├─ Распределение задач                               │
│  └─ Глобальная координация                             │
│                                                         │
│           ↓                                             │
│                                                         │
│  Агенты (Role-based):                                  │
│  ├─ MASTER       → Стратегические решения             │
│  ├─ ANALYST      → Анализ данных                      │
│  ├─ OPTIMIZER    → Оптимизация                        │
│  ├─ MONITOR      → Мониторинг                         │
│  └─ EXECUTOR     → Выполнение команд                  │
│                                                         │
│           ↓                                             │
│                                                         │
│  Azure OpenAI Backend (GPT-4 / Claude):                │
│  ├─ Chat Completions                                   │
│  ├─ Token counting                                     │
│  └─ Advanced reasoning                                 │
│                                                         │
│           ↓                                             │
│                                                         │
│  Memory System (SQLite3):                              │
│  ├─ Agent memories                                     │
│  ├─ Decision logs                                      │
│  └─ Statistics                                         │
│                                                         │
│           ↓                                             │
│                                                         │
│  P2P Network (ARGOS Integration):                      │
│  ├─ Distributed decision making                       │
│  ├─ Cross-node agent coordination                      │
│  └─ Global state management                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 УСТАНОВКА

### 1. Предварительные требования

```bash
# Python 3.9+
python --version

# pip
pip --version

# Git (для клонирования репозитория)
git --version
```

### 2. Установка зависимостей

```bash
# Клонировать репозиторий ARGOS
cd /home/ava/argoss

# Установить зависимости Brain
pip install -r requirements-brain.txt

# Или вручную (если нет requirements)
pip install azure-ai-openai flask flask-cors aiohttp pandas numpy
```

### 3. Структура файлов

```
~/.argos/
├── .env                      # Переменные окружения
├── agent_memory.db          # База памяти агентов
├── brain.log                # Логи мозга
├── config.json              # Конфигурация
└── logs/
    └── ...                  # Архив логов

Код:
├── argos_ai_brain.py        # Основной мозг
├── argos_brain_api.py       # REST API
├── argos_brain_examples.py  # Примеры
└── ARGOS_BRAIN_SETUP.sh     # Скрипт установки
```

---

## ☁️ КОНФИГУРАЦИЯ AZURE

### 1. Создание Azure OpenAI ресурса

```bash
# Установить Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Войти в Azure
az login

# Создать ресурс OpenAI
az cognitiveservices account create \
  --name argos-openai \
  --resource-group rg-argos \
  --kind OpenAI \
  --sku s0 \
  --location eastus \
  --assign-identity
```

### 2. Получить credentials

```bash
# Получить ключ
AZURE_OPENAI_KEY=$(az cognitiveservices account keys list \
  --name argos-openai \
  --resource-group rg-argos \
  --query key1 -o tsv)

# Получить endpoint
AZURE_OPENAI_ENDPOINT=$(az cognitiveservices account show \
  --name argos-openai \
  --resource-group rg-argos \
  --query properties.endpoint -o tsv)

echo "Key: $AZURE_OPENAI_KEY"
echo "Endpoint: $AZURE_OPENAI_ENDPOINT"
```

### 3. Задеплоить модель GPT-4

```bash
az cognitiveservices account deployment create \
  --resource-group rg-argos \
  --name argos-openai \
  --deployment-id argos-gpt4 \
  --model-name gpt-4-turbo \
  --model-version 2024-02-15-preview \
  --sku standard \
  --capacity 1
```

### 4. Конфигурировать .env

```bash
# Создать файл .env
mkdir -p ~/.argos
cat > ~/.argos/.env << EOF
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_KEY=$AZURE_OPENAI_KEY
AZURE_OPENAI_VERSION=2024-02-15-preview
AZURE_OPENAI_MODEL=gpt-4-turbo
AZURE_DEPLOYMENT_NAME=argos-gpt4

# ARGOS Configuration
ARGOS_NODE_ID=local-pc
ARGOS_P2P_PORT=55771
ARGOS_API_PORT=5001

# Logging
LOG_LEVEL=INFO
LOG_FILE=~/.argos/brain.log
EOF

# Применить
export $(cat ~/.argos/.env | xargs)
```

---

## 🚀 ЗАПУСК

### Вариант 1: Локально (разработка)

```bash
# Инициализировать мозг
python argos_ai_brain.py

# В отдельном терминале запустить API
python argos_brain_api.py

# Проверить здоровье
curl http://localhost:5001/health
```

### Вариант 2: В фоне

```bash
# Запустить в фоне
nohup python argos_brain_api.py > ~/.argos/brain.log 2>&1 &

# Посмотреть PID
ps aux | grep argos_brain_api.py

# Остановить
kill <PID>
```

### Вариант 3: Docker

```bash
# Создать Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements-brain.txt .
RUN pip install -r requirements-brain.txt

COPY argos_ai_brain.py .
COPY argos_brain_api.py .

ENV FLASK_APP=argos_brain_api.py

CMD ["python", "argos_brain_api.py"]
EOF

# Построить образ
docker build -t argos-brain:latest .

# Запустить контейнер
docker run -d \
  --name argos-brain \
  -p 5001:5001 \
  -v ~/.argos:/root/.argos \
  -e AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT \
  -e AZURE_OPENAI_KEY=$AZURE_OPENAI_KEY \
  argos-brain:latest

# Проверить логи
docker logs -f argos-brain
```

### Вариант 4: Azure Container Instances

```bash
# Создать контейнер в Azure
az container create \
  --resource-group rg-argos \
  --name argos-brain \
  --image argos-brain:latest \
  --ports 5001 \
  --environment-variables \
    AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT \
    AZURE_OPENAI_KEY=$AZURE_OPENAI_KEY \
  --cpu 2 \
  --memory 4

# Получить IP адрес
az container show \
  --resource-group rg-argos \
  --name argos-brain \
  --query ipAddress.ip -o tsv
```

---

## 📡 ИСПОЛЬЗОВАНИЕ API

### Базовые операции

#### 1. Проверка здоровья

```bash
curl http://localhost:5001/health
# {"status": "online", "service": "ARGOS AI Brain API"}
```

#### 2. Получить статус мозга

```bash
curl http://localhost:5001/brain/status
# Статус всех агентов, памяти, и системы
```

#### 3. Список агентов

```bash
curl http://localhost:5001/agents
# Получить список всех запущенных агентов
```

### Основные запросы

#### 4. Простой запрос (think)

```bash
curl -X POST http://localhost:5001/think \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Какова текущая производительность системы?",
    "role": "monitor"
  }'
```

#### 5. Координация агентов

```bash
curl -X POST http://localhost:5001/coordinate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Оптимизировать производительность на 30%",
    "agents": ["analyst", "optimizer", "executor"]
  }'
```

#### 6. Анализ данных

```bash
curl -X POST http://localhost:5001/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "cpu": 45,
      "memory": 60,
      "network": "stable"
    }
  }'
```

#### 7. Оптимизация

```bash
curl -X POST http://localhost:5001/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": {
      "cpu_usage": 85,
      "response_time": 500
    },
    "targets": {
      "cpu_usage": 50,
      "response_time": 200
    }
  }'
```

#### 8. Мониторинг

```bash
curl -X POST http://localhost:5001/monitor \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": {
      "cpu_percent": 45,
      "memory_percent": 62,
      "errors_last_hour": 2
    }
  }'
```

---

## 💻 ПРИМЕРЫ

### Пример на Python

```python
from argos_brain_examples import ARGOSBrainClient

# Создать клиент
client = ARGOSBrainClient("http://localhost:5001")

# Запрос к мозгу
result = client.think(
    query="Какие bottlenecks в системе?",
    role="analyst"
)

print(f"Ответ: {result.response}")
print(f"Время мышления: {result.thinking_time}s")
```

### Запуск всех примеров

```bash
python argos_brain_examples.py

# Включает примеры:
# 1. Базовое мышление
# 2. Анализ данных
# 3. Оптимизация
# 4. Многоагентная координация
# 5. Мониторинг системы
# 6. Управление агентами
# 7. Контекстное мышление
```

---

## 🔗 ИНТЕГРАЦИЯ С ARGOS

### Интеграция в main.py

```python
# В main.py добавить:
from argos_brain_examples import ARGOSBrainClient

class ARGOSSystem:
    def __init__(self):
        # ... существующий код ...
        self.brain = ARGOSBrainClient("http://localhost:5001")
    
    async def analyze_network(self):
        """Анализировать состояние сети с помощью мозга"""
        metrics = self.get_network_metrics()
        result = self.brain.analyze(metrics)
        return result

# Использование в P2P команде
def p2p_status(self):
    """Улучшенная команда p2p status"""
    status = super().p2p_status()
    
    # Попросить мозг проанализировать статус
    analysis = asyncio.run(self.analyze_network())
    
    print(f"Status: {status}")
    print(f"Brain Analysis: {analysis.response}")
```

### Интеграция в P2P сеть

```python
# Синхронизация состояния между узлами через мозг
async def sync_state_with_brain(self):
    """Синхронизировать состояние системы через AI"""
    
    task = "Найти оптимальный способ балансирования нагрузки"
    result = await self.brain.coordinate(
        task=task,
        agents=['analyst', 'optimizer']
    )
    
    # Применить рекомендации
    for agent_result in result['agent_results'].values():
        if agent_result.get('success'):
            self.apply_recommendations(agent_result['response'])
```

---

## 📊 МОНИТОРИНГ

### Просмотр логов

```bash
# Реальное время
tail -f ~/.argos/brain.log

# Последние 100 строк
tail -100 ~/.argos/brain.log

# Поиск ошибок
grep "ERROR" ~/.argos/brain.log
```

### Статистика агентов

```bash
# Запросить статус мозга
curl http://localhost:5001/brain/status | jq '.agents'

# Или из БД
sqlite3 ~/.argos/agent_memory.db << SQL
SELECT agent_id, tasks_completed, tasks_failed, total_tokens 
FROM agent_stats;
SQL
```

### Метрики Azure

```bash
# Просмотреть использование Azure OpenAI
az monitor metrics list \
  --resource argos-openai \
  --resource-group rg-argos \
  --metric Tokens \
  --aggregation Total

# Стоимость API
az cognitiveservices account usage \
  --name argos-openai \
  --resource-group rg-argos
```

---

## 🔧 TROUBLESHOOTING

### Проблема: Azure SDK не установлена

```bash
# Решение
pip install azure-ai-openai azure-identity
```

### Проблема: Ошибка подключения к Azure

```bash
# Проверить credentials
echo $AZURE_OPENAI_KEY
echo $AZURE_OPENAI_ENDPOINT

# Перегенерировать ключи
az cognitiveservices account keys regenerate \
  --name argos-openai \
  --resource-group rg-argos \
  --key-name key1
```

### Проблема: API недоступен

```bash
# Проверить, что сервер запущен
ps aux | grep argos_brain_api.py

# Проверить логи
tail -100 ~/.argos/brain.log

# Проверить порт
netstat -tuln | grep 5001
```

### Проблема: Высокое использование tokens

```bash
# Проверить использование
sqlite3 ~/.argos/agent_memory.db \
  "SELECT SUM(tokens_used) FROM agent_stats;"

# Оптимизировать:
# - Снизить max_tokens в конфиге агентов
# - Увеличить кэширование
# - Использовать более краткие промпты
```

---

## 📈 PERFORMANCE TUNING

### Оптимизация памяти

```python
# В argos_ai_brain.py:
memory_db = AgentMemoryDB()

# Очистить старые записи
sqlite3 ~/.argos/agent_memory.db << SQL
DELETE FROM memories 
WHERE timestamp < datetime('now', '-7 days');
SQL
```

### Оптимизация Azure

```bash
# Использовать меньший размер capacity
az cognitiveservices account deployment update \
  --deployment-id argos-gpt4 \
  --capacity 2  # Вместо стандартного

# Или использовать более дешёвую модель
az cognitiveservices account deployment create \
  --model-name gpt-35-turbo  # Вместо gpt-4
```

---

## ✅ ЧЕКЛИСТ ГОТОВНОСТИ

- [ ] ✅ Azure OpenAI ресурс создан
- [ ] ✅ Модель GPT-4 задеплоена
- [ ] ✅ Credentials получены и установлены
- [ ] ✅ .env файл создан
- [ ] ✅ Зависимости установлены
- [ ] ✅ База данных инициализирована
- [ ] ✅ API запущен и доступен
- [ ] ✅ Примеры работают
- [ ] ✅ Интегрирован с ARGOS
- [ ] ✅ Мониторинг настроен

---

## 🎉 ЗАКЛЮЧЕНИЕ

**ARGOS AI Brain** - это мощная система для интеллектуальной автоматизации вашей распределённой сети!

Со своей помощью система может:
- 🧠 Анализировать состояние сети
- ⚡ Оптимизировать производительность
- 👁️ Мониторить здоровье системы
- 🤝 Координировать работу компонентов
- 💡 Принимать умные решения

**Готов к Production!** 🚀

---

**Поддержка:** Используйте примеры в `argos_brain_examples.py`  
**Документация:** http://localhost:5001/  
**Логирование:** `~/.argos/brain.log`

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
