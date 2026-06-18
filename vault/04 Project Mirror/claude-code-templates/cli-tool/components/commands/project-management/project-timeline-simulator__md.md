---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/project-timeline-simulator.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\project-timeline-simulator.md
source_ext: .md
source_sha256: 9f7636a52c1a4a2e9951944f187a9eb0d20b0ac5037fd59c3271aaddad287010
text_sha256: 5511a7aa50fd79d543fd1fc8b9aea1cbba41e1c4ad7e86d1b21ceab308b2ad05
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# project-timeline-simulator.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/project-timeline-simulator.md`
- Extract: `text`
- SHA256: `9f7636a52c1a4a2e9951944f187a9eb0d20b0ac5037fd59c3271aaddad287010`

## Content

---
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [project-type] | --duration | --team-size | --risk-level
description: Simulate project outcomes with variable modeling, risk assessment, and resource optimization
---

# Project Timeline Simulator

Simulate project outcomes with comprehensive variable modeling and risk assessment: **$ARGUMENTS**

## Current Project Context

- Project type: Based on $ARGUMENTS or codebase analysis
- Team capacity: !`git shortlog -sn --since="90 days ago" | wc -l` contributors
- Velocity data: !`git log --oneline --since="30 days ago" | wc -l` commits/month
- Risk indicators: @RISKS.md or project documentation

## Task

Generate comprehensive project timeline simulations with multiple scenarios:

**Simulation Framework**:
1. **Variable Modeling** - Team capacity, skill levels, external dependencies, technical complexity
2. **Scenario Generation** - Baseline, optimistic, pessimistic, and disruption scenarios
3. **Risk Assessment** - Technical, resource, business, and external risk factors
4. **Resource Optimization** - Team allocation, budget distribution, timeline buffers
5. **Decision Points** - Milestone gates, adaptation triggers, contingency activation

**Output Deliverables**:
- Timeline prediction ranges with confidence intervals
- Critical path analysis and dependency mapping
- Risk-adjusted resource allocation recommendations
- Early warning indicators and decision triggers
- Monte Carlo simulation results with probability distributions

**Success Optimization**: Multi-objective optimization for time, quality, and resource efficiency.

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
