# ARGOS Unified State 2026-05-07

Обновлено: `2026-05-07`
Оператор: `Всеволод (Seva / AvA / SiG)`
Режим: `production → autonomous`

## Канонические точки

- Проект: `F:\debug\argoss`
- Vault: `F:\debug\аргос`
- MCP endpoint: `http://127.0.0.1:8000/mcp`
- AutoGPT Config: `F:\debug\argoss\config\autogpt_goal.yaml`

## Парадигмальный сдвиг

**Статус: СИСТЕМА СТАЛА СУБЪЕКТОМ.**  
Переход от «CLI-ассистента» к «автономному агенту с памятью и волей».

---

## Критические изменения 2026-05-07

### Облачная инфраструктура
- ❌ **Azure VM УДАЛЕНЫ** — все старые VM (Sweden, Japan, Australia) деактивированы
- ❌ **Старый Azure аккаунт закрыт**
- ✅ **Новый аккаунт:** GCP `argos-489214`
- ✅ **Локальный GPU кластер:** 3x Vulkan (RX 580 / Vega 11 / RX 560)
- 📄 Подробности: [[ARGOS Cloud Architecture Change 2026-05-06]]

### Исправление критической ошибки
- ✅ **Ошибка устранена**: "No API provider registered for api: ollama" в Telegram
- **Причина**: Дублирование процессов ARGOS (старый PID 4436, uptime 6.8ч + новый)
- **Решение**: Полная очистка всех Python-процессов, запуск единственного экземпляра
- **Результат**: Система стабильна, uptime сброшен

### LLM-Wiki интеграция
- ✅ **Модуль создан**: `src/llm_wiki/` с инструментами MCP
- **Инструменты**: `wiki_ingest`, `wiki_lint`, `wiki_query`
- **Архитектура**: raw → wiki → AGENTS.md (Karpathy LLM-Wiki)
- 📄 Подробности: [[LLM-Wiki Integration]]

### Подготовка Fine-Tuning датасета
- ✅ **Датасет создан**: 5,537 примеров, 18.73 MB
- **Формат**: OpenAI chat (system/user/assistant)
- **Источник**: Obsidian vault (5,537 Markdown файлов, ~12M токенов)
- **Конфиги**: Vertex AI (`config/vertex_job.json`), Kaggle fallback
- 📄 Подробности: [[Fine-Tune Strategy Personal AI Brain]]

## Выполнено 2026-05-07

### Патчи безопасности
- ✅ **JSON-эскейпинг** (`src/self_healing.py:167-189`) — защита от неэкранированных кавычек в ASM/JSON
- ✅ **Grist Loop Prevention** (`src/connectivity/p2p_bridge.py:752-758`) — детекция и дроп пакетов от самой себя

### Конфигурация AutoGPT-агента
- ✅ **Safety Rails** в `.env`:
  - Бюджет: $50/мес (авто-остановка GCP при превышении)
  - Подтверждение: destructive, cloud provision, fine-tune > $5
  - Read-only: `C:/Windows`, `F:/debug/аргос`
- ✅ **Primary Goal** зафиксирован:
  > Обеспечить 99.5% аптайм MCP через health-check → self-healing → fallback, и ежедневно порождать обучающий датасет из Obsidian-логов.

### GCP Infrastructure
- ✅ **Квота A100:** ЗАПРОШЕНА (ожидание ответа Google 24-48ч)
- ✅ **Мониторинг квот:** Модуль `src/gcp_quota_monitor.py` создан и готов
  - Проверка каждые 5 минут
  - Алерт в Obsidian при появлении квоты
  - Интеграция с AutoGPT Phase 3
- ⚠️ **Текущий статус:** A100 = 0 во всех регионах, L4/T4 = 1 (доступно, но downgrade)
- ✅ **VM:** Нет запущенных (ожидание квоты A100)

### API Обновления
- ✅ **Gemini**: Ключ обновлен (старые истекли), модель `gemini-2.5-flash`
- ❌ **Gmail OAuth**: Заблокирован Google (403), переход на App Password
- ⏳ **Email App Password**: Ожидает создания пользователем

### Системная стабилизация
- ✅ **Процессы**: Убиты дубли, запущен единственный экземпляр ARGOS
- ✅ **GPU кластер**: 3/3 сервера активны и отвечают
- ✅ **MCP**: Стабильная работа на порту 8000
- ✅ **Telegram**: Отправка сообщений восстановлена

---

## AI Провайдеры (актуально)

| Провайдер | Статус | Примечание |
|-----------|--------|------------|
| **DeepSeek** | ✅ OK | v4-flash, v4-pro |
| **OpenAI** | ✅ OK | 70+ моделей |
| **Azure OpenAI** | ❌ Deprecated | Аккаунт закрыт, VM удалены |
| **Groq** | ✅ OK | llama-3.3-70b-versatile |
| **Kimi** | ✅ OK | api.moonshot.ai, k2.6 |
| **Gemini** | ✅ OK | Обновлен, `gemini-2.5-flash` работает |
| **HuggingFace** | ✅ OK | Датасеты доступны |
| **Cloudflare** | ✅ OK | Workers AI |
| **WatsonX** | ✅ OK | IBM Lite tier |
| **Ollama** | ✅ OK | Локальный GPU cluster |
| **Grok** | ❌ Заблокирован | Нужен новый ключ x.ai |
| **SERPAPI** | ❌ Нет запросов | Пополнить |

---

## Phase-машина автономии

| Phase | Статус | Описание |
|-------|--------|----------|
| **P0 Safety** | ✅ Активно | Бюджет, read-only, алерты |
| **P1 Resilience** | ✅ Активно | Health-check MCP каждые 60с |
| **P2 Dataset** | ✅ Готов | Датасет создан: 5,537 примеров, 18.73 MB |
| **P3 Cloud** | ⏳ Блокер | Ожидание квоты A100 или Kaggle fallback |

---

## Критические блокеры

1. **Email App Password:** ⏳ Ожидает создания пользователем
2. **GCP A100 Quota:** 0 (запрос отправлен вручную, ожидание 24-48ч)
3. **Grok API:** Заблокирован (заменить ключ на x.ai)
4. **SERPAPI:** Нет запросов (пополнить баланс)

## Системные метрики

| Метрика | Значение |
|---------|----------|
| Uptime ARGOS | ~5.2 часа (стабильно) |
| CPU | ~25% |
| RAM | 64.6% |
| GPU | 3/3 активны |
| Файлов в vault | 5,514 |
| Размер vault | 63.6 MB |
| Свободно на F:\ | 19.9 GB / 132 GB |

---

## Следующие шаги

1. [ ] Одобрение квоты A100 → авто-деплой `a2-highgpu-1g`
2. [ ] Замена ключа Grok
3. [ ] Пополнение SERPAPI
4. [ ] Первый автономный цикл P2 (генерация датасета)
5. [ ] Интеграция AutoGPT с `process_logic_async` (ядро ARGOS)

---

## Связи
- [[2026-05-05 AI Providers Audit]]
- [[2026-05-05 Infrastructure Reconnaissance]]
- [[2026-05-06 GCP A100 Quota Request]]
- [[ARGOS Cloud Architecture Change 2026-05-06]]
- [[ARGOS Memory Web]]

[[Backbone Hub]]

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
