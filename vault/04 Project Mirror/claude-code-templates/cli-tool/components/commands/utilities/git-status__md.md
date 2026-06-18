---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/utilities/git-status.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\utilities\git-status.md
source_ext: .md
source_sha256: cf7a78a3d43c4232f3ecadd6fa4dc0d42dfe8cff8effc5e7515785ebe2b293bb
text_sha256: 89acf696c7cbc530e05dd5fe4dee22a07ba0a9e19a585ee4de19a6542ed4253f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# git-status.md

- Source: `claude-code-templates/cli-tool/components/commands/utilities/git-status.md`
- Extract: `text`
- SHA256: `cf7a78a3d43c4232f3ecadd6fa4dc0d42dfe8cff8effc5e7515785ebe2b293bb`

## Content

# Git Status Command

Show detailed git repository status

*Command originally created by IndyDevDan (YouTube: https://www.youtube.com/@indydevdan) / DislerH (GitHub: https://github.com/disler)*

## Instructions

Analyze the current state of the git repository by performing the following steps:

1. **Run Git Status Commands**
   - Execute `git status` to see current working tree state
   - Run `git diff HEAD origin/main` to check differences with remote
   - Execute `git branch --show-current` to display current branch
   - Check for uncommitted changes and untracked files

2. **Analyze Repository State**
   - Identify staged vs unstaged changes
   - List any untracked files
   - Check if branch is ahead/behind remote
   - Review any merge conflicts if present

3. **Read Key Files**
   - Review README.md for project context
   - Check for any recent changes in important files
   - Understand project structure if needed

4. **Provide Summary**
   - Current branch and its relationship to main/master
   - Number of commits ahead/behind
   - List of modified files with change types
   - Any action items (commits needed, pulls required, etc.)

This command helps developers quickly understand:
- What changes are pending
- The repository's sync status
- Whether any actions are needed before continuing work

Arguments: $ARGUMENTS

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
