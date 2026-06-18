---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/datadog-cli/references/workflows.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\datadog-cli\references\workflows.md
source_ext: .md
source_sha256: 8d4f2f64bf3335ee3e2026fb34a0333cc338a82029a1974978c6ea81df2826e2
text_sha256: 22acfb7b8d5590926a6b75abe33d7fe22f60f1e90511cf95ad3e84a49b88af6c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# workflows.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/datadog-cli/references/workflows.md`
- Extract: `text`
- SHA256: `8d4f2f64bf3335ee3e2026fb34a0333cc338a82029a1974978c6ea81df2826e2`

## Content

# Common Workflows

## Incident Triage

Step-by-step workflow for investigating production issues.

```bash
# 1. Quick error overview
npx @leoflores/datadog-cli errors --from 1h --pretty

# 2. Is this new? Compare to previous period
npx @leoflores/datadog-cli logs compare --query "status:error" --period 1h --pretty

# 3. Find error patterns
npx @leoflores/datadog-cli logs patterns --query "status:error" --from 1h --pretty

# 4. Narrow down by service
npx @leoflores/datadog-cli logs search --query "status:error service:payment-api" --from 1h --pretty

# 5. Get context around a specific timestamp
npx @leoflores/datadog-cli logs context --timestamp "2024-01-15T10:30:00Z" --service api --before 5m --after 2m --pretty

# 6. Follow the distributed trace
npx @leoflores/datadog-cli logs trace --id "TRACE_ID" --pretty
```

## Real-time Debugging

Monitor logs as they arrive.

```bash
# Stream all errors
npx @leoflores/datadog-cli logs tail --query "status:error" --pretty

# Watch specific service
npx @leoflores/datadog-cli logs tail --query "service:api status:error" --pretty

# Monitor deployments
npx @leoflores/datadog-cli logs tail --query "service:deploy" --pretty
```

## Service Health Check

Assess overall service health.

```bash
# List all services
npx @leoflores/datadog-cli services --from 24h --pretty

# Check error distribution for a service
npx @leoflores/datadog-cli logs agg --query "service:api" --facet status --from 1h --pretty

# Check CPU/memory usage
npx @leoflores/datadog-cli metrics query --query "avg:system.cpu.user{service:api}" --from 1h --pretty
npx @leoflores/datadog-cli metrics query --query "avg:system.mem.used{service:api}" --from 1h --pretty

# Error summary for service
npx @leoflores/datadog-cli errors --service api --from 24h --pretty
```

## Export for Sharing

Save results to files for reports or sharing.

```bash
# Save search results
npx @leoflores/datadog-cli logs search --query "status:error" --from 1h --output errors.json --pretty

# Save error summary
npx @leoflores/datadog-cli errors --from 24h --output error-report.json --pretty

# Save metrics data
npx @leoflores/datadog-cli metrics query --query "avg:system.cpu.user{*}" --from 24h --output cpu-metrics.json --pretty
```

## Multi-Query Investigation

Run parallel queries for comprehensive view.

```bash
# Compare error types across services
npx @leoflores/datadog-cli logs multi \
  --queries "api-errors:service:api status:error,payment-errors:service:payment status:error,auth-errors:service:auth status:error" \
  --from 1h --pretty
```

## ⚠️ Safe Dashboard Update

**CRITICAL:** Dashboard updates are destructive and replace the entire dashboard.

Follow the **Safe Dashboard Update Workflow** in [dashboards.md](dashboards.md) to avoid data loss.

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
