---
argos_import: project_file
source_path: claude-code-config-main/claude-code-config-main/templates/CLAUDE-web-app.md
source_abs: F:\debug\argoss\claude-code-config-main\claude-code-config-main\templates\CLAUDE-web-app.md
source_ext: .md
source_sha256: 528c4b80f61933eaaf3c6412953b0bb0e0ec9e4550a1ebc60ed101d29a90ea0e
text_sha256: 528c4b80f61933eaaf3c6412953b0bb0e0ec9e4550a1ebc60ed101d29a90ea0e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:27
---

# CLAUDE-web-app.md

- Source: `claude-code-config-main/claude-code-config-main/templates/CLAUDE-web-app.md`
- Extract: `text`
- SHA256: `528c4b80f61933eaaf3c6412953b0bb0e0ec9e4550a1ebc60ed101d29a90ea0e`

## Content

# Project Rules

## Stack

{{framework}} + {{language}} + {{styling}} + {{database}}

## Commands

```bash
# Development
{{dev_command}}

# Test
{{test_command}}

# Build
{{build_command}}

# Lint
{{lint_command}}

# Type check
{{typecheck_command}}
```

## File Structure

```
src/
  components/    # Reusable UI components
  pages/         # Route-level components
  lib/           # Shared utilities, API clients
  hooks/         # Custom React/Vue hooks
  types/         # TypeScript type definitions
```

## Style Guide

```typescript
// Components: PascalCase, one component per file
// Files: kebab-case (user-profile.tsx, not UserProfile.tsx)
// Hooks: usePrefix (useAuth, useDebounce)
// Utils: camelCase functions, UPPER_SNAKE for constants

// Prefer named exports over default exports
export function UserProfile() { ... }

// Error handling: at component boundaries, not every function
// Use error boundaries for rendering, try/catch for async
```

## API Patterns

```typescript
// API calls go through lib/api.ts, not directly in components
// Use {{data_fetching}} for data fetching
// Environment-specific URLs in .env, never hardcoded
```

## Testing

```typescript
// Unit tests: *.test.ts next to the source file
// Integration tests: tests/ directory
// Test user behavior, not implementation details
// Mock external APIs, not internal modules
```

## Red Lines

1. Never commit .env files - use .env.example for templates
2. Never use `any` type without a comment explaining why
3. Never fetch data in components - use hooks or server-side
4. Never store sensitive data in localStorage - use httpOnly cookies
5. Never disable eslint rules without a comment

## Supply Chain Defense

```ini
# ~/.npmrc (or project .npmrc)
min-release-age=7
```

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
