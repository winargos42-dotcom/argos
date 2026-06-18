---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-gateway/features.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\ai-gateway\features.md
source_ext: .md
source_sha256: fbc10d9218c42415ce51179aa70918b8ad09690c94d8303f7dbdfd61ac1d4f98
text_sha256: efbc7d2d4464c1aab4881f059589439e2979b9967568878c32f7cb3e72cc6ccf
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# features.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-gateway/features.md`
- Extract: `text`
- SHA256: `fbc10d9218c42415ce51179aa70918b8ad09690c94d8303f7dbdfd61ac1d4f98`

## Content

# Features & Capabilities

## Caching

Dashboard: Settings → Cache Responses → Enable

```typescript
// Custom TTL (1 hour)
headers: { 'cf-aig-cache-ttl': '3600' }

// Skip cache
headers: { 'cf-aig-skip-cache': 'true' }

// Custom cache key
headers: { 'cf-aig-cache-key': 'greeting-en' }
```

**Limits:** TTL 60s - 30 days. **Does NOT work with streaming.**

## Rate Limiting

Dashboard: Settings → Rate-limiting → Enable

- **Fixed window:** Resets at intervals
- **Sliding window:** Rolling window (more accurate)
- Returns `429` when exceeded

## Guardrails

Dashboard: Settings → Guardrails → Enable

Filter prompts/responses for inappropriate content. Actions: Flag (log) or Block (reject).

## Data Loss Prevention (DLP)

Dashboard: Settings → DLP → Enable

Detect PII (emails, SSNs, credit cards). Actions: Flag, Block, or Redact.

## Billing Modes

| Mode | Description | Setup |
|------|-------------|-------|
| **Unified Billing** | Pay through Cloudflare, no provider keys | Use `cf-aig-authorization` header only |
| **BYOK** | Store provider keys in dashboard | Add keys in Provider Keys section |
| **Pass-through** | Send provider key with each request | Include provider's auth header |

## Zero Data Retention

Dashboard: Settings → Privacy → Zero Data Retention

No prompts/responses stored. Request counts and costs still tracked.

## Logging

Dashboard: Settings → Logs → Enable (up to 10M logs)

Each entry: prompt, response, provider, model, tokens, cost, duration, cache status, metadata.

```typescript
// Skip logging for request
headers: { 'cf-aig-collect-log': 'false' }
```

**Export:** Use Logpush to S3, GCS, Datadog, Splunk, etc.

## Custom Cost Tracking

For models not in Cloudflare's pricing database:

Dashboard: Gateway → Settings → Custom Costs

Or via API: set `model`, `input_cost`, `output_cost`.

## Supported Providers (22+)

| Provider | Unified API | Notes |
|----------|-------------|-------|
| OpenAI | `openai/gpt-4o` | Full support |
| Anthropic | `anthropic/claude-sonnet-4-5` | Full support |
| Google AI | `google-ai-studio/gemini-2.0-flash` | Full support |
| Workers AI | `workersai/@cf/meta/llama-3` | Native |
| Azure OpenAI | `azure-openai/*` | Deployment names |
| AWS Bedrock | Provider endpoint only | `/bedrock/*` |
| Groq | `groq/*` | Fast inference |
| Mistral, Cohere, Perplexity, xAI, DeepSeek, Cerebras | Full support | - |

## Best Practices

1. Enable caching for deterministic prompts
2. Set rate limits to prevent abuse
3. Use guardrails for user-facing AI
4. Enable DLP for sensitive data
5. Use unified billing or BYOK for simpler key management
6. Enable logging for debugging
7. Use zero data retention when privacy required

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
