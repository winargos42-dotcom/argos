---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/setup-monitoring-observability.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\setup-monitoring-observability.md
source_ext: .md
source_sha256: 8bb375b0c5114a3997478aa526d49b66c8922d09e6ebf895ec7afcff1b3bb2d3
text_sha256: f119a3813adf13caf689fd66cb886d4188298ea3672a0db2181e46c945181e47
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# setup-monitoring-observability.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/setup-monitoring-observability.md`
- Extract: `text`
- SHA256: `8bb375b0c5114a3997478aa526d49b66c8922d09e6ebf895ec7afcff1b3bb2d3`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [monitoring-type] | --metrics | --logging | --tracing | --full-stack
description: Setup comprehensive monitoring and observability with metrics, logging, tracing, and alerting
---

# Setup Monitoring & Observability

Setup comprehensive monitoring and observability infrastructure: **$ARGUMENTS**

## Current Application State

- Application type: @package.json or @requirements.txt (detect framework and services)
- Existing monitoring: !`find . -name "*prometheus*" -o -name "*grafana*" -o -name "*jaeger*" | wc -l`
- Infrastructure: @docker-compose.yml or @kubernetes/ or cloud platform detection
- Logging setup: !`grep -r "winston\|logging\|console.log" src/ 2>/dev/null | wc -l`

## Task

Implement production-ready monitoring and observability with comprehensive insights:

**Monitoring Type**: Use $ARGUMENTS to focus on metrics, logging, distributed tracing, or complete observability stack

**Observability Stack**:
1. **Metrics Collection** - Application metrics, infrastructure monitoring, business KPIs, custom dashboards
2. **Logging Infrastructure** - Centralized logging, structured logs, log aggregation, search capabilities
3. **Distributed Tracing** - Request tracing, performance analysis, bottleneck identification, service dependencies
4. **Alerting System** - Smart alerts, escalation policies, notification channels, incident management
5. **Performance Monitoring** - APM integration, real-user monitoring, synthetic monitoring, SLA tracking
6. **Analytics & Reports** - Usage analytics, performance trends, capacity planning, business insights

**Platform Integration**: Prometheus, Grafana, ELK Stack, Jaeger, DataDog, New Relic, cloud-native solutions.

**Production Features**: High availability, data retention policies, security controls, cost optimization.

**Output**: Complete observability platform with real-time monitoring, intelligent alerting, and comprehensive analytics dashboards.

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
