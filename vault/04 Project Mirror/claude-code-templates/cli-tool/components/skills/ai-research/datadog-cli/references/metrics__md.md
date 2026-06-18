---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/datadog-cli/references/metrics.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\datadog-cli\references\metrics.md
source_ext: .md
source_sha256: 9a1dca63aad22c7424693a58b1186b9e57e30ab079df5913732dc0881d711e54
text_sha256: e9a56f75dbef1b389a517565ce9e4d62e479e2002373a107da08678cf71a5fce
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# metrics.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/datadog-cli/references/metrics.md`
- Extract: `text`
- SHA256: `9a1dca63aad22c7424693a58b1186b9e57e30ab079df5913732dc0881d711e54`

## Content

# Metrics Reference

## metrics query

Query timeseries metrics from Datadog.

```bash
npx @leoflores/datadog-cli metrics query --query "<metrics-query>" [--from <time>] [--to <time>]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--query` | required | Metrics query |
| `--from` | `15m` | Start time |
| `--to` | `now` | End time |

## Query Format

```
<aggregation>:<metric>{<tags>}
```

**Aggregations:** `avg`, `sum`, `min`, `max`, `count`

## Examples

### System Metrics
```bash
npx @leoflores/datadog-cli metrics query --query "avg:system.cpu.user{*}" --from 1h --pretty
npx @leoflores/datadog-cli metrics query --query "avg:system.mem.used{*}" --from 1h --pretty
```

### Service-Specific
```bash
npx @leoflores/datadog-cli metrics query --query "avg:system.cpu.user{service:api}" --from 1h --pretty
```

### APM Metrics
```bash
npx @leoflores/datadog-cli metrics query --query "sum:trace.http.request.errors{service:api}.as_count()" --from 1h --pretty
npx @leoflores/datadog-cli metrics query --query "p99:trace.http.request.duration{service:api}" --from 1h --pretty
```

### With Tags
```bash
npx @leoflores/datadog-cli metrics query --query "avg:system.cpu.user{env:prod,service:api}" --from 1h --pretty
```

## Output

Returns series with:
- Metric name and scope
- Point list (timestamp/value pairs)
- Tags
- Latest value + min/max/avg stats

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
