---
argos_import: project_file
source_path: claude-code-templates/cli-tool/templates/javascript-typescript/examples/react-app/.claude/commands/hooks.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\templates\javascript-typescript\examples\react-app\.claude\commands\hooks.md
source_ext: .md
source_sha256: 2a6f557253a91d46072d29a11c161c4aafc4495706e240c40c1b466d453161f8
text_sha256: dfa97d95b3a4df5c013f7727ec610fb1be6bd7cd950bd44ef5f1f645af8f0912
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# hooks.md

- Source: `claude-code-templates/cli-tool/templates/javascript-typescript/examples/react-app/.claude/commands/hooks.md`
- Extract: `text`
- SHA256: `2a6f557253a91d46072d29a11c161c4aafc4495706e240c40c1b466d453161f8`

## Content

# React Hooks

Create or optimize React hooks for $ARGUMENTS following project conventions.

## Task

Analyze the request and create appropriate React hooks:

1. **Examine existing hooks**: Check project for existing custom hooks patterns and conventions
2. **Identify hook type**: Determine if creating new custom hook, optimizing existing hook, or implementing specific hook pattern
3. **Check TypeScript usage**: Verify if project uses TypeScript and follow typing conventions
4. **Implement hook**: Create hook with proper:
   - Naming convention (use prefix)
   - TypeScript types and interfaces
   - Proper dependency arrays
   - Error handling
   - Performance optimizations
5. **Add tests**: Create comprehensive unit tests using project's testing framework
6. **Add documentation**: Include JSDoc comments and usage examples

## Common Hook Patterns

When creating hooks, consider these patterns based on the request:
- **Data fetching**: API calls, loading states, error handling
- **State management**: Local state, derived state, state persistence
- **Side effects**: Event listeners, timers, subscriptions
- **Context consumption**: Theme, auth, app state
- **Form handling**: Input management, validation, submission
- **Performance**: Memoization, debouncing, throttling

## Requirements

- Follow existing project hook conventions
- Use TypeScript if project uses it
- Include proper cleanup in useEffect
- Add error boundaries where appropriate
- Write tests that cover all hook functionality
- IMPORTANT: Always check existing hooks first to understand project patterns

## Notes

- Ask for clarification if the hook requirements are ambiguous
- Suggest optimizations for existing hooks if relevant
- Consider accessibility implications for UI-related hooks

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
