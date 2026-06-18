---
argos_import: project_file
source_path: claude-code-config-main/claude-code-config-main/rules/memory-crosslinks.md
source_abs: F:\debug\argoss\claude-code-config-main\claude-code-config-main\rules\memory-crosslinks.md
source_ext: .md
source_sha256: 346b25a68cd5fa15a4821ab4cd99b0d1c2b3cc9d25f75a6fdd018427b5d1fd53
text_sha256: 346b25a68cd5fa15a4821ab4cd99b0d1c2b3cc9d25f75a6fdd018427b5d1fd53
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:26
---

# memory-crosslinks.md

- Source: `claude-code-config-main/claude-code-config-main/rules/memory-crosslinks.md`
- Extract: `text`
- SHA256: `346b25a68cd5fa15a4821ab4cd99b0d1c2b3cc9d25f75a6fdd018427b5d1fd53`

## Content

# Memory Cross-Links - wiki-links graph pattern

Memory files can reference each other using wiki-links `\[\[filename\]\]` (without .md extension). This creates a navigable knowledge graph without any database.

## Where to add links

**Inline** in text body:
```markdown
Training runs on \[\[reference_gpu_servers\]\] using the \[\[docker_production\]\] image.
```

**## Related** section at end of file:
```markdown
## Related
- \[\[reference_gpu_servers\]\] - trains on these servers
- \[\[project_model_v2\]\] - result of this training
- \[\[practice_autoresearch\]\] - methodology used for optimization
```

## When to add links

- When **creating** a new memory file - immediately link to existing related entries
- When **updating** a memory file - check if new connections emerged
- Only **meaningful** relationships, not links for the sake of linking
- A good test: "would navigating this link help me understand the current entry better?"

## Common clusters

| Cluster | Contains | Example links |
|---|---|---|
| Infrastructure | servers, docker, tunnels, access rules | server -> docker image -> access rules |
| Projects | active work, LoRAs, research | project -> server (where it runs) -> methodology (how) |
| Methodology | practices, patterns, articles | practice -> article (source) -> project (applied in) |
| Tools | references, repos, services | tool A <-> tool B (alternatives) |
| Feedback | corrections, rules | feedback -> context (which project/server triggered it) |

## Benefits

- **Navigation**: from a project, find which servers it uses and what methodology applies
- **Context**: when reading about a server, see what projects run there
- **Discovery**: find related knowledge you forgot existed
- **No database**: graph lives in plain markdown, survives any tool change

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
