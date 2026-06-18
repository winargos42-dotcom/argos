# AI Providers — ARGOS Universal OS v2.1.3

## Provider Status (Updated)

| # | Provider | Status | RPM | Context | Notes |
|---|----------|--------|-----|---------|-------|
| 1 | OpenAI GPT-4o | ✅ Active | 60 | 128k | Primary provider |
| 2 | Grok (xAI) | ✅ Active | 60 | 128k | Secondary reasoning |
| 3 | Groq | ✅ Active | 30 | 32k | Fast inference |
| 4 | DeepSeek | ✅ Active | 15 | 128k | Deep reasoning |
| 5 | Gemini Flash | ✅ Active | 25 | 1M | 5 keys, 5 RPM each |
| 6 | GigaChat | ⏸️ Standby | 5 | 32k | Russian-specific |
| 7 | YandexGPT | ⏸️ Standby | 5 | 8k | Russian-specific |
| 8 | Kimi K2.5 | ✅ Active | 60 | 256k | api.moonshot.ai (global) |
| 9 | WatsonX | ⏸️ Standby | 5 | 8k | IBM Cloud |
| 10 | Cloudflare Workers | ✅ Active | 60 | 256k | kimi-k2.5 model |
| 11 | Azure OpenAI | ⏸️ Standby | 60 | 128k | Enterprise |
| 12 | Ollama (PC) | ✅ Active | ∞ | 32k | qwen2.5:7b, local |
| 13 | Ollama-Vision | 🔄 Setup | ∞ | — | llava:7b (pulling) |

## Active: 7/13 | Standby: 5/13 | Setup: 1/13

## Configuration
```env
# .env highlights
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_HOST=http://192.168.1.66:11434
OLLAMA_VISION_MODEL=llava:7b
ARGOS_DISABLE_GEMINI=0
ARGOS_DISABLE_DEEPSEEK=0
KIMI_API_BASE=https://api.moonshot.ai/v1
```

## Auto-Consensus Chain
```
OpenAI → Grok → Groq → DeepSeek → Gemini → GigaChat → YandexGPT → Kimi → WatsonX → Cloudflare → Azure → Ollama-SE → Ollama-JP → Ollama-AU → Ollama → HiveMind
```

---
#ai-providers #argos #configuration
