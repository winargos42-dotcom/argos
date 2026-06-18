---
argos_import: project_file
source_path: awesome-claude-code-subagents-main/awesome-claude-code-subagents-main/tools/subagent-catalog/fetch.md
source_abs: F:\debug\argoss\awesome-claude-code-subagents-main\awesome-claude-code-subagents-main\tools\subagent-catalog\fetch.md
source_ext: .md
source_sha256: ca80b6b6c727acdc73b9b236cafea23f114e319f65f082956f8e349ada5a7fd7
text_sha256: ca80b6b6c727acdc73b9b236cafea23f114e319f65f082956f8e349ada5a7fd7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:16
---

# fetch.md

- Source: `awesome-claude-code-subagents-main/awesome-claude-code-subagents-main/tools/subagent-catalog/fetch.md`
- Extract: `text`
- SHA256: `ca80b6b6c727acdc73b9b236cafea23f114e319f65f082956f8e349ada5a7fd7`

## Content

---
name: fetch
description: "Fetch full subagent definition from catalog. Use when user wants to get, download, view, or use a specific subagent."
---

# Subagent Catalog - Fetch

Get the full definition of a specific agent.

## Input: $ARGUMENTS

Accepts: agent name, path, or GitHub URL.

## Example

```
/subagent-catalog:fetch code-reviewer

## code-reviewer

**Category**: Quality & Security
**Tools**: Read, Write, Edit, Bash, Glob, Grep

Expert code reviewer specializing in code quality, security vulnerabilities...

[full definition follows]

---
**What now?**
- save to ~/.claude/agents/code-reviewer.md
- customize for this project
- spawn as Task subagent
```

## Instructions

### Progress checklist

Copy and track:
- [ ] Step 1: Resolve agent path from catalog
- [ ] Step 2: Fetch full definition
- [ ] Step 3: Display and offer options

### Step 1: Resolve path

```bash
source ~/.claude/commands/subagent-catalog/config.sh
subagent_catalog_ensure_cache

# find the agent (use -F for literal match)
grep -iF "{{NAME}}" "$SUBAGENT_CATALOG_CACHE_FILE"
```

Extract path from: `[**name**](path)`

### Step 2: Fetch definition

```bash
tmp_file=$(mktemp)
if curl -sf "$SUBAGENT_CATALOG_REPO_URL/{{PATH}}" -o "$tmp_file"; then
  cat "$tmp_file"
  rm -f "$tmp_file"
else
  rm -f "$tmp_file"
  subagent_catalog_log_error "failed to fetch. try /subagent-catalog:search first"
fi
```

### Step 3: Display and offer options

Show the definition with frontmatter parsed, then offer:
1. save locally (`~/.claude/agents/<name>.md`)
2. customize for project
3. spawn as Task

### Error handling

| error | suggestion |
|-------|------------|
| not found | run `/subagent-catalog:search <partial>` |
| multiple matches | list them, ask user to specify |
| network error | check connection, retry |

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
