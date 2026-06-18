---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/pages-functions/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\pages-functions\README.md
source_ext: .md
source_sha256: b4a6202b468a3bdb07fcd0212f14dee0e55051ef954121c648d10cdd24c58129
text_sha256: 19474e50d4c3c5fda0184f62df8302aef0ba8a09999fc3111d8cb979aa280fd7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/pages-functions/README.md`
- Extract: `text`
- SHA256: `b4a6202b468a3bdb07fcd0212f14dee0e55051ef954121c648d10cdd24c58129`

## Content

# Cloudflare Pages Functions

Serverless functions on Cloudflare Pages using Workers runtime. Full-stack dev with file-based routing.

## Quick Navigation

**Need to...**
| Task | Go to |
|------|-------|
| Set up TypeScript types | [configuration.md](./configuration.md) - TypeScript Setup |
| Configure bindings (KV, D1, R2) | [configuration.md](./configuration.md) - wrangler.jsonc |
| Access request/env/params | [api.md](./api.md) - EventContext |
| Add middleware or auth | [patterns.md](./patterns.md) - Middleware, Auth |
| Background tasks (waitUntil) | [patterns.md](./patterns.md) - Background Tasks |
| Debug errors or check limits | [gotchas.md](./gotchas.md) - Common Errors, Limits |

## Decision Tree: Is This Pages Functions?

```
Need serverless backend? 
├─ Yes, for a static site → Pages Functions
├─ Yes, standalone API → Workers
└─ Just static hosting → Pages (no functions)

Have existing Worker?
├─ Complex routing logic → Use _worker.js (Advanced Mode)
└─ Simple routes → Migrate to /functions (File-Based)

Framework-based?
├─ Next.js/SvelteKit/Remix → Uses _worker.js automatically
└─ Vanilla/HTML/React SPA → Use /functions
```

## File-Based Routing

```
/functions
  ├── index.js              → /
  ├── api.js                → /api
  ├── users/
  │   ├── index.js          → /users/
  │   ├── [user].js         → /users/:user
  │   └── \[\[catchall\]\].js   → /users/*
  └── _middleware.js        → runs on all routes
```

**Rules:**
- `index.js` → directory root
- Trailing slash optional
- Specific routes precede catch-alls
- Falls back to static if no match

## Dynamic Routes

**Single segment** `[param]` → string:
```js
// /functions/users/[user].js
export function onRequest(context) {
  return new Response(`Hello ${context.params.user}`);
}
// Matches: /users/nevi
```

**Multi-segment** `\[\[param\]\]` → array:
```js
// /functions/users/\[\[catchall\]\].js
export function onRequest(context) {
  return new Response(JSON.stringify(context.params.catchall));
}
// Matches: /users/nevi/foobar → ["nevi", "foobar"]
```

## Key Features

- **Method handlers:** `onRequestGet`, `onRequestPost`, etc.
- **Middleware:** `_middleware.js` for cross-cutting concerns
- **Bindings:** KV, D1, R2, Durable Objects, Workers AI, Service bindings
- **TypeScript:** Full type support via `wrangler types` command
- **Advanced mode:** Use `_worker.js` for custom routing logic

## Reading Order

**New to Pages Functions?** Start here:
1. [README.md](./README.md) - Overview, routing, decision tree (you are here)
2. [configuration.md](./configuration.md) - TypeScript setup, wrangler.jsonc, bindings
3. [api.md](./api.md) - EventContext, handlers, bindings reference
4. [patterns.md](./patterns.md) - Middleware, auth, CORS, rate limiting, caching
5. [gotchas.md](./gotchas.md) - Common errors, debugging, limits

**Quick reference lookup:**
- Bindings table → [api.md](./api.md)
- Error diagnosis → [gotchas.md](./gotchas.md)
- TypeScript setup → [configuration.md](./configuration.md)

## See Also
- [pages](../pages/) - Pages platform overview and static site deployment
- [workers](../workers/) - Workers runtime API reference
- [d1](../d1/) - D1 database integration with Pages Functions

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
