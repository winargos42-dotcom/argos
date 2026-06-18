---
argos_import: project_file
source_path: awesome-claude-code-subagents-main/awesome-claude-code-subagents-main/tools/subagent-catalog/search.md
source_abs: F:\debug\argoss\awesome-claude-code-subagents-main\awesome-claude-code-subagents-main\tools\subagent-catalog\search.md
source_ext: .md
source_sha256: b21874199e5cca2014af10e3ce9e04f90c09881d7ae02d2c199012c8e225eda9
text_sha256: b21874199e5cca2014af10e3ce9e04f90c09881d7ae02d2c199012c8e225eda9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:16
---

# search.md

- Source: `awesome-claude-code-subagents-main/awesome-claude-code-subagents-main/tools/subagent-catalog/search.md`
- Extract: `text`
- SHA256: `b21874199e5cca2014af10e3ce9e04f90c09881d7ae02d2c199012c8e225eda9`

## Content

---
name: search
description: "Search the awesome-claude-code-subagents catalog. Use when user wants to find, discover, or browse available subagents by name, category, or capability."
---

# Subagent Catalog - Search

Find agents by name, description, or category.

## Input: $ARGUMENTS

## Example output

```
## Results for "kubernetes"

| Agent | Description |
|-------|-------------|
| [kubernetes-specialist](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/kubernetes-specialist.md) | Container orchestration master |
| [devops-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/devops-engineer.md) | CI/CD and automation expert |

→ use `/subagent-catalog:fetch <name>` to get full definition
```

## Instructions

### Step 1: Get catalog

```bash
source ~/.claude/commands/subagent-catalog/config.sh
subagent_catalog_ensure_cache
cat "$SUBAGENT_CATALOG_CACHE_FILE"
```

### Step 2: Match and return

Search the catalog content for matches (case-insensitive substring):
- agent names
- descriptions
- category names

Format each match as a table row with GitHub link.

### Step 3: Handle edge cases

- **no results**: suggest related terms or `/subagent-catalog:list`
- **too many results**: ask user to narrow the query
- **category match**: show all agents in that category

## Query examples

| query | matches |
|-------|---------|
| `kubernetes` | kubernetes-specialist, devops-engineer |
| `security` | security-engineer, security-auditor, penetration-tester |
| `python` | python-pro, django-developer |
| `review` | code-reviewer, architect-reviewer |
| `infrastructure` | entire category 03 |

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
