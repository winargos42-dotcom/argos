---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/railway/railway-docs/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\railway\railway-docs\SKILL.md
source_ext: .md
source_sha256: ae164a750f556058a44a10975fbf8578b8ce73df0f0058e2c3644b5305e706ba
text_sha256: 883f1702fcf98d59966774c7144e9e9ed0c0c75c5668431fcd95f3bd8cbd591b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/railway/railway-docs/SKILL.md`
- Extract: `text`
- SHA256: `ae164a750f556058a44a10975fbf8578b8ce73df0f0058e2c3644b5305e706ba`

## Content

---
name: railway-docs
description: Fetch up-to-date Railway documentation to answer questions accurately. Use when user asks about Railway features, how Railway works, or shares a docs.railway.com URL.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Documentation, Docs, Help, Reference, Learning]
dependencies: [railway-cli]
---

# Railway Documentation

Fetch up-to-date Railway documentation to answer questions accurately.

## When to Use

- User asks how something works on Railway (projects, deployments, volumes, etc.)
- User shares a docs.railway.com URL
- User needs current info about Railway features or pricing
- Before answering Railway questions from memory - check the docs first

## LLM-Optimized Sources

Start here for comprehensive, up-to-date info:

| Source             | URL                                         |
| ------------------ | ------------------------------------------- |
| **Full docs**      | `https://docs.railway.com/api/llms-docs.md` |
| **llms.txt index** | `https://railway.com/llms.txt`              |
| **Templates**      | `https://railway.com/llms-templates.md`     |
| **Changelog**      | `https://railway.com/llms-changelog.md`     |
| **Blog**           | `https://blog.railway.com/llms-blog.md`     |

## Fetching Specific Pages

Append `.md` to any docs.railway.com URL:

```
https://docs.railway.com/guides/projects
→ https://docs.railway.com/guides/projects.md
```

## Common Doc Paths

| Topic       | URL                                              |
| ----------- | ------------------------------------------------ |
| Projects    | `https://docs.railway.com/guides/projects.md`    |
| Deployments | `https://docs.railway.com/guides/deployments.md` |
| Volumes     | `https://docs.railway.com/guides/volumes.md`     |
| Variables   | `https://docs.railway.com/guides/variables.md`   |
| CLI         | `https://docs.railway.com/reference/cli-api.md`  |
| Pricing     | `https://docs.railway.com/reference/pricing.md`  |

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
