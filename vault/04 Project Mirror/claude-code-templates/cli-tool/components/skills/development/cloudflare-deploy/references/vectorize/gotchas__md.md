---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/vectorize/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\vectorize\gotchas.md
source_ext: .md
source_sha256: 75d90ba780c91084686163453ddca427250072ab0407bc6ce5e08978b14cf188
text_sha256: 41368d07e71f80db6d649b07ed871b9ac463bcc8db8d53563e07d24634fd5633
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/vectorize/gotchas.md`
- Extract: `text`
- SHA256: `75d90ba780c91084686163453ddca427250072ab0407bc6ce5e08978b14cf188`

## Content

# Vectorize Gotchas

## Critical Warnings

### Async Mutations
Insert/upsert/delete return immediately but vectors aren't queryable for 5-10 seconds.

### Batch Size Limit
**Workers API: 500 vectors max per call** (undocumented, silently truncates)

```typescript
// ✅ Chunk into 500
for (let i = 0; i < vectors.length; i += 500) {
  await env.VECTORIZE.upsert(vectors.slice(i, i + 500));
}
```

### Metadata Truncation
`returnMetadata: "indexed"` returns only first 64 bytes of strings. Use `"all"` for complete metadata (but max topK drops to 20).

### topK Limits

| returnMetadata | returnValues | Max topK |
|----------------|--------------|----------|
| `"none"` / `"indexed"` | `false` | 100 |
| `"all"` | any | **20** |
| any | `true` | **20** |

### Metadata Indexes First
Create BEFORE inserting - existing vectors not retroactively indexed.

```bash
# ✅ Create index FIRST
wrangler vectorize create-metadata-index my-index --property-name=category --type=string
wrangler vectorize insert my-index --file=data.ndjson
```

### Index Config Immutable
Cannot change dimensions/metric after creation. Must create new index and migrate.

## Limits (V2)

| Resource | Limit |
|----------|-------|
| Vectors per index | 10,000,000 |
| Max dimensions | 1536 |
| Batch upsert (Workers) | **500** |
| Indexed string metadata | **64 bytes** |
| Metadata indexes | 10 |
| Namespaces | 50,000 (paid) / 1,000 (free) |

## Common Mistakes

1. **Wrong embedding shape:** Extract `result.data[0]` from Workers AI
2. **Metadata index after data:** Re-upsert all vectors
3. **Insert vs upsert:** `insert` ignores duplicates, `upsert` overwrites
4. **Not batching:** Individual inserts ~1K/min, batched ~200K+/min

## Troubleshooting

**No results?**
- Wait 5-10s after insert
- Check namespace spelling (case-sensitive)
- Verify metadata index exists
- Check dimension mismatch

**Metadata filter not working?**
- Index must exist before data insert
- Strings >64 bytes truncated
- Use dot notation for nested: `"product.category"`

## Model Dimensions

- `@cf/baai/bge-small-en-v1.5`: 384
- `@cf/baai/bge-base-en-v1.5`: 768
- `@cf/baai/bge-large-en-v1.5`: 1024

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
