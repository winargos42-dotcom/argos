---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/react-best-practices/rules/server-cache-lru.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\react-best-practices\rules\server-cache-lru.md
source_ext: .md
source_sha256: 19d844eebd1fb7ef5f43f4d1e85baf1fc0160547400ab838ba4d40226eb891b9
text_sha256: 1924b64561841923b88a657085097a0aeba3e0ba2d5470b9f5c15cc10d6ae70f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:46
---

# server-cache-lru.md

- Source: `claude-code-templates/cli-tool/components/skills/development/react-best-practices/rules/server-cache-lru.md`
- Extract: `text`
- SHA256: `19d844eebd1fb7ef5f43f4d1e85baf1fc0160547400ab838ba4d40226eb891b9`

## Content

---
title: Cross-Request LRU Caching
impact: HIGH
impactDescription: caches across requests
tags: server, cache, lru, cross-request
---

## Cross-Request LRU Caching

`React.cache()` only works within one request. For data shared across sequential requests (user clicks button A then button B), use an LRU cache.

**Implementation:**

```typescript
import { LRUCache } from 'lru-cache'

const cache = new LRUCache<string, any>({
  max: 1000,
  ttl: 5 * 60 * 1000  // 5 minutes
})

export async function getUser(id: string) {
  const cached = cache.get(id)
  if (cached) return cached

  const user = await db.user.findUnique({ where: { id } })
  cache.set(id, user)
  return user
}

// Request 1: DB query, result cached
// Request 2: cache hit, no DB query
```

Use when sequential user actions hit multiple endpoints needing the same data within seconds.

**With Vercel's [Fluid Compute](https://vercel.com/docs/fluid-compute):** LRU caching is especially effective because multiple concurrent requests can share the same function instance and cache. This means the cache persists across requests without needing external storage like Redis.

**In traditional serverless:** Each invocation runs in isolation, so consider Redis for cross-process caching.

Reference: [https://github.com/isaacs/node-lru-cache](https://github.com/isaacs/node-lru-cache)

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
