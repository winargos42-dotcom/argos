---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/team/team-velocity-tracker.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\team\team-velocity-tracker.md
source_ext: .md
source_sha256: 37c2f75f4548e90e9375fd06b7bde699c49bf83a356bb1a9f33f16f37ec964b3
text_sha256: eb84c51bd496352bb47b752250b998cbe66bfd588710b1dd58930528f6c70f72
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# team-velocity-tracker.md

- Source: `claude-code-templates/cli-tool/components/commands/team/team-velocity-tracker.md`
- Extract: `text`
- SHA256: `37c2f75f4548e90e9375fd06b7bde699c49bf83a356bb1a9f33f16f37ec964b3`

## Content

---
allowed-tools: Read, Bash, Glob, Grep
argument-hint: [analysis-period] | --sprint | --monthly | --quarterly | --trend-analysis
description: Track and analyze team velocity with predictive forecasting and performance optimization recommendations
---

# Team Velocity Tracker

Track team velocity patterns with predictive forecasting and performance optimization: **$ARGUMENTS**

## Current Velocity Context

- Sprint velocity: !`git log --oneline --since='2 weeks ago' | wc -l` commits per current sprint
- Team consistency: Analysis of velocity stability across recent sprints
- Linear tracking: Sprint point completion rates and story delivery metrics
- Capacity factors: Team size changes, availability, and skill development impact

## Task

Execute comprehensive velocity tracking with predictive analytics and optimization recommendations:

**Analysis Period**: Use $ARGUMENTS to focus on sprint velocity, monthly trends, quarterly patterns, or comprehensive trend analysis

**Velocity Tracking Framework**:
1. **Historical Velocity Analysis** - Extract sprint completion data, analyze story point delivery, calculate team throughput, identify performance patterns
2. **Consistency Assessment** - Measure velocity stability, identify variance patterns, assess predictability factors, evaluate planning accuracy
3. **Capacity Correlation** - Analyze team size impact, assess skill level effects, evaluate availability constraints, measure external factor influence
4. **Predictive Forecasting** - Generate velocity projections, predict sprint outcomes, estimate delivery timelines, calculate confidence intervals
5. **Performance Optimization** - Identify improvement opportunities, recommend capacity adjustments, suggest process enhancements, optimize team composition
6. **Quality Integration** - Correlate velocity with quality metrics, assess technical debt impact, evaluate sustainable pace, measure team satisfaction

**Advanced Features**: Monte Carlo forecasting, velocity trend decomposition, capacity planning optimization, performance anomaly detection, sustainable pace analysis.

**Predictive Analytics**: Sprint outcome predictions, delivery timeline forecasting, capacity requirement planning, performance trend analysis.

**Output**: Comprehensive velocity analysis with predictive forecasts, optimization recommendations, capacity planning insights, and sustainable performance strategies.

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
