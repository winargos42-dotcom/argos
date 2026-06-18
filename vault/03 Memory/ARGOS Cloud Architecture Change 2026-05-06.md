# Архитектура ARGOS: Изменения в облачной инфраструктуре

**Дата:** 2026-05-06  
**Автор:** System  
**Теги:** #infra #azure #cloud #argos-v2 #migration

---

## Ключевое изменение

**Azure VM больше не используются.**

Все предыдущие Azure-инстансы (Ollama VM Sweden, Japan East, Australia East) деактивированы и не входят в текущую архитектуру ARGOS v2.1.3.

## Причина

- Старые Azure-аккаунты были привязаны к предыдущей версии ARGOS (v1.x)
- Новая версия ARGOS v2 требует чистого облачного окружения
- Безопасность: изоляция старых credentials и VM от новой автономной системы

## Что будет

### Новый аккаунт ARGOS
- **Платформа:** Google Cloud Platform (GCP)
- **Проект:** `argos-489214` (уже создан)
- **Billing:** Активен
- **Целевые GPU:**
  - **A100** — для fine-tune и обучения (ожидание квоты, запрос подан)
  - **L4** — для inference (доступен, 1 instance)
  - **T4** — для тестирования (доступен, 1 instance)

### Архитектура v2.1.3 (текущая)

```
┌─────────────────────────────────────┐
│         ЛОКАЛЬНЫЙ ХОСТ              │
│  Windows + WSL2 + Docker Desktop    │
├─────────────────────────────────────┤
│  GPU Cluster (3x Vulkan):           │
│    • RX 580  @ :8082 (qwen2.5:3b)   │
│    • Vega 11 @ :8083 (tinyllama)    │
│    • RX 560  @ :8084 (qwen2.5:3b)   │
├─────────────────────────────────────┤
│  ARGOS Core (.venv):                │
│    • MCP        :8000               │
│    • Dashboard  :8080               │
│    • Telegram   @Argosssbot         │
│    • P2P Bridge :8010               │
│    • Brain API  :5010               │
├─────────────────────────────────────┤
│  API Providers (9/12):              │
│    ✅ Kimi, Grok, OpenAI, Groq      │
│    ✅ Cloudflare, DeepSeek          │
│    ✅ WatsonX, Ollama               │
│    ⚠️  Gemini (expired)             │
│    ❌ Azure (deprecated)            │
└─────────────────────────────────────┘
                   │
                   │  (будущее)
                   ▼
┌─────────────────────────────────────┐
│      GOOGLE CLOUD PLATFORM          │
│  Project: argos-489214              │
│                                     │
│  Compute:                           │
│    • a2-highgpu-1g (A100) — pending │
│    • g2-standard-4 (L4)  — ready    │
│                                     │
│  Services:                          │
│    • Cloud Storage (datasets)       │
│    • Vertex AI (training)           │
│    • Cloud Monitoring               │
└─────────────────────────────────────┘
```

## Устаревшие компоненты (v1.x)

| Компонент | Статус | Замена |
|-----------|--------|--------|
| Azure VM Sweden (Ollama) | ❌ Удалена | GCP L4 |
| Azure VM Japan East | ❌ Удалена | GCP A100 |
| Azure VM Australia | ❌ Удалена | GCP T4 |
| Старый Azure аккаунт | ❌ Закрыт | argos-489214 |
| Ollama remote endpoints | ❌ Отключены | Локальный GPU cluster |

## Текущий статус миграции

- [x] GCP проект создан
- [x] Billing настроен
- [x] Квота L4/T4 получена
- [ ] Квота A100 (ожидание 24-48ч)
- [ ] Terraform конфигурация (в планах)
- [ ] Auto-deploy pipeline (P3)

## Связанные документы

- [[ARGOS Unified State 2026-05-06]]
- [[2026-05-06 GCP A100 Quota Request]]
- [[AutoGPT Integration Complete]]

---

*Backbone Hub*

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
