---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/team/estimate-assistant.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\team\estimate-assistant.md
source_ext: .md
source_sha256: 05d32fe5b1642b6eb467f08371ca67049bd209517cd9f190c74ba7617fbb0486
text_sha256: 96a8968dd74fbde4bb4463a077f584821e50dd7734e94887e24ca2e13e823a53
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# estimate-assistant.md

- Source: `claude-code-templates/cli-tool/components/commands/team/estimate-assistant.md`
- Extract: `text`
- SHA256: `05d32fe5b1642b6eb467f08371ca67049bd209517cd9f190c74ba7617fbb0486`

## Content

---
allowed-tools: Read, Bash, Glob, Grep
argument-hint: [task-description] | --historical | --complexity-analysis | --team-velocity | --confidence-intervals
description: Generate accurate task estimates using historical data, complexity analysis, and team velocity metrics
---

# Estimate Assistant

Generate data-driven task estimates with confidence intervals and accuracy tracking: **$ARGUMENTS**

## Current Estimation Context

- Team velocity: !`git log --oneline --since='1 month ago' | wc -l` commits in last month
- Historical data: Git history analysis for similar task completion patterns
- Code complexity: !`find . -name "*.js" -o -name "*.ts" -o -name "*.py" | head -5 | xargs wc -l 2>/dev/null | tail -1 || echo "No code files"`
- Sprint tracking: Linear task completion times and estimate accuracy

## Task

Execute comprehensive task estimation with historical analysis and confidence modeling:

**Estimation Focus**: Use $ARGUMENTS for task description analysis, historical pattern matching, complexity assessment, or team velocity calculation

**Estimation Framework**:
1. **Historical Pattern Analysis** - Analyze similar past tasks, extract completion time patterns, identify velocity trends, calculate accuracy metrics
2. **Complexity Assessment** - Evaluate technical complexity, assess scope uncertainty, identify risk factors, estimate effort distribution
3. **Team Velocity Integration** - Calculate sprint velocity, analyze individual capacity, assess team expertise, factor in availability constraints
4. **Confidence Modeling** - Generate confidence intervals, assess estimation uncertainty, identify risk factors, provide accuracy ranges
5. **Calibration Analysis** - Compare past estimates vs actuals, identify systematic biases, calculate estimation accuracy, improve prediction models
6. **Context Integration** - Factor in current sprint load, assess team familiarity, evaluate external dependencies, integrate deadline pressure

**Advanced Features**: Multi-point estimation, Monte Carlo simulation, reference class forecasting, estimation accuracy tracking, bias correction algorithms.

**Quality Metrics**: Estimation confidence levels, accuracy historical trends, velocity stability, complexity correlation analysis.

**Output**: Data-driven estimates with confidence intervals, historical accuracy metrics, risk assessment, and calibration recommendations.

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
