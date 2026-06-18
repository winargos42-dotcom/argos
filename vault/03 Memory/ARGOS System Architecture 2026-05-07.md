# ARGOS System Architecture — 2026-05-07

## Общая схема

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ Telegram │  │ Obsidian │  │ Dashboard│                 │
│  │  (Bot)   │  │  (Vault) │  │ (:8080)  │                 │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                 │
└───────┼─────────────┼─────────────┼─────────────────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
┌─────────────────────▼─────────────────────────────────────┐
│                  ARGOS CORE (.venv)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  AutoGPT     │  │   LLM-Wiki   │  │  Telegram    │   │
│  │  Engine      │  │   Module     │  │  Handler     │   │
│  │  (P0-P3)     │  │              │  │              │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                  │                  │           │
│         └──────────────────┼──────────────────┘           │
│                            │                              │
│  ┌─────────────────────────▼──────────────────────────┐  │
│  │              AI Decision Router                    │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐     │  │
│  │  │Gemini  │ │DeepSeek│ │Kimi    │ │Ollama  │     │  │
│  │  │(Cloud) │ │(Cloud) │ │(Cloud) │ │(Local) │     │  │
│  │  └────────┘ └────────┘ └────────┘ └────────┘     │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
        │
┌───────▼──────────────────────────────────────────────────┐
│                 MCP SERVER (System Python)               │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Endpoint: http://127.0.0.1:8000/mcp               │  │
│  │                                                      │  │
│  │  Инструменты:                                        │  │
│  │  • wiki_ingest  — Telegram → Obsidian               │  │
│  │  • wiki_lint    — Проверка vault                    │  │
│  │  • wiki_query   — Поиск по знаниям                  │  │
│  │  • gpu_status   — Статус GPU кластера               │  │
│  │  • gcp_quota    — Мониторинг квот                   │  │
│  │  • send_email   — Отправка email                    │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
        │
┌───────▼──────────────────────────────────────────────────┐
│              GPU CLUSTER (Vulkan llama-server)           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  :8082      │  │  :8083      │  │  :8084      │     │
│  │ RX 580 8GB  │  │ Vega 11 2GB │  │ RX 560 4GB  │     │
│  │ qwen2.5:3b  │  │ tinyllama   │  │ qwen2.5:3b  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└──────────────────────────────────────────────────────────┘
        │
┌───────▼──────────────────────────────────────────────────┐
│              EXTERNAL SERVICES                           │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │
│  │  GCP   │  │Kaggle  │  │Google  │  │GitHub  │        │
│  │(Cloud) │  │(Train) │  │(OAuth) │  │(Repo)  │        │
│  └────────┘  └────────┘  └────────┘  └────────┘        │
└──────────────────────────────────────────────────────────┘
```

## Компоненты

### 1. User Interface Layer

**Telegram Bot**
- Интерактивный чат с ARGOS
- Поддержка команд: `/status`, `/mcp`, `/health`
- Получает ответы от AI Decision Router

**Obsidian Vault**
- Хранилище знаний (5,514 файлов)
- LLM-Wiki архитектура: raw → wiki → AGENTS.md
- Интеграция через LLM-Wiki модуль

**Dashboard (:8080)**
- Веб-интерфейс мониторинга
- Статус GPU, MCP, системы
- Логи и метрики

### 2. ARGOS Core (.venv)

**AutoGPT Engine**
- Phase-машина автономии (P0-P3)
- P0: Safety Rails (бюджет, read-only)
- P1: Resilience (health-check каждые 60с)
- P2: Dataset generation (4:00 AM)
- P3: Cloud deployment (ожидание A100)

**LLM-Wiki Module**
- `telegram_ingest.py` — импорт чатов в wiki
- `obsidian_lint.py` — проверка качества vault
- `wiki_query.py` — LLM-поиск по знаниям

**AI Decision Router**
- Выбор провайдера на основе задачи
- Приоритет: Local GPU → Gemini → DeepSeek → Kimi
- Fallback цепочка при ошибках

### 3. MCP Server (System Python)

**Endpoint**: `http://127.0.0.1:8000/mcp`

