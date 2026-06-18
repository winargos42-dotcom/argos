---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/web-design-guidelines/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\web-design-guidelines\SKILL.md
source_ext: .md
source_sha256: cb9648c402ebf969c85b2fa6f4dbfa1cb9d567472bbb8c5c45bec96ce902fbfe
text_sha256: fc48547ce7b3f384043d0804d823a0c6bd02f4a94a484bc724551d28fcd6b90d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/web-design-guidelines/SKILL.md`
- Extract: `text`
- SHA256: `cb9648c402ebf969c85b2fa6f4dbfa1cb9d567472bbb8c5c45bec96ce902fbfe`

## Content

---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
argument-hint: <file-or-pattern>
---

# Web Interface Guidelines

Review files for compliance with Web Interface Guidelines.

## How It Works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask the user which files to review.

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
