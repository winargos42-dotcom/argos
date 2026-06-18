---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/hyperdrive/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\hyperdrive\README.md
source_ext: .md
source_sha256: 248bcdef6379f27f2b53bc8fa92f915e2ac0f995d70e4040734a47936a928831
text_sha256: 4d0e1a0e8366975d6ac0dcfd183e8b0a925f582c35917897aace568addff09f6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/hyperdrive/README.md`
- Extract: `text`
- SHA256: `248bcdef6379f27f2b53bc8fa92f915e2ac0f995d70e4040734a47936a928831`

## Content

# Hyperdrive

Accelerates database queries from Workers via connection pooling, edge setup, query caching.

## Key Features

- **Connection Pooling**: Persistent connections eliminate TCP/TLS/auth handshakes (~7 round-trips)
- **Edge Setup**: Connection negotiation at edge, pooling near origin
- **Query Caching**: Auto-cache non-mutating queries (default 60s TTL)
- **Support**: PostgreSQL, MySQL + compatibles (CockroachDB, Timescale, PlanetScale, Neon, Supabase)

## Architecture

```
Worker → Edge (setup) → Pool (near DB) → Origin
         ↓ cached reads
         Cache
```

## Quick Start

```bash
# Create config
npx wrangler hyperdrive create my-db \
  --connection-string="postgres://user:pass@host:5432/db"

# wrangler.jsonc
{
  "compatibility_flags": ["nodejs_compat"],
  "hyperdrive": [{"binding": "HYPERDRIVE", "id": "<ID>"}]
}
```

```typescript
import { Client } from "pg";

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const client = new Client({
      connectionString: env.HYPERDRIVE.connectionString,
    });
    await client.connect();
    const result = await client.query("SELECT * FROM users WHERE id = $1", [123]);
    await client.end();
    return Response.json(result.rows);
  },
};
```

## When to Use

✅ Global access to single-region DBs, high read ratios, popular queries, connection-heavy loads
❌ Write-heavy, real-time data (<1s), single-region apps close to DB

**💡 Pair with Smart Placement** for Workers making multiple queries - executes near DB to minimize latency.

## Driver Choice

| Driver | Use When | Notes |
|--------|----------|-------|
| **pg** (recommended) | General use, TypeScript, ecosystem compatibility | Stable, widely used, works with most ORMs |
| **postgres.js** | Advanced features, template literals, streaming | Lighter than pg, `prepare: true` is default |
| **mysql2** | MySQL/MariaDB/PlanetScale | MySQL only, less mature support |

## Reading Order

| New to Hyperdrive | Implementing | Troubleshooting |
|-------------------|--------------|-----------------|
| 1. README (this) | 1. [configuration.md](./configuration.md) | 1. [gotchas.md](./gotchas.md) |
| 2. [configuration.md](./configuration.md) | 2. [api.md](./api.md) | 2. [patterns.md](./patterns.md) |
| 3. [api.md](./api.md) | 3. [patterns.md](./patterns.md) | 3. [api.md](./api.md) |

## In This Reference
- [configuration.md](./configuration.md) - Setup, wrangler config, Smart Placement
- [api.md](./api.md) - Binding APIs, query patterns, driver usage
- [patterns.md](./patterns.md) - Use cases, ORMs, multi-query optimization
- [gotchas.md](./gotchas.md) - Limits, troubleshooting, connection management

## See Also
- [smart-placement](../smart-placement/) - Optimize multi-query Workers near databases
- [d1](../d1/) - Serverless SQLite alternative for edge-native apps
- [workers](../workers/) - Worker runtime with database bindings

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
