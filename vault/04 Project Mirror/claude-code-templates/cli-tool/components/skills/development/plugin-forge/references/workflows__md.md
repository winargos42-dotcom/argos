---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/plugin-forge/references/workflows.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\plugin-forge\references\workflows.md
source_ext: .md
source_sha256: e117598ff0bbd9c990278f08f5b2f01a834fff3d5893990e6ebd1874e6c1f4a2
text_sha256: 23851bc59bdc50fcf744493772e5e3d3e91cc0515d7530a8a0b27925a39854bd
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# workflows.md

- Source: `claude-code-templates/cli-tool/components/skills/development/plugin-forge/references/workflows.md`
- Extract: `text`
- SHA256: `e117598ff0bbd9c990278f08f5b2f01a834fff3d5893990e6ebd1874e6c1f4a2`

## Content

# Plugin Development Workflows

## Creating a New Plugin

### 1. Create Plugin Directory Structure

```bash
mkdir -p plugins/plugin-name/.claude-plugin
mkdir -p plugins/plugin-name/commands
mkdir -p plugins/plugin-name/skills
```

### 2. Create Plugin Manifest

Create `plugins/plugin-name/.claude-plugin/plugin.json`:

```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "Plugin description",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "keywords": ["keyword1", "keyword2"]
}
```

### 3. Add Plugin to Marketplace

Update `.claude-plugin/marketplace.json` by adding entry to `plugins` array:

```json
{
  "name": "plugin-name",
  "source": "./plugins/plugin-name",
  "description": "Plugin description",
  "version": "0.1.0",
  "keywords": ["keyword1", "keyword2"],
  "category": "productivity"
}
```

### 4. Add Plugin Components

Create commands, skills, agents, or hooks as needed in their respective directories.

## Version Bumping

When making changes to a plugin, update version in **both** locations:

1. `plugins/<plugin-name>/.claude-plugin/plugin.json`
2. `.claude-plugin/marketplace.json` (matching plugin entry)

**Semantic versioning:**

- **Major (x.0.0)**: Breaking changes
- **Minor (0.x.0)**: New features, refactoring
- **Patch (0.0.x)**: Bug fixes, documentation only

## Local Testing Workflow

### Initial Setup

```bash
# Add marketplace
/plugin marketplace add /path/to/marketplace-root

# Install plugin
/plugin install plugin-name@marketplace-name
```

### Iterative Testing

After making changes to a plugin:

```bash
# Uninstall
/plugin uninstall plugin-name@marketplace-name

# Reinstall
/plugin install plugin-name@marketplace-name

# Restart Claude Code to load changes
```

**Note:** Claude Code caches plugin files, so restart may be required for changes to take effect.

## Publishing Workflow

### 1. Commit Changes

Use conventional commits:

```bash
git add .
git commit -m "feat: add new plugin"
git commit -m "fix: correct plugin manifest"
git commit -m "docs: update plugin README"
```

### 2. Push to Repository

```bash
git push origin main
```

### 3. Distribution

**GitHub-hosted marketplace:**

Users add via:

```bash
/plugin marketplace add owner/repo
/plugin install plugin-name@marketplace-name
```

**Local marketplace:**

Users add via absolute path:

```bash
/plugin marketplace add /path/to/marketplace
```

## Command Naming Convention

Commands use subdirectory-based namespacing:

- File: `commands/namespace/command.md`
- Invoked as: `/namespace:command`
- The `:` represents directory separator `/`

**Examples:**

- `commands/prime/vue.md` → `/prime:vue`
- `commands/docs/generate.md` → `/docs:generate`
- `commands/simple.md` → `/simple`

## Common Plugin Patterns

### Framework Plugin

Structure for framework-specific guidance (React, Vue, Nuxt, etc.):

```
plugins/framework-name/
├── .claude-plugin/plugin.json
├── skills/
│   └── framework-name/
│       ├── SKILL.md              # Quick reference
│       └── references/           # Library-specific patterns
├── commands/
│   └── prime/                    # Namespace for loading patterns
│       ├── components.md
│       └── framework.md
└── README.md
```

### Utility Plugin

Structure for tools and utilities:

```
plugins/utility-name/
├── .claude-plugin/plugin.json
├── commands/
│   ├── action1.md
│   └── action2.md
└── README.md
```

### Domain Plugin

Structure for domain-specific knowledge:

```
plugins/domain-name/
├── .claude-plugin/plugin.json
├── skills/
│   └── domain-name/
│       ├── SKILL.md
│       ├── references/
│       │   ├── schema.md
│       │   └── policies.md
│       └── scripts/
│           └── automation.py
└── README.md
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
