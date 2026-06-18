---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/database/supabase-realtime-monitor.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\database\supabase-realtime-monitor.md
source_ext: .md
source_sha256: 5b021554134099630f3c7548d18d493445471db751ace151a7acb0b85fe75111
text_sha256: a97f1b845dbe42abebd3d6aefc8bac2efda2cc7c6b6fecb47bb7ce2fab3d5036
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# supabase-realtime-monitor.md

- Source: `claude-code-templates/cli-tool/components/commands/database/supabase-realtime-monitor.md`
- Extract: `text`
- SHA256: `5b021554134099630f3c7548d18d493445471db751ace151a7acb0b85fe75111`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [monitoring-type] | --connections | --subscriptions | --performance | --debug | --analytics
description: Monitor and optimize Supabase realtime connections with performance analysis and debugging
---

# Supabase Realtime Monitor

Monitor and optimize Supabase realtime connections with comprehensive performance analysis: **$ARGUMENTS**

## Current Realtime Context

- Supabase realtime: Connection status and subscription management via MCP
- Application subscriptions: !`find . -name "*.ts" -o -name "*.js" | xargs grep -l "subscribe\|realtime\|channel" 2>/dev/null | head -5` active subscription code
- Performance metrics: Current connection performance and message throughput
- Error patterns: Recent realtime connection issues and debugging information

## Task

Execute comprehensive realtime monitoring with performance optimization and debugging support:

**Monitoring Type**: Use $ARGUMENTS to focus on connection monitoring, subscription analysis, performance optimization, debugging assistance, or analytics reporting

**Realtime Monitoring Framework**:
1. **Connection Analysis** - Monitor active connections, analyze connection stability, track connection lifecycle, identify connection issues
2. **Subscription Management** - Track active subscriptions, analyze subscription performance, optimize subscription patterns, manage subscription lifecycle
3. **Performance Optimization** - Analyze message throughput, optimize payload sizes, reduce connection overhead, improve subscription efficiency
4. **Error Monitoring** - Track connection errors, analyze failure patterns, implement retry strategies, provide debugging insights
5. **Analytics Dashboard** - Generate usage analytics, track performance trends, monitor resource utilization, provide optimization recommendations
6. **Developer Tools** - Provide debugging utilities, implement connection testing, create performance profiling, optimize development workflow

**Advanced Features**: Real-time performance monitoring, predictive analytics, automated optimization suggestions, comprehensive logging, alert management.

**Integration Support**: Application performance monitoring, CI/CD integration, team collaboration tools, documentation generation, troubleshooting guides.

**Output**: Comprehensive realtime monitoring with performance analytics, optimization recommendations, debugging tools, and developer documentation.

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
