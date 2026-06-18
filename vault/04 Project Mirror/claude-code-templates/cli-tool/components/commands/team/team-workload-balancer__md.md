---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/team/team-workload-balancer.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\team\team-workload-balancer.md
source_ext: .md
source_sha256: 89a84c1511a633bc999da8508b77b8459a9e14d2c5937528bd0c21f64002e0da
text_sha256: 5359fc295f7eec09fbae2cc3a4ef0cd72cf3b38cb42a25f68760d8114cb8b52e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# team-workload-balancer.md

- Source: `claude-code-templates/cli-tool/components/commands/team/team-workload-balancer.md`
- Extract: `text`
- SHA256: `89a84c1511a633bc999da8508b77b8459a9e14d2c5937528bd0c21f64002e0da`

## Content

---
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [analysis-type] | --current-workload | --skill-matching | --capacity-planning | --assignment-optimization
description: Analyze and optimize team workload distribution with skill matching and capacity planning
---

# Team Workload Balancer

Analyze and optimize team workload distribution with intelligent assignment recommendations: **$ARGUMENTS**

## Current Team Context

- Team size: !`git log --format='%ae' --since='1 month ago' | sort -u | wc -l` active team members
- Active tasks: Linear MCP query for current sprint tasks and assignments
- Recent activity: !`git log --oneline --since='1 week ago' | wc -l` commits in last week
- Capacity metrics: Analysis of team velocity and individual contribution patterns

## Task

Execute comprehensive workload analysis with intelligent assignment optimization:

**Analysis Type**: Use $ARGUMENTS to focus on current workload assessment, skill matching, capacity planning, or assignment optimization

**Workload Balancing Framework**:
1. **Current Workload Assessment** - Analyze task distribution, evaluate individual capacity, assess deadline pressure, identify overloaded team members
2. **Skill Matching Analysis** - Map team member expertise, identify skill gaps, assess learning opportunities, optimize skill utilization
3. **Capacity Planning** - Calculate available capacity, project future workload, plan skill development, optimize resource allocation
4. **Performance Integration** - Analyze historical performance, identify productivity patterns, assess collaboration effectiveness, factor in availability constraints
5. **Assignment Optimization** - Generate optimal task assignments, balance workload distribution, maximize skill utilization, minimize bottlenecks
6. **Risk Mitigation** - Identify single points of failure, plan cross-training, assess knowledge distribution, ensure backup coverage

**Advanced Features**: Predictive workload modeling, skill gap analysis, burnout prevention, performance-based assignment, dynamic rebalancing recommendations.

**Quality Metrics**: Workload distribution equity, skill utilization efficiency, team satisfaction indicators, delivery predictability measures.

**Output**: Comprehensive workload analysis with optimized assignments, capacity recommendations, skill development plans, and team health insights.

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
