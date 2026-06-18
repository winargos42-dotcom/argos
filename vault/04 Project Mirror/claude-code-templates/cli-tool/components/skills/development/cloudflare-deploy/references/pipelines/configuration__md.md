---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/pipelines/configuration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\pipelines\configuration.md
source_ext: .md
source_sha256: 1429539b853c3afe586c0ab2a01b04cde7ac31cf45490be5d2e5492f9ff5ef4b
text_sha256: 2b838aaa75b3e304b586799bf07f66d878e1e6ef4911c6f4c0252c597ef2fb14
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# configuration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/pipelines/configuration.md`
- Extract: `text`
- SHA256: `1429539b853c3afe586c0ab2a01b04cde7ac31cf45490be5d2e5492f9ff5ef4b`

## Content

# Pipelines Configuration

## Worker Binding

```jsonc
// wrangler.jsonc
{
  "pipelines": [
    { "pipeline": "<STREAM_ID>", "binding": "STREAM" }
  ]
}
```

Get stream ID: `npx wrangler pipelines streams list`

## Schema (Structured Streams)

```json
{
  "fields": [
    { "name": "user_id", "type": "string", "required": true },
    { "name": "event_type", "type": "string", "required": true },
    { "name": "amount", "type": "float64", "required": false },
    { "name": "timestamp", "type": "timestamp", "required": true }
  ]
}
```

**Types:** `string`, `int32`, `int64`, `float32`, `float64`, `bool`, `timestamp`, `json`, `binary`, `list`, `struct`

## Stream Setup

```bash
# With schema
npx wrangler pipelines streams create my-stream --schema-file schema.json

# Unstructured (no validation)
npx wrangler pipelines streams create my-stream

# List/get/delete
npx wrangler pipelines streams list
npx wrangler pipelines streams get <ID>
npx wrangler pipelines streams delete <ID>
```

## Sink Configuration

**R2 Data Catalog (Iceberg):**
```bash
npx wrangler pipelines sinks create my-sink \
  --type r2-data-catalog \
  --bucket my-bucket --namespace default --table events \
  --catalog-token $TOKEN \
  --compression zstd --roll-interval 60
```

**R2 Raw (Parquet):**
```bash
npx wrangler pipelines sinks create my-sink \
  --type r2 --bucket my-bucket --format parquet \
  --path analytics/events \
  --partitioning "year=%Y/month=%m/day=%d" \
  --access-key-id $KEY --secret-access-key $SECRET
```

| Option | Values | Guidance |
|--------|--------|----------|
| `--compression` | `zstd`, `snappy`, `gzip` | `zstd` best ratio, `snappy` fastest |
| `--roll-interval` | Seconds | Low latency: 10-60, Query perf: 300 |
| `--roll-size` | MB | Larger = better compression |

## Pipeline Creation

```bash
npx wrangler pipelines create my-pipeline \
  --sql "INSERT INTO my_sink SELECT * FROM my_stream WHERE event_type = 'purchase'"
```

**⚠️ Pipelines are immutable** - cannot modify SQL. Must delete/recreate.

## Credentials

| Type | Permission | Get From |
|------|------------|----------|
| Catalog token | R2 Admin Read & Write | Dashboard → R2 → API tokens |
| R2 credentials | Object Read & Write | `wrangler r2 bucket create` output |
| HTTP ingest token | Workers Pipeline Send | Dashboard → Workers → API tokens |

## Complete Example

```bash
npx wrangler r2 bucket create my-bucket
npx wrangler r2 bucket catalog enable my-bucket
npx wrangler pipelines streams create my-stream --schema-file schema.json
npx wrangler pipelines sinks create my-sink --type r2-data-catalog --bucket my-bucket ...
npx wrangler pipelines create my-pipeline --sql "INSERT INTO my_sink SELECT * FROM my_stream"
npx wrangler deploy
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
