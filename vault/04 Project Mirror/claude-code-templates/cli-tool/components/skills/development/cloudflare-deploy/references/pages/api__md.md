---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/pages/api.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\pages\api.md
source_ext: .md
source_sha256: 6a6ad86447aeff766c4cac209a4a4da077339d3ec265e6c38ab036bae1a344d2
text_sha256: 90989f928df3e394e9bc9587ac4eda172bf3735a338a0b1f6edba4d6af3a2652
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# api.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/pages/api.md`
- Extract: `text`
- SHA256: `6a6ad86447aeff766c4cac209a4a4da077339d3ec265e6c38ab036bae1a344d2`

## Content

# Functions API

## File-Based Routing

```
/functions/index.ts              → example.com/
/functions/api/users.ts          → example.com/api/users
/functions/api/users/[id].ts     → example.com/api/users/:id
/functions/api/users/\[\[path\]\].ts → example.com/api/users/* (catchall)
/functions/_middleware.ts        → Runs before all routes
```

**Rules**: `[param]` = single segment, `\[\[param\]\]` = multi-segment catchall, more specific wins.

## Request Handlers

```typescript
import type { PagesFunction } from '@cloudflare/workers-types';

interface Env {
  DB: D1Database;
  KV: KVNamespace;
}

// All methods
export const onRequest: PagesFunction<Env> = async (context) => {
  return new Response('All methods');
};

// Method-specific
export const onRequestGet: PagesFunction<Env> = async (context) => {
  const { request, env, params, data } = context;
  
  const user = await env.DB.prepare(
    'SELECT * FROM users WHERE id = ?'
  ).bind(params.id).first();
  
  return Response.json(user);
};

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const body = await context.request.json();
  return Response.json({ success: true });
};

// Also: onRequestPut, onRequestPatch, onRequestDelete, onRequestHead, onRequestOptions
```

## Context Object

```typescript
interface EventContext<Env, Params, Data> {
  request: Request;              // HTTP request
  env: Env;                      // Bindings (KV, D1, R2, etc.)
  params: Params;                // Route parameters
  data: Data;                    // Middleware-shared data
  waitUntil: (promise: Promise<any>) => void;  // Background tasks
  next: () => Promise<Response>; // Next handler
  passThroughOnException: () => void;  // Error fallback (not in advanced mode)
}
```

## Dynamic Routes

```typescript
// Single segment: functions/users/[id].ts
export const onRequestGet: PagesFunction = async ({ params }) => {
  // /users/123 → params.id = "123"
  return Response.json({ userId: params.id });
};

// Multi-segment: functions/files/\[\[path\]\].ts
export const onRequestGet: PagesFunction = async ({ params }) => {
  // /files/docs/api/v1.md → params.path = ["docs", "api", "v1.md"]
  const filePath = (params.path as string[]).join('/');
  return new Response(filePath);
};
```

## Middleware

```typescript
// functions/_middleware.ts
// Single
export const onRequest: PagesFunction = async (context) => {
  const response = await context.next();
  response.headers.set('X-Custom-Header', 'value');
  return response;
};

// Chained (runs in order)
const errorHandler: PagesFunction = async (context) => {
  try {
    return await context.next();
  } catch (err) {
    return new Response(err.message, { status: 500 });
  }
};

const auth: PagesFunction = async (context) => {
  const token = context.request.headers.get('Authorization');
  if (!token) return new Response('Unauthorized', { status: 401 });
  context.data.userId = await verifyToken(token);
  return context.next();
};

export const onRequest = [errorHandler, auth];
```

**Scope**: `functions/_middleware.ts` → all; `functions/api/_middleware.ts` → `/api/*` only

## Bindings Usage

```typescript
export const onRequestGet: PagesFunction<Env> = async ({ env }) => {
  // KV
  const cached = await env.KV.get('key', 'json');
  await env.KV.put('key', JSON.stringify({data: 'value'}), {expirationTtl: 3600});
  
  // D1
  const result = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(userId).first();
  
  // R2, Queue, AI - see respective reference docs
  
  return Response.json({success: true});
};
```

## Advanced Mode

Full Workers API, bypasses file-based routing:

```javascript
// functions/_worker.js
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Custom routing
    if (url.pathname.startsWith('/api/')) {
      return new Response('API response');
    }
    
    // REQUIRED: Serve static assets
    return env.ASSETS.fetch(request);
  }
};
```

**When to use**: WebSockets, complex routing, scheduled handlers, email handlers.

## Smart Placement

Automatically optimizes function execution location based on traffic patterns.

**Configuration** (in wrangler.jsonc):
```jsonc
{
  "placement": {
    "mode": "smart"  // Enables optimization (default: off)
  }
}
```

**How it works**: Analyzes traffic patterns over time and places functions closer to users or data sources (e.g., D1 databases). Requires no code changes.

**Trade-offs**: Initial requests may see slightly higher latency during learning period (hours-days). Performance improves as system optimizes.

**When to use**: Global apps with centralized databases or geographically concentrated traffic sources.

## getRequestContext (Framework SSR)

Access bindings in framework code:

```typescript
// SvelteKit
import type { RequestEvent } from '@sveltejs/kit';
export async function load({ platform }: RequestEvent) {
  const data = await platform.env.DB.prepare('SELECT * FROM users').all();
  return { users: data.results };
}

// Astro
const { DB } = Astro.locals.runtime.env;
const data = await DB.prepare('SELECT * FROM users').all();

// Solid Start (server function)
import { getRequestEvent } from 'solid-js/web';
const event = getRequestEvent();
const data = await event.locals.runtime.env.DB.prepare('SELECT * FROM users').all();
```

**✅ Supported adapters** (2026):
- **SvelteKit**: `@sveltejs/adapter-cloudflare`
- **Astro**: Built-in Cloudflare adapter
- **Nuxt**: Set `nitro.preset: 'cloudflare-pages'` in `nuxt.config.ts`
- **Qwik**: Built-in Cloudflare adapter
- **Solid Start**: `@solidjs/start-cloudflare-pages`

**❌ Deprecated/Unsupported**:
- **Next.js**: Official adapter (`@cloudflare/next-on-pages`) deprecated. Use Vercel or self-host on Workers.
- **Remix**: Official adapter (`@remix-run/cloudflare-pages`) deprecated. Migrate to supported frameworks.

See [gotchas.md](./gotchas.md#framework-specific) for migration guidance.

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
