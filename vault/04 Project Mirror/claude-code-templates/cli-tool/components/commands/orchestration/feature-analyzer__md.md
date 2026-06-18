---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/orchestration/feature-analyzer.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\orchestration\feature-analyzer.md
source_ext: .md
source_sha256: 7d5e67a016d01a5897075864a66667b30d2c4ff276fda4974384eee072ff96ef
text_sha256: fdfc662df62b3df9e4368ba15aab91e366be7e1888f1f62b7cc2b9bc8c4757d4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# feature-analyzer.md

- Source: `claude-code-templates/cli-tool/components/commands/orchestration/feature-analyzer.md`
- Extract: `text`
- SHA256: `7d5e67a016d01a5897075864a66667b30d2c4ff276fda4974384eee072ff96ef`

## Content

---
description: "Turn ideas into fully formed designs and specs through natural collaborative dialogue. Use before implementing new features or making significant changes."
argument-hint: Optional feature description
allowed-tools: Read, Write, Grep, Glob, Bash, TodoWrite, AskUserQuestion, Skill, Task
---

## Phase 1: Discovery

**Goal**: Understand what needs to be built

Initial request: $ARGUMENTS

**Actions**:
1. Create todo list with all phases
2. If feature unclear, ask user for:
   - What problem are they solving?
   - What should the feature do?
   - Any constraints or requirements?
3. Summarize understanding and confirm with user

---

## Phase 2: Run with Feature Analyzer Skill

Use the Skill tool to invoke the "feature-design-assistant" skill and follow its complete process.

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
