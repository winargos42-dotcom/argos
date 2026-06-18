---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workerd/api.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\workerd\api.md
source_ext: .md
source_sha256: 2f184241ffebc876862f48d3a93aef14e1159c88d6105947d4a80aed339ebe73
text_sha256: 7a6652e76e27424b0ce0d7393e1a04595460290d44e5ca937e3b0090a3b61166
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# api.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workerd/api.md`
- Extract: `text`
- SHA256: `2f184241ffebc876862f48d3a93aef14e1159c88d6105947d4a80aed339ebe73`

## Content

# Workerd APIs

## Worker Code (JS/TS)

### ES Modules (Recommended)
```javascript
export default {
  async fetch(request, env, ctx) {
    const value = await env.KV.get("key");           // Bindings in env
    const response = await env.API.fetch(request);   // Service binding
    ctx.waitUntil(logRequest(request));              // Background task
    return new Response("OK");
  },
  async adminApi(request, env, ctx) { /* Named entrypoint */ },
  async queue(batch, env, ctx) { /* Queue consumer */ },
  async scheduled(event, env, ctx) { /* Cron handler */ }
};
```

### TypeScript Types

**Generate from wrangler.toml (Recommended):**
```bash
wrangler types  # Output: worker-configuration.d.ts
```

**Manual types:**
```typescript
interface Env {
  API: Fetcher;
  CACHE: KVNamespace;
  STORAGE: R2Bucket;
  ROOMS: DurableObjectNamespace;
  API_KEY: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return new Response(await env.CACHE.get("key"));
  }
};
```

**Setup:**
```bash
npm install -D @cloudflare/workers-types
```

```json
// tsconfig.json
{"compilerOptions": {"types": ["@cloudflare/workers-types"]}}
```

### Service Worker Syntax (Legacy)
```javascript
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const value = await KV.get("key");  // Bindings as globals
  return new Response("OK");
}
```

### Durable Objects
```javascript
export class Room {
  constructor(state, env) { this.state = state; this.env = env; }
  
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname === "/increment") {
      const value = (await this.state.storage.get("counter")) || 0;
      await this.state.storage.put("counter", value + 1);
      return new Response(String(value + 1));
    }
    return new Response("Not found", {status: 404});
  }
}
```

### RPC Between Services
```javascript
// Caller: env.AUTH.validateToken(token) returns structured data
const user = await env.AUTH.validateToken(request.headers.get("Authorization"));

// Callee: export methods that return data
export default {
  async validateToken(token) { return {id: 123, name: "Alice"}; }
};
```

## Web Platform APIs

### Fetch
- `fetch()`, `Request`, `Response`, `Headers`
- `AbortController`, `AbortSignal`

### Streams
- `ReadableStream`, `WritableStream`, `TransformStream`
- Byte streams, BYOB readers

### Web Crypto
- `crypto.subtle` (encrypt/decrypt/sign/verify)
- `crypto.randomUUID()`, `crypto.getRandomValues()`

### Encoding
- `TextEncoder`, `TextDecoder`
- `atob()`, `btoa()`

### Web Standards
- `URL`, `URLSearchParams`
- `Blob`, `File`, `FormData`
- `WebSocket`

### Server-Sent Events (EventSource)
```javascript
// Server-side SSE
const { readable, writable } = new TransformStream();
const writer = writable.getWriter();
writer.write(new TextEncoder().encode('data: Hello\n\n'));
return new Response(readable, {headers: {'Content-Type': 'text/event-stream'}});
```

### HTMLRewriter (HTML Parsing/Transformation)
```javascript
const response = await fetch('https://example.com');
return new HTMLRewriter()
  .on('a[href]', {
    element(el) {
      el.setAttribute('href', `/proxy?url=${encodeURIComponent(el.getAttribute('href'))}`);
    }
  })
  .on('script', { element(el) { el.remove(); } })
  .transform(response);
```

### TCP Sockets (Experimental)
```javascript
const socket = await connect({ hostname: 'example.com', port: 80 });
const writer = socket.writable.getWriter();
await writer.write(new TextEncoder().encode('GET / HTTP/1.1\r\n\r\n'));
const reader = socket.readable.getReader();
const { value } = await reader.read();
return new Response(value);
```

### Performance
- `performance.now()`, `performance.timeOrigin`
- `setTimeout()`, `setInterval()`, `queueMicrotask()`

### Console
- `console.log()`, `console.error()`, `console.warn()`

### Node.js Compat (`nodejs_compat` flag)
```javascript
import { Buffer } from 'node:buffer';
import { randomBytes } from 'node:crypto';

const buf = Buffer.from('Hello');
const random = randomBytes(16);
```

**Available:** `node:buffer`, `node:crypto`, `node:stream`, `node:util`, `node:events`, `node:assert`, `node:path`, `node:querystring`, `node:url`
**NOT available:** `node:fs`, `node:http`, `node:net`, `node:child_process`

## CLI Commands

```bash
workerd serve config.capnp [constantName]          # Start server
workerd serve config.capnp --socket-addr http=*:3000 --verbose
workerd compile config.capnp constantName -o binary  # Compile to binary
workerd test config.capnp [--test-only=test.js]    # Run tests
```

## Wrangler Integration

Use Wrangler for development:
```bash
wrangler dev     # Uses workerd internally
wrangler types   # Generate TypeScript types from wrangler.toml
```

See [patterns.md](./patterns.md) for usage examples, [configuration.md](./configuration.md) for config details.

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
