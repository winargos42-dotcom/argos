---
argos_import: project_file
source_path: mempalace-develop/.claude-plugin/skills/mempalace/SKILL.md
source_abs: F:\debug\argoss\mempalace-develop\.claude-plugin\skills\mempalace\SKILL.md
source_ext: .md
source_sha256: 4f6fb2a89060364cfbf4719301d37ce9c722353e44e37311aac00c366c964697
text_sha256: 4f6fb2a89060364cfbf4719301d37ce9c722353e44e37311aac00c366c964697
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# SKILL.md

- Source: `mempalace-develop/.claude-plugin/skills/mempalace/SKILL.md`
- Extract: `text`
- SHA256: `4f6fb2a89060364cfbf4719301d37ce9c722353e44e37311aac00c366c964697`

## Content

---
name: mempalace
description: MemPalace — mine projects and conversations into a searchable memory palace. Use when asked about mempalace, memory palace, mining memories, searching memories, or palace setup.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# MemPalace

A searchable memory palace for AI — mine projects and conversations, then search them semantically.

## Prerequisites

Ensure `mempalace` is installed:

```bash
mempalace --version
```

If not installed:

```bash
pip install mempalace
```

## Usage

MemPalace provides dynamic instructions via the CLI. To get instructions for any operation:

```bash
mempalace instructions <command>
```

Where `<command>` is one of: `help`, `init`, `mine`, `search`, `status`.

Run the appropriate instructions command, then follow the returned instructions step by step.

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
