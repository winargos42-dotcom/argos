---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/plugin-forge/references/plugin-structure.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\plugin-forge\references\plugin-structure.md
source_ext: .md
source_sha256: ba3b27cf70be065336af00317b4a3a77b8a2247693d775f9118399aa436e9251
text_sha256: 88bdce4368a29409c20500df5138cc88990989e47575382a494231a4a8e5f9a5
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# plugin-structure.md

- Source: `claude-code-templates/cli-tool/components/skills/development/plugin-forge/references/plugin-structure.md`
- Extract: `text`
- SHA256: `ba3b27cf70be065336af00317b4a3a77b8a2247693d775f9118399aa436e9251`

## Content

# Plugin Structure Reference

## Directory Hierarchy

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin metadata manifest
├── commands/                 # Optional: Custom slash commands
├── agents/                   # Optional: Agent definitions
├── skills/                   # Optional: Agent Skills
│   └── skill-name/
│       ├── SKILL.md         # Required for each skill
│       ├── scripts/         # Optional: Executable code
│       ├── references/      # Optional: Documentation
│       └── assets/          # Optional: Output files
├── hooks/                    # Optional: Event handlers
│   └── hooks.json
└── .mcp.json                # Optional: MCP server integrations
```

## Plugin Manifest (`plugin.json`)

**Location:** `.claude-plugin/plugin.json` (must be in this directory)

**Required fields:**

- `name`: Unique identifier (kebab-case)

**Standard metadata:**

- `version`: Semantic versioning (e.g., "1.0.0")
- `description`: Plugin purpose
- `author`: Object with name, email, url
- `homepage`: URL
- `repository`: URL
- `license`: SPDX identifier
- `keywords`: Array of search terms

**Component paths (optional):**

- `commands`: Path to commands directory
- `agents`: Path to agents directory
- `hooks`: Path to hooks configuration
- `mcpServers`: Path to MCP configuration

### Example plugin.json

```json
{
  "name": "example-plugin",
  "version": "1.0.0",
  "description": "Example plugin for demonstration",
  "author": {
    "name": "Plugin Creator",
    "email": "creator@example.com"
  },
  "keywords": ["example", "demo"]
}
```

## Component Types

### Commands

**Location:** `commands/` directory
**Format:** Markdown files with frontmatter
**Naming:** Subdirectories create namespaces via `:`

```
commands/
├── simple.md              # Invoked as /simple
└── namespace/
    └── command.md         # Invoked as /namespace:command
```

### Agents

**Location:** `agents/` directory
**Format:** Markdown files describing agent capabilities

### Skills

**Location:** `skills/` directory
**Format:** Subdirectories with `SKILL.md` file
**Structure:** See skills documentation

### Hooks

**Location:** `hooks/hooks.json` or path specified in manifest
**Events:** PreToolUse, PostToolUse, UserPromptSubmit, Notification, Stop, SubagentStop, SessionStart, SessionEnd, PreCompact

### MCP Servers

**Location:** `.mcp.json` at plugin root
**Purpose:** External tool integrations

## Path Requirements

- All paths relative to plugin root
- Start with `./` for custom paths
- Use `${CLAUDE_PLUGIN_ROOT}` for dynamic resolution in hooks/MCP
- Components must be at plugin root, not inside `.claude-plugin/`

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
