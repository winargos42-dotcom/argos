---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers-ai/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\workers-ai\patterns.md
source_ext: .md
source_sha256: 2018af7eba96ef5892b2ceda9cbb766fdfe7307f474b83e6a3ab8f53c462eeb1
text_sha256: 1ebfd949690bd1e8150435c1bd1bf7b5cd3e6ab35eec5442f7af8bf39ea80198
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers-ai/patterns.md`
- Extract: `text`
- SHA256: `2018af7eba96ef5892b2ceda9cbb766fdfe7307f474b83e6a3ab8f53c462eeb1`

## Content

# Workers AI Patterns

## RAG (Retrieval-Augmented Generation)

```typescript
// 1. Embed query
const embedding = await env.AI.run('@cf/baai/bge-base-en-v1.5', { text: query });

// 2. Search vectors
const results = await env.VECTORIZE.query(embedding.data[0], {
  topK: 5, returnMetadata: true
});

// 3. Build context
const context = results.matches.map(m => m.metadata?.text).join('\n\n');

// 4. Generate with context
const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [
    { role: 'system', content: `Answer based on:\n\n${context}` },
    { role: 'user', content: query }
  ]
});
```

## Streaming (SSE)

```typescript
const stream = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages, stream: true
});

const { readable, writable } = new TransformStream();
const writer = writable.getWriter();

(async () => {
  for await (const chunk of stream) {
    await writer.write(new TextEncoder().encode(`data: ${JSON.stringify(chunk)}\n\n`));
  }
  await writer.write(new TextEncoder().encode('data: [DONE]\n\n'));
  await writer.close();
})();

return new Response(readable, {
  headers: { 'Content-Type': 'text/event-stream' }
});
```

## Error Handling & Retry

```typescript
async function runWithRetry(env, model, input, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await env.AI.run(model, input);
    } catch (error) {
      if (error.message?.includes('7505') && attempt < maxRetries - 1) {
        await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 1000));
        continue;
      }
      throw error;
    }
  }
}
```

## Model Fallback

```typescript
try {
  return await env.AI.run('@cf/meta/llama-3.1-70b-instruct', { messages });
} catch {
  return await env.AI.run('@cf/meta/llama-3.1-8b-instruct', { messages });
}
```

## Prompt Patterns

```typescript
// System prompts
const PROMPTS = {
  json: 'Respond with valid JSON only.',
  concise: 'Keep responses brief.',
  cot: 'Think step by step before answering.'
};

// Few-shot
messages: [
  { role: 'system', content: 'Extract as JSON' },
  { role: 'user', content: 'John bought 3 apples for $5' },
  { role: 'assistant', content: '{"name":"John","item":"apples","qty":3}' },
  { role: 'user', content: actualInput }
]
```

## Parallel Execution

```typescript
const [sentiment, summary, embedding] = await Promise.all([
  env.AI.run('@cf/mistral/mistral-7b-instruct-v0.1', { messages: sentimentPrompt }),
  env.AI.run('@cf/meta/llama-3.1-8b-instruct', { messages: summaryPrompt }),
  env.AI.run('@cf/baai/bge-base-en-v1.5', { text })
]);
```

## Cost Optimization

| Task | Model | Neurons |
|------|-------|---------|
| Classify | `@cf/mistral/mistral-7b-instruct-v0.1` | ~50 |
| Chat | `@cf/meta/llama-3.1-8b-instruct` | ~200 |
| Complex | `@cf/meta/llama-3.1-70b-instruct` | ~2000 |
| Embed | `@cf/baai/bge-base-en-v1.5` | ~10 |

```typescript
// Batch embeddings
const response = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
  text: textsArray // Process multiple at once
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
