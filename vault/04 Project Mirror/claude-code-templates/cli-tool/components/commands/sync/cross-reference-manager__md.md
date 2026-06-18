---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/sync/cross-reference-manager.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\sync\cross-reference-manager.md
source_ext: .md
source_sha256: 9b622857eb3efce9956b05566a93aa6b75052f04ba962815a674083e0b2f3c64
text_sha256: a23abb323289d747cbdd0c92ea5ddb8f81adcd77874705c1252246820ca2cb3d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# cross-reference-manager.md

- Source: `claude-code-templates/cli-tool/components/commands/sync/cross-reference-manager.md`
- Extract: `text`
- SHA256: `9b622857eb3efce9956b05566a93aa6b75052f04ba962815a674083e0b2f3c64`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [action] | audit | repair | map | validate | export
description: Manage cross-platform reference links between GitHub and Linear with integrity checking
---

# Cross-Reference Manager

Manage comprehensive cross-platform reference links with integrity validation: **$ARGUMENTS**

## Current Reference State

- GitHub CLI: !`gh --version 2>/dev/null && echo "✓ Available" || echo "⚠ Not available"`
- Linear MCP: Check Linear MCP server connectivity and authentication
- Reference database: @.reference-mappings.json or reference state files
- Link integrity: !`find . -name "*sync*" -o -name "*reference*" | wc -l` mapping files found

## Task

Implement comprehensive cross-reference management for GitHub-Linear integration:

**Management Action**: Use $ARGUMENTS to specify audit, repair, mapping, validation, or export operations

**Reference Management Framework**:
1. **Reference Database** - Initialize mapping storage, track bidirectional links, maintain sync history
2. **Integrity Auditing** - Scan cross-references, identify orphaned links, detect mismatches, validate consistency
3. **Smart Repair** - Fix broken references, update outdated links, consolidate duplicates, remove invalid entries
4. **Mapping Visualization** - Display reference networks, show connection health, highlight problems, provide statistics
5. **Deep Validation** - Verify link functionality, test bidirectional navigation, check field consistency, ensure data integrity
6. **Export & Documentation** - Generate mapping reports, create backup files, provide import instructions, maintain audit trails

**Advanced Features**: Automated orphan detection, intelligent reference reconstruction, duplicate consolidation, comprehensive validation.

**Data Protection**: Backup before modifications, transaction-based operations, rollback capabilities, comprehensive logging.

**Output**: Complete reference management system with integrity reports, repair summaries, mapping visualizations, and comprehensive cross-platform link maintenance.

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
