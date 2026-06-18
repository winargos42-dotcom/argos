---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/productivity/address-github-comments/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\productivity\address-github-comments\SKILL.md
source_ext: .md
source_sha256: 67c49f98191191e4933e83e22a6840878ab203153b1d2eac52a003f400ab4976
text_sha256: 075bcc90295ffb889983451a906e0a0e92c052e0a2ea56cc7a37e46ed853f29a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/productivity/address-github-comments/SKILL.md`
- Extract: `text`
- SHA256: `67c49f98191191e4933e83e22a6840878ab203153b1d2eac52a003f400ab4976`

## Content

---
name: address-github-comments
description: Use when you need to address review or issue comments on an open GitHub Pull Request using the gh CLI.
---

# Address GitHub Comments

## Overview

Efficiently address PR review comments or issue feedback using the GitHub CLI (`gh`). This skill ensures all feedback is addressed systematically.

## Prerequisites

Ensure `gh` is authenticated.

```bash
gh auth status
```

If not logged in, run `gh auth login`.

## Workflow

### 1. Inspect Comments

Fetch the comments for the current branch's PR.

```bash
gh pr view --comments
```

Or use a custom script if available to list threads.

### 2. Categorize and Plan

- List the comments and review threads.
- Propose a fix for each.
- **Wait for user confirmation** on which comments to address first if there are many.

### 3. Apply Fixes

Apply the code changes for the selected comments.

### 4. Respond to Comments

Once fixed, respond to the threads as resolved.

```bash
gh pr comment <PR_NUMBER> --body "Addressed in latest commit."
```

## Common Mistakes

- **Applying fixes without understanding context**: Always read the surrounding code of a comment.
- **Not verifying auth**: Check `gh auth status` before starting.

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
