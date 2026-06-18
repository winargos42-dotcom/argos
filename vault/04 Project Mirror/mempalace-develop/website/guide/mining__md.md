---
argos_import: project_file
source_path: mempalace-develop/website/guide/mining.md
source_abs: F:\debug\argoss\mempalace-develop\website\guide\mining.md
source_ext: .md
source_sha256: c3d715bc3f6f44375f5a571d4e8d70dc1b16a7cdfec0deab7def0c14be6c5d86
text_sha256: c3d715bc3f6f44375f5a571d4e8d70dc1b16a7cdfec0deab7def0c14be6c5d86
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# mining.md

- Source: `mempalace-develop/website/guide/mining.md`
- Extract: `text`
- SHA256: `c3d715bc3f6f44375f5a571d4e8d70dc1b16a7cdfec0deab7def0c14be6c5d86`

## Content

# Mining Your Data

MemPalace ingests your data by **mining** — scanning files and filing their content as verbatim drawers in the palace.

## Mining Modes

### Projects Mode (default)

Scans code, docs, and notes. Respects `.gitignore` by default.

```bash
mempalace mine ~/projects/myapp
```

Each file becomes a drawer, tagged with a wing (project name) and room (topic). Rooms are auto-detected from your folder structure during `mempalace init`.

Options:
```bash
# Override wing name
mempalace mine ~/projects/myapp --wing myapp

# Ignore .gitignore rules
mempalace mine ~/projects/myapp --no-gitignore

# Include specific ignored paths
mempalace mine ~/projects/myapp --include-ignored dist,build

# Limit number of files
mempalace mine ~/projects/myapp --limit 100

# Preview without filing
mempalace mine ~/projects/myapp --dry-run
```

### Conversations Mode

Indexes conversation exports from Claude, ChatGPT, Slack, and other tools. Chunks by exchange pair (human + assistant turns).

```bash
mempalace mine ~/chats/ --mode convos
```

Supports five chat formats automatically:
- Claude JSON exports
- ChatGPT exports
- Slack exports
- Markdown conversations
- Plain text transcripts

### General Extraction

Auto-classifies conversation content into five memory types:

```bash
mempalace mine ~/chats/ --mode convos --extract general
```

Memory types:
- **Decisions** — choices made, options rejected
- **Preferences** — habits, likes, opinions
- **Milestones** — sessions completed, goals reached
- **Problems** — bugs, blockers, issues encountered
- **Emotional context** — reactions, concerns, excitement

## Splitting Mega-Files

Some transcript exports concatenate multiple sessions into one huge file. Split them first:

```bash
# Preview what would be split
mempalace split ~/chats/ --dry-run

# Split files with 2+ sessions (default)
mempalace split ~/chats/

# Only split files with 3+ sessions
mempalace split ~/chats/ --min-sessions 3

# Output to a different directory
mempalace split ~/chats/ --output-dir ~/chats-split/
```

::: tip
Always run `mempalace split` before mining conversation files. It's a no-op if files don't need splitting.
:::

## Multi-Project Setup

Mine each project into its own wing:

```bash
mempalace mine ~/chats/orion/  --mode convos --wing orion
mempalace mine ~/chats/nova/   --mode convos --wing nova
mempalace mine ~/chats/helios/ --mode convos --wing helios
```

Six months later:
```bash
# Project-specific search
mempalace search "database decision" --wing orion

# Cross-project search
mempalace search "rate limiting approach"
# → finds your approach in Orion AND Nova, shows the differences
```

## Team Usage

Mine Slack exports and AI conversations for team history:

```bash
mempalace mine ~/exports/slack/ --mode convos --wing driftwood
mempalace mine ~/.claude/projects/ --mode convos
```

Then search across people and projects:
```bash
mempalace search "Soren sprint" --wing driftwood
# → 14 closets: OAuth refactor, dark mode, component library migration
```

## Agent Tag

Every drawer is tagged with the agent that filed it:

```bash
# Default agent name
mempalace mine ~/data/ --agent mempalace

# Custom agent name
mempalace mine ~/data/ --agent reviewer
```

This is used by [Specialist Agents](/concepts/agents) to partition memories.

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
