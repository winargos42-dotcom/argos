---
argos_import: project_file
source_path: mempalace-develop/website/guide/getting-started.md
source_abs: F:\debug\argoss\mempalace-develop\website\guide\getting-started.md
source_ext: .md
source_sha256: 1e480dc9687ac84fe4f5d9a9bfba97f45fe0d52d3ac15381ec18f86b4b5e28ce
text_sha256: 1e480dc9687ac84fe4f5d9a9bfba97f45fe0d52d3ac15381ec18f86b4b5e28ce
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# getting-started.md

- Source: `mempalace-develop/website/guide/getting-started.md`
- Extract: `text`
- SHA256: `1e480dc9687ac84fe4f5d9a9bfba97f45fe0d52d3ac15381ec18f86b4b5e28ce`

## Content

# Getting Started

## Installation

Install MemPalace from PyPI:

```bash
pip install mempalace
```

::: danger Security Warning
The domain `mempalace.tech` is a **brand-squatting site** not affiliated with this project. It is known to run ad-redirects and potential malware. The official MemPalace distribution is only available via this [GitHub repository](https://github.com/milla-jovovich/mempalace) and [PyPI](https://pypi.org/project/mempalace/). Never install binaries or scripts from unofficial domains.
:::

### Requirements

- Python 3.9+
- `chromadb>=0.5.0` (installed automatically)
- `pyyaml>=6.0` (installed automatically)

No API key required for the core local workflow. After installation, the main storage and retrieval path runs locally.

### From Source

```bash
git clone https://github.com/milla-jovovich/mempalace.git
cd mempalace
pip install -e ".[dev]"
```

## Quick Start

Three steps: **init**, **mine**, **search**.

### 1. Initialize Your Palace

```bash
mempalace init ~/projects/myapp
```

This scans your project directory and:
- Detects people and projects from file content
- Creates rooms from your folder structure
- Sets up `~/.mempalace/` config directory

### 2. Mine Your Data

```bash
# Mine project files (code, docs, notes)
mempalace mine ~/projects/myapp

# Mine conversation exports (Claude, ChatGPT, Slack)
mempalace mine ~/chats/ --mode convos

# Mine with auto-classification into memory types
mempalace mine ~/chats/ --mode convos --extract general
```

Two mining modes plus one extraction strategy:
- **projects** — code and docs, auto-detected rooms
- **convos** — conversation exports, chunked by exchange pair
- **general extraction** — an `--extract general` option for conversation mining that classifies content into decisions, preferences, milestones, problems, and emotional context

### 3. Search

```bash
mempalace search "why did we switch to GraphQL"
```

That gives you a working local memory index.

## What Happens Next

After the one-time setup, you don't run MemPalace commands manually. Your AI uses it for you through [MCP integration](/guide/mcp-integration) or a [Claude Code plugin](/guide/claude-code).

Ask your AI anything:

> *"What did we decide about auth last month?"*

It calls `mempalace_search` automatically, gets verbatim results, and answers you. You never type `mempalace search` again.

## Next Steps

- [Mining Your Data](/guide/mining) — deep dive into mining modes
- [MCP Integration](/guide/mcp-integration) — connect to Claude, ChatGPT, Cursor, Gemini
- [The Palace](/concepts/the-palace) — understand wings, rooms, halls, and tunnels

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
