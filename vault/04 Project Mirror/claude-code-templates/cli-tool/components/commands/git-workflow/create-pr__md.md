---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/git-workflow/create-pr.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\git-workflow\create-pr.md
source_ext: .md
source_sha256: 7caf2a25c50259c8a2a4d5e0da5f3061aa9608bd6da640060871a284f6dc2d51
text_sha256: 695750001a3ab02ad8a1448e86b132ee951fe9465806aa918d4c2ab98fadbbcb
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# create-pr.md

- Source: `claude-code-templates/cli-tool/components/commands/git-workflow/create-pr.md`
- Extract: `text`
- SHA256: `7caf2a25c50259c8a2a4d5e0da5f3061aa9608bd6da640060871a284f6dc2d51`

## Content

# Create Pull Request Command

Create a new branch, commit changes, and submit a pull request.

## Behavior
- Creates a new branch based on current changes
- Formats modified files using Biome
- Analyzes changes and automatically splits into logical commits when appropriate
- Each commit focuses on a single logical change or feature
- Creates descriptive commit messages for each logical unit
- Pushes branch to remote
- Creates pull request with proper summary and test plan

## Guidelines for Automatic Commit Splitting
- Split commits by feature, component, or concern
- Keep related file changes together in the same commit
- Separate refactoring from feature additions
- Ensure each commit can be understood independently
- Multiple unrelated changes should be split into separate commits

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
