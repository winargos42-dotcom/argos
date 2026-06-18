---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/add-to-changelog.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\add-to-changelog.md
source_ext: .md
source_sha256: 4d8b6bf9d1a68713e0033e6deda2448d49010bd91bd9058b33c0c570af853222
text_sha256: 96d5fa64847613664c7bca093490d00422af5c73020426d6f0f4884f4ede2ff7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# add-to-changelog.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/add-to-changelog.md`
- Extract: `text`
- SHA256: `4d8b6bf9d1a68713e0033e6deda2448d49010bd91bd9058b33c0c570af853222`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [version] [change-type] [message] | --added | --changed | --fixed
description: Add entry to project changelog following Keep a Changelog format
---

# Update Changelog

Add a new entry to the project's CHANGELOG.md file: **$ARGUMENTS**

## Usage Examples
- `/add-to-changelog 1.1.0 added "New markdown to BlockDoc conversion feature"`
- `/add-to-changelog 1.0.2 fixed "Bug in HTML renderer causing incorrect output"`

## Current Changelog State

- Existing changelog: @CHANGELOG.md (if exists)
- Project version files: @package.json or @setup.py (if exists)

## Task

Add the specified change entry to CHANGELOG.md:

**Arguments**: 
- Version: First argument (e.g., "1.1.0")
- Change Type: Second argument (added/changed/deprecated/removed/fixed/security)  
- Message: Third argument (description of the change)

**Requirements**:
1. Create CHANGELOG.md with standard header if it doesn't exist
2. Find or create version section with today's date
3. Add entry under appropriate change type section
4. Follow Keep a Changelog format and Semantic Versioning
5. Update package version files if this is a new version

The changelog should follow [Keep a Changelog](https://keepachangelog.com/) format.

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
