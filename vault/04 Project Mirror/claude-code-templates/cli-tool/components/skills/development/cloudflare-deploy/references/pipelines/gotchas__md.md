---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/pipelines/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\pipelines\gotchas.md
source_ext: .md
source_sha256: 475a7bdaf55524fbfcc35086fb76e2add401397e532c4e5a02988c9f09488d9a
text_sha256: c227e49aba59e449ea3f5bb8751bc5c623287ea35f898db2deb873808d326e69
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/pipelines/gotchas.md`
- Extract: `text`
- SHA256: `475a7bdaf55524fbfcc35086fb76e2add401397e532c4e5a02988c9f09488d9a`

## Content

# Pipelines Gotchas

## Critical Issues

### Events Silently Dropped

**Most common issue.** Events accepted (HTTP 200) but never appear in sink.

**Causes:**
1. Schema validation fails - structured streams drop invalid events silently
2. Waiting for roll interval (10-300s) - expected behavior

**Solution:** Validate client-side with Zod:
```typescript
const EventSchema = z.object({ user_id: z.string(), amount: z.number() });
try {
  const validated = EventSchema.parse(rawEvent);
  await env.STREAM.send([validated]);
} catch (e) { /* get immediate feedback */ }
```

### Pipelines Are Immutable

Cannot modify SQL after creation. Must delete and recreate.

```bash
npx wrangler pipelines delete old-pipeline
npx wrangler pipelines create new-pipeline --sql "..."
```

**Tip:** Use version naming (`events-pipeline-v1`) and keep SQL in version control.

### Worker Binding Not Found

**`env.STREAM is undefined`**

1. Use **stream ID** (not pipeline ID) in `wrangler.jsonc`
2. Redeploy after adding binding

```bash
npx wrangler pipelines streams list  # Get stream ID
npx wrangler deploy
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Events not in R2 | Roll interval not elapsed | Wait 10-300s, check `roll_interval` |
| Schema validation failures | Type mismatch, missing fields | Validate client-side |
| Rate limit (429) | >5 MB/s per stream | Batch events, request increase |
| Payload too large (413) | >1 MB request | Split into smaller batches |
| Cannot delete stream | Pipeline references it | Delete pipelines first |
| Sink credential errors | Token expired | Recreate sink with new credentials |

## Limits (Open Beta)

| Resource | Limit |
|----------|-------|
| Streams/Sinks/Pipelines per account | 20 each |
| Payload size | 1 MB |
| Ingest rate per stream | 5 MB/s |
| Event retention | 24 hours |
| Recommended batch size | 100 events |

## SQL Limitations

- **No JOINs** - single stream per pipeline
- **No window functions** - basic SQL only
- **No subqueries** - must use `INSERT INTO ... SELECT ... FROM`
- **No schema evolution** - cannot modify after creation

## Debug Checklist

- [ ] Stream exists: `npx wrangler pipelines streams list`
- [ ] Pipeline healthy: `npx wrangler pipelines get <ID>`
- [ ] SQL syntax matches schema
- [ ] Worker redeployed after binding added
- [ ] Waited for roll interval
- [ ] Accepted vs processed count matches (no validation drops)

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
