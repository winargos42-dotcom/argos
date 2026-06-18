---
argos_import: project_file
source_path: claude-code-config-main/claude-code-config-main/principles/13-research-pipeline.md
source_abs: F:\debug\argoss\claude-code-config-main\claude-code-config-main\principles\13-research-pipeline.md
source_ext: .md
source_sha256: 9fd484aa6f85883afe3b7f0aef9d893749da0ffbe776a754408c38e578450eb0
text_sha256: 9fd484aa6f85883afe3b7f0aef9d893749da0ffbe776a754408c38e578450eb0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:26
---

# 13-research-pipeline.md

- Source: `claude-code-config-main/claude-code-config-main/principles/13-research-pipeline.md`
- Extract: `text`
- SHA256: `9fd484aa6f85883afe3b7f0aef9d893749da0ffbe776a754408c38e578450eb0`

## Content

# Principle 13: Research Pipeline - Save What You Find

## Problem

Agents do deep research (web searches, code analysis, paper reviews) but results live only in conversation history. When a similar question comes next week - the agent researches from scratch. Knowledge is generated and immediately lost.

## Solution

After any research task, save a copy of structured results to a dedicated incoming folder. This creates a knowledge pipeline:

```
Research session -> structured results -> incoming folder -> review -> knowledge base
```

## Implementation

### Step 1: Create an incoming research folder

```
project/
  .research/
    incoming/        # Raw research drops here
    _intake.md       # Index of what's been added
```

### Step 2: Add a rule for agents

Add to your CLAUDE.md or `.claude/rules/`:

```markdown
# Research Pipeline Rule

After completing ANY research task (deep research, security analysis,
technology comparison, architecture review):

1. Save structured results to `.research/incoming/{topic}.md`
2. Add entry to `.research/incoming/_intake.md` with date and summary
3. Use descriptive filename: `{topic}--{subtopic}.md`
```

### Step 3: Process incoming research periodically

Review `.research/incoming/` and either:
- **Merge** into project docs/knowledge base
- **Archive** if already addressed
- **Defer** if not relevant yet

## Why This Matters

- **No duplicate work** - agent checks incoming folder before researching
- **Knowledge compounds** - each session builds on previous findings
- **Audit trail** - you can see what was researched and when
- **Batch processing** - accumulate findings, process them in bulk into articles/docs

## Anti-patterns

- Dumping raw conversation logs (too noisy, no structure)
- Saving only conclusions without sources (can't verify later)
- Forgetting to date entries (can't tell if research is stale)

## Connection to Other Principles

- **Codified Context** (07): research results become persistent context
- **Session Handoff**: research intake survives session boundaries
- **Autoresearch** (03): systematic improvement loop can consume research intake
- **Proof Loop** (02): research findings serve as evidence artifacts

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
