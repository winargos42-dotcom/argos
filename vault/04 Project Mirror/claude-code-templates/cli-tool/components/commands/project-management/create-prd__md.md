---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/create-prd.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\create-prd.md
source_ext: .md
source_sha256: 386f0ed02bb2658295429c8dce61c09e94c8d59242437649e241f30919e5ce22
text_sha256: a9a7062792bf3661f603b7b6660d4589ca215b1505823bbf6c52d4b3ed93536b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# create-prd.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/create-prd.md`
- Extract: `text`
- SHA256: `386f0ed02bb2658295429c8dce61c09e94c8d59242437649e241f30919e5ce22`

## Content

---
allowed-tools: Read, Write, Edit, Grep, Glob
argument-hint: [feature-name] | --template | --interactive
description: Create Product Requirements Document (PRD) for new features
---

# Create Product Requirements Document

You are an experienced Product Manager. Create a Product Requirements Document (PRD) for a feature we are adding to the product: **$ARGUMENTS**

**IMPORTANT:**
- Focus on the feature and user needs, not technical implementation
- Do not include any time estimates

## Product Context

1. **Product Documentation**: @product-development/resources/product.md (to understand the product)
2. **Feature Documentation**: @product-development/current-feature/feature.md (to understand the feature idea)
3. **JTBD Documentation**: @product-development/current-feature/JTBD.md (to understand the Jobs to be Done)

## Task

Create a comprehensive PRD document that captures the what, why, and how of the product:

1. Use the PRD template from `@product-development/resources/PRD-template.md`
2. Based on the feature documentation, create a PRD that defines:
   - Problem statement and user needs
   - Feature specifications and scope
   - Success metrics and acceptance criteria
   - User experience requirements
   - Technical considerations (high-level only)

3. Output the completed PRD to `product-development/current-feature/PRD.md`

Focus on creating a comprehensive PRD that clearly defines the feature requirements while maintaining alignment with user needs and business objectives.

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
