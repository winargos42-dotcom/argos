---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/gh-address-comments/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\gh-address-comments\SKILL.md
source_ext: .md
source_sha256: 5e3acb77ff2d7a3b1b7e6b4cafff73ad6d9c117efe89a9dac389b43706618176
text_sha256: de973d9e10e510373b5817e951e308b3494d1876d253231f67a35b32fe88f973
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/development/gh-address-comments/SKILL.md`
- Extract: `text`
- SHA256: `5e3acb77ff2d7a3b1b7e6b4cafff73ad6d9c117efe89a9dac389b43706618176`

## Content

---
name: gh-address-comments
description: Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authenticate if not logged in.
metadata:
  short-description: Address comments in a GitHub PR review
hooks:
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "echo \"[$(date)] GH Address Comments: Executed gh command to address PR comments\" >> ~/.claude/gh-address-comments.log"
---

# PR Comment Handler

Guide to find the open PR for the current branch and address its comments with gh CLI. Run all `gh` commands with elevated network access.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (include workflow/repo scopes) so `gh` commands succeed. If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

## 1) Inspect comments needing attention
- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR

## 2) Ask the user for clarification
- Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it
- Ask the user which numbered comments should be addressed

## 3) If user chooses comments
- Apply fixes for the selected comments

Notes:
- If gh hits auth/rate issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.

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
