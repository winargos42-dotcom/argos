---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/testing/setup-load-testing.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\testing\setup-load-testing.md
source_ext: .md
source_sha256: c8444918944fb2eced2988cd3e97fb09d91e0ed57a2d5065cb0e9e98053107f0
text_sha256: e30de07ba85e5f8d630bf7d02a5ed967eb4f9eaacfd70b6bc330e66f833ece97
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# setup-load-testing.md

- Source: `claude-code-templates/cli-tool/components/commands/testing/setup-load-testing.md`
- Extract: `text`
- SHA256: `c8444918944fb2eced2988cd3e97fb09d91e0ed57a2d5065cb0e9e98053107f0`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [testing-type] | --capacity | --stress | --spike | --endurance | --volume
description: Configure comprehensive load testing with performance metrics and bottleneck identification
---

# Setup Load Testing

Configure comprehensive load testing with performance analysis and bottleneck identification: **$ARGUMENTS**

## Current Performance Context

- Application type: !`find . -name "server.js" -o -name "app.py" -o -name "main.go" | head -1 && echo "Server application" || echo "Detect app type"`
- API endpoints: !`grep -r "app\\.get\\|app\\.post\\|@RequestMapping" . 2>/dev/null | wc -l` detected endpoints
- Database: !`find . -name "*.sql" -o -name "database.js" | head -1 && echo "Database detected" || echo "No database files"`
- Current monitoring: !`find . -name "prometheus.yml" -o -name "newrelic.js" | head -1 || echo "No monitoring detected"`

## Task

Implement comprehensive load testing with performance optimization and bottleneck analysis:

**Testing Type**: Use $ARGUMENTS to focus on capacity planning, stress testing, spike testing, endurance testing, or volume testing

**Load Testing Framework**:

1. **Strategy & Requirements** - Analyze application architecture, define testing objectives, determine scenarios, identify performance metrics
2. **Tool Selection & Setup** - Choose appropriate tools (k6, Artillery, JMeter, Gatling), install dependencies, configure environments
3. **Test Scenario Design** - Create realistic user scenarios, implement API test scripts, configure data generation, design load patterns
4. **Performance Metrics** - Configure response time monitoring, throughput measurement, error rate tracking, resource utilization monitoring
5. **Infrastructure Setup** - Configure test environments, setup monitoring dashboards, implement result collection, optimize test execution
6. **Analysis & Optimization** - Identify performance bottlenecks, analyze resource constraints, recommend optimizations, track improvements

**Advanced Features**: Distributed load generation, real-time monitoring, automated performance regression detection, CI/CD integration, chaos engineering.

**Quality Assurance**: Test reliability, result accuracy, environment consistency, monitoring completeness.

**Output**: Complete load testing setup with configured scenarios, performance monitoring, bottleneck analysis, and optimization recommendations.

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
