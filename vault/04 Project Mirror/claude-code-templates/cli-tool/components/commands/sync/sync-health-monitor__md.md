---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/sync/sync-health-monitor.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\sync\sync-health-monitor.md
source_ext: .md
source_sha256: 610267e2b797bcd7e6a371dee3cf3d3ec33f01422b581dbc1a862a72f74f5aa9
text_sha256: d352777d282c0418ddd3c3e49fbe746dc8225588b70b28dcac55088f97459bc2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# sync-health-monitor.md

- Source: `claude-code-templates/cli-tool/components/commands/sync/sync-health-monitor.md`
- Extract: `text`
- SHA256: `610267e2b797bcd7e6a371dee3cf3d3ec33f01422b581dbc1a862a72f74f5aa9`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [scope] | --github | --linear | --webhooks | --performance | --report
description: Monitor and diagnose GitHub-Linear sync health with performance analytics and automated troubleshooting
---

# Sync Health Monitor

Monitor comprehensive GitHub-Linear synchronization health and performance: **$ARGUMENTS**

## Current Sync Environment

- GitHub API status: !`gh api rate_limit -q '.rate | "GitHub: \(.remaining)/\(.limit) requests"' 2>/dev/null || echo "GitHub API check needed"`
- Linear connectivity: Linear MCP server status and authentication validation
- Webhook status: Active webhook configurations and event processing health
- Sync performance: Current throughput, latency metrics, and error rates

## Task

Implement comprehensive sync health monitoring with automated diagnostics and performance optimization:

**Monitor Scope**: Use $ARGUMENTS to specify GitHub health, Linear connectivity, webhook diagnostics, performance analysis, or complete health report

**Health Monitoring Framework**:
1. **API Health Assessment** - Monitor GitHub/Linear API status, rate limits, authentication, connectivity issues
2. **Sync Performance Analysis** - Track throughput metrics, latency patterns, processing times, queue depths
3. **Error Pattern Detection** - Identify recurring failures, classify error types, analyze failure trends
4. **Webhook Diagnostics** - Validate webhook configurations, test event delivery, monitor processing latency
5. **Data Integrity Validation** - Verify sync consistency, detect orphaned records, validate cross-references
6. **Automated Troubleshooting** - Run diagnostic tests, suggest fixes, implement automated recovery procedures

**Advanced Features**: Real-time health dashboards, predictive failure detection, automated recovery workflows, comprehensive performance profiling.

**Diagnostic Capabilities**: Deep error analysis, bottleneck identification, configuration validation, automated testing suites.

**Output**: Complete health assessment with performance metrics, error analysis, recommended optimizations, and automated diagnostic reports.

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
