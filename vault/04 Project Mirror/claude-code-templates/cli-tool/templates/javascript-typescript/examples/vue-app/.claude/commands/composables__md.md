---
argos_import: project_file
source_path: claude-code-templates/cli-tool/templates/javascript-typescript/examples/vue-app/.claude/commands/composables.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\templates\javascript-typescript\examples\vue-app\.claude\commands\composables.md
source_ext: .md
source_sha256: 089b1d37aea7fb65a755c9ef8c42dcfb366363c3c7e82a14e299c97fc33d9390
text_sha256: 0b9e2c215f17e72df28a39b1437ef22780921cb9e7dbfdd77babb51523d38301
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# composables.md

- Source: `claude-code-templates/cli-tool/templates/javascript-typescript/examples/vue-app/.claude/commands/composables.md`
- Extract: `text`
- SHA256: `089b1d37aea7fb65a755c9ef8c42dcfb366363c3c7e82a14e299c97fc33d9390`

## Content

# Vue Composables

Create Vue composables for $ARGUMENTS following project conventions.

## Task

Create or optimize Vue composables based on the requirements:

1. **Analyze existing composables**: Check project for existing composable patterns, naming conventions, and file organization
2. **Examine Vue setup**: Verify Vue 3 Composition API usage and TypeScript configuration
3. **Identify composable type**: Determine the composable category:
   - State management (reactive data, computed properties)
   - API/HTTP operations (data fetching, mutations)
   - DOM interactions (event listeners, element refs)
   - Utility functions (validation, formatting, storage)
   - Lifecycle management (cleanup, watchers)
4. **Check dependencies**: Review existing composables to avoid duplication
5. **Implement composable**: Create composable with proper TypeScript types and reactivity
6. **Add lifecycle management**: Include proper cleanup with onUnmounted when needed
7. **Create tests**: Write comprehensive unit tests for composable logic
8. **Add documentation**: Include JSDoc comments and usage examples

## Implementation Requirements

- Follow project's TypeScript conventions and interfaces
- Use appropriate Vue reactivity APIs (ref, reactive, computed, watch)
- Include proper error handling and loading states
- Add cleanup for side effects (event listeners, timers, subscriptions)
- Make composables reusable and focused on single responsibility
- Consider performance implications (shallow vs deep reactivity)

## Common Composable Patterns

Based on the request:
- **Data fetching**: API calls with loading/error states
- **Form handling**: Input management, validation, submission
- **State management**: Local state, persistence, computed values
- **DOM utilities**: Element refs, event handling, intersection observer
- **Storage**: localStorage, sessionStorage, IndexedDB
- **Authentication**: User state, token management, permissions
- **UI utilities**: Dark mode, responsive breakpoints, modals

## Important Notes

- ALWAYS examine existing composables first to understand project patterns
- Use proper Vue 3 Composition API patterns
- Follow project's folder structure for composables (usually /composables)
- Don't install new dependencies without asking
- Consider composable composition (using other composables within composables)
- Add proper TypeScript return types and generic constraints
- Include proper reactivity patterns (avoid losing reactivity)

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
