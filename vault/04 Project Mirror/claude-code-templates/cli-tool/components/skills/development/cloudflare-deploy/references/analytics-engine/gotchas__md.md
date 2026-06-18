---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/analytics-engine/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\analytics-engine\gotchas.md
source_ext: .md
source_sha256: d8f3cfae8579efacf7a93a50d5b4dcb7b0723589d42c285598bed1cf51b176ba
text_sha256: 08d11a06bc1cc955bdf4ade8d1a523b0e78157434d559169c4bc2d36f886667b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/analytics-engine/gotchas.md`
- Extract: `text`
- SHA256: `d8f3cfae8579efacf7a93a50d5b4dcb7b0723589d42c285598bed1cf51b176ba`

## Content

# Analytics Engine Gotchas

## Critical Issues

### Sampling at High Volumes

**Problem:** Queries return fewer points than written at >1M writes/min.

**Solution:**
```typescript
// Pre-aggregate before writing
let buffer = { count: 0, total: 0 };
buffer.count++; buffer.total += value;

// Write once per second instead of per request
if (Date.now() % 1000 === 0) {
  env.ANALYTICS.writeDataPoint({ doubles: [buffer.count, buffer.total] });
}
```

**Detection:** `npx wrangler tail` → look for "sampling enabled"

### writeDataPoint Returns void

```typescript
// ❌ Pointless await
await env.ANALYTICS.writeDataPoint({...});

// ✅ Fire-and-forget
env.ANALYTICS.writeDataPoint({...});
```

Writes can fail silently. Check tail logs.

### Index vs Blob

| Cardinality | Use | Example |
|-------------|-----|---------|
| Millions | **Index** | user_id, api_key |
| Hundreds | **Blob** | endpoint, status_code, country |

```typescript
// ✅ Correct
{ blobs: [method, path, status], indexes: [userId] }
```

### Can't Query from Workers

Query API requires HTTP auth. Use external service or cache in KV/D1.

### No Custom Timestamps

Auto-generated at write time. Store original in blob if needed.

## Common Errors

| Error | Fix |
|-------|-----|
| Binding not found | Check wrangler.jsonc, redeploy |
| No data in query | Wait 30s; check dataset name; check time range |
| Query timeout | Add time filter; use index for filtering |

## Limits

| Resource | Limit |
|----------|-------|
| Blobs per point | 20 |
| Doubles per point | 20 |
| Indexes per point | 1 |
| Blob/Index size | 16KB |
| Write rate (no sampling) | ~1M/min |
| Retention | 90 days |
| Query timeout | 30s |

## Best Practices

✅ Pre-aggregate at high volumes  
✅ Use index for high-cardinality (millions)  
✅ Always include time filter in queries  
✅ Design schema before coding  

❌ Don't await writeDataPoint  
❌ Don't use index for low-cardinality  
❌ Don't query without time range  
❌ Don't assume all writes succeed

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
