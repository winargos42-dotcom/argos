---
argos_import: sharedmemory_mirror
source_path: claude/project_cloud_providers.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_cloud_providers.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_cloud_providers.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_cloud_providers.md`
- Category: [[Claude Hub]]

## Content

---
name: Cloud AI Providers
description: Статус облачных AI провайдеров ARGOS — проверено 2026-05-10
type: project
originSessionId: 07f7f1bc-6a4f-49cb-aca5-c0efa4942a8e
---
## Рабочие провайдеры

| Провайдер | Модель | Контекст | Endpoint |
|-----------|--------|----------|----------|
| Ollama (локальный) | qwen2.5:3b | 32k | localhost:11434 |
| DeepSeek | deepseek-chat (V3) | 128k | api.deepseek.com |
| Kimi / Moonshot | kimi-k2.5 | 256k | api.moonshot.ai/v1 (глобальный!) |
| OpenAI | gpt-4o-mini | 128k | api.openai.com |

## Нерабочие (причины)

| Провайдер | Причина | Как починить |
|-----------|---------|-------------|
| Gemini (5 ключей) | API key expired | Новые ключи: aistudio.google.com |
| Groq | 401 Invalid API Key | Новый ключ: console.groq.com |
| Grok (xAI) | 403 Key blocked | Проверить подписку xAI |
| WatsonX | 429 Лимит исчерпан | Ждать сброса месячного лимита |
| GigaChat | 402 Payment Required | Пополнить на developers.sber.ru |
| Cloudflare | Нет CLOUDFLARE_API_TOKEN | Создать токен на dash.cloudflare.com |
| YandexGPT | Нет IAM_TOKEN | Настроить на console.yandex.cloud |

## Конфигурация (.env)
- `ARGOS_AI_PRIORITY="ollama,deepseek,kimi,openai"`
- Kimi: используй api.moonshot.ai (НЕ .cn — гео-блок из РФ!)
- Нерабочие отключены через ARGOS_DISABLE_*

**Why:** облачные провайдеры для обработки большого объёма, когда локальный qwen2.5:3b не справляется.
**How to apply:** при работе с AI — Ollama первый, DeepSeek+Kimi облачные, OpenAI фоллбэк.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: \[\[ARGOS Memory Web\]\]
- Тематический узел: \[\[Claude Hub\]\]
- Карта памяти: \[\[Карта памяти\]\]
- Контекст работы: \[\[Контекст работы\]\]
- Журнал MCP: \[\[2026-05-04 MCP Skill Audit\]\]
- Источник связи: `shared-memory`
<!-- ARGOS_MEMORY_WEB:END -->

\[\[Backbone Hub\]\]

## Graph Bridge
- \[\[ARGOS Memory Web\]\]
- \[\[Backbone Hub\]\]
- \[\[Claude Hub\]\]

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_cloud_providers.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
