---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-data/scrape/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-data\scrape\SKILL.md
source_ext: .md
source_sha256: 515401808e66c180ce33e092edd5d0f09bb552a3dc27223e404b241a1c75d946
text_sha256: b3329adc7add28fe08797f86b56eed2a6ac4f0aba22e29d45c24e884225f9393
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/web-data/scrape/SKILL.md`
- Extract: `text`
- SHA256: `515401808e66c180ce33e092edd5d0f09bb552a3dc27223e404b241a1c75d946`

## Content

---
name: scrape
description: Scrape any webpage as clean markdown via Bright Data Web Unlocker API. Bypasses bot detection and CAPTCHA. Requires BRIGHTDATA_API_KEY and BRIGHTDATA_UNLOCKER_ZONE environment variables.
---

# Bright Data - Web Scraper

Scrape any webpage and get clean markdown content using Bright Data's Web Unlocker API. Automatically bypasses bot detection and CAPTCHA.

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
bash scripts/scrape.sh "url"
```

**Parameters:**
- `url` (required): The webpage URL to scrape

**Examples:**
```bash
# Scrape a news article
bash scripts/scrape.sh "https://example.com/article"

# Scrape a product page
bash scripts/scrape.sh "https://shop.example.com/product/123"
```

## Output Format

Returns clean markdown content extracted from the webpage:
```markdown
# Page Title

Main content of the page converted to markdown format...

## Section Heading

More content...
```

## Features

- **Bot Detection Bypass**: Automatically handles anti-bot measures
- **CAPTCHA Solving**: Bypasses CAPTCHA challenges
- **Clean Markdown**: Returns well-formatted markdown content
- **JavaScript Rendering**: Handles JavaScript-heavy pages

## Dependencies

- `curl` - For API requests

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
