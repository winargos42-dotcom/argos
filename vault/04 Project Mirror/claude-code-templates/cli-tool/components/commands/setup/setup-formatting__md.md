---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/setup-formatting.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\setup-formatting.md
source_ext: .md
source_sha256: 324ffcc9377770670898971ab64921c747d1a45a58a6195bf408727d593fec8e
text_sha256: abddb67279e9b76c7f39161085cf2c59f6afc05fd37fb9a2996884f431034419
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# setup-formatting.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/setup-formatting.md`
- Extract: `text`
- SHA256: `324ffcc9377770670898971ab64921c747d1a45a58a6195bf408727d593fec8e`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [language] | --javascript | --typescript | --python | --multi-language
description: Configure comprehensive code formatting tools with consistent style enforcement
---

# Setup Code Formatting

Configure comprehensive code formatting with consistent style enforcement: **$ARGUMENTS**

## Current Project State

- Languages detected: !`find . -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.rs" | head -5`
- Existing formatters: @.prettierrc or @pyproject.toml or @rustfmt.toml
- Package manager: @package.json or @requirements.txt or @Cargo.toml
- IDE config: @.vscode/settings.json or @.editorconfig

## Task

Setup comprehensive code formatting system with automated enforcement and team consistency:

**Language Focus**: Use $ARGUMENTS to configure JavaScript/TypeScript, Python, Rust, or multi-language formatting

**Formatting Setup**:
1. **Tool Installation** - Prettier, Black, rustfmt, language-specific formatters and plugins
2. **Configuration** - Style rules, line length, indentation, quotes, trailing commas, language-specific options
3. **IDE Integration** - Editor extensions, format-on-save, keyboard shortcuts, workspace settings
4. **Automation** - Pre-commit hooks, CI/CD formatting checks, automated formatting scripts
5. **Team Sync** - Shared configurations, style guides, enforcement policies, onboarding documentation
6. **Validation** - Formatting verification, CI integration, team compliance monitoring

**Advanced Features**: Custom rules, framework-specific formatting, performance optimization, incremental formatting.

**Consistency**: Cross-platform compatibility, team standardization, legacy code migration strategies.

**Output**: Complete formatting system with automated enforcement, team configurations, and style compliance monitoring.

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
