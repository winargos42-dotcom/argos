---
argos_import: project_file
source_path: claude-code-templates/cli-tool/templates/javascript-typescript/examples/react-app/.claude/commands/state-management.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\templates\javascript-typescript\examples\react-app\.claude\commands\state-management.md
source_ext: .md
source_sha256: a5a034db43d6ead352428363effb915823c79090e967dcef347b3bc752f42f5c
text_sha256: 473be148b662a84cfc4d11be35308f564cd75284701b8e4cc0a41266404fdbef
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# state-management.md

- Source: `claude-code-templates/cli-tool/templates/javascript-typescript/examples/react-app/.claude/commands/state-management.md`
- Extract: `text`
- SHA256: `a5a034db43d6ead352428363effb915823c79090e967dcef347b3bc752f42f5c`

## Content

# React State Management

Implement state management solution for $ARGUMENTS following project conventions.

## Task

Set up or optimize state management based on the requirements:

1. **Analyze current setup**: Check existing state management approach and project structure
2. **Determine solution**: Based on requirements, choose appropriate state management:
   - Context API for simple, localized state
   - Redux Toolkit for complex, global state
   - Zustand for lightweight global state
   - Custom hooks for component-level state
3. **Examine dependencies**: Check package.json for existing state management libraries
4. **Implement solution**: Create store, providers, and hooks with proper TypeScript types
5. **Set up middleware**: Add devtools, persistence, or other middleware as needed
6. **Create typed hooks**: Generate properly typed selectors and dispatch hooks
7. **Add tests**: Write unit tests for state logic and reducers
8. **Update providers**: Integrate with app's provider hierarchy

## Implementation Requirements

- Follow project's TypeScript conventions
- Use existing state management patterns if present
- Create proper type definitions for state shape
- Include error handling and loading states
- Add proper debugging setup (devtools)
- Consider performance optimizations (selectors, memoization)

## State Management Selection Guide

Choose based on complexity:
- **Simple state**: React hooks + Context API
- **Medium complexity**: Zustand or custom hooks
- **Complex state**: Redux Toolkit with RTK Query
- **Form state**: React Hook Form or Formik

## Important Notes

- ALWAYS check existing state management first
- Don't install new dependencies without asking
- Follow project's folder structure for state files
- Consider server state vs client state separation
- Add proper TypeScript types for all state interfaces

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
