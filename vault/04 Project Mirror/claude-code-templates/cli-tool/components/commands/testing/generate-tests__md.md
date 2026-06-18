---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/testing/generate-tests.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\testing\generate-tests.md
source_ext: .md
source_sha256: 5dd031a4a451e6ba64fb4559e11e16fe56ae2d46d09f5a6ee867da19712259c0
text_sha256: 207c1854888e489279f60a34dd7478c1515116c00131aab8dc1c2eb4df66b009
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# generate-tests.md

- Source: `claude-code-templates/cli-tool/components/commands/testing/generate-tests.md`
- Extract: `text`
- SHA256: `5dd031a4a451e6ba64fb4559e11e16fe56ae2d46d09f5a6ee867da19712259c0`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [file-path] | [component-name]
description: Generate a complete test file for a specified source file or component. Use when the user explicitly asks to write, create, or generate tests for a specific file.
---

# Generate Tests

Generate comprehensive test suite for: $ARGUMENTS

## Current Testing Setup

- Test framework: !`cat package.json 2>/dev/null | grep -E '"jest"|"vitest"|"mocha"|"jasmine"' | head -3 || cat jest.config.* vitest.config.* 2>/dev/null | head -5 || echo "Framework not detected"`
- Existing tests: !`find . -name "*.test.*" -o -name "*.spec.*" | head -5`
- Test coverage: !`npm run test:coverage 2>/dev/null || echo "No coverage script"`
- Target: if $ARGUMENTS is a file path, read it with @$ARGUMENTS; if it is a component name, search for it with Grep before writing tests

## Test Generation Framework

1. **Analyze** the target file/component structure — identify all exported functions, classes, methods, and their signatures
2. **Strategy** — examine existing test patterns in the project; choose unit vs integration scope; identify critical paths and error scenarios
3. **Mock Design** — map all external dependencies (I/O, APIs, timers, dates); create factories for test data; plan cleanup for async operations
4. **Unit Tests** — write isolated tests per function/method covering happy path, edge cases, and error conditions; follow AAA pattern (Arrange, Act, Assert)
5. **Integration Tests** — test component interactions, API layers with mocked responses, and end-to-end user workflows where applicable
6. **Quality Check** — verify naming describes behavior not implementation; confirm 80%+ coverage on critical business logic; ensure test isolation

## Framework-Specific Guidance

- **React**: Component testing with React Testing Library; test user interactions and rendering
- **Vue**: Component testing with Vue Test Utils; test props, events, and slots
- **Angular**: Component and service testing with TestBed; test dependency injection
- **Node.js**: API endpoint and middleware testing; test request/response cycles
- **Python**: `pytest` with fixtures, `unittest.mock` for patching, `pytest-cov` for coverage
- **Go**: Table-driven tests in `_test.go` files, `testify/assert` for assertions, subtests via `t.Run()`
- **Rust**: `#[cfg(test)]` modules, `#[test]` attributes, `mockall` for mocking

## Best Practices

- Follow AAA pattern (Arrange, Act, Assert)
- 80%+ coverage; prioritize critical business logic and error paths
- Mock external I/O; use factories for test data
- Naming: describe what the function does, not implementation details

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
