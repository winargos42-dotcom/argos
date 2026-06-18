---
argos_import: project_file
source_path: mempalace-develop/website/concepts/knowledge-graph.md
source_abs: F:\debug\argoss\mempalace-develop\website\concepts\knowledge-graph.md
source_ext: .md
source_sha256: e6a76e60174d80bd4ff47837f7fd69330820e4b70b282ded49b607adf2e34813
text_sha256: e6a76e60174d80bd4ff47837f7fd69330820e4b70b282ded49b607adf2e34813
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# knowledge-graph.md

- Source: `mempalace-develop/website/concepts/knowledge-graph.md`
- Extract: `text`
- SHA256: `e6a76e60174d80bd4ff47837f7fd69330820e4b70b282ded49b607adf2e34813`

## Content

# Knowledge Graph

MemPalace includes a temporal entity-relationship graph — like Zep's Graphiti, but SQLite instead of Neo4j. Local and free.

## What It Stores

Entity-relationship triples with temporal validity:

```
Subject → Predicate → Object [valid_from → valid_to]
```

Facts have time windows. When something stops being true, you invalidate it — and historical queries still find it.

## Usage

### Python API

```python
from mempalace.knowledge_graph import KnowledgeGraph

kg = KnowledgeGraph()

# Add facts
kg.add_triple("Kai", "works_on", "Orion", valid_from="2025-06-01")
kg.add_triple("Maya", "assigned_to", "auth-migration", valid_from="2026-01-15")
kg.add_triple("Maya", "completed", "auth-migration", valid_from="2026-02-01")

# Query: everything about Kai
kg.query_entity("Kai")
# → [Kai → works_on → Orion (current), Kai → recommended → Clerk (2026-01)]

# Query: what was true in January?
kg.query_entity("Maya", as_of="2026-01-20")
# → [Maya → assigned_to → auth-migration (active)]

# Timeline
kg.timeline("Orion")
# → chronological story of the project
```

### Invalidating Facts

When something stops being true:

```python
kg.invalidate("Kai", "works_on", "Orion", ended="2026-03-01")
```

Now queries for Kai's current work won't return Orion. Historical queries still will.

### MCP Tools

Through the MCP server, the knowledge graph is available as tools:

| Tool | Description |
|------|-------------|
| `mempalace_kg_query` | Query entity relationships with time filtering |
| `mempalace_kg_add` | Add facts |
| `mempalace_kg_invalidate` | Mark facts as ended |
| `mempalace_kg_timeline` | Chronological entity story |
| `mempalace_kg_stats` | Graph overview |

## Storage

The knowledge graph uses SQLite with two tables:

**`entities`** — people, projects, tools, concepts:
- `id` — lowercase normalized name
- `name` — display name
- `type` — person, project, tool, concept, etc.
- `properties` — JSON blob for extra metadata

**`triples`** — relationships between entities:
- `subject` → `predicate` → `object`
- `valid_from` — when this became true
- `valid_to` — when it stopped being true (NULL = still current)
- `confidence` — 0.0 to 1.0
- `source_closet` — link back to the verbatim memory

Database location: `~/.mempalace/knowledge_graph.sqlite3`

## Comparison

| Feature | MemPalace | Zep (Graphiti) |
|---------|-----------|----------------|
| Storage | SQLite (local) | Neo4j (cloud) |
| Cost | Free | $25/mo+ |
| Temporal validity | Yes | Yes |
| Self-hosted | Always | Enterprise only |
| Privacy | Everything local | SOC 2, HIPAA |

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
