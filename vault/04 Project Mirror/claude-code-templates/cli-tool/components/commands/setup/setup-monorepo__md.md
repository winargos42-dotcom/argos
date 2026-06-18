---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/setup-monorepo.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\setup-monorepo.md
source_ext: .md
source_sha256: a1590cb74b83c03be94291ab4f2fa6aaa61297cefbc806c84dde718785639c22
text_sha256: ca274d22c4cdfab5efe03e2d5e0f87220c1fd638b9885bf7596222d7f6c2902c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# setup-monorepo.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/setup-monorepo.md`
- Extract: `text`
- SHA256: `a1590cb74b83c03be94291ab4f2fa6aaa61297cefbc806c84dde718785639c22`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [monorepo-tool] | --nx | --lerna | --rush | --turborepo | --yarn-workspaces
description: Configure monorepo project structure with comprehensive workspace management and build orchestration
---

# Setup Monorepo

Configure comprehensive monorepo structure with advanced workspace management: **$ARGUMENTS**

## Current Project State

- Repository structure: !`find . -maxdepth 2 -type d | head -10`
- Package manager: @package.json or existing workspace configuration
- Existing monorepo: @nx.json or @lerna.json or @rush.json or @turbo.json
- Project count: !`find . -name "package.json" -not -path "./node_modules/*" | wc -l`

## Task

Implement production-ready monorepo with advanced workspace management and build orchestration:

**Monorepo Tool**: Use $ARGUMENTS to configure Nx, Lerna, Rush, Turborepo, or Yarn Workspaces

**Monorepo Architecture**:
1. **Workspace Structure** - Directory organization, package architecture, shared libraries, application separation
2. **Dependency Management** - Workspace dependencies, version management, package hoisting, conflict resolution
3. **Build Orchestration** - Task dependencies, parallel builds, incremental compilation, affected package detection
4. **Development Workflow** - Hot reloading, debugging, testing strategies, development server coordination
5. **CI/CD Integration** - Build pipelines, affected project detection, deployment orchestration, artifact management
6. **Tooling Configuration** - Shared configurations, code quality tools, testing frameworks, documentation

**Advanced Features**: Task caching, distributed execution, performance optimization, plugin ecosystem integration.

**Team Productivity**: Developer experience optimization, onboarding automation, maintenance procedures.

**Output**: Complete monorepo setup with optimized build system, comprehensive tooling, and team productivity enhancements.

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
