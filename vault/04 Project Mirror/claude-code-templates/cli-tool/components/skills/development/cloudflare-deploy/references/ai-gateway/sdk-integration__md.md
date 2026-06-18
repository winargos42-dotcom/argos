---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-gateway/sdk-integration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\ai-gateway\sdk-integration.md
source_ext: .md
source_sha256: 3ffba25aa166dd8f687f37c588a82f9a6a71cc00d53e10124c0d8ed3375e6579
text_sha256: 3633951a1ea8f419d85059dfb98f23e830805f728b516d7d87d1fa11ef9d9101
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# sdk-integration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-gateway/sdk-integration.md`
- Extract: `text`
- SHA256: `3ffba25aa166dd8f687f37c588a82f9a6a71cc00d53e10124c0d8ed3375e6579`

## Content

# AI Gateway SDK Integration

## Vercel AI SDK (Recommended)

```typescript
import { createAiGateway } from 'ai-gateway-provider';
import { createOpenAI } from '@ai-sdk/openai';
import { generateText } from 'ai';

const gateway = createAiGateway({
  accountId: process.env.CF_ACCOUNT_ID,
  gateway: process.env.CF_GATEWAY_ID,
  apiKey: process.env.CF_API_TOKEN // Optional for auth gateways
});

const openai = createOpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Single model
const { text } = await generateText({
  model: gateway(openai('gpt-4o')),
  prompt: 'Hello'
});

// Automatic fallback array
const { text } = await generateText({
  model: gateway([
    openai('gpt-4o'),
    anthropic('claude-sonnet-4-5'),
    openai('gpt-4o-mini')
  ]),
  prompt: 'Complex task'
});
```

### Options

```typescript
model: gateway(openai('gpt-4o'), {
  cacheKey: 'my-key',
  cacheTtl: 3600,
  metadata: { userId: 'u123', team: 'eng' }, // Max 5 entries
  retries: { maxAttempts: 3, backoff: 'exponential' }
})
```

## OpenAI SDK

```typescript
const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: `https://gateway.ai.cloudflare.com/v1/${accountId}/${gatewayId}/openai`,
  defaultHeaders: { 'cf-aig-authorization': `Bearer ${cfToken}` }
});

// Unified API - switch providers via model name
model: 'openai/gpt-4o'  // or 'anthropic/claude-sonnet-4-5'
```

## Anthropic SDK

```typescript
const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
  baseURL: `https://gateway.ai.cloudflare.com/v1/${accountId}/${gatewayId}/anthropic`,
  defaultHeaders: { 'cf-aig-authorization': `Bearer ${cfToken}` }
});
```

## Workers AI Binding

```toml
# wrangler.toml
[ai]
binding = "AI"
\[\[ai.gateway\]\]
id = "my-gateway"
```

```typescript
await env.AI.run('@cf/meta/llama-3-8b-instruct', 
  { messages: [...] },
  { gateway: { id: 'my-gateway', metadata: { userId: '123' } } }
);
```

## LangChain / LlamaIndex

```typescript
// Use OpenAI SDK pattern with custom baseURL
new ChatOpenAI({
  configuration: {
    baseURL: `https://gateway.ai.cloudflare.com/v1/${accountId}/${gatewayId}/openai`
  }
});
```

## HTTP / cURL

```bash
curl https://gateway.ai.cloudflare.com/v1/{account}/{gateway}/openai/chat/completions \
  -H "Authorization: Bearer $OPENAI_KEY" \
  -H "cf-aig-authorization: Bearer $CF_TOKEN" \
  -H "cf-aig-metadata: {\"userId\":\"123\"}" \
  -d '{"model":"gpt-4o","messages":[...]}'
```

## Headers Reference

| Header | Purpose |
|--------|---------|
| `cf-aig-authorization` | Gateway auth token |
| `cf-aig-metadata` | JSON object (max 5 keys) |
| `cf-aig-cache-ttl` | Cache TTL in seconds |
| `cf-aig-skip-cache` | `true` to bypass cache |

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
