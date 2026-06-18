---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-data/bright-data-mcp/references/mcp-setup.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-data\bright-data-mcp\references\mcp-setup.md
source_ext: .md
source_sha256: ac6fc331c16b4380f663820afb8d601a317083ba5fbea38a05f3a9271841eb6f
text_sha256: b1f4ef5a19c0354d418f917ebb2f223804e46825aee94aeb7a5e301e93e4d259
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# mcp-setup.md

- Source: `claude-code-templates/cli-tool/components/skills/web-data/bright-data-mcp/references/mcp-setup.md`
- Extract: `text`
- SHA256: `ac6fc331c16b4380f663820afb8d601a317083ba5fbea38a05f3a9271841eb6f`

## Content

# Bright Data MCP Server Setup

## Prerequisites

1. A Bright Data account - sign up at [brightdata.com](https://brightdata.com)
2. An API token from the [Bright Data Dashboard](https://brightdata.com/cp)

## Remote MCP Server (Recommended)

The remote MCP server requires no local installation. Connect directly via URL.

### Base URL

```
https://mcp.brightdata.com/mcp?token=<YOUR_BRIGHTDATA_API_TOKEN>
```

### Optional Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `pro` | `1` | Enable all 60+ Pro tools (browser automation, structured extraction) |
| `groups` | Group name(s) | Enable specific tool groups without full Pro mode |
| `tools` | Tool name(s) | Enable only specific individual tools |

### URL Examples

**Rapid (Free) mode** - search and scrape only:
```
https://mcp.brightdata.com/mcp?token=YOUR_TOKEN
```

**Full Pro mode** - all 60+ tools:
```
https://mcp.brightdata.com/mcp?token=YOUR_TOKEN&pro=1
```

**Specific groups** - e.g., social media + e-commerce:
```
https://mcp.brightdata.com/mcp?token=YOUR_TOKEN&groups=social,ecommerce
```

**Specific tools** - e.g., only Amazon product and search:
```
https://mcp.brightdata.com/mcp?token=YOUR_TOKEN&tools=web_data_amazon_product,search_engine
```

### Setup in Claude.ai

1. Go to Settings > Extensions
2. Click "Add Extension" or "Add MCP Server"
3. Enter the MCP URL with your token
4. Verify connection shows "Connected" status

### Setup in Claude Code

Add to your Claude Code MCP settings (typically `~/.claude/settings.json` or project-level `.claude/settings.json`):

```json
{
  "mcpServers": {
    "brightdata": {
      "url": "https://mcp.brightdata.com/mcp?token=YOUR_TOKEN&pro=1"
    }
  }
}
```

For Rapid (free) mode only:
```json
{
  "mcpServers": {
    "brightdata": {
      "url": "https://mcp.brightdata.com/mcp?token=YOUR_TOKEN"
    }
  }
}
```

## Local MCP Server

For users who prefer running the MCP server locally.

### Installation

Install via npm:
```bash
npm install -g @brightdata/mcp
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_TOKEN` | Yes | Your Bright Data API token |
| `PRO_MODE` | No | Set to `true` to enable Pro tools |
| `GROUPS` | No | Comma-separated group names |

### Running Locally

```bash
API_TOKEN=your_token PRO_MODE=true npx @brightdata/mcp
```

## Choosing Your Mode

### Rapid (Free) - Default
- `search_engine` and `scrape_as_markdown` available
- No additional cost beyond standard API usage
- Best for: everyday browsing, reading web pages, search queries

### Pro Mode (`pro=1`)
- All 60+ tools enabled
- Structured data from Amazon, LinkedIn, Instagram, TikTok, YouTube, etc.
- Browser automation tools
- Best for: data extraction, social media analysis, e-commerce monitoring, automation

### Groups (Selective Pro)
Enable only the tool groups you need:
- `ecommerce` - Amazon, Walmart, eBay, Best Buy, etc.
- `social` - LinkedIn, Instagram, Facebook, TikTok, YouTube, X, Reddit
- `business` - Crunchbase, ZoomInfo, Google Maps, Zillow
- `finance` - Yahoo Finance
- `research` - Reuters, GitHub
- `app_stores` - Google Play, Apple App Store
- `travel` - Booking.com
- `browser` - Full browser automation
- `advanced_scraping` - HTML scraping, AI extraction, batch operations

## Verifying Your Setup

After connecting, test with a simple tool call:

1. Ask Claude: "Use the Bright Data MCP to search for 'test query'"
2. This should call `search_engine` and return results
3. If it works, your MCP connection is active

If it fails:
- Check your API token is valid and not expired
- Verify the MCP URL is correctly formatted
- Check network connectivity to mcp.brightdata.com
- Try reconnecting in Settings > Extensions

## Documentation

Full documentation index: https://docs.brightdata.com/llms.txt

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
