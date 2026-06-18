---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/jupyter-notebook/references/notebook-structure.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\jupyter-notebook\references\notebook-structure.md
source_ext: .md
source_sha256: 58b2418597fe3a2b58d83075c62400b195cbd34330b0c5e7ee0451f9a6159c3c
text_sha256: a85051a2e88fd3424bbed2636e952ec5f858e7efa4e076c28d62a8cc2cc9dc06
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# notebook-structure.md

- Source: `claude-code-templates/cli-tool/components/skills/development/jupyter-notebook/references/notebook-structure.md`
- Extract: `text`
- SHA256: `58b2418597fe3a2b58d83075c62400b195cbd34330b0c5e7ee0451f9a6159c3c`

## Content

# Notebook Structure

Jupyter notebooks are JSON documents with this high-level shape:

- `nbformat` and `nbformat_minor`
- `metadata`
- `cells` (a list of markdown and code cells)

When editing `.ipynb` files programmatically:

- Preserve `nbformat` and `nbformat_minor` from the template.
- Keep `cells` as an ordered list; do not reorder unless intentional.
- For code cells, set `execution_count` to `null` when unknown.
- For code cells, set `outputs` to an empty list when scaffolding.
- For markdown cells, keep `cell_type="markdown"` and `metadata={}`.

Prefer scaffolding from the bundled templates or `new_notebook.py` (for example, `$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py`) instead of hand-authoring raw notebook JSON.

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
