---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/kv/configuration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\kv\configuration.md
source_ext: .md
source_sha256: 5b0f3b731ebb2f04a16b91b268851044b07854eede6a23d507d0463fb3dcf52c
text_sha256: 59138344e7c23b43b360e0df44a23ee56253d013a4a1a9633c5b459b3d4ebac3
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# configuration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/kv/configuration.md`
- Extract: `text`
- SHA256: `5b0f3b731ebb2f04a16b91b268851044b07854eede6a23d507d0463fb3dcf52c`

## Content

# KV Configuration

## Create Namespace

```bash
wrangler kv namespace create MY_NAMESPACE
# Output: { binding = "MY_NAMESPACE", id = "abc123..." }

wrangler kv namespace create MY_NAMESPACE --preview  # For local dev
```

## Workers Binding

**wrangler.jsonc:**
```jsonc
{
  "kv_namespaces": [
    {
      "binding": "MY_KV",
      "id": "abc123xyz789"
    },
    // Optional: Different namespace for preview/development
    {
      "binding": "MY_KV",
      "preview_id": "preview-abc123"
    }
  ]
}
```

## TypeScript Types

**env.d.ts:**
```typescript
interface Env {
  MY_KV: KVNamespace;
  SESSIONS: KVNamespace;
  CACHE: KVNamespace;
}
```

**worker.ts:**
```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    // env.MY_KV is now typed as KVNamespace
    const value = await env.MY_KV.get("key");
    return new Response(value || "Not found");
  }
} satisfies ExportedHandler<Env>;
```

**Type-safe JSON operations:**
```typescript
interface UserProfile {
  name: string;
  email: string;
  role: "admin" | "user";
}

const profile = await env.USERS.get<UserProfile>("user:123", "json");
// profile: UserProfile | null (type-safe!)
if (profile) {
  console.log(profile.name); // TypeScript knows this is a string
}
```

## CLI Operations

```bash
# Put
wrangler kv key put --binding=MY_KV "key" "value"
wrangler kv key put --binding=MY_KV "key" --path=./file.json --ttl=3600

# Get
wrangler kv key get --binding=MY_KV "key"

# Delete
wrangler kv key delete --binding=MY_KV "key"

# List
wrangler kv key list --binding=MY_KV --prefix="user:"

# Bulk operations (max 10,000 keys per file)
wrangler kv bulk put data.json --binding=MY_KV
wrangler kv bulk get keys.json --binding=MY_KV
wrangler kv bulk delete keys.json --binding=MY_KV --force
```

## Local Development

```bash
wrangler dev                # Local KV (isolated)
wrangler dev --remote       # Remote KV (production)

# Or in wrangler.jsonc:
# "kv_namespaces": [{ "binding": "MY_KV", "id": "...", "remote": true }]
```

## REST API

### Single Operations

```typescript
import Cloudflare from 'cloudflare';

const client = new Cloudflare({
  apiEmail: process.env.CLOUDFLARE_EMAIL,
  apiKey: process.env.CLOUDFLARE_API_KEY
});

// Single key operations
await client.kv.namespaces.values.update(namespaceId, 'key', {
  account_id: accountId,
  value: 'value',
  expiration_ttl: 3600
});
```

### Bulk Operations

```typescript
// Bulk update (up to 10,000 keys, max 100MB total)
await client.kv.namespaces.bulkUpdate(namespaceId, {
  account_id: accountId,
  body: [
    { key: "key1", value: "value1", expiration_ttl: 3600 },
    { key: "key2", value: "value2", metadata: { version: 1 } },
    { key: "key3", value: "value3" }
  ]
});

// Bulk get (up to 100 keys)
const results = await client.kv.namespaces.bulkGet(namespaceId, {
  account_id: accountId,
  keys: ["key1", "key2", "key3"]
});

// Bulk delete (up to 10,000 keys)
await client.kv.namespaces.bulkDelete(namespaceId, {
  account_id: accountId,
  keys: ["key1", "key2", "key3"]
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
