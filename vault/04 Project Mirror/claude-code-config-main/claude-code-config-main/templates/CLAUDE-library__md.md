---
argos_import: project_file
source_path: claude-code-config-main/claude-code-config-main/templates/CLAUDE-library.md
source_abs: F:\debug\argoss\claude-code-config-main\claude-code-config-main\templates\CLAUDE-library.md
source_ext: .md
source_sha256: abc27a92fb457fcee543357da7f5b35703c11771218df9dbe29e72cef9374efc
text_sha256: abc27a92fb457fcee543357da7f5b35703c11771218df9dbe29e72cef9374efc
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:27
---

# CLAUDE-library.md

- Source: `claude-code-config-main/claude-code-config-main/templates/CLAUDE-library.md`
- Extract: `text`
- SHA256: `abc27a92fb457fcee543357da7f5b35703c11771218df9dbe29e72cef9374efc`

## Content

# Project Rules

## Stack

{{language}} + {{build_tool}} + {{test_framework}}

## Commands

```bash
# Build
{{build_command}}

# Test
{{test_command}}

# Lint
{{lint_command}}

# Type check
{{typecheck_command}}

# Publish (dry run)
{{publish_dry_run}}
```

## File Structure

```
src/           # Source code
tests/         # Test files mirror src/ structure
docs/          # Documentation
examples/      # Usage examples (must stay working)
benchmarks/    # Performance benchmarks
```

## Public API Rules

```
# Every public function/class needs:
# 1. Type annotations
# 2. Docstring with example
# 3. At least one test

# Breaking changes:
# 1. Deprecation warning in current version
# 2. Removal in next major version
# 3. Migration guide in CHANGELOG

# Exports: explicit in __init__.py / index.ts
# No re-exports of internal modules
```

## Testing

```
# Unit tests: test every public API function
# Property tests: for pure functions with invariants
# Integration tests: for I/O-dependent code
# Examples in docs/ must be tested (doctest or extract+run)
# Benchmark regressions block merge
```

## Versioning

```
# Semantic versioning: MAJOR.MINOR.PATCH
# MAJOR: breaking API changes
# MINOR: new features, backward compatible
# PATCH: bug fixes only

# CHANGELOG.md: updated with every PR
# Version bump: separate commit, not mixed with feature code
```

## Red Lines

1. Never break public API without a deprecation cycle
2. Never add a dependency without justification in PR description
3. Never commit generated files (dist/, build/, *.pyc)
4. Never publish without running full test suite
5. Never expose internal implementation details in public types

## Supply Chain Defense

```ini
# For npm packages
min-release-age=7
```

```toml
# For Python packages
exclude-newer = "7 days"
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
