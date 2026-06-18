---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/deployment/changelog-demo-command.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\deployment\changelog-demo-command.md
source_ext: .md
source_sha256: 4448a7bea7d835787e7013c63fdc320e76a00e77b6927145a3d7288ae4b54f87
text_sha256: 484d0ffd57b7d19844812af5dfd5bf135094965f1bb73d6cc9d1b236a31c9e51
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# changelog-demo-command.md

- Source: `claude-code-templates/cli-tool/components/commands/deployment/changelog-demo-command.md`
- Extract: `text`
- SHA256: `4448a7bea7d835787e7013c63fdc320e76a00e77b6927145a3d7288ae4b54f87`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [format] | --generate | --validate | --demo
description: Demonstrate changelog automation features with real examples and validation
---

# Changelog Automation Demo

Demonstrate changelog automation features: $ARGUMENTS

## Current Project State

- Existing changelog: @CHANGELOG.md (if exists)
- Package version: @package.json or @pyproject.toml or @Cargo.toml (if exists)
- Recent commits: !`git log --oneline -10`
- Git tags: !`git tag -l | tail -5`

## Demo Features

### 1. **Changelog Generation Demo**
- Generate sample changelog entries from git commits
- Show different changelog formats (Keep a Changelog, conventional-changelog)
- Demonstrate automatic categorization of changes
- Show version numbering and semantic versioning

### 2. **Format Validation Demo**
- Validate existing changelog format compliance
- Show format inconsistencies and suggestions
- Demonstrate automated formatting fixes
- Show integration with release automation

### 3. **Integration Testing**
- Test changelog automation without affecting main workflow
- Validate changelog generation pipeline
- Test different commit message patterns
- Show error handling and recovery

### 4. **Performance Benchmarking**
- Measure changelog generation speed
- Test with large commit histories
- Show memory usage and optimization
- Benchmark different parsing strategies

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
