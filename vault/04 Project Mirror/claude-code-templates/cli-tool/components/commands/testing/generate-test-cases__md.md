---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/testing/generate-test-cases.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\testing\generate-test-cases.md
source_ext: .md
source_sha256: 3698dfa93370bcdd7b40beabbbadaac3f25aedc394a9dc6aa83ebfe65e71db2f
text_sha256: fe04ce2809d417d01f2583c18dce4191797a5a648b2eeeaaf01e21bd2b6aa400
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# generate-test-cases.md

- Source: `claude-code-templates/cli-tool/components/commands/testing/generate-test-cases.md`
- Extract: `text`
- SHA256: `3698dfa93370bcdd7b40beabbbadaac3f25aedc394a9dc6aa83ebfe65e71db2f`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [target] | [scope] | --unit | --integration | --edge-cases | --automatic
description: Generate comprehensive test cases with automatic analysis and coverage optimization
---

# Generate Test Cases

Generate comprehensive test cases with automatic analysis and intelligent coverage: **$ARGUMENTS**

## Current Test Generation Context

- Target code: Analysis of $ARGUMENTS for test case generation requirements
- Test framework: !`find . -name "jest.config.*" -o -name "*.test.*" | head -1 && echo "Jest/Vitest detected" || echo "Detect framework"`
- Code complexity: !`find . -name "*.js" -o -name "*.ts" -o -name "*.py" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}' || echo "0"` lines of code
- Existing patterns: !`find . -name "*.test.*" -o -name "*.spec.*" | head -3` test file patterns

## Task

Execute intelligent test case generation with comprehensive coverage and optimization:

**Generation Scope**: Use $ARGUMENTS to specify target file, unit tests, integration tests, edge cases, or automatic comprehensive generation

**Test Case Generation Framework**:

1. **Code Structure Analysis** - Parse function signatures, analyze control flow, identify branching paths, assess complexity metrics
2. **Test Pattern Recognition** - Analyze existing test patterns, identify testing conventions, extract reusable patterns, optimize consistency
3. **Input Space Analysis** - Identify parameter domains, analyze boundary conditions, discover edge cases, evaluate error conditions
4. **Test Case Design** - Generate positive test cases, negative test cases, boundary value tests, equivalence class tests
5. **Mock Strategy Planning** - Identify external dependencies, design mock implementations, create test data factories, optimize test isolation
6. **Coverage Optimization** - Ensure path coverage, optimize test efficiency, eliminate redundancy, maximize testing value

**Advanced Features**: Automatic edge case discovery, intelligent input generation, test data synthesis, coverage gap analysis, performance test generation.

**Quality Assurance**: Test maintainability, execution performance, assertion quality, debugging effectiveness.

**Output**: Comprehensive test case suite with optimized coverage, intelligent mocking, proper assertions, and maintenance guidelines.

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
