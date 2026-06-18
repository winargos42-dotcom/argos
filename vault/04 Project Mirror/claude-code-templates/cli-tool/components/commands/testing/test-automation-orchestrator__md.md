---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/testing/test-automation-orchestrator.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\testing\test-automation-orchestrator.md
source_ext: .md
source_sha256: 0c9be589199cfad1d75f01090049310c735343b370da87f1e30b4509560f03be
text_sha256: 748fded9ef75fb6139060db0970a9ff65e55b7bb66e836c92dfb623e2523ba9c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# test-automation-orchestrator.md

- Source: `claude-code-templates/cli-tool/components/commands/testing/test-automation-orchestrator.md`
- Extract: `text`
- SHA256: `0c9be589199cfad1d75f01090049310c735343b370da87f1e30b4509560f03be`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [orchestration-type] | --parallel | --sequential | --conditional | --pipeline-optimization
description: Orchestrate comprehensive test automation with intelligent execution and optimization
---

# Test Automation Orchestrator

Orchestrate intelligent test automation with execution optimization and resource management: **$ARGUMENTS**

## Current Orchestration Context

- Test suites: !`find . -name "*.test.*" -o -name "*.spec.*" | wc -l` test files across project
- Test frameworks: !`find . -name "jest.config.*" -o -name "cypress.config.*" -o -name "playwright.config.*" | wc -l` configured frameworks
- CI system: !`find . -name ".github" -o -name ".gitlab-ci.yml" | head -1 || echo "No CI detected"`
- Resource usage: Analysis of current test execution patterns and performance

## Task

Implement intelligent test orchestration with execution optimization and resource management:

**Orchestration Type**: Use $ARGUMENTS to focus on parallel execution, sequential execution, conditional testing, or pipeline optimization

**Test Orchestration Framework**:

1. **Test Discovery & Classification** - Analyze test suites, classify test types, assess execution requirements, optimize categorization
2. **Execution Strategy Design** - Design parallel execution strategies, implement intelligent batching, optimize resource allocation, configure conditional execution
3. **Dependency Management** - Analyze test dependencies, implement execution ordering, configure prerequisite validation, optimize dependency resolution
4. **Resource Optimization** - Configure parallel execution, implement resource pooling, optimize memory usage, design scalable execution
5. **Pipeline Integration** - Design CI/CD integration, implement stage orchestration, configure failure handling, optimize feedback loops
6. **Monitoring & Analytics** - Implement execution monitoring, configure performance tracking, design failure analysis, optimize reporting

**Advanced Features**: AI-driven test selection, predictive execution optimization, dynamic resource allocation, intelligent failure recovery, cost optimization.

**Quality Assurance**: Execution reliability, performance consistency, resource efficiency, maintainability optimization.

**Output**: Complete test orchestration system with optimized execution, intelligent resource management, comprehensive monitoring, and performance analytics.

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
