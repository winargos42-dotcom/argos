---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/do-storage/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\do-storage\README.md
source_ext: .md
source_sha256: 25d22d74615401e8fd9d39a6d86902e322a5a32434ea9de39cb3dfb2201009c3
text_sha256: 2dd7fa0efc7db9a4edb0935b77a48973fe79978b693d29385db0403f1792154a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/do-storage/README.md`
- Extract: `text`
- SHA256: `25d22d74615401e8fd9d39a6d86902e322a5a32434ea9de39cb3dfb2201009c3`

## Content

# Cloudflare Durable Objects Storage

Persistent storage API for Durable Objects with SQLite and KV backends, PITR, and automatic concurrency control.

## Overview

DO Storage provides:
- SQLite-backed (recommended) or KV-backed
- SQL API + synchronous/async KV APIs
- Automatic input/output gates (race-free)
- 30-day point-in-time recovery (PITR)
- Transactions and alarms

**Use cases:** Stateful coordination, real-time collaboration, counters, sessions, rate limiters

**Billing:** Charged by request, GB-month storage, and rowsRead/rowsWritten for SQL operations

## Quick Start

```typescript
export class Counter extends DurableObject {
  sql: SqlStorage;
  
  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    this.sql.exec('CREATE TABLE IF NOT EXISTS data(key TEXT PRIMARY KEY, value INTEGER)');
  }
  
  async increment(): Promise<number> {
    const result = this.sql.exec(
      'INSERT INTO data VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = value + 1 RETURNING value',
      'counter', 1
    ).one();
    return result?.value || 1;
  }
}
```

## Storage Backends

| Backend | Create Method | APIs | PITR |
|---------|---------------|------|------|
| SQLite (recommended) | `new_sqlite_classes` | SQL + sync KV + async KV | ✅ |
| KV (legacy) | `new_classes` | async KV only | ❌ |

## Core APIs

- **SQL API** (`ctx.storage.sql`): Full SQLite with extensions (FTS5, JSON, math)
- **Sync KV** (`ctx.storage.kv`): Synchronous key-value (SQLite only)
- **Async KV** (`ctx.storage`): Asynchronous key-value (both backends)
- **Transactions** (`transactionSync()`, `transaction()`)
- **PITR** (`getBookmarkForTime()`, `onNextSessionRestoreBookmark()`)
- **Alarms** (`setAlarm()`, `alarm()` handler)

## Reading Order

**New to DO storage:** configuration.md → api.md → patterns.md → gotchas.md  
**Building features:** patterns.md → api.md → gotchas.md  
**Debugging issues:** gotchas.md → api.md  
**Writing tests:** testing.md

## In This Reference

- [configuration.md](./configuration.md) - wrangler.jsonc migrations, SQLite vs KV setup, RPC binding
- [api.md](./api.md) - SQL exec/cursors, KV methods, storage options, transactions, alarms, PITR
- [patterns.md](./patterns.md) - Schema migrations, caching, rate limiting, batch processing, parent-child coordination
- [gotchas.md](./gotchas.md) - Concurrency gates, INTEGER precision, transaction rules, SQL limits
- [testing.md](./testing.md) - vitest-pool-workers setup, testing DOs with SQL/alarms/PITR

## See Also

- [durable-objects](../durable-objects/) - DO fundamentals and coordination patterns
- [workers](../workers/) - Worker runtime for DO stubs
- [d1](../d1/) - Shared database alternative to per-DO storage

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
