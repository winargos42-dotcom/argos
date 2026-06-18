---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/testing/add-property-based-testing.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\testing\add-property-based-testing.md
source_ext: .md
source_sha256: 17c12bd0db37deeb539862c2f28bc799f180ae4afb23ededb106397ed7dab4d7
text_sha256: cd6920f2913fc7f47d143e40a2a8b6cc6f5907d857868a11faf240b3c401ba52
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# add-property-based-testing.md

- Source: `claude-code-templates/cli-tool/components/commands/testing/add-property-based-testing.md`
- Extract: `text`
- SHA256: `17c12bd0db37deeb539862c2f28bc799f180ae4afb23ededb106397ed7dab4d7`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [language] | --javascript | --python | --java | --haskell | --rust | --clojure
description: Implement property-based testing with framework selection and invariant identification
---

# Add Property-Based Testing

Implement property-based testing framework with invariant analysis and test generation: **$ARGUMENTS**

## Current Testing Context

- Language: !`find . -name "*.js" -o -name "*.ts" | head -1 >/dev/null && echo "JavaScript/TypeScript" || find . -name "*.py" | head -1 >/dev/null && echo "Python" || echo "Multi-language"`
- Test framework: !`find . -name "jest.config.*" -o -name "pytest.ini" | head -1 || echo "Detect framework"`
- Mathematical functions: Analysis of codebase for property-testable functions
- Business logic: Identification of invariants and properties in domain logic

## Task

Implement comprehensive property-based testing with invariant analysis and automated test generation:

**Language Focus**: Use $ARGUMENTS to specify JavaScript, Python, Java, Haskell, Rust, Clojure, or auto-detect from codebase

**Property-Based Testing Framework**:

1. **Framework Selection** - Choose appropriate tool (fast-check, Hypothesis, QuickCheck, proptest), install dependencies, configure integration
2. **Property Identification** - Analyze mathematical properties, identify business invariants, discover symmetries, evaluate round-trip properties
3. **Generator Design** - Create custom data generators, implement constraint-based generation, design composite generators, optimize generation strategies
4. **Property Implementation** - Write property tests, implement preconditions, design postconditions, create invariant checks
5. **Shrinking Configuration** - Configure test case shrinking, optimize failure minimization, implement custom shrinkers, enhance debugging
6. **Integration & Reporting** - Integrate with existing test suite, configure reporting, setup CI integration, optimize execution performance

**Advanced Features**: Stateful property testing, model-based testing, custom generators, parallel property execution, performance property testing.

**Quality Assurance**: Property completeness analysis, edge case coverage, performance optimization, maintainability assessment.

**Output**: Complete property-based testing setup with identified properties, custom generators, integrated test suite, and performance optimization.

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
