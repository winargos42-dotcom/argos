---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/sentry/deslop/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\sentry\deslop\SKILL.md
source_ext: .md
source_sha256: 30422176eec074837d858cae0a998476df56ca82822829a2b05818c14bdf8871
text_sha256: 2b106d2147e8aa353e0d5feb429ca4e20b5bc700719acc677bf5482e53e785fa
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/sentry/deslop/SKILL.md`
- Extract: `text`
- SHA256: `30422176eec074837d858cae0a998476df56ca82822829a2b05818c14bdf8871`

## Content

---
name: deslop
description: Remove AI-generated code slop from a branch. Use when cleaning up AI-generated code, removing unnecessary comments, defensive checks, or type casts. Checks diff against main and fixes style inconsistencies.
---

# Remove AI Code Slop

Check the diff against main and remove all AI-generated slop introduced in this branch.

## What to Remove

- Extra comments that a human wouldn't add or are inconsistent with the rest of the file
- Extra defensive checks or try/catch blocks that are abnormal for that area of the codebase (especially if called by trusted/validated codepaths)
- Casts to `any` to get around type issues
- Inline imports in Python (move to top of file with other imports)
- Any other style that is inconsistent with the file

## Process

1. Get the diff against main: `git diff main...HEAD`
2. Review each changed file for slop patterns
3. Remove identified slop while preserving legitimate changes
4. Report a 1-3 sentence summary of what was changed

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
