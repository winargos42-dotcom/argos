# Kimi K2.5 Agent

## Identity
- **Name**: Kimi Agent
- **Type**: AI Provider / AutoGPT Entity
- **Model**: kimi-k2.6 (Moonshot AI)
- **Status**: ✅ Active
- **API**: https://api.moonshot.ai/v1 (global)
- **RPM**: 60 | **Context**: 256k tokens

## Capabilities
- Long-context reasoning (256k tokens)
- Tool calling (ARGOS skills integration)
- Multi-turn dialogue with memory

## Configuration
```env
KIMI_API_KEY=sk-e9hN...
ARGOS_DISABLE_KIMI=0
ARGOS_KIMI_TOOLS=1
```

## Integration
- Uses `KimiBridge` + `KimiToolCalling` for skill dispatch
- Provider chain position: After YandexGPT, before Cloudflare

---
#autogpt #kimi #agent #ai-provider
