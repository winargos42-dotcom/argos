---
argos_import: project_file
source_path: claude-code-config-main/claude-code-config-main/templates/README.md
source_abs: F:\debug\argoss\claude-code-config-main\claude-code-config-main\templates\README.md
source_ext: .md
source_sha256: f2a25a52389fbc5bca5932ce869de80034c98515f085a4b08328ce85cc332352
text_sha256: f2a25a52389fbc5bca5932ce869de80034c98515f085a4b08328ce85cc332352
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:27
---

# README.md

- Source: `claude-code-config-main/claude-code-config-main/templates/README.md`
- Extract: `text`
- SHA256: `f2a25a52389fbc5bca5932ce869de80034c98515f085a4b08328ce85cc332352`

## Content

# Starter Templates

Drop-in configuration files for common project types. Each template is a starting point - customize for your project.

## Available Templates

| Template | Target | Size |
|---|---|---|
| [CLAUDE-web-app.md](CLAUDE-web-app.md) | Web applications (React, Vue, Next.js, etc.) | ~80 lines |
| [CLAUDE-ml-project.md](CLAUDE-ml-project.md) | ML/AI projects (training, inference, data pipelines) | ~80 lines |
| [CLAUDE-library.md](CLAUDE-library.md) | Libraries and packages (npm, PyPI, crates.io) | ~70 lines |
| [REVIEW.md](REVIEW.md) | Code review guidelines (any project type) | ~60 lines |

## How to Use

1. Copy the relevant template to your project root
2. Rename to `CLAUDE.md` (or `REVIEW.md` for review template)
3. Fill in project-specific values (marked with `{{placeholder}}`)
4. Remove sections that don't apply
5. Add project-specific rules

## Design Principles

- **Under 150 lines** - fits in a single KV-cache prefix for efficiency
- **Commands before prose** - `npm test`, `cargo build` before explanations
- **Code over descriptions** - style shown by example, not described in words
- **No linting rules** - use deterministic tools (eslint, ruff) instead
- **No general programming advice** - only project-specific, non-obvious rules

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
