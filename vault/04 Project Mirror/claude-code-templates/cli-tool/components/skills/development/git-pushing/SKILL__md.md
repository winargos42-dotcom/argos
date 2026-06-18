---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/git-pushing/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\git-pushing\SKILL.md
source_ext: .md
source_sha256: 8e212d59ffb77dca6794d5eca2dd8ab559d2d38f9cf5471f139e3991c074401b
text_sha256: 58ba22907d621bca88f93c44fb278cee88ef365f3c186189dc1d308d2d6fcfdd
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/development/git-pushing/SKILL.md`
- Extract: `text`
- SHA256: `8e212d59ffb77dca6794d5eca2dd8ab559d2d38f9cf5471f139e3991c074401b`

## Content

---
name: git-pushing
description: Stage, commit, and push git changes with conventional commit messages. Use when user wants to commit and push changes, mentions pushing to remote, or asks to save and push their work. Also activates when user says "push changes", "commit and push", "push this", "push to github", or similar git workflow requests.
---

# Git Push Workflow

Stage all changes, create a conventional commit, and push to the remote branch.

## When to Use

Automatically activate when the user:

- Explicitly asks to push changes ("push this", "commit and push")
- Mentions saving work to remote ("save to github", "push to remote")
- Completes a feature and wants to share it
- Says phrases like "let's push this up" or "commit these changes"

## Workflow

**ALWAYS use the script** - do NOT use manual git commands:

```bash
bash skills/git-pushing/scripts/smart_commit.sh
```

With custom message:

```bash
bash skills/git-pushing/scripts/smart_commit.sh "feat: add feature"
```

Script handles: staging, conventional commit message, Claude footer, push with -u flag.

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