**Инструменты**:
- `wiki_ingest` — Преобразование Telegram-логов
- `wiki_lint` — Линтинг Obsidian vault
- `wiki_query` — Поиск с LLM-контекстом
- `gpu_status` — Мониторинг GPU кластера
- `gcp_quota` — Проверка GCP квот
- `send_email` — Отправка уведомлений

### 4. GPU Cluster

**Архитектура**: Vulkan llama-server

| Сервер | GPU | VRAM | Модель | Порт |
|--------|-----|------|--------|------|
| Primary | RX 580 | 8GB | qwen2.5:3b | :8082 |
| Secondary | Vega 11 | 2GB | tinyllama | :8083 |
| Tertiary | RX 560 | 4GB | qwen2.5:3b | :8084 |

**Auto-start**: Запускается автоматически при старте ARGOS

### 5. External Services

**GCP (argos-489214)**
- Проект: `argos-489214`
- Сервисный аккаунт: `argoss@argos-489214.iam.gserviceaccount.com`
- Квота A100: ⏳ Ожидает подтверждения
- Vertex AI: Готов к деплою

**Kaggle**
- Fallback для fine-tuning
- Бесплатно: T4 x2, 30ч/неделю
- Ноутбук: `config/kaggle_finetune.ipynb`

**Google OAuth**
- Статус: ❌ Заблокирован (403)
- Альтернатива: App Password
- Email: `winargos42@gmail.com`

## Потоки данных

### 1. Telegram → ARGOS
```
User message → Telegram Bot → AI Router → (GPU/Cloud) → Response
                                    ↓
                              LLM-Wiki Module
                                    ↓
                              Obsidian Vault
```

### 2. Fine-Tuning Pipeline
```
Obsidian Vault → Converter → train.jsonl → GCS → Vertex AI/Kaggle → Model
```

### 3. AutoGPT P2 (Dataset Generation)
```
Scheduler (4:00 AM) → Scan vault → Create examples → Update train.jsonl
```

### 4. Health Monitoring
```
Health Check → MCP Status → GPU Status → Alert (if failed)
                   ↓
              Self-Healing → Restart → Fallback
```

## Безопасность

### Safety Rails
- Бюджетный лимит: $50/мес
- Read-only директории: `C:/Windows`, `F:/debug/аргос`
- Подтверждение destructive операций
- Content filtering (Gemini Safety API)

### API Key Rotation
- Gemini: Обновлен 2026-05-07
- Grok: Требует замены
- SERPAPI: Требует пополнения

## Масштабирование

### Вертикальное (Local)
- Добавление GPU в кластер
- Увеличение RAM для моделей
- NVMe для быстрого I/O

### Горизонтальное (Cloud)
- GCP A100 для training
- Multi-region deployment
- Auto-scaling Vertex AI endpoints

## Мониторинг

| Метрика | Инструмент | Частота |
|---------|-----------|---------|
| CPU/RAM | Windows Task Manager | Real-time |
| GPU Usage | nvidia-smi / Vulkan | Real-time |
| MCP Health | HTTP :8000/health | Каждые 60с |
| GPU Status | MCP tool gpu_status | Каждые 5 мин |
| GCP Quota | MCP tool gcp_quota | Каждые 5 мин |
| Disk Space | Windows | Каждые 15 мин |

---

## Связанные документы

- [[ARGOS Unified State 2026-05-06]] — Текущее состояние системы
- [[ARGOS Next Steps 2026-05-07]] — План действий
- [[ARGOS Memory Web]] — Граф знаний
- [[ARGOS Session 2026-05-07 Evening]] — Отчет сессии
- [[Контекст работы]] — Контекст оператора

*Архитектура актуальна на: 2026-05-07*
*Версия: 2.0*
*Следующее обновление: после fine-tuning*

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
