---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers-for-platforms/api.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\workers-for-platforms\api.md
source_ext: .md
source_sha256: d9d5608c611d7895f3994e2a30b20260d2dd343f79ebe500ade2a6f733cccb5c
text_sha256: 6bc581bf87e21dd9764b88e7658b8cce841491943bd67b0ab8c37e1fcb2b9835
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# api.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers-for-platforms/api.md`
- Extract: `text`
- SHA256: `d9d5608c611d7895f3994e2a30b20260d2dd343f79ebe500ade2a6f733cccb5c`

## Content

# API Operations

## Deploy User Worker

```bash
curl -X PUT \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/workers/dispatch/namespaces/$NAMESPACE/scripts/$SCRIPT_NAME" \
  -H "Authorization: Bearer $API_TOKEN" \
  -F 'metadata={"main_module": "worker.mjs"};type=application/json' \
  -F 'worker.mjs=@worker.mjs;type=application/javascript+module'
```

### TypeScript SDK
```typescript
import Cloudflare from "cloudflare";

const client = new Cloudflare({ apiToken: process.env.API_TOKEN });

const scriptFile = new File([scriptContent], `${scriptName}.mjs`, {
  type: "application/javascript+module",
});

await client.workersForPlatforms.dispatch.namespaces.scripts.update(
  namespace, scriptName,
  {
    account_id: accountId,
    metadata: { main_module: `${scriptName}.mjs` },
    files: [scriptFile],
  }
);
```

## TypeScript Types

```typescript
import type { DispatchNamespace } from '@cloudflare/workers-types';

interface DispatchNamespace {
  get(name: string, options?: Record<string, unknown>, dispatchOptions?: DynamicDispatchOptions): Fetcher;
}

interface DynamicDispatchOptions {
  limits?: DynamicDispatchLimits;
  outbound?: Record<string, unknown>;
}

interface DynamicDispatchLimits {
  cpuMs?: number;        // Max CPU milliseconds
  subRequests?: number;  // Max fetch() calls
}

// Usage
const userWorker = env.DISPATCHER.get('customer-123', {}, {
  limits: { cpuMs: 50, subRequests: 20 },
  outbound: { customerId: '123', url: request.url }
});
```

## Deploy with Bindings
```bash
curl -X PUT ".../scripts/$SCRIPT_NAME" \
  -F 'metadata={
    "main_module": "worker.mjs",
    "bindings": [
      {"type": "kv_namespace", "name": "MY_KV", "namespace_id": "'$KV_ID'"}
    ],
    "tags": ["customer-123", "production"],
    "compatibility_date": "2026-01-01"  // Use current date for new projects
  };type=application/json' \
  -F 'worker.mjs=@worker.mjs;type=application/javascript+module'
```

## List/Delete Workers

```bash
# List
curl "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/workers/dispatch/namespaces/$NAMESPACE/scripts" \
  -H "Authorization: Bearer $API_TOKEN"

# Delete by name
curl -X DELETE ".../scripts/$SCRIPT_NAME" -H "Authorization: Bearer $API_TOKEN"

# Delete by tag
curl -X DELETE ".../scripts?tags=customer-123%3Ayes" -H "Authorization: Bearer $API_TOKEN"
```

**Pagination:** SDK supports async iteration. Manual: add `?per_page=100&page=1` query params.

## Static Assets

**3-step process:** Create session → Upload files → Deploy Worker

### 1. Create Upload Session
```bash
curl -X POST ".../scripts/$SCRIPT_NAME/assets-upload-session" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "manifest": {
      "/index.html": {"hash": "08f1dfda4574284ab3c21666d1ee8c7d4", "size": 1234}
    }
  }'
# Returns: jwt, buckets
```

**Hash:** SHA-256 truncated to first 16 bytes (32 hex characters)

### 2. Upload Files
```bash
curl -X POST ".../workers/assets/upload?base64=true" \
  -H "Authorization: Bearer $UPLOAD_JWT" \
  -F '08f1dfda4574284ab3c21666d1ee8c7d4=<BASE64_CONTENT>'
# Returns: completion jwt
```

**Multiple buckets:** Upload to all returned bucket URLs (typically 2 for redundancy) using same JWT and hash.

### 3. Deploy with Assets
```bash
curl -X PUT ".../scripts/$SCRIPT_NAME" \
  -F 'metadata={
    "main_module": "index.js",
    "assets": {"jwt": "<COMPLETION_TOKEN>"},
    "bindings": [{"type": "assets", "name": "ASSETS"}]
  };type=application/json' \
  -F 'index.js=export default {...};type=application/javascript+module'
```

**Asset Isolation:** Assets shared across namespace by default. For customer isolation, salt hash: `sha256(customerId + fileContents).slice(0, 32)`

## Dispatch Workers

### Subdomain Routing
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const userWorkerName = new URL(request.url).hostname.split(".")[0];
    const userWorker = env.DISPATCHER.get(userWorkerName);
    return await userWorker.fetch(request);
  },
};
```

### Path Routing
```typescript
const pathParts = new URL(request.url).pathname.split("/").filter(Boolean);
const userWorker = env.DISPATCHER.get(pathParts[0]);
return await userWorker.fetch(request);
```

### KV Routing
```typescript
const hostname = new URL(request.url).hostname;
const userWorkerName = await env.ROUTING_KV.get(hostname);
const userWorker = env.DISPATCHER.get(userWorkerName);
return await userWorker.fetch(request);
```

## Outbound Workers

Control external fetch from user Workers:

### Configure
```typescript
const userWorker = env.DISPATCHER.get(
  workerName, {},
  { outbound: { customer_context: { customer_name: workerName, url: request.url } } }
);
```

### Implement
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const customerName = env.customer_name;
    const url = new URL(request.url);
    
    // Block domains
    if (["malicious.com"].some(d => url.hostname.includes(d))) {
      return new Response("Blocked", { status: 403 });
    }
    
    // Inject auth
    if (url.hostname === "api.example.com") {
      const headers = new Headers(request.headers);
      headers.set("Authorization", `Bearer ${generateJWT(customerName)}`);
      return fetch(new Request(request, { headers }));
    }
    
    return fetch(request);
  },
};
```

**Note:** Doesn't intercept DO/mTLS fetch.

See [README.md](./README.md), [configuration.md](./configuration.md), [patterns.md](./patterns.md), [gotchas.md](./gotchas.md)

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
