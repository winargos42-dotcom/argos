---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-data/search/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-data\search\SKILL.md
source_ext: .md
source_sha256: 3907584d4e6ad71c5ffe5bfc85e484ffa509a547db73eeb25839d833d229e448
text_sha256: c5ebbe4fb8a80c9a595d1ee0d84b39384aaa96508a766076b00d3b03281574cf
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/web-data/search/SKILL.md`
- Extract: `text`
- SHA256: `3907584d4e6ad71c5ffe5bfc85e484ffa509a547db73eeb25839d833d229e448`

## Content

---
name: search
description: Search Google via Bright Data SERP API. Returns structured JSON results with title, link, and description. Requires BRIGHTDATA_API_KEY and BRIGHTDATA_UNLOCKER_ZONE environment variables.
---

# Bright Data - Google Search

Search Google and get structured JSON results using Bright Data's SERP API.

## Setup

**1. Get your API Key:**
Get a key from [Bright Data Dashboard](https://brightdata.com/cp).

**2. Create a Web Unlocker zone:**
Create a zone at brightdata.com/cp by clicking "Add" (top-right), selecting "Unlocker zone".

**3. Set environment variables:**
```bash
export BRIGHTDATA_API_KEY="your-api-key"
export BRIGHTDATA_UNLOCKER_ZONE="your-zone-name"
```

## Usage

```bash
bash scripts/search.sh "query" [cursor]
```

**Parameters:**
- `query` (required): Search term
- `cursor` (optional): Page number for pagination (0-indexed, default: 0)

**Examples:**
```bash
# Basic search
bash scripts/search.sh "climate change"

# Get page 2 of results
bash scripts/search.sh "climate change" 1
```

## Output Format

Returns JSON with structured `organic` array:
```json
{
  "organic": [
    {
      "link": "https://example.com/article",
      "title": "Article Title",
      "description": "Brief description of the page..."
    }
  ]
}
```

## Dependencies

- `curl` - For API requests
- `jq` - For JSON processing

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
