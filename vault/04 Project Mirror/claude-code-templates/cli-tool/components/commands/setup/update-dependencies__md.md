---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/update-dependencies.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\update-dependencies.md
source_ext: .md
source_sha256: e2c7196d9762516c434791a55c928f9f7bc8efdabcf3294fde1b159ffea113c3
text_sha256: 4462f8b8836909368a48a1beb7d21e77cebfd2c22ecfad49f8930de1941b0d20
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# update-dependencies.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/update-dependencies.md`
- Extract: `text`
- SHA256: `e2c7196d9762516c434791a55c928f9f7bc8efdabcf3294fde1b159ffea113c3`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [update-strategy] | --patch | --minor | --major | --security-only
description: Update and modernize project dependencies with comprehensive testing and compatibility checks
---

# Update Dependencies

Update and modernize project dependencies with safety checks: **$ARGUMENTS**

## Current Dependencies State

- Package manager: @package.json or @requirements.txt or @Cargo.toml (detect package manager)
- Outdated packages: !`npm outdated 2>/dev/null || pip list --outdated 2>/dev/null || echo "Manual check needed"`
- Security issues: !`npm audit --audit-level=moderate 2>/dev/null || pip check 2>/dev/null || echo "Run security audit"`
- Lock files: @package-lock.json or @poetry.lock or @Cargo.lock

## Task

Systematically update project dependencies with comprehensive testing and compatibility validation:

**Update Strategy**: Use $ARGUMENTS to specify patch updates, minor updates, major updates, or security-only updates

**Update Process**:
1. **Dependency Analysis** - Audit current versions, identify outdated packages, assess security vulnerabilities
2. **Impact Assessment** - Check changelogs, breaking changes, deprecation warnings, compatibility matrix
3. **Staged Updates** - Apply patch updates first, then minor, finally major versions with testing between stages
4. **Testing & Validation** - Run full test suite, build verification, integration testing, performance checks
5. **Rollback Strategy** - Document changes, create restore points, maintain rollback procedures
6. **Documentation Updates** - Update README, dependencies list, migration guides, team notifications

**Safety Features**: Automated testing between updates, dependency conflict resolution, security vulnerability prioritization.

**Output**: Updated dependency manifest with comprehensive testing results, security audit report, and upgrade documentation.

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
