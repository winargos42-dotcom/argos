---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/pages-functions/configuration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\pages-functions\configuration.md
source_ext: .md
source_sha256: 52846d6ce860e8853eb2ad55ea5f54f79891b9ef47ac166a7d061e33237b6c9b
text_sha256: adaf79d53ca4d46ebc1be695314bb67aa42a11f412d9b61a48a765c828dd0d94
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# configuration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/pages-functions/configuration.md`
- Extract: `text`
- SHA256: `52846d6ce860e8853eb2ad55ea5f54f79891b9ef47ac166a7d061e33237b6c9b`

## Content

# Configuration

## TypeScript Setup

**Generate types from wrangler.jsonc** (replaces deprecated `@cloudflare/workers-types`):

```bash
npx wrangler types
```

Creates `worker-configuration.d.ts` with typed `Env` interface based on your bindings.

```typescript
// functions/api.ts
export const onRequest: PagesFunction<Env> = async (ctx) => {
  // ctx.env.KV, ctx.env.DB, etc. are fully typed
  return Response.json({ ok: true });
};
```

**Manual types** (if not using wrangler types):

```typescript
interface Env {
  KV: KVNamespace;
  DB: D1Database;
  API_KEY: string;
}
export const onRequest: PagesFunction<Env> = async (ctx) => { /* ... */ };
```

## wrangler.jsonc

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-pages-app",
  "pages_build_output_dir": "./dist",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"],
  
  "vars": { "API_URL": "https://api.example.com" },
  "kv_namespaces": [{ "binding": "KV", "id": "abc123" }],
  "d1_databases": [{ "binding": "DB", "database_name": "prod-db", "database_id": "xyz789" }],
  "r2_buckets": [{ "binding": "BUCKET", "bucket_name": "my-bucket" }],
  "durable_objects": { "bindings": [{ "name": "COUNTER", "class_name": "Counter", "script_name": "counter-worker" }] },
  "services": [{ "binding": "AUTH", "service": "auth-worker" }],
  "ai": { "binding": "AI" },
  "vectorize": [{ "binding": "VECTORIZE", "index_name": "my-index" }],
  "analytics_engine_datasets": [{ "binding": "ANALYTICS" }]
}
```

## Environment Overrides

Top-level → local dev, `env.preview` → preview, `env.production` → production

```jsonc
{
  "vars": { "API_URL": "http://localhost:8787" },
  "env": {
    "production": { "vars": { "API_URL": "https://api.example.com" } }
  }
}
```

**Note:** If overriding `vars`, `kv_namespaces`, `d1_databases`, etc., ALL must be redefined (non-inheritable)

## Local Secrets (.dev.vars)

**Local dev only** - NOT deployed:

```bash
# .dev.vars (add to .gitignore)
SECRET_KEY="my-secret-value"
```

Accessed via `ctx.env.SECRET_KEY`. Set production secrets:
```bash
echo "value" | npx wrangler pages secret put SECRET_KEY --project-name=my-app
```

## Static Config Files

**_routes.json** - Custom routing:
```json
{ "version": 1, "include": ["/api/*"], "exclude": ["/static/*"] }
```

**_headers** - Static headers:
```
/static/*
  Cache-Control: public, max-age=31536000
```

**_redirects** - Redirects:
```
/old  /new  301
```

## Local Dev & Deployment

```bash
# Dev server
npx wrangler pages dev ./dist

# With bindings
npx wrangler pages dev ./dist --kv=KV --d1=DB=db-id --r2=BUCKET

# Durable Objects (2 terminals)
cd do-worker && npx wrangler dev
cd pages-project && npx wrangler pages dev ./dist --do COUNTER=Counter@do-worker

# Deploy
npx wrangler pages deploy ./dist
npx wrangler pages deploy ./dist --branch preview

# Download config
npx wrangler pages download config my-project
```

**See also:** [api.md](./api.md) for binding usage examples

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
