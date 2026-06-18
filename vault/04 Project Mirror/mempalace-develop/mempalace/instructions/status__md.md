---
argos_import: project_file
source_path: mempalace-develop/mempalace/instructions/status.md
source_abs: F:\debug\argoss\mempalace-develop\mempalace\instructions\status.md
source_ext: .md
source_sha256: 7da31885ee1c362896921d095adbac82b186b508f010d87a1bd939c4f63730d4
text_sha256: 7da31885ee1c362896921d095adbac82b186b508f010d87a1bd939c4f63730d4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# status.md

- Source: `mempalace-develop/mempalace/instructions/status.md`
- Extract: `text`
- SHA256: `7da31885ee1c362896921d095adbac82b186b508f010d87a1bd939c4f63730d4`

## Content

# MemPalace Status

Display the current state of the user's memory palace.

## Step 1: Gather Palace Status

Check if MCP tools are available (look for mempalace_status in available tools).

- If MCP is available: Call the mempalace_status tool to retrieve palace state.
- If MCP is not available: Run the CLI command: mempalace status

## Step 2: Display Wing/Room/Drawer Counts

Present the palace structure counts clearly:
- Number of wings
- Number of rooms
- Number of drawers
- Total memories stored

Keep the output concise -- use a brief summary format, not verbose tables.

## Step 3: Knowledge Graph Stats (MCP only)

If MCP tools are available, also call:
- mempalace_kg_stats -- for a knowledge graph overview (triple count, entity
  count, relationship types)
- mempalace_graph_stats -- for connectivity information (connected components,
  average connections per entity)

Present these alongside the palace counts in a unified summary.

## Step 4: Suggest Next Actions

Based on the current state, suggest one relevant action:

- Empty palace (zero memories): Suggest "Try /mempalace:mine to add data from
  files, URLs, or text."
- Has data but no knowledge graph (memories exist but KG stats show zero
  triples): Suggest "Consider adding knowledge graph triples for richer
  queries."
- Healthy palace (has memories and KG data): Suggest "Use /mempalace:search to
  query your memories."

## Output Style

- Be concise and informative -- aim for a quick glance, not a report.
- Use short labels and numbers, not prose paragraphs.
- If any step fails or a tool is unavailable, note it briefly and continue
  with what is available.

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
