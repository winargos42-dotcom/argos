---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-maestro/planning/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-maestro\planning\SKILL.md
source_ext: .md
source_sha256: 30524df29bf33df32b8eee89b3b674364c82c07c5f726e7183caef6b80d957b0
text_sha256: 34a4a12808a054be8ee8fea1d1b252e73a1b11959b884a33f041439529020de3
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-maestro/planning/SKILL.md`
- Extract: `text`
- SHA256: `30524df29bf33df32b8eee89b3b674364c82c07c5f726e7183caef6b80d957b0`

## Content

---
name: planning
description: Create and manage persistent markdown planning files for structured task execution. Use when the user asks to "create a plan", "track progress", "start a research project", or when a task requires more than 5 tool calls and needs structured phase tracking to stay focused and avoid goal drift.
---

# AI Maestro Planning

Solve the execution problem -- staying focused during complex, multi-step tasks. Uses persistent markdown files to track goals, findings, and progress so you never lose context. Part of the [AI Maestro](https://github.com/23blocks-OS/ai-maestro) suite.

## When to Use

- Multi-step tasks (3+ steps)
- Research projects
- Building features requiring >5 tool calls
- Any task where you might lose track of the goal

## The 3-File Pattern

Create in `docs_dev/` (or `$AIMAESTRO_PLANNING_DIR`):

| File | Purpose | Update When |
|------|---------|-------------|
| `task_plan.md` | Goals, phases, decisions, errors | After each phase |
| `findings.md` | Research, discoveries, resources | During research |
| `progress.md` | Session log, test results | Throughout session |

## Quick Start

```bash
PLAN_DIR="${AIMAESTRO_PLANNING_DIR:-docs_dev}"
mkdir -p "$PLAN_DIR"
```

Then create `task_plan.md` with:
```markdown
# Task: [Goal]

## Phases
- [ ] Phase 1: Research
- [ ] Phase 2: Design
- [ ] Phase 3: Implement
- [ ] Phase 4: Test

## Decisions
| Decision | Rationale | Date |
|----------|-----------|------|

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
```

## The 6 Rules

1. **Create plan first** -- Never start complex work without `task_plan.md`
2. **Read before decide** -- Re-read the plan before any major decision
3. **Update after act** -- Mark phases complete, log what changed
4. **2-action rule** -- After every 2 search/browse operations, save findings to `findings.md`
5. **Log all errors** -- Every error goes in the plan with attempt number and resolution
6. **Never repeat failures** -- If an action failed, change your approach

## The 3-Strike Protocol

| Strike | Action |
|--------|--------|
| 1 | Diagnose root cause, apply targeted fix |
| 2 | Try a different approach entirely |
| 3 | Question assumptions, search for similar issues |
| After 3 | Escalate to user with all attempts documented |

## The 5-Question Reboot

Lost? Answer these from your planning files:

1. Where am I? (current phase in `task_plan.md`)
2. Where am I going? (remaining phases)
3. What's the goal? (goal section)
4. What have I learned? (`findings.md`)
5. What have I done? (`progress.md`)

## Full AI Maestro Experience

This skill works standalone with no dependencies. For the complete experience including **memory search**, **docs search**, **graph query**, **agent messaging**, and **agent management**, install the full [AI Maestro](https://github.com/23blocks-OS/ai-maestro) platform.

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
