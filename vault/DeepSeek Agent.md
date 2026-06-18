# DeepSeek Agent

## Identity
- **Name**: DeepSeek Agent
- **Type**: AI Provider / AutoGPT Entity
- **Model**: deepseek-chat (DeepSeek V3 / R1)
- **Status**: ✅ Active
- **API**: https://api.deepseek.com/v1
- **RPM**: 15 | **Context**: 128k tokens

## Capabilities
- General-purpose chat and reasoning
- Code generation and analysis
- Mathematical problem solving
- Multi-step task planning

## Configuration
```env
DEEPSEEK_API_KEY=sk-d5ef4313...
DEEPSEEK_MODEL=deepseek-chat
ARGOS_DISABLE_DEEPSEEK=0
```

## Integration
- Provider chain position: After OpenAI/Grok, before Ollama fallback
- Used via `_ask_openai_compat(provider_name="DeepSeek")`

---
#autogpt #deepseek #agent #ai-provider
