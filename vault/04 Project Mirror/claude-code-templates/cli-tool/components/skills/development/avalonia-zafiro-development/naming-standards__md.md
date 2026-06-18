---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-zafiro-development/naming-standards.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-zafiro-development\naming-standards.md
source_ext: .md
source_sha256: c51c1e6135f939158e54b860e87a95d44e10fa216d1f28d98d580907fd8897c2
text_sha256: 31c7bac64e687b48554d489da7ca7ee4631e5c2940e37356f0fecf31e90cc575
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# naming-standards.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-zafiro-development/naming-standards.md`
- Extract: `text`
- SHA256: `c51c1e6135f939158e54b860e87a95d44e10fa216d1f28d98d580907fd8897c2`

## Content

# Naming & Coding Standards

## General Standards

- **Explicit Names**: Favor clarity over cleverness.
- **Async Suffix**: Do **NOT** use the `Async` suffix in method names, even if they return `Task`.
- **Private Fields**: Do **NOT** use the `_` prefix for private fields.
- **Static State**: Avoid static state unless explicitly justified and documented.
- **Method Design**: Keep methods small, expressive, and with low cyclomatic complexity.

## Error Handling

- **Result & Maybe**: Use types from **CSharpFunctionalExtensions** for flow control and error handling.
- **Exceptions**: Reserved strictly for truly exceptional, unrecoverable situations.
- **Boundaries**: Never allow exceptions to leak across architectural boundaries.

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
