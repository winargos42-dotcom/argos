# 2026-05-10 Аудит облачных AI провайдеров

## Тестирование (прямые API-вызовы)

| Провайдер | Статус | Модель | Контекст | Проблема |
|-----------|--------|--------|----------|----------|
| DeepSeek | ✅ Работает | deepseek-chat (V3) | 128k | — |
| OpenAI | ✅ Работает | gpt-4o-mini | 128k | Системная переменная OPENAI_API_KEY содержала ключ Kimi (override=True в main.py решает) |
| Ollama | ✅ Локальный | llama3.2:1b | — | ngrok туннель |
| Gemini | ❌ 5 ключей протухли | gemini-2.5-flash | 1M | API key expired (все 5) |
| Groq | ❌ Ключ невалидный | llama-3.3-70b | 128k | 401 Invalid API Key |
| Grok (xAI) | ❌ Нет доступа | grok-3-mini | 2M | 403 No permission |
| WatsonX | ❌ Лимит исчерпан | llama-3.3-70b | 128k | 429 consumption_limit_reached |
| GigaChat | ❌ Требуется оплата | GigaChat-2 | 32k | 402 Payment Required |
| Kimi | ❌ Таймаут | moonshot-v1 | 256k | Гео-блок из РФ (api.moonshot.cn недоступен) |
| Cloudflare | ❌ Нет токена | — | 256k | CLOUDFLARE_API_TOKEN отсутствует |
| YandexGPT | ❌ Нет токена | — | 32k | IAM_TOKEN не настроен |

## Что исправлено
- .env: убран LAPTOP MODE, включены рабочие провайдеры
- ARGOS_AI_PRIORITY="deepseek,openai"
- Нерабочие провайдеры отключены с комментариями причин
- TG-Bridge логи исключены из Obsidian RAG

## Что нужно для восстановления
- **Gemini**: перегенерировать API ключи на console.cloud.google.com
- **Groq**: новый ключ на console.groq.com
- **Grok**: проверить подписку xAI
- **WatsonX**: ждать сброса месячного лимита
- **GigaChat**: пополнить баланс на developers.sber.ru
- **Kimi**: нужен VPN/прокси для доступа из РФ

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
