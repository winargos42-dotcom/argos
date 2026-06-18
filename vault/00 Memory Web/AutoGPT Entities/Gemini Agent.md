# Gemini Agent

## Identity
- **Name**: Gemini Flash
- **Type**: AI Provider / AutoGPT Entity
- **Model**: gemini-2.5-flash
- **Status**: ✅ Active (5 keys × 5 RPM = 25 RPM)
- **Context**: 1M tokens

## Capabilities
- Largest context window (1M tokens)
- Multi-modal (text + images)
- 7,500 RPD across 5 API keys

## Configuration
```env
GEMINI_API_KEY_0..4=AIzaSy...
GEMINI_RPM_PER_KEY=5
ARGOS_DISABLE_GEMINI=0
```

## Key Pool
- 5 API keys rotating automatically
- Rate limit: 5 RPM per key = 25 RPM total
- Fallback position: Primary cloud provider

---
#autogpt #gemini #agent #ai-provider
