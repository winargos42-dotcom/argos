---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-development/react-best-practices/references/rules/js-cache-storage.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-development\react-best-practices\references\rules\js-cache-storage.md
source_ext: .md
source_sha256: 8e359202442e238d4cc0c45b9eb82df94e69e13d1a478f7b659db1217611d625
text_sha256: dfbe43c55d1973e7cf456cfa6978f6f09f57c3fd1d5e7fd09ba9d4708c472b8e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# js-cache-storage.md

- Source: `claude-code-templates/cli-tool/components/skills/web-development/react-best-practices/references/rules/js-cache-storage.md`
- Extract: `text`
- SHA256: `8e359202442e238d4cc0c45b9eb82df94e69e13d1a478f7b659db1217611d625`

## Content

---
title: Cache Storage API Calls
impact: LOW-MEDIUM
impactDescription: reduces expensive I/O
tags: javascript, localStorage, storage, caching, performance
---

## Cache Storage API Calls

`localStorage`, `sessionStorage`, and `document.cookie` are synchronous and expensive. Cache reads in memory.

**Incorrect (reads storage on every call):**

```typescript
function getTheme() {
  return localStorage.getItem('theme') ?? 'light'
}
// Called 10 times = 10 storage reads
```

**Correct (Map cache):**

```typescript
const storageCache = new Map<string, string | null>()

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key))
  }
  return storageCache.get(key)
}

function setLocalStorage(key: string, value: string) {
  localStorage.setItem(key, value)
  storageCache.set(key, value)  // keep cache in sync
}
```

Use a Map (not a hook) so it works everywhere: utilities, event handlers, not just React components.

**Cookie caching:**

```typescript
let cookieCache: Record<string, string> | null = null

function getCookie(name: string) {
  if (!cookieCache) {
    cookieCache = Object.fromEntries(
      document.cookie.split('; ').map(c => c.split('='))
    )
  }
  return cookieCache[name]
}
```

**Important:** If storage can change externally (another tab, server-set cookies), invalidate cache:

```typescript
window.addEventListener('storage', (e) => {
  if (e.key) storageCache.delete(e.key)
})

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    storageCache.clear()
  }
})
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
