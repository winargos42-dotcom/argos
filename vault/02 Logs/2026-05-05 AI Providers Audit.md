# Отчёт: Проверка AI-провайдеров ARGOS

Дата: 2026-05-05
Статус: ✅ Оперативно

---

## Проверено: 9 провайдеров

### ✅ РАБОТАЮТ (4/9)

| Провайдер | API | Статус | Модели |
|-----------|-----|--------|--------|
| **DeepSeek** | api.deepseek.com | ✅ OK | deepseek-v4-flash, deepseek-v4-pro |
| **OpenAI** | api.openai.com | ✅ OK | 70+ моделей (GPT-4o, GPT-5.5, o3, o4-mini...) |
| **Azure OpenAI** | argoss-sig-2026.openai.azure.com | ✅ OK | gpt-4 |
| **Kimi** | api.moonshot.ai | ✅ **ПОЧИНЕН** | k2.6, k2.5, moonshot-v1-128k (9 моделей) |

### ❌ НЕ РАБОТАЮТ (2/9)

| Провайдер | Проблема | Решение |
|-----------|----------|---------|
| **xAI Grok** | 🔒 API key заблокирован | Получить новый ключ на x.ai |
| **Cloudflare AI** | 🚫 Invalid API Token | Обновить токен в Cloudflare Dashboard |

### ⚠️ ОТКЛЮЧЕНЫ (3/9)

| Провайдер | Причина | Действие |
|-----------|---------|----------|
| **Gemini** | `ARGOS_DISABLE_GEMINI=1` | ✅ **ВКЛЮЧЕН** — 6 ключей готовы |
| **GigaChat** | `ARGOS_DISABLE_GIGACHAT=1` | Оставлено отключённым |
| **YandexGPT** | Пустой IAM токен | Нужно получить IAM токен |

---

## Исправления в конфигурации

### `.env` (F:\debug\argoss\.env)

```diff
# Kimi — исправлен endpoint
- KIMI_API_KEY=sk-e9hNy4zn4BaU8KnJbL5I6NWN5zWTKa3Q31MS1CF3MhWmR7zN
+ KIMI_API_KEY=sk-e9hNy4zn4BaU8KnJbL5I6NWN5zWTKa3Q31MS1CF3MhWmR7zN
+ KIMI_BASE_URL=https://api.moonshot.ai/v1

# Gemini — включён
- ARGOS_DISABLE_GEMINI=1
+ ARGOS_DISABLE_GEMINI=0
```

---

## Технические детали

### Kimi (Moonshot AI)
- **Проблема:** `api.moonshot.cn` — таймаут (китайский endpoint)
- **Решение:** Переключено на `api.moonshot.ai` (global)
- **Оба ключа работают:**
  - `sk-e9hNy4z...` — ✅ 9 моделей
  - `sk-XFF8sBh...` — ✅ 9 моделей

### Доступные модели Kimi
- `kimi-k2.6` — latest (vision + video + reasoning, 256K context)
- `kimi-k2.5` — (vision + video + reasoning, 256K context)
- `moonshot-v1-128k` — (131K context)
- `moonshot-v1-32k`, `moonshot-v1-8k`, `moonshot-v1-auto`
- Vision preview модели

---

## Система

- **ARGOS:** v2.1.3
- **Uptime:** ~40 сек (свежий запуск)
- **GPU:** 3x llama-server Vulkan (RX 580, Vega 11, RX 560)
- **MCP:** localhost:8000 (30 tools)
- **CPU:** 100% | **RAM:** 56.2%

---

## Следующие шаги

1. [ ] Получить новый Grok API key
2. [ ] Обновить Cloudflare API token
3. [ ] Получить Yandex IAM токен (если нужен)
4. [ ] Перезапустить ARGOS для применения изменений

---

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
