---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/pac-validate.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\pac-validate.md
source_ext: .md
source_sha256: 61b9cee9c2f837ec314023dc30282ae1c5d033e8474c78a3018db79e871b31e7
text_sha256: 8afe3f670eeb6b9606cbb583063db974ea988964eaf09f63ae78f7518d0d6460
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# pac-validate.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/pac-validate.md`
- Extract: `text`
- SHA256: `61b9cee9c2f837ec314023dc30282ae1c5d033e8474c78a3018db79e871b31e7`

## Content

---
allowed-tools: Read, Bash
argument-hint: [scope] | --file | --epic | --fix | --pre-commit
description: Validate Product as Code project structure and files for PAC specification compliance
---

# Validate PAC Structure

Validate Product as Code project structure and files for PAC specification compliance: **$ARGUMENTS**

## Current PAC State

- PAC directory: !`ls -la .pac/ 2>/dev/null || echo "No .pac directory found"`
- Configuration: @.pac/pac.config.yaml (if exists)
- Epic count: !`find .pac/epics/ -name "*.yaml" 2>/dev/null | wc -l`
- Ticket count: !`find .pac/tickets/ -name "*.yaml" 2>/dev/null | wc -l`

## Task

Comprehensive validation of PAC project structure and specification compliance:

**Validation Scope**: Use $ARGUMENTS for specific files/epics or validate entire PAC structure

**Validation Checks**:
1. **Structure Validation** - Directory structure and required files
2. **Configuration Compliance** - PAC config file format and values
3. **Epic Validation** - YAML syntax, required fields, and spec compliance
4. **Ticket Validation** - Format, metadata, and epic references
5. **Cross-Reference Integrity** - Epic-ticket relationships and dependencies
6. **Data Consistency** - Timestamps, status transitions, and ID uniqueness

**Output**: Detailed validation report with compliance status, issues found, and specific recommendations for fixes. Use --fix to automatically resolve common issues.

**Exit Codes**: 0 (valid), 1 (errors found), 2 (configuration issues)

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
