---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/subagent-driven-development/code-quality-reviewer-prompt.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\subagent-driven-development\code-quality-reviewer-prompt.md
source_ext: .md
source_sha256: a8169318eed6295f25c2e58b49468603f383c803352cbb89406cbd9e4da75f6e
text_sha256: 11de35dba7990f9def49b90039f1f2d8e7f546ae42ca8e1105d308f09456803e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:46
---

# code-quality-reviewer-prompt.md

- Source: `claude-code-templates/cli-tool/components/skills/development/subagent-driven-development/code-quality-reviewer-prompt.md`
- Extract: `text`
- SHA256: `a8169318eed6295f25c2e58b49468603f383c803352cbb89406cbd9e4da75f6e`

## Content

# Code Quality Reviewer Prompt Template

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify implementation is well-built (clean, tested, maintainable)

**Only dispatch after spec compliance review passes.**

```
Task tool (superpowers:code-reviewer):
  Use template at requesting-code-review/code-reviewer.md

  WHAT_WAS_IMPLEMENTED: [from implementer's report]
  PLAN_OR_REQUIREMENTS: Task N from [plan-file]
  BASE_SHA: [commit before task]
  HEAD_SHA: [current commit]
  DESCRIPTION: [task summary]
```

**Code reviewer returns:** Strengths, Issues (Critical/Important/Minor), Assessment

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
