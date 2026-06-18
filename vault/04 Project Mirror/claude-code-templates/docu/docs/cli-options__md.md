---
argos_import: project_file
source_path: claude-code-templates/docu/docs/cli-options.md
source_abs: F:\debug\argoss\claude-code-templates\docu\docs\cli-options.md
source_ext: .md
source_sha256: 6f96e072934dfac9a0569ade5fc0fa9141c5ac3beec7b410473b686ca5f0a4a0
text_sha256: 169f03d9f4810ae2350acee0ecc739911835023d9923e17c23cecad783e3c242
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# cli-options.md

- Source: `claude-code-templates/docu/docs/cli-options.md`
- Extract: `text`
- SHA256: `6f96e072934dfac9a0569ade5fc0fa9141c5ac3beec7b410473b686ca5f0a4a0`

## Content

---
sidebar_position: 1
---

# CLI Options Reference

This section provides a comprehensive reference of all available command-line options for `claude-code-templates`.

## Template and Component Options

| Option | Description | Example |
|--------|-------------|---------|
| `--template` | **[PREFERRED]** Specify template to install | `--template=python`, `--template=react` |
| `--agent` | Install individual agent component | `--agent=react-performance` |
| `--command` | Install individual command component | `--command=check-file` |
| `--mcp` | Install individual MCP component | `--mcp=github-integration` |

## Legacy Options (Deprecated)

| Option | Description | Example | Status |
|--------|-------------|---------|---------|
| `-l, --language` | Specify programming language | `--language python` | ⚠️ **Deprecated** - Use `--template` instead |
| `-f, --framework` | Specify framework | `--framework react` | ⚠️ **Deprecated** - Use `--template` instead |

## General Options

| Option | Description | Example |
|--------|-------------|---------|
| `-d, --directory` | Target directory | `--directory /path/to/project` |
| `-y, --yes` | Skip prompts and use defaults | `--yes` |
| `--dry-run` | Show what would be installed | `--dry-run` |

## Analysis and Monitoring Options

| Option | Description | Example |
|--------|-------------|---------|
| `--health-check` | Run comprehensive system validation | `--health-check` |
| `--command-stats, --commands-stats` | Analyze existing commands | `--command-stats` |
| `--hook-stats, --hooks-stats` | Analyze automation hooks | `--hook-stats` |
| `--mcp-stats, --mcps-stats` | Analyze MCP server configurations | `--mcp-stats` |
| `--analytics` | Launch real-time analytics dashboard | `--analytics` |

## Help and Information

| Option | Description | Example |
|--------|-------------|---------|
| `--help` | Show help information | `--help` |

## Usage Examples

### Modern Template Installation (Recommended)
```bash
# Install React template with all components
npx claude-code-templates@latest --template=react --yes

# Install Python template with all components
npx claude-code-templates@latest --template=python --yes

# Install Node.js template with all components
npx claude-code-templates@latest --template=nodejs --yes
```

### Individual Component Installation
```bash
# Install specific agent
npx claude-code-templates@latest --agent=react-performance --yes

# Install specific command
npx claude-code-templates@latest --command=check-file --yes

# Install specific MCP
npx claude-code-templates@latest --mcp=github-integration --yes
```

### Legacy Syntax (Still Supported)
```bash
# Old syntax - still works but deprecated
npx claude-code-templates@latest --language=javascript-typescript --framework=react --yes
```

## GitHub Download System

All templates and components are now downloaded directly from GitHub in real-time:

- **Templates**: Downloaded from `templates/` directory
- **Components**: Downloaded from `components/` directory (agents, commands, MCPs)
- **Caching**: Downloaded files are cached for performance
- **Transparency**: All download URLs are visible during installation

This ensures you always get the latest versions and provides complete transparency about what is being installed.

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
