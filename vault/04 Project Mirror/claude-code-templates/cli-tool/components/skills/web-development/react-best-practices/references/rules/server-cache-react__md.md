---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-development/react-best-practices/references/rules/server-cache-react.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-development\react-best-practices\references\rules\server-cache-react.md
source_ext: .md
source_sha256: c56625f6ba3404dee7c07f72d935ccc897f0f086432ada5a28a4532f47999031
text_sha256: 56b75e081aaaea192effc4127b879a6a83f880585ee85f8fab0a9dece13a650b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# server-cache-react.md

- Source: `claude-code-templates/cli-tool/components/skills/web-development/react-best-practices/references/rules/server-cache-react.md`
- Extract: `text`
- SHA256: `c56625f6ba3404dee7c07f72d935ccc897f0f086432ada5a28a4532f47999031`

## Content

---
title: Per-Request Deduplication with React.cache()
impact: HIGH
impactDescription: deduplicates within request
tags: server, cache, react-cache, deduplication
---

## Per-Request Deduplication with React.cache()

Use `React.cache()` for server-side request deduplication. Authentication and database queries benefit most.

**Usage:**

```typescript
import { cache } from 'react'

export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({
    where: { id: session.user.id }
  })
})
```

Within a single request, multiple calls to `getCurrentUser()` execute the query only once.

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
