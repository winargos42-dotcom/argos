---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/plugin-forge/references/marketplace-schema.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\plugin-forge\references\marketplace-schema.md
source_ext: .md
source_sha256: e5adeca330cd29b6de9d10323dca75e14c354ad9a6412b51329458a01e8f0a7b
text_sha256: 5a9b0859b06d7a9ed28a4cf62b71b94b8d7970d5b96a11d602f76975a025d29c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# marketplace-schema.md

- Source: `claude-code-templates/cli-tool/components/skills/development/plugin-forge/references/marketplace-schema.md`
- Extract: `text`
- SHA256: `e5adeca330cd29b6de9d10323dca75e14c354ad9a6412b51329458a01e8f0a7b`

## Content

# Marketplace Schema Reference

## Marketplace Structure

A marketplace is a JSON catalog enabling plugin discovery and distribution.

**File location:** `.claude-plugin/marketplace.json`

## Required Fields

```json
{
  "name": "marketplace-identifier",
  "owner": {
    "name": "Maintainer Name",
    "email": "maintainer@example.com"
  },
  "plugins": []
}
```

**name**: Kebab-case marketplace identifier
**owner**: Maintainer contact information
**plugins**: Array of plugin entries

## Optional Marketplace Fields

**description**: Marketplace overview text
**version**: Release version
**pluginRoot**: Base path for relative plugin sources

## Plugin Entry Schema

Each plugin entry in the `plugins` array:

**Required:**

- `name`: Plugin identifier (kebab-case, must match plugin.json)
- `source`: Plugin origin specification

**Optional:**

- `description`: Plugin purpose
- `version`: Plugin version (semantic versioning)
- `author`: Creator information
- `homepage`: URL
- `repository`: URL
- `license`: SPDX identifier
- `keywords`: Array of search terms
- `category`: Classification (e.g., "framework", "productivity")
- `tags`: Additional discovery tags
- `commands`: Path to commands directory
- `agents`: Path to agents directory
- `hooks`: Path to hooks configuration
- `mcpServers`: Path to MCP configuration

## Source Specifications

### Relative Path Source

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

### GitHub Source

```json
{
  "name": "my-plugin",
  "source": {
    "source": "github",
    "repo": "owner/repo"
  }
}
```

### Generic Git Source

```json
{
  "name": "my-plugin",
  "source": {
    "source": "url",
    "url": "https://git.example.com/plugin.git"
  }
}
```

## Complete Example

```json
{
  "name": "example-marketplace",
  "description": "Example plugin marketplace",
  "version": "1.0.0",
  "owner": {
    "name": "Marketplace Owner",
    "email": "owner@example.com"
  },
  "pluginRoot": "./plugins",
  "plugins": [
    {
      "name": "example-plugin",
      "source": "./example-plugin",
      "description": "Example plugin",
      "version": "1.0.0",
      "keywords": ["example"],
      "category": "productivity"
    }
  ]
}
```

## Team Distribution

Configure automatic marketplace availability via `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": [
    {
      "source": {
        "source": "github",
        "repo": "company/marketplace"
      }
    }
  ]
}
```

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
