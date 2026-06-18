---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/kv/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\kv\README.md
source_ext: .md
source_sha256: 0aaba2c9896682ba79c4f29b6f4e9a9f6e7818367d4f2857d04afb10f802faa7
text_sha256: c141ec2f48645a0f0884511baceee0265776075f3073aefbd199f3037b420681
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/kv/README.md`
- Extract: `text`
- SHA256: `0aaba2c9896682ba79c4f29b6f4e9a9f6e7818367d4f2857d04afb10f802faa7`

## Content

# Cloudflare Workers KV

Globally-distributed, eventually-consistent key-value store optimized for high read volume and low latency.

## Overview

KV provides:
- Eventual consistency (60s global propagation)
- Read-optimized performance
- 25 MiB value limit per key
- Auto-replication to Cloudflare edge
- Metadata support (1024 bytes)

**Use cases:** Config storage, user sessions, feature flags, caching, A/B testing

## When to Use KV

| Need | Recommendation |
|------|----------------|
| Strong consistency | → [Durable Objects](../durable-objects/) |
| SQL queries | → [D1](../d1/) |
| Object storage (files) | → [R2](../r2/) |
| High read, low write volume | → KV ✅ |
| Sub-10ms global reads | → KV ✅ |

**Quick comparison:**

| Feature | KV | D1 | Durable Objects |
|---------|----|----|-----------------|
| Consistency | Eventual | Strong | Strong |
| Read latency | <10ms | ~50ms | <1ms |
| Write limit | 1/s per key | Unlimited | Unlimited |
| Use case | Config, cache | Relational data | Coordination |

## Quick Start

```bash
wrangler kv namespace create MY_NAMESPACE
# Add binding to wrangler.jsonc
```

```typescript
// Write
await env.MY_KV.put("key", "value", { expirationTtl: 300 });

// Read
const value = await env.MY_KV.get("key");
const json = await env.MY_KV.get<Config>("config", "json");
```

## Core Operations

| Method | Purpose | Returns |
|--------|---------|---------|
| `get(key, type?)` | Single read | `string \| null` |
| `get(keys, type?)` | Bulk read (≤100) | `Map<string, T \| null>` |
| `put(key, value, options?)` | Write | `Promise<void>` |
| `delete(key)` | Delete | `Promise<void>` |
| `list(options?)` | List keys | `{ keys, list_complete, cursor? }` |
| `getWithMetadata(key)` | Get + metadata | `{ value, metadata }` |

## Consistency Model

- **Write visibility:** Immediate in same location, ≤60s globally
- **Read path:** Eventually consistent
- **Write rate:** 1 write/second per key (429 on exceed)

## Reading Order

| Task | Files to Read |
|------|---------------|
| Quick start | README → configuration.md |
| Implement feature | README → api.md → patterns.md |
| Debug issues | gotchas.md → api.md |
| Batch operations | api.md (bulk section) → patterns.md |
| Performance tuning | gotchas.md (performance) → patterns.md (caching) |

## In This Reference

- [configuration.md](./configuration.md) - wrangler.jsonc setup, namespace creation, TypeScript types
- [api.md](./api.md) - KV methods, bulk operations, cacheTtl, content types
- [patterns.md](./patterns.md) - Caching, sessions, rate limiting, A/B testing
- [gotchas.md](./gotchas.md) - Eventual consistency, concurrent writes, value limits

## See Also

- [workers](../workers/) - Worker runtime for KV access
- [d1](../d1/) - Use D1 for strong consistency needs
- [durable-objects](../durable-objects/) - Strongly consistent alternative

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
