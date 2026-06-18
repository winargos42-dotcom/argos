---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/documentation/load-llms-txt.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\documentation\load-llms-txt.md
source_ext: .md
source_sha256: f08e43468bf4f2c48187e819865a596f028919a2e095cd23940255d7b7dfc3e6
text_sha256: 1086cf4f8d6b2d36c440145758c170759657e3c4bc8c258fceccff2d7d22e549
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# load-llms-txt.md

- Source: `claude-code-templates/cli-tool/components/commands/documentation/load-llms-txt.md`
- Extract: `text`
- SHA256: `f08e43468bf4f2c48187e819865a596f028919a2e095cd23940255d7b7dfc3e6`

## Content

---
allowed-tools: Bash, WebFetch
argument-hint: [data-source] | --xatu | --custom-url | --validate
description: Load and process external documentation context from llms.txt files or custom sources
---

# External Documentation Context Loader

Load external documentation context: $ARGUMENTS

## Current Context Status

- Network access: !`curl -s --connect-timeout 5 https://httpbin.org/status/200 >/dev/null && echo "✅ Available" || echo "❌ Limited"`
- Existing context: Check for local llms.txt or documentation cache
- Project type: @package.json or @README.md (detect project context needs)

## Task

Load and process external documentation context from specified source.

### Default Action (Xatu Data)
Load the llms.txt file from Xatu data repository:
```bash
curl -s https://raw.githubusercontent.com/ethpandaops/xatu-data/refs/heads/master/llms.txt
```

### Custom Source Loading
For custom URLs or alternative documentation sources:
- Validate URL accessibility
- Download and cache content
- Process and structure information
- Integration with project context

### Processing Options
- **Raw loading**: Direct content retrieval
- **Validation**: Check content format and structure  
- **Integration**: Merge with existing project documentation
- **Caching**: Store locally for offline access

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
