---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers-ai/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\workers-ai\gotchas.md
source_ext: .md
source_sha256: 8c86045c5d5e0bca5c4b9d256f175bcc3f58dd4c64fd2484853888d2e601b062
text_sha256: 10fe3b26750c2fc92ff6ccdefc1200352cdae88c573071cd7735d0a84ff925da
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers-ai/gotchas.md`
- Extract: `text`
- SHA256: `8c86045c5d5e0bca5c4b9d256f175bcc3f58dd4c64fd2484853888d2e601b062`

## Content

# Workers AI Gotchas

## Critical: @cloudflare/ai is DEPRECATED

```typescript
// ❌ WRONG - Don't install @cloudflare/ai
import Ai from '@cloudflare/ai';

// ✅ CORRECT - Use native binding
export default {
  async fetch(request: Request, env: Env) {
    await env.AI.run('@cf/meta/llama-3.1-8b-instruct', { messages: [...] });
  }
}
```

## Development

### "AI inference doesn't work locally"
```bash
# ❌ Local AI doesn't work
wrangler dev
# ✅ Use remote
wrangler dev --remote
```

### "env.AI is undefined"
Add binding to wrangler.jsonc:
```jsonc
{ "ai": { "binding": "AI" } }
```

## API Responses

### Embedding response shape varies
```typescript
// @cf/baai/bge-base-en-v1.5 returns: { data: \[\[0.1, 0.2, ...\]\] }
const embedding = response.data[0]; // Get first element
```

### Stream returns ReadableStream
```typescript
const stream = await env.AI.run(model, { messages: [...], stream: true });
for await (const chunk of stream) { console.log(chunk.response); }
```

## Rate Limits & Pricing

| Model Type | Neurons/Request |
|------------|-----------------|
| Small text (7B) | ~50-200 |
| Large text (70B) | ~500-2000 |
| Embeddings | ~5-20 |
| Image gen | ~10,000+ |

**Free tier**: 10,000 neurons/day

```typescript
// ❌ EXPENSIVE - 70B model
await env.AI.run('@cf/meta/llama-3.1-70b-instruct', ...);
// ✅ CHEAPER - Use smallest that works
await env.AI.run('@cf/meta/llama-3.1-8b-instruct', ...);
```

## Model-Specific

### Function calling
Only `@cf/meta/llama-3.1-*` and `mistral-7b-instruct-v0.2` support tools.

### Empty response
Check context limits (2K-8K tokens). Validate input structure.

### Inconsistent responses
Set `temperature: 0` for deterministic outputs.

### Cold start latency
First request: 1-3s. Use AI Gateway caching for frequent prompts.

## TypeScript

```typescript
interface Env {
  AI: Ai; // From @cloudflare/workers-types
}

interface TextGenerationResponse { response: string; }
interface EmbeddingResponse { data: number[][]; shape: number[]; }
```

## Common Errors

### 7502: Model not found
Check exact model name at developers.cloudflare.com/workers-ai/models/

### 7504: Input validation failed
```typescript
// Text gen requires messages array
await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [{ role: 'user', content: 'Hello' }]  // ✅
});

// Embeddings require text
await env.AI.run('@cf/baai/bge-base-en-v1.5', { text: 'Hello' });  // ✅
```

## Vercel AI SDK Integration

```typescript
import { openai } from '@ai-sdk/openai';
const model = openai('gpt-3.5-turbo', {
  baseURL: 'https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/ai/v1',
  headers: { Authorization: 'Bearer <API_TOKEN>' }
});
```

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
