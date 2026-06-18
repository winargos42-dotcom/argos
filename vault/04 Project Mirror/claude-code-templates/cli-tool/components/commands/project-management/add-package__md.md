---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/add-package.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\add-package.md
source_ext: .md
source_sha256: 9767b3143fc5aef09441fa7b3b57b290a1835827a14b89bee13f538154fb2add
text_sha256: 69208d83bcaf13a6ba694235785837e40bbf448a7d5fe766df59122c407b84ea
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# add-package.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/add-package.md`
- Extract: `text`
- SHA256: `9767b3143fc5aef09441fa7b3b57b290a1835827a14b89bee13f538154fb2add`

## Content

---
allowed-tools: Read, Write, Edit, Bash, Glob
argument-hint: [package-name] [package-type] | --library | --application | --tool
description: Add and configure new package to workspace with proper structure and dependencies
---

# Add Package to Workspace

Add and configure new project dependencies: **$ARGUMENTS**

## Instructions

1. **Package Definition and Analysis**
   - Parse package name and type from arguments: `$ARGUMENTS` (format: name [type])
   - If no arguments provided, prompt for package name and type
   - Validate package name follows workspace naming conventions
   - Determine package type: library, application, tool, shared, service, component-library
   - Check for naming conflicts with existing packages

2. **Package Structure Creation**
   - Create package directory in appropriate workspace location (packages/, apps/, libs/)
   - Set up standard package directory structure based on type:
     - `src/` for source code
     - `tests/` or `__tests__/` for testing
     - `docs/` for package documentation
     - `examples/` for usage examples (if library)
     - `public/` for static assets (if application)
   - Create package-specific configuration files

3. **Package Configuration Setup**
   - Generate package.json with proper metadata:
     - Name following workspace conventions
     - Version aligned with workspace strategy
     - Dependencies and devDependencies
     - Scripts for build, test, lint, dev
     - Entry points and exports configuration
   - Configure TypeScript (tsconfig.json) extending workspace settings
   - Set up package-specific linting and formatting rules

4. **Package Type-Specific Setup**
   - **Library**: Configure build system, export definitions, API documentation
   - **Application**: Set up routing, environment configuration, build optimization
   - **Tool**: Configure CLI setup, binary exports, command definitions
   - **Shared**: Set up common utilities, type definitions, shared constants
   - **Service**: Configure server setup, API routes, database connections
   - **Component Library**: Set up Storybook, component exports, styling system

5. **Workspace Integration**
   - Register package in workspace configuration (nx.json, lerna.json, etc.)
   - Configure package dependencies and peer dependencies
   - Set up cross-package imports and references
   - Configure workspace-wide build order and dependencies
   - Add package to workspace scripts and task runners

6. **Development Environment**
   - Configure package-specific development server (if applicable)
   - Set up hot reloading and watch mode
   - Configure debugging and source maps
   - Set up development proxy and API mocking (if needed)
   - Configure environment variable management

7. **Testing Infrastructure**
   - Set up testing framework configuration for the package
   - Create initial test files and examples
   - Configure test coverage reporting
   - Set up package-specific test scripts
   - Configure integration testing with other workspace packages

8. **Build and Deployment**
   - Configure build system for the package type
   - Set up build artifacts and output directories
   - Configure bundling and optimization
   - Set up package publishing configuration (if library)
   - Configure deployment scripts (if application)

9. **Documentation and Examples**
   - Create package README with installation and usage instructions
   - Set up API documentation generation
   - Create usage examples and demos
   - Document package architecture and design decisions
   - Add package to workspace documentation

10. **Validation and Integration Testing**
    - Verify package builds successfully
    - Test package installation and imports
    - Validate workspace dependency resolution
    - Test development workflow and hot reloading
    - Verify CI/CD pipeline includes new package
    - Test cross-package functionality and integration

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
