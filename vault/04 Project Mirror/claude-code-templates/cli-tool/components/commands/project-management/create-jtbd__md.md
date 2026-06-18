---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/create-jtbd.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\create-jtbd.md
source_ext: .md
source_sha256: 0753732c746db8e88ed68d210dee47d2f8204777067d71dab168d14a8598261f
text_sha256: 1cf424961c1cbc4273259b0329e2aedd322abf9ee417e2005e53840ea3788663
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# create-jtbd.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/create-jtbd.md`
- Extract: `text`
- SHA256: `0753732c746db8e88ed68d210dee47d2f8204777067d71dab168d14a8598261f`

## Content

---
allowed-tools: Read, Write, Edit, Grep, Glob
argument-hint: [feature-name] | --template | --interactive
description: Create Jobs-to-be-Done (JTBD) analysis for product features
---

# Create Jobs-to-be-Done Document

You are an experienced Product Manager. Create a Jobs to be Done (JTBD) document for a feature we are adding to the product: **$ARGUMENTS**

**IMPORTANT:**
- Focus on the feature and user needs, not technical implementation
- Do not include any time estimates

## Required Documentation

1. **Product Documentation**: @product-development/resources/product.md (to understand the product)
2. **Feature Idea**: @product-development/current-feature/feature.md (to understand the feature idea)

**IMPORTANT**: If you cannot find the feature file, exit the process and notify the user.

## Task

Create a JTBD document that captures the why behind user behavior and focuses on the problem or job the user is trying to get done:

1. Use the JTBD template from `@product-development/resources/JTBD-template.md` 
2. Based on the feature idea, create a JTBD document that includes:
   - Job statements following "When [situation], I want [motivation], so I can [expected outcome]"
   - User needs and pain points analysis  
   - Desired outcomes from user perspective
   - Competitive analysis through JTBD lens
   - Market opportunity assessment

3. Output the JTBD document to `product-development/current-feature/JTBD.md`

Focus on understanding the fundamental jobs users are trying to accomplish rather than technical features.

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
