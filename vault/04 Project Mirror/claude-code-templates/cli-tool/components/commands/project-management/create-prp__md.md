---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/create-prp.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\create-prp.md
source_ext: .md
source_sha256: 6131acd69ba2fb358d5d2a9fe5195f25f8b0ca7bcfa11703b1dbf045fc8cb4a3
text_sha256: f3a4ed4210d5e7c0282c7088de2a8fa89e097fb1956f0c5c75508939b3747557
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# create-prp.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/create-prp.md`
- Extract: `text`
- SHA256: `6131acd69ba2fb358d5d2a9fe5195f25f8b0ca7bcfa11703b1dbf045fc8cb4a3`

## Content

---
allowed-tools: Read, Write, Edit, WebSearch, Grep, Glob
argument-hint: [feature-description] | --research | --template | --validate
description: Create comprehensive Product Requirement Prompt (PRP) with research and validation
---

# Create Product Requirement Prompt

Create comprehensive Product Requirement Prompt (PRP) following structured research process: **$ARGUMENTS**

## PRP Foundation

- Base template: @concept_library/cc_PRP_flow/PRPs/base_template_v1
- PRP concept: @concept_library/cc_PRP_flow/README.md
- Existing PRPs: !`find concept_library/cc_PRP_flow/PRPs/ -name "*.md" | head -5`
- Documentation: @ai_docs/ directory analysis

## Task

Develop comprehensive PRP through systematic research and structured documentation:

**Research Process**:
1. **Documentation Review** - Analyze existing ai_docs/ and project documentation
2. **Web Research** - Gather implementation examples, library docs, and best practices
3. **Template Analysis** - Study base_template_v1 structure and existing PRPs
4. **Codebase Exploration** - Identify patterns, dependencies, and integration points
5. **Context Synthesis** - Compile comprehensive implementation context

**PRP Development**:
- Follow base_template_v1 structure exactly
- Include specific file references and web resources
- Provide curated codebase intelligence
- Define clear validation criteria and success metrics
- Create production-ready implementation guide

**Remember**: PRP = PRD + curated codebase intelligence + agent/runbook—the minimum viable packet an AI needs to ship production-ready code on the first pass.

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
