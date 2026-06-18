---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/testing/test-coverage.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\testing\test-coverage.md
source_ext: .md
source_sha256: 61d79fb2e54cb63c0017bb1c02aad69c1710ac245d5d7af86455193b01a98338
text_sha256: 12776142c1fc2c05b6d15a73e97748c55528aaaf8aef64e336bd604dca66db89
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# test-coverage.md

- Source: `claude-code-templates/cli-tool/components/commands/testing/test-coverage.md`
- Extract: `text`
- SHA256: `61d79fb2e54cb63c0017bb1c02aad69c1710ac245d5d7af86455193b01a98338`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [coverage-type] | --line | --branch | --function | --statement | --report
description: Analyze and improve test coverage with comprehensive reporting and gap identification
---

# Test Coverage

Analyze and improve test coverage with detailed reporting and gap analysis: **$ARGUMENTS**

## Current Coverage Context

- Test framework: !`find . -name "jest.config.*" -o -name ".nycrc*" -o -name "coverage.xml" | head -1 || echo "Detect framework"`
- Coverage tools: !`npm ls nyc jest @jest/core 2>/dev/null | grep -E "nyc|jest" | head -2 || echo "No JS coverage tools"`
- Existing coverage: !`find . -name "coverage" -type d | head -1 && echo "Coverage data exists" || echo "No coverage data"`
- Test files: !`find . -name "*.test.*" -o -name "*.spec.*" | wc -l` test files

## Task

Execute comprehensive coverage analysis with improvement recommendations and reporting:

**Coverage Type**: Use $ARGUMENTS to focus on line coverage, branch coverage, function coverage, statement coverage, or comprehensive reporting

**Coverage Analysis Framework**:

1. **Coverage Tool Setup** - Configure appropriate tools (Jest, NYC, Istanbul, Coverage.py, JaCoCo), setup collection settings, optimize performance, enable reporting
2. **Coverage Measurement** - Generate line coverage, branch coverage, function coverage, statement coverage reports, identify uncovered code paths
3. **Gap Analysis** - Identify critical uncovered paths, analyze coverage quality, assess business logic coverage, evaluate edge case handling
4. **Threshold Management** - Configure coverage thresholds, implement quality gates, setup trend monitoring, enforce minimum standards
5. **Reporting & Visualization** - Generate detailed reports, create coverage dashboards, implement trend analysis, setup automated notifications
6. **Improvement Planning** - Prioritize coverage gaps, recommend test additions, identify refactoring opportunities, plan coverage enhancement

**Advanced Features**: Differential coverage analysis, coverage trend monitoring, integration with code review, automated coverage alerts, performance impact assessment.

**Quality Insights**: Coverage quality assessment, test effectiveness analysis, maintainability correlation, risk area identification.

**Output**: Comprehensive coverage analysis with detailed reports, gap identification, improvement recommendations, and quality metrics tracking.

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
