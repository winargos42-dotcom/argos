---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/testing/test-quality-analyzer.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\testing\test-quality-analyzer.md
source_ext: .md
source_sha256: d971c10fa498d6900db098db8ff03b1eab72083cb11df8f80bb1983e9131d8ef
text_sha256: 0d222698d00399c0f6ad4cf5a2c5916ef81b2c234e4278d3abf8321e60037a2c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# test-quality-analyzer.md

- Source: `claude-code-templates/cli-tool/components/commands/testing/test-quality-analyzer.md`
- Extract: `text`
- SHA256: `d971c10fa498d6900db098db8ff03b1eab72083cb11df8f80bb1983e9131d8ef`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [analysis-type] | --coverage-quality | --test-effectiveness | --maintainability | --performance-analysis
description: Analyze test suite quality with comprehensive metrics and improvement recommendations
---

# Test Quality Analyzer

Analyze test suite quality with comprehensive metrics and actionable improvement insights: **$ARGUMENTS**

## Current Quality Context

- Test coverage: !`find . -name "coverage" -type d | head -1 && echo "Coverage data available" || echo "No coverage data"`
- Test files: !`find . -name "*.test.*" -o -name "*.spec.*" | wc -l` test files
- Test complexity: Analysis of test suite maintainability and effectiveness patterns
- Performance metrics: Current test execution times and resource utilization

## Task

Execute comprehensive test quality analysis with improvement recommendations and optimization strategies:

**Analysis Type**: Use $ARGUMENTS to focus on coverage quality, test effectiveness, maintainability analysis, or performance analysis

**Test Quality Analysis Framework**:

1. **Coverage Quality Assessment** - Analyze coverage depth, evaluate coverage quality, assess edge case handling, identify coverage gaps
2. **Test Effectiveness Evaluation** - Measure defect detection capability, analyze test reliability, assess assertion quality, evaluate test value
3. **Maintainability Analysis** - Evaluate test code quality, analyze test organization, assess refactoring needs, optimize test structure
4. **Performance Assessment** - Analyze execution performance, identify bottlenecks, optimize test speed, reduce resource consumption
5. **Anti-Pattern Detection** - Identify testing anti-patterns, detect flaky tests, analyze test smells, recommend corrections
6. **Quality Metrics Tracking** - Implement quality scoring, track improvement trends, configure quality gates, optimize quality processes

**Advanced Features**: AI-powered quality assessment, predictive quality modeling, automated improvement suggestions, quality trend analysis, benchmark comparison.

**Quality Insights**: Test ROI analysis, quality correlation analysis, maintenance cost assessment, effectiveness benchmarking.

**Output**: Comprehensive quality analysis with detailed metrics, improvement recommendations, optimization strategies, and quality tracking framework.

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
