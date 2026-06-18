---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/testing/write-tests.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\testing\write-tests.md
source_ext: .md
source_sha256: 10b874af5eb8497188f54e3eacbe6b64d2845d2a1d076e3467df5454e8083b53
text_sha256: 8aaf5e66799dae2718b48a49bc08905b14d8983276c787e63897c86a132cca78
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# write-tests.md

- Source: `claude-code-templates/cli-tool/components/commands/testing/write-tests.md`
- Extract: `text`
- SHA256: `10b874af5eb8497188f54e3eacbe6b64d2845d2a1d076e3467df5454e8083b53`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [target-file] | [test-type] | --unit | --integration | --e2e | --component
description: Write comprehensive unit and integration tests with proper mocking and coverage
---

# Write Tests

Write comprehensive unit and integration tests with framework-specific best practices: **$ARGUMENTS**

## Current Testing Context

- Test framework: !`find . -name "jest.config.*" -o -name "*.test.*" | head -1 && echo "Jest/Vitest detected" || echo "Detect framework"`
- Target file: Analysis of $ARGUMENTS for test requirements and complexity
- Project patterns: !`find . -name "*.test.*" -o -name "*.spec.*" | head -3` existing test patterns
- Coverage setup: !`grep -l "coverage" package.json jest.config.* 2>/dev/null | head -1 || echo "Setup needed"`

## Task

Execute comprehensive test writing with framework-specific optimizations and best practices:

**Test Focus**: Use $ARGUMENTS to specify target file, unit tests, integration tests, e2e tests, or component tests

**Test Writing Framework**:

1. **Code Analysis** - Analyze target code structure, identify testable functions, assess dependency complexity, evaluate edge cases
2. **Test Strategy Design** - Plan test organization, design test hierarchies, identify mock requirements, optimize test isolation
3. **Framework Integration** - Setup framework-specific patterns, configure test utilities, implement proper assertions, optimize test performance
4. **Mock Implementation** - Design dependency mocks, implement test doubles, create factory functions, setup async handling
5. **Test Case Generation** - Write unit tests, integration tests, edge cases, error scenarios, performance tests, snapshot tests
6. **Quality Assurance** - Ensure test maintainability, optimize execution speed, validate coverage, implement proper cleanup

**Advanced Features**: Property-based testing, contract testing, visual regression testing, accessibility testing, performance benchmarking.

**Framework Support**: Jest/Vitest, React Testing Library, Vue Test Utils, Angular TestBed, Cypress, Playwright integration.

**Output**: Comprehensive test suite with unit tests, integration tests, proper mocking, test utilities, and coverage optimization.

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
