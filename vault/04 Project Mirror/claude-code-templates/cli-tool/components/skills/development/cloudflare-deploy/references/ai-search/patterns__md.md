---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-search/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\ai-search\patterns.md
source_ext: .md
source_sha256: 7abe82a818df5dab634e23e53205dec970a06539e92618e12353461bed531c91
text_sha256: 1215875bf8a9e6317d31019a84a124aa7ba7e85bac10b92bc445d0ef7383d619
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-search/patterns.md`
- Extract: `text`
- SHA256: `7abe82a818df5dab634e23e53205dec970a06539e92618e12353461bed531c91`

## Content

# AI Search Patterns

## search() vs aiSearch()

| Use | Method | Returns |
|-----|--------|---------|
| Custom UI, analytics | `search()` | Raw chunks only (~100-300ms) |
| Chatbots, Q&A | `aiSearch()` | AI response + chunks (~500-2000ms) |

## rewrite_query

| Setting | Use When |
|---------|----------|
| `true` | User input (typos, vague queries) |
| `false` | LLM-generated queries (already optimized) |

## Multitenancy (Folder-Based)

```typescript
const answer = await env.AI.autorag("saas-docs").aiSearch({
  query: "refund policy",
  model: "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
  filters: {
    column: "folder",
    operator: "gte",  // "starts with" pattern
    value: `tenants/${tenantId}/`
  }
});
```

## Streaming

```typescript
const stream = await env.AI.autorag("docs").aiSearch({
  query, model: "@cf/meta/llama-3.3-70b-instruct-fp8-fast", stream: true
});
return new Response(stream, { headers: { "Content-Type": "text/event-stream" } });
```

## Score Threshold

| Threshold | Use |
|-----------|-----|
| 0.3 (default) | Broad recall, exploratory |
| 0.5 | Balanced, production default |
| 0.7 | High precision, critical accuracy |

## System Prompt Template

```typescript
const systemPrompt = `You are a documentation assistant.
- Answer ONLY based on provided context
- If context doesn't contain answer, say "I don't have information"
- Include code examples from context`;
```

## Compound Filters

```typescript
// OR: Multiple folders
filters: {
  operator: "or",
  filters: [
    { column: "folder", operator: "gte", value: "docs/api/" },
    { column: "folder", operator: "gte", value: "docs/auth/" }
  ]
}

// AND: Folder + date
filters: {
  operator: "and",
  filters: [
    { column: "folder", operator: "gte", value: "docs/" },
    { column: "timestamp", operator: "gte", value: oneWeekAgoSeconds }
  ]
}
```

## Reranking

Enable for high-stakes use cases (adds ~300ms latency):

```typescript
reranking: { enabled: true, model: "@cf/baai/bge-reranker-base" }
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
