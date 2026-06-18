---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/analytics-engine/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\analytics-engine\README.md
source_ext: .md
source_sha256: 135e3b898db6938457f3f59c2d7644c6ba267329de67fa0d04112abd6ef3d759
text_sha256: 123cb825f034688e3603b5a5fb6b372bbd9d82cabaa047bf787631ecb2026702
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/analytics-engine/README.md`
- Extract: `text`
- SHA256: `135e3b898db6938457f3f59c2d7644c6ba267329de67fa0d04112abd6ef3d759`

## Content

# Cloudflare Workers Analytics Engine Reference

Expert guidance for implementing unlimited-cardinality analytics at scale using Cloudflare Workers Analytics Engine.

## What is Analytics Engine?

Time-series analytics database designed for high-cardinality data (millions of unique dimensions). Write data points from Workers, query via SQL API. Use for:
- Custom user-facing analytics dashboards
- Usage-based billing & metering
- Per-customer/per-feature monitoring
- High-frequency instrumentation without performance impact

**Key Capability:** Track metrics with unlimited unique values (e.g., millions of user IDs, API keys) without performance degradation.

## Core Concepts

| Concept | Description | Example |
|---------|-------------|---------|
| **Dataset** | Logical table for related metrics | `api_requests`, `user_events` |
| **Data Point** | Single measurement with timestamp | One API request's metrics |
| **Blobs** | String dimensions (max 20) | endpoint, method, status, user_id |
| **Doubles** | Numeric values (max 20) | latency_ms, request_count, bytes |
| **Indexes** | Filtered blobs for efficient queries | customer_id, api_key |

## Reading Order

| Task | Start Here | Then Read |
|------|------------|-----------|
| **First-time setup** | [configuration.md](configuration.md) → [api.md](api.md) → [patterns.md](patterns.md) | |
| **Writing data** | [api.md](api.md) → [gotchas.md](gotchas.md) (sampling) | |
| **Querying data** | [api.md](api.md) (SQL API) → [patterns.md](patterns.md) (examples) | |
| **Debugging** | [gotchas.md](gotchas.md) → [api.md](api.md) (limits) | |
| **Optimization** | [patterns.md](patterns.md) (anti-patterns) → [gotchas.md](gotchas.md) | |

## When to Use Analytics Engine

```
Need to track metrics? → Yes
  ↓
Millions of unique dimension values? → Yes
    ↓
  Need real-time queries? → Yes
      ↓
    Use Analytics Engine ✓

Alternative scenarios:
- Low cardinality (<10k unique values) → Workers Analytics (free tier)
- Complex joins/relations → D1 Database
- Logs/debugging → Tail Workers (logpush)
- External tools → Send to external analytics (Datadog, etc.)
```

## Quick Start

1. Add binding to `wrangler.jsonc`:
```jsonc
{
  "analytics_engine_datasets": [
    { "binding": "ANALYTICS", "dataset": "my_events" }
  ]
}
```

2. Write data points (fire-and-forget, no await):
```typescript
env.ANALYTICS.writeDataPoint({
  blobs: ["/api/users", "GET", "200"],
  doubles: [145.2, 1],  // latency_ms, count
  indexes: [customerId]
});
```

3. Query via SQL API (HTTP):
```sql
SELECT blob1, SUM(double2) AS total_requests
FROM my_events
WHERE index1 = 'customer_123'
  AND timestamp >= NOW() - INTERVAL '7' DAY
GROUP BY blob1
ORDER BY total_requests DESC
```

## In This Reference

- **[configuration.md](configuration.md)** - Setup, bindings, TypeScript types, limits
- **[api.md](api.md)** - `writeDataPoint()`, SQL API, query syntax
- **[patterns.md](patterns.md)** - Use cases, examples, anti-patterns
- **[gotchas.md](gotchas.md)** - Sampling, index selection, troubleshooting

## See Also

- [Cloudflare Analytics Engine Docs](https://developers.cloudflare.com/analytics/analytics-engine/)

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
