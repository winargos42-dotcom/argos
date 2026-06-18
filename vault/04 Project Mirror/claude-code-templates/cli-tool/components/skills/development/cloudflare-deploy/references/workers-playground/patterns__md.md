---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers-playground/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\workers-playground\patterns.md
source_ext: .md
source_sha256: af952e98983a3a300376317a79edc9026158639c7065f814fcd5b48721987b33
text_sha256: c95d27741ecccbad12386ff4fa9dae6c8ff21438bf83f3edfd177ec156a8da69
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers-playground/patterns.md`
- Extract: `text`
- SHA256: `af952e98983a3a300376317a79edc9026158639c7065f814fcd5b48721987b33`

## Content

# Workers Playground Patterns

## JSON API

```javascript
export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname === '/api/hello') return Response.json({ message: 'Hello' });
    if (url.pathname === '/api/echo' && request.method === 'POST') {
      return Response.json({ received: await request.json() });
    }
    return Response.json({ error: 'Not found' }, { status: 404 });
  }
};
```

## Router Pattern

```javascript
const routes = {
  '/': () => new Response('Home'),
  '/api/users': () => Response.json([{ id: 1, name: 'Alice' }])
};

export default {
  async fetch(request) {
    const handler = routes[new URL(request.url).pathname];
    return handler ? handler() : new Response('Not Found', { status: 404 });
  }
};
```

## Proxy Pattern

```javascript
export default {
  async fetch(request) {
    const url = new URL(request.url);
    url.hostname = 'api.example.com';
    return fetch(url.toString(), {
      method: request.method, headers: request.headers, body: request.body
    });
  }
};
```

## CORS Handling

```javascript
export default {
  async fetch(request) {
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }
      });
    }
    const response = await fetch('https://api.example.com', request);
    const modified = new Response(response.body, response);
    modified.headers.set('Access-Control-Allow-Origin', '*');
    return modified;
  }
};
```

## Caching

```javascript
export default {
  async fetch(request) {
    if (request.method !== 'GET') return fetch(request);
    const cache = caches.default;
    let response = await cache.match(request);
    if (!response) {
      response = await fetch('https://api.example.com');
      if (response.status === 200) await cache.put(request, response.clone());
    }
    return response;
  }
};
```

## Hono Framework

```javascript
import { Hono } from 'https://esm.sh/hono@3';
const app = new Hono();
app.get('/', (c) => c.text('Hello'));
app.get('/api/users/:id', (c) => c.json({ id: c.req.param('id') }));
app.notFound((c) => c.json({ error: 'Not found' }, 404));
export default app;
```

## Authentication

```javascript
export default {
  async fetch(request) {
    const auth = request.headers.get('Authorization');
    if (!auth?.startsWith('Bearer ')) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }
    const token = auth.substring(7);
    if (token !== 'secret-token') {
      return Response.json({ error: 'Invalid token' }, { status: 403 });
    }
    return Response.json({ message: 'Authenticated' });
  }
};
```

## Error Handling

```javascript
export default {
  async fetch(request) {
    try {
      const response = await fetch('https://api.example.com');
      if (!response.ok) throw new Error(`API returned ${response.status}`);
      return response;
    } catch (error) {
      return Response.json({ error: error.message }, { status: 500 });
    }
  }
};
```

**Note:** In-memory state (Maps, variables) resets on Worker cold start. Use Durable Objects or KV for persistence.

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
