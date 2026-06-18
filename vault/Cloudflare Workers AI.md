# Cloudflare Workers AI Agent

## Identity
- **Name**: CF Workers AI
- **Type**: AI Provider / AutoGPT Entity
- **Model**: @cf/moonshotai/kimi-k2.5
- **Status**: ✅ Active
- **API**: Cloudflare Workers AI (Edge)
- **RPM**: 60 | **Context**: 256k tokens

## Capabilities
- Edge inference with low latency
- Reasoning model (kimi-k2.5)
- Fallback for other providers

## Configuration
```env
CLOUDFLARE_API_TOKEN=cfat_xXNs...
CLOUDFLARE_ACCOUNT_ID=19ee18f...
ARGOS_DISABLE_CLOUDFLARE=0
```

## Integration
- Uses `_ask_openai_compat(provider_name="Cloudflare")`
- Provider chain position: After Kimi, before Azure OpenAI

---
#autogpt #cloudflare #agent #ai-provider
