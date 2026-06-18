---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/datadog-cli/references/query-syntax.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\datadog-cli\references\query-syntax.md
source_ext: .md
source_sha256: 1363ab6542dcfe9801ea91088803d68ee5bef5e89c3c864c61be7945463788b9
text_sha256: fa60d601d5e943fd6f4eac79a4ed800d01044708a701858ca2423f6b8ca80ad8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# query-syntax.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/datadog-cli/references/query-syntax.md`
- Extract: `text`
- SHA256: `1363ab6542dcfe9801ea91088803d68ee5bef5e89c3c864c61be7945463788b9`

## Content

# Datadog Query Syntax

## Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `AND` | `service:api status:error` | Both conditions (implicit) |
| `OR` | `status:error OR status:warn` | Either condition |
| `-` | `-status:info` | Exclude |
| `*` | `service:api-*` | Wildcard |
| `>=` `<=` | `@http.status_code:>=400` | Numeric comparison |
| `[TO]` | `@duration:[1000 TO 5000]` | Range |

## Common Attributes

| Attribute | Description |
|-----------|-------------|
| `service` | Service name |
| `status` | Log level (error, warn, info, debug) |
| `host` | Hostname |
| `@http.status_code` | HTTP status code |
| `@http.method` | HTTP method |
| `@http.url` | Request URL |
| `@error.kind` | Error type |
| `@error.message` | Error message |
| `@trace_id` | Trace ID |
| `@dd.trace_id` | Datadog trace ID |

## Time Formats

### Relative
- `1m` - 1 minute
- `30m` - 30 minutes
- `1h` - 1 hour
- `6h` - 6 hours
- `24h` - 24 hours
- `7d` - 7 days

### Absolute
- ISO 8601: `2024-01-15T10:30:00Z`

## Example Queries

```bash
# All errors
status:error

# Errors in specific service
service:api status:error

# 5xx HTTP errors
@http.status_code:>=500

# Exclude info logs
-status:info

# Multiple services
service:api OR service:payment

# Timeout errors
error:timeout OR @error.kind:TimeoutError

# Slow requests (>1s)
@duration:>=1000
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
