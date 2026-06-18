---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/analytics-engine/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\analytics-engine\patterns.md
source_ext: .md
source_sha256: 968aa453468d1f0da03c9f68e9314623774d213407b6a4a7b3f4de53051229cd
text_sha256: d294a7ee3ce2d58fbb8413eb6e58faf7af8f699cecc7480b955ceb31e87204b2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/analytics-engine/patterns.md`
- Extract: `text`
- SHA256: `968aa453468d1f0da03c9f68e9314623774d213407b6a4a7b3f4de53051229cd`

## Content

# Analytics Engine Patterns

## Use Cases

| Use Case | Key Metrics | Index On |
|----------|-------------|----------|
| API Metering | requests, bytes, compute_units | api_key |
| Feature Usage | feature, action, duration | user_id |
| Error Tracking | error_type, endpoint, count | customer_id |
| Performance | latency_ms, cache_status | endpoint |
| A/B Testing | variant, conversions | user_id |

## API Metering (Billing)

```typescript
env.ANALYTICS.writeDataPoint({
  blobs: [pathname, method, status, tier],
  doubles: [1, computeUnits, bytes, latencyMs],
  indexes: [apiKey]
});

// Query: Monthly usage by customer
// SELECT index1 AS api_key, SUM(double2) AS compute_units
// FROM usage WHERE timestamp >= DATE_TRUNC('month', NOW()) GROUP BY index1
```

## Error Tracking

```typescript
env.ANALYTICS.writeDataPoint({
  blobs: [endpoint, method, errorName, errorMessage.slice(0, 1000)],
  doubles: [1, timeToErrorMs],
  indexes: [customerId]
});
```

## Performance Monitoring

```typescript
env.ANALYTICS.writeDataPoint({
  blobs: [pathname, method, cacheStatus, status],
  doubles: [latencyMs, 1],
  indexes: [userId]
});

// Query: P95 latency by endpoint
// SELECT blob1, quantile(0.95)(double1) AS p95_ms FROM perf GROUP BY blob1
```

## Anti-Patterns

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| `await writeDataPoint()` | `writeDataPoint()` (fire-and-forget) |
| `indexes: [method]` (low cardinality) | `blobs: [method]`, `indexes: [userId]` |
| `blobs: [JSON.stringify(obj)]` | Store ID in blob, full object in D1/KV |
| Write every request at 10M/min | Pre-aggregate per second |
| Query from Worker | Query from external service/API |

## Best Practices

1. **Design schema upfront** - Document blob/double/index assignments
2. **Always include count metric** - `doubles: [latency, 1]` for AVG calculations
3. **Use enums for blobs** - Consistent values like `Status.SUCCESS`
4. **Handle sampling** - Use ratios (avg_latency = SUM(latency)/SUM(count))
5. **Test queries early** - Validate schema before heavy writes

## Schema Template

```typescript
/**
 * Dataset: my_metrics
 * 
 * Blobs:
 *   blob1: endpoint, blob2: method, blob3: status
 * 
 * Doubles:
 *   double1: latency_ms, double2: count (always 1)
 * 
 * Indexes:
 *   index1: customer_id (high cardinality)
 */
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
