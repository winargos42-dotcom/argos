# AI Providers

## Active (7/12)
| Provider | Model | RPM | Context | Status |
|----------|-------|-----|---------|--------|
| DeepSeek | V3 / R1 | 15 | 128k | Active |
| Gemini | 2.5 Flash | 25 | 1M | Active |
| Grok | xAI | 60 | 2M | Active |
| OpenAI | GPT-4o | 3 | 128k | Active |
| Kimi | K2.5 | 60 | 256k | Active |
| WatsonX | IBM Lite | 120 | 128k | Active |
| Ollama | Local 3-GPU | unlimited | varies | Active |

## Pending Keys
| Provider | Model | RPM | Context | Status |
|----------|-------|-----|---------|--------|
| GigaChat | Sber | 60 | 32k | Key needed |
| YandexGPT | Lite | 300/h | 32k | Key needed |
| Groq | Llama 3 / Mixtral | 30 | 128k | Key needed |
| Cloudflare | Workers AI | 60 | 256k | Key needed |
| Ollama Fast | Reflector | - | 2k | Config needed |

## Failover Order
1. Ollama local (fastest, free)
2. Gemini Flash (7500 RPD, largest context)
3. Grok (60 RPM, 2M context)
4. DeepSeek (128k context)
5. Kimi (256k context)
6. OpenAI (limited RPM)
7. WatsonX (300k tokens/month)

#providers #ai #failover
