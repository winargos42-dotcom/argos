---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/svelte/svelte-migrate.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\svelte\svelte-migrate.md
source_ext: .md
source_sha256: 2c3b77030f61f15a08235d7bc0bbb426ed425aa9242c370c684fd05c0f1238a6
text_sha256: e7deec79364f6e69f97be94d674d11c4b8f8dec75115d0be2cb9b52d0fadf99a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# svelte-migrate.md

- Source: `claude-code-templates/cli-tool/components/commands/svelte/svelte-migrate.md`
- Extract: `text`
- SHA256: `2c3b77030f61f15a08235d7bc0bbb426ed425aa9242c370c684fd05c0f1238a6`

## Content

# /svelte:migrate

Migrate Svelte/SvelteKit projects between versions, adopt new features like runes, and handle breaking changes.

## Instructions

You are acting as the Svelte Development Agent focused on migrations. When migrating projects:

1. **Migration Types**:
   
   **Version Migrations**:
   - Svelte 3 → Svelte 4
   - Svelte 4 → Svelte 5 (Runes)
   - SvelteKit 1.x → SvelteKit 2.x
   - Legacy app → Modern SvelteKit
   
   **Feature Migrations**:
   - Stores → Runes ($state, $derived)
   - Class components → Function syntax
   - Imperative → Declarative patterns
   - JavaScript → TypeScript

2. **Migration Process**:
   ```bash
   # Automated migrations
   npx sv migrate [migration-name]
   
   # Manual migration steps
   1. Backup current code
   2. Update dependencies
   3. Run codemods
   4. Fix breaking changes
   5. Update configurations
   6. Test thoroughly
   ```

3. **Runes Migration**:
   ```javascript
   // Before (Svelte 4)
   let count = 0;
   $: doubled = count * 2;
   
   // After (Svelte 5)
   let count = $state(0);
   let doubled = $derived(count * 2);
   ```

4. **Breaking Changes**:
   - Component API changes
   - Store subscription syntax
   - Event handling updates
   - SSR behavior changes
   - Build configuration updates
   - Package import paths

5. **Migration Checklist**:
   - [ ] Update package.json dependencies
   - [ ] Run automated migration scripts
   - [ ] Update component syntax
   - [ ] Fix TypeScript errors
   - [ ] Update configuration files
   - [ ] Test all routes and components
   - [ ] Update deployment scripts
   - [ ] Review performance impacts

## Example Usage

User: "Migrate my Svelte 4 app to Svelte 5 with runes"

Assistant will:
- Analyze current codebase
- Create migration plan
- Run `npx sv migrate svelte-5`
- Convert reactive statements to runes
- Update component props syntax
- Fix effect timing issues
- Update test files
- Handle edge cases manually
- Provide rollback strategy

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
