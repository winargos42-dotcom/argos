---
argos_import: project_file
source_path: awesome-claude-code-subagents-main/awesome-claude-code-subagents-main/tools/subagent-catalog/invalidate.md
source_abs: F:\debug\argoss\awesome-claude-code-subagents-main\awesome-claude-code-subagents-main\tools\subagent-catalog\invalidate.md
source_ext: .md
source_sha256: 97cc95add315d4738e8b4c9d15ea128175d55aa16fc325e92b9ff9330d7ae37c
text_sha256: 97cc95add315d4738e8b4c9d15ea128175d55aa16fc325e92b9ff9330d7ae37c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:16
---

# invalidate.md

- Source: `awesome-claude-code-subagents-main/awesome-claude-code-subagents-main/tools/subagent-catalog/invalidate.md`
- Extract: `text`
- SHA256: `97cc95add315d4738e8b4c9d15ea128175d55aa16fc325e92b9ff9330d7ae37c`

## Content

---
name: invalidate
description: "Invalidate the subagent-catalog cache. Use when results seem stale or user explicitly asks to refresh or clear cache."
---

# Subagent Catalog - Invalidate

Force-refresh the cached catalog by deleting the local cache file. The next `search` or `fetch` call will pull fresh data from the repository.

## Input: $ARGUMENTS

No arguments required. Optional: pass `--fetch` to immediately refresh after invalidation.

## Instructions

### Step 1: Source config

```bash
source ~/.claude/commands/subagent-catalog/config.sh
```

### Step 2: Invalidate (and optionally refresh)

**Invalidate only** (default):

```bash
subagent_catalog_invalidate_cache
```

**Invalidate and refresh** (if `$ARGUMENTS` contains `--fetch` or user explicitly asks to refresh):

```bash
subagent_catalog_invalidate_cache
subagent_catalog_refresh_cache
```

### Step 3: Confirm

Report the result:
- If invalidated only: "cache invalidated. next search/fetch will pull fresh data."
- If refreshed: "cache invalidated and refreshed with latest catalog."

### When to use

- After the upstream repo has been updated with new subagents
- If you suspect the cache is corrupted
- To troubleshoot stale results

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
