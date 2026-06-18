---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/testing/setup-comprehensive-testing.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\testing\setup-comprehensive-testing.md
source_ext: .md
source_sha256: 7407ef7398db8f1d3b49ad77668c7d195f39321feed273564676a03366e8e6c1
text_sha256: 9ffc00695894c2c2556f53252752720198ac3b1eb1381dad8bbc4dcccc3058fe
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# setup-comprehensive-testing.md

- Source: `claude-code-templates/cli-tool/components/commands/testing/setup-comprehensive-testing.md`
- Extract: `text`
- SHA256: `7407ef7398db8f1d3b49ad77668c7d195f39321feed273564676a03366e8e6c1`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [scope] | --unit | --integration | --e2e | --visual | --performance | --full-stack
description: Setup complete testing infrastructure with framework configuration and CI integration
---

# Setup Comprehensive Testing

Setup complete testing infrastructure with multi-layer testing strategy: **$ARGUMENTS**

## Current Testing Infrastructure

- Project type: !`[ -f package.json ] && echo "Node.js" || [ -f requirements.txt ] && echo "Python" || [ -f pom.xml ] && echo "Java" || echo "Multi-language"`
- Existing tests: !`find . -name "*.test.*" -o -name "*.spec.*" | wc -l` test files
- CI system: !`find . -name ".github" -o -name ".gitlab-ci.yml" -o -name "Jenkinsfile" | head -1 || echo "No CI detected"`
- Framework: !`grep -l "jest\\|vitest\\|pytest\\|junit" package.json requirements.txt pom.xml 2>/dev/null | head -1 || echo "Detect framework"`

## Task

Implement comprehensive testing infrastructure with multi-layer testing strategy:

**Setup Scope**: Use $ARGUMENTS to focus on unit, integration, e2e, visual, performance testing, or full-stack implementation

**Comprehensive Testing Framework**:

1. **Testing Strategy Design** - Analyze project requirements, define testing pyramid, plan coverage goals, optimize testing investment
2. **Unit Testing Setup** - Configure primary framework (Jest, Vitest, pytest), setup test runners, implement test utilities, optimize execution
3. **Integration Testing** - Setup integration test framework, configure test databases, implement API testing, optimize test isolation
4. **E2E Testing Configuration** - Setup browser testing (Cypress, Playwright), configure test environments, implement page objects
5. **Visual & Performance Testing** - Setup visual regression testing, configure performance benchmarks, implement accessibility testing
6. **CI/CD Integration** - Configure automated test execution, setup parallel testing, implement quality gates, optimize pipeline performance

**Advanced Features**: Contract testing, chaos engineering, load testing, security testing, cross-browser testing, mobile testing.

**Infrastructure Quality**: Test reliability, execution performance, maintainability, scalability, cost optimization.

**Output**: Complete testing infrastructure with configured frameworks, CI integration, quality metrics, and maintenance workflows.

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
