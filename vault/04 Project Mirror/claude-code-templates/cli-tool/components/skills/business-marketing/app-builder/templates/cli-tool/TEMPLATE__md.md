---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/cli-tool/TEMPLATE.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\business-marketing\app-builder\templates\cli-tool\TEMPLATE.md
source_ext: .md
source_sha256: 229eb9fad32b9f7e7d6289e43d20b6aecb708639bba08ff084e8cd3aed4fd47f
text_sha256: 89c0e5940c9fc79e664981d2826f9d5b2c4855a343d6b179ed0087032d3a323d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# TEMPLATE.md

- Source: `claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/cli-tool/TEMPLATE.md`
- Extract: `text`
- SHA256: `229eb9fad32b9f7e7d6289e43d20b6aecb708639bba08ff084e8cd3aed4fd47f`

## Content

---
name: cli-tool
description: Node.js CLI tool template principles. Commander.js, interactive prompts.
---

# CLI Tool Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Runtime | Node.js 20+ |
| Language | TypeScript |
| CLI Framework | Commander.js |
| Prompts | Inquirer.js |
| Output | chalk + ora |
| Config | cosmiconfig |

---

## Directory Structure

```
project-name/
├── src/
│   ├── index.ts         # Entry point
│   ├── cli.ts           # CLI setup
│   ├── commands/        # Command handlers
│   ├── lib/
│   │   ├── config.ts    # Config loader
│   │   └── logger.ts    # Styled output
│   └── types/
├── bin/
│   └── cli.js           # Executable
└── package.json
```

---

## CLI Design Principles

| Principle | Description |
|-----------|-------------|
| Subcommands | Group related actions |
| Options | Flags with defaults |
| Interactive | Prompts when needed |
| Non-interactive | Support --yes flags |

---

## Key Components

| Component | Purpose |
|-----------|---------|
| Commander | Command parsing |
| Inquirer | Interactive prompts |
| Chalk | Colored output |
| Ora | Spinners/loading |
| Cosmiconfig | Config file discovery |

---

## Setup Steps

1. Create project directory
2. `npm init -y`
3. Install deps: `npm install commander @inquirer/prompts chalk ora cosmiconfig`
4. Configure bin in package.json
5. `npm link` for local testing

---

## Publishing

```bash
npm login
npm publish
```

---

## Best Practices

- Provide helpful error messages
- Support both interactive and non-interactive modes
- Use consistent output styling
- Validate inputs with Zod
- Exit with proper codes (0 success, 1 error)

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
