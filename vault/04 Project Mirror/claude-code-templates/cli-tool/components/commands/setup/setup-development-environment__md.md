---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/setup-development-environment.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\setup-development-environment.md
source_ext: .md
source_sha256: 220f96e5438ab3313a58b023a83c6f77fd57a0ca79db4cc23e87f3fd7c5b0062
text_sha256: 2d8b42d811adc4ff5374c3b78cacf2c5ab62385d2b4dcd8274554fd0cb8b3612
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# setup-development-environment.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/setup-development-environment.md`
- Extract: `text`
- SHA256: `220f96e5438ab3313a58b023a83c6f77fd57a0ca79db4cc23e87f3fd7c5b0062`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [environment-type] | --local | --docker | --cloud | --full-stack
description: Setup comprehensive development environment with tools, configurations, and workflows
---

# Setup Development Environment

Setup comprehensive development environment with modern tooling: **$ARGUMENTS**

## Current Environment State

- Operating system: !`uname -s` and architecture detection
- Development tools: !`node --version 2>/dev/null || python --version 2>/dev/null || echo "No runtime detected"`
- Package managers: !`which npm yarn pnpm pip poetry cargo 2>/dev/null | wc -l` managers available
- IDE/Editor: Check for VS Code, IntelliJ, or other development environments

## Task

Configure complete development environment with modern tools and best practices:

**Environment Type**: Use $ARGUMENTS to specify local setup, Docker-based, cloud environment, or full-stack development

**Environment Setup**:
1. **Runtime Installation** - Programming languages, package managers, version managers (nvm, pyenv, rustup)
2. **Development Tools** - IDE configuration, extensions, debuggers, profilers, database clients
3. **Build System** - Compilers, bundlers, task runners, CI/CD tools, testing frameworks
4. **Code Quality** - Linting, formatting, pre-commit hooks, code analysis tools
5. **Environment Configuration** - Environment variables, secrets management, configuration files
6. **Team Synchronization** - Shared configurations, documentation, onboarding guides

**Advanced Features**: Hot reloading, debugging configuration, performance monitoring, container orchestration.

**Automation**: Automated setup scripts, configuration management, team environment synchronization.

**Output**: Complete development environment with documented setup process, team configurations, and troubleshooting guides.

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
