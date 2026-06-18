---
argos_import: project_file
source_path: awesome-claude-code-subagents-main/awesome-claude-code-subagents-main/tools/subagent-catalog/list.md
source_abs: F:\debug\argoss\awesome-claude-code-subagents-main\awesome-claude-code-subagents-main\tools\subagent-catalog\list.md
source_ext: .md
source_sha256: b83beeb61298a1e852a23f20abf66c50f50d1d031b6dbfd385e82942b17755e9
text_sha256: b83beeb61298a1e852a23f20abf66c50f50d1d031b6dbfd385e82942b17755e9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:16
---

# list.md

- Source: `awesome-claude-code-subagents-main/awesome-claude-code-subagents-main/tools/subagent-catalog/list.md`
- Extract: `text`
- SHA256: `b83beeb61298a1e852a23f20abf66c50f50d1d031b6dbfd385e82942b17755e9`

## Content

---
name: list
description: "List all categories and agents in the subagent catalog. Use when user wants to see everything available or browse the full catalog."
---

# Subagent Catalog - List

Browse all available categories and agents from the awesome-claude-code-subagents catalog.

## Input: $ARGUMENTS

No arguments required.

## Instructions

### Step 1: Ensure cache is fresh

```bash
source ~/.claude/commands/subagent-catalog/config.sh
subagent_catalog_ensure_cache
```

### Step 2: Extract and display categories

Parse the catalog and display all categories with their agents:

```bash
# extract category headers and agent entries
grep -E "^### \[|^\- \[\*\*" "$SUBAGENT_CATALOG_CACHE_FILE"
```

### Step 3: Format output

Display as a scannable list:

```
## Subagent Catalog

### 01. Core Development
api-designer, backend-developer, frontend-developer, fullstack-developer, ...

### 02. Language Specialists
typescript-pro, python-pro, rust-engineer, golang-pro, ...

### 03. Infrastructure
cloud-architect, devops-engineer, kubernetes-specialist, terraform-engineer, ...

[...continue for all 10 categories...]
```

### Tips

- use `/subagent-catalog:search <query>` to filter by keyword
- use `/subagent-catalog:fetch <name>` to get full definition

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
