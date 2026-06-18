---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/migrate-to-typescript.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\migrate-to-typescript.md
source_ext: .md
source_sha256: 3be1081fbff8fd8ddc4ada85097bd58e1b64d7ebb85613efbcce6df6140d58c9
text_sha256: e50ad7e3975651819350741874ac26d088776e60ca03472b724dee9335189e18
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# migrate-to-typescript.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/migrate-to-typescript.md`
- Extract: `text`
- SHA256: `3be1081fbff8fd8ddc4ada85097bd58e1b64d7ebb85613efbcce6df6140d58c9`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [migration-strategy] | --gradual | --complete | --strict | --incremental
description: Migrate JavaScript project to TypeScript with proper typing and tooling setup
---

# Migrate to TypeScript

Migrate JavaScript project to TypeScript with comprehensive type safety: **$ARGUMENTS**

## Current JavaScript State

- Project structure: @package.json (analyze JS/TS mix and dependencies)
- JavaScript files: !`find . -name "*.js" -not -path "./node_modules/*" | wc -l`
- Existing TypeScript: !`find . -name "*.ts" -not -path "./node_modules/*" | wc -l`
- Build system: @webpack.config.js or @vite.config.js or @rollup.config.js

## Task

Systematically migrate JavaScript codebase to TypeScript with proper typing and tooling:

**Migration Strategy**: Use $ARGUMENTS to specify gradual migration, complete conversion, strict mode, or incremental approach

**Migration Process**:
1. **Environment Setup** - TypeScript installation, tsconfig.json configuration, build tool integration
2. **Type Definitions** - Install @types packages, create custom type declarations, define interfaces
3. **File Migration** - Rename .js to .ts/.tsx, add type annotations, resolve compiler errors
4. **Code Transformation** - Convert classes, functions, and modules with proper typing
5. **Error Resolution** - Fix type mismatches, null/undefined handling, strict mode issues
6. **Testing & Validation** - Update test files, configure type checking, validate type coverage

**Advanced Features**: Generic types, mapped types, conditional types, module augmentation, and strict compiler settings.

**Developer Experience**: Configure IDE integration, debugging, linting rules, and team onboarding.

**Output**: Fully typed TypeScript codebase with strict type checking, comprehensive IntelliSense, and improved developer productivity.

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
