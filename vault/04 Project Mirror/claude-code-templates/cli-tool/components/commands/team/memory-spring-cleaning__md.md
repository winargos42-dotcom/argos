---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/team/memory-spring-cleaning.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\team\memory-spring-cleaning.md
source_ext: .md
source_sha256: 42613d946acda2ec38f3883a7a5654433ab82205f5173fc6cd0cdd5d623fdf13
text_sha256: 162544bc68c018e8c3c5d3eb1f235386def83c5221feec3be57a4b5241be31a6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# memory-spring-cleaning.md

- Source: `claude-code-templates/cli-tool/components/commands/team/memory-spring-cleaning.md`
- Extract: `text`
- SHA256: `42613d946acda2ec38f3883a7a5654433ab82205f5173fc6cd0cdd5d623fdf13`

## Content

---
allowed-tools: Read, Write, Edit, Glob
argument-hint: [scope] | --claude-md | --documentation | --outdated-patterns | --implementation-sync
description: Clean and organize project memory files with implementation synchronization and pattern updates
---

# Memory Spring Cleaning

Clean and synchronize project memory with current implementation patterns: **$ARGUMENTS**

## Current Memory Context

- Memory files: !`find . -name "CLAUDE*.md" | wc -l` CLAUDE.md files in project
- Documentation: !`find . -name "README*" -o -name "*.md" | wc -l` total documentation files
- Last update: !`find . -name "CLAUDE.md" -exec stat -c "%y" {} \; 2>/dev/null | head -1 || echo "No CLAUDE.md found"`
- Implementation drift: Analysis of documented vs actual patterns

## Task

Execute comprehensive memory cleanup with implementation synchronization:

**Cleanup Scope**: Use $ARGUMENTS to focus on CLAUDE.md files, general documentation, outdated pattern identification, or implementation synchronization

**Memory Cleaning Framework**:
1. **Memory File Discovery** - Locate all CLAUDE.md and documentation files, assess hierarchy and organization, identify redundant content
2. **Implementation Analysis** - Compare documented patterns with actual code, identify implementation drift, assess accuracy gaps
3. **Pattern Validation** - Verify documented conventions, validate code examples, check dependency accuracy, assess technology stack alignment
4. **Content Optimization** - Remove outdated information, consolidate duplicate content, improve organization structure, enhance clarity
5. **Synchronization Updates** - Update development commands, refresh technology stack references, sync architectural patterns, validate workflows
6. **Quality Assurance** - Ensure consistency across files, validate markdown formatting, check link integrity, maintain version alignment

**Advanced Features**: Automated pattern detection, implementation drift analysis, cross-reference validation, documentation health scoring.

**Memory Health**: Content freshness metrics, accuracy validation, usage pattern analysis, maintenance scheduling recommendations.

**Output**: Cleaned and synchronized memory files with updated patterns, validated implementations, and maintenance recommendations.

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
