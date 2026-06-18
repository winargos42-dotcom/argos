---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/productivity/skill-creator/references/workflows.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\productivity\skill-creator\references\workflows.md
source_ext: .md
source_sha256: 82c591fb4d7fe184954c52db7697719c044755cd704fe49904a0350cfa748d09
text_sha256: ef4846877d5dab47511a01a6cf31476ad64f5bc5945635459295794575338980
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# workflows.md

- Source: `claude-code-templates/cli-tool/components/skills/productivity/skill-creator/references/workflows.md`
- Extract: `text`
- SHA256: `82c591fb4d7fe184954c52db7697719c044755cd704fe49904a0350cfa748d09`

## Content

# Workflow Patterns

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
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
