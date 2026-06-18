---
argos_import: project_file
source_path: mempalace-develop/mempalace/instructions/mine.md
source_abs: F:\debug\argoss\mempalace-develop\mempalace\instructions\mine.md
source_ext: .md
source_sha256: 79e9fa4c9c59c183c335b72859046a999934f1fb41d82d582b62c9e0e85726df
text_sha256: 79e9fa4c9c59c183c335b72859046a999934f1fb41d82d582b62c9e0e85726df
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# mine.md

- Source: `mempalace-develop/mempalace/instructions/mine.md`
- Extract: `text`
- SHA256: `79e9fa4c9c59c183c335b72859046a999934f1fb41d82d582b62c9e0e85726df`

## Content

# MemPalace Mine

When the user invokes this skill, follow these steps:

## 1. Ask what to mine

Ask the user what they want to mine and where the source data is located.
Clarify:
- Is it a project directory (code, docs, notes)?
- Is it conversation exports (Claude, ChatGPT, Slack)?
- Do they want auto-classification (decisions, milestones, problems)?

## 2. Choose the mining mode

There are three mining modes:

### Project mining

    mempalace mine <dir>

Mines code files, documentation, and notes from a project directory.

### Conversation mining

    mempalace mine <dir> --mode convos

Mines conversation exports from Claude, ChatGPT, or Slack into the palace.

### General extraction (auto-classify)

    mempalace mine <dir> --mode convos --extract general

Auto-classifies mined content into decisions, milestones, and problems.

## 3. Optionally split mega-files first

If the source directory contains very large files, suggest splitting them
before mining:

    mempalace split <dir> [--dry-run]

Use --dry-run first to preview what will be split without making changes.

## 4. Optionally tag with a wing

If the user wants to organize mined content under a specific wing, add the
--wing flag:

    mempalace mine <dir> --wing <name>

## 5. Show progress and results

Run the selected mining command and display progress as it executes. After
completion, summarize the results including:
- Number of items mined
- Categories or classifications applied
- Any warnings or skipped files

## 6. Suggest next steps

After mining completes, suggest the user try:
- /mempalace:search -- search the newly mined content
- /mempalace:status -- check the current state of their palace
- Mine more data from additional sources

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
