# ARGOS Cluster Status — 2026-04-20

## Узлы кластера

| Узел | IP | VPN | ARGOS | Dashboard | Ollama модели | WireGuard |
|------|----|-----|-------|-----------|---------------|-----------|
| **LOCAL** | 127.0.0.1 | 10.8.0.2 | ✅ :8000 (Groq) | ✅ :8080 | qwen2.5:7b, llama3.2:1b, argos-v1, **tinyllama** ✅ | — |
| **JP1** | 40.81.208.101 | 10.8.0.4 | ✅ :8000 | ✅ :8080 | qwen2.5:3b, tinyllama, qwen2.5:1.5b | ✅ UP |
| **JP2** | 172.207.209.134 | 10.8.0.5 | ✅ :8000 | ✅ :8080 | qwen2.5:3b, tinyllama, qwen2.5:1.5b | ✅ UP |
| **AU** | 20.53.240.36 | 10.8.0.1 | ✅ :8000 | ✅ :8080 | tinyllama, deepseek-r1:1.5b, llama3.2:1b (+ qwen2.5:3b когда запущен) | ⚠️ Deallocated |
| **SE** | 20.240.192.35 | 10.8.0.6 | ❌ (Ollama-нода) | ❌ | qwen2.5:3b, phi4, deepseek-r1:7b | ✅ UP |

*tinyllama на LOCAL: скачивается; qwen2.5:3b на AU: скачивается

## SE VM — OpenClaw Gateway

- **Статус:** ✅ Running на порту 18789
- **Плагины:** acpx, browser, **kimi-claw** ✅
- **Config:** `/root/.openclaw/openclaw.json`
- **Autostart:** `systemctl enable openclaw-gateway`
- **kimi-claw token:** `km_b_prod_mbp22gfR4yQkfz70yb7VFlix9VhwGClV`
- **Gateway token:** `claw_11abb93d2efee16138b2cc96e57721fc`

## WireGuard Mesh (hub-and-spoke)

- **Hub:** AU (10.8.0.1), wg-easy Docker на AU, порт 51820
- **VPN домен:** `vpn.argosssss.win:51820`
- **Clients:** LOCAL (10.8.0.2), JP1 (10.8.0.4), JP2 (10.8.0.5), SE (10.8.0.6)

## Azure OpenAI

- **Endpoint:** `https://argoss-sig-2026.openai.azure.com/`
- **Deployment:** `argos-gpt4` (модель: gpt-5.1-2025-11-13)
- **Env:** `AZURE_DEPLOYMENT_NAME=argos-gpt4`, `AZURE_OPENAI_MODEL=argos-gpt4`
- **Fix в core.py:** `max_completion_tokens` для gpt-5.x (вместо `max_tokens`)

## Провайдеры (статус .env)

| Провайдер | Статус | Примечание |
|-----------|--------|------------|
| Groq | ✅ Активен | `GROQ_API_KEY` задан |
| Azure OpenAI | ✅ Исправлен | deployment: argos-gpt4 |
| OpenAI | ✅ | gpt-4o-mini |
| DeepSeek | ✅ | deepseek-chat |
| WatsonX | ✅ | IBM Cloud IAM, 429 = rate limit (OK) |
| Kimi | ⏸ Отключён | `ARGOS_DISABLE_KIMI=1` (rate limit 20.04) |
| OpenClaw | ⏸ Отключён | `ARGOS_DISABLE_OPENCLAW=1` (rate limit 20.04) |
| xAI/Grok | ⏸ Отключён | `ARGOS_DISABLE_GROK=1` (кредиты исчерпаны) |
| Anthropic | ⚠️ Нет ключа | `ANTHROPIC_API_KEY=` — нужно заполнить |
| Cloudflare AI | ✅ | kimi-k2.5 |
| HuggingFace | ✅ | |
| GigaChat | ✅ | `ARGOS_DISABLE_GIGACHAT=0` |
| Ollama LOCAL | ✅ | qwen2.5:7b главная, llama3.2:1b fast |

## Изменения в коде (этот сеанс)

### src/core.py
- `_ask_azure_openai()`: `deploy` читается из `AZURE_DEPLOYMENT_NAME` || `AZURE_OPENAI_MODEL` (fallback `argos-gpt4`)
- `_ask_azure_openai()`: gpt-5.x использует `max_completion_tokens` вместо `max_tokens`

### src/awa_core.py
- `OLLAMA_FAST_MODEL` default: `tinyllama` → `llama3.2:1b`

### src/interface/web_engine.py
- **ПОЛНАЯ ПЕРЕЗАПИСЬ** — Cluster Dashboard v2.1
- 5 нод в реальном времени через `/api/cluster`
- Tabs: Кластер, Консоль, WireGuard, Метрики

### .env
- `AZURE_OPENAI_MODEL=argos-gpt4` (было gpt-4o)
- `AZURE_DEPLOYMENT_NAME=argos-gpt4` (добавлено)
- `ANTHROPIC_API_KEY=` (placeholder, нужно заполнить)
- `OLLAMA_JP2_HOST=http://172.207.209.134:11434` (добавлено)
- `OLLAMA_FAST_MODEL=llama3.2:1b` (было qwen2.5:3b — не было локально)

## Требует действия

1. **ANTHROPIC_API_KEY** — добавить ключ: https://console.anthropic.com → API Keys
2. **xAI кредиты** — пополнить: https://console.x.ai (Grok отключён до пополнения)
3. **Kimi rate-limit** — снимется само, убрать `ARGOS_DISABLE_KIMI=1` когда пройдёт
4. **OpenClaw local** — OpenClaw на LOCAL не запущен (порт 47392 неактивен)
