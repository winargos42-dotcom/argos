---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/workflow-automation/n8n/n8n-expression-syntax/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\workflow-automation\n8n\n8n-expression-syntax\README.md
source_ext: .md
source_sha256: aa7124e69077976b0ddaf309d7158c467908ad3bbfc4b1784321c4d602966b26
text_sha256: 30eef969ebe6b5c8fff8f9f9d99dd195f6c5e5390b26e143f508a7484030134e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/workflow-automation/n8n/n8n-expression-syntax/README.md`
- Extract: `text`
- SHA256: `aa7124e69077976b0ddaf309d7158c467908ad3bbfc4b1784321c4d602966b26`

## Content

# n8n Expression Syntax

Expert guide for writing correct n8n expressions in workflows.

---

## Purpose

Teaches correct n8n expression syntax ({{ }} patterns) and fixes common mistakes, especially the critical webhook data structure gotcha.

## Activates On

- expression
- {{}} syntax
- $json, $node, $now, $env
- webhook data
- troubleshoot expression error
- undefined in workflow

## File Count

4 files, ~450 lines total

## Dependencies

**n8n-mcp tools**:
- None directly (syntax knowledge skill)
- Works with n8n-mcp validation tools

**Related skills**:
- n8n Workflow Patterns (uses expressions in examples)
- n8n MCP Tools Expert (validates expressions)
- n8n Node Configuration (when expressions are needed)

## Coverage

### Core Topics
- Expression format ({{ }})
- Core variables ($json, $node, $now, $env)
- **Webhook data structure** ($json.body.*)
- When NOT to use expressions (Code nodes)

### Common Patterns
- Accessing nested fields
- Referencing other nodes
- Array and object access
- Date/time formatting
- String manipulation

### Error Prevention
- 15 common mistakes with fixes
- Quick reference table
- Debugging process

## Evaluations

4 scenarios (100% coverage expected):
1. **eval-001**: Missing curly braces
2. **eval-002**: Webhook body data access (critical!)
3. **eval-003**: Code node vs expression confusion
4. **eval-004**: Node reference syntax

## Key Features

✅ **Critical Gotcha Highlighted**: Webhook data under `.body`
✅ **Real Examples**: From MCP testing and real templates
✅ **Quick Fixes Table**: Fast reference for common errors
✅ **Code vs Expression**: Clear distinction
✅ **Comprehensive**: Covers 95% of expression use cases

## Files

- **SKILL.md** (285 lines) - Main content with all essential knowledge
- **COMMON_MISTAKES.md** (380 lines) - Complete error catalog with 15 common mistakes
- **EXAMPLES.md** (450 lines) - 10 real working examples
- **README.md** (this file) - Skill metadata

## Success Metrics

**Expected outcomes**:
- Users correctly wrap expressions in {{ }}
- Zero webhook `.body` access errors
- No expressions used in Code nodes
- Correct $node reference syntax

## Last Updated

2025-10-20

---

**Part of**: n8n-skills repository
**Conceived by**: Romuald Członkowski - [www.aiadvisors.pl/en](https://www.aiadvisors.pl/en)

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
