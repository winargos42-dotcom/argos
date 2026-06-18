---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/screenshot-feature-extractor/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\screenshot-feature-extractor\SKILL.md
source_ext: .md
source_sha256: 744c9a25b94de75dac8d811026a7a2dd6e9c2e2fbce581eab8917d959566f1e4
text_sha256: ffd5144d4b4230b216db2fc581d69f8b14eb6c0a0f18c3bcbc7649e6e62e1a7c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:46
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/development/screenshot-feature-extractor/SKILL.md`
- Extract: `text`
- SHA256: `744c9a25b94de75dac8d811026a7a2dd6e9c2e2fbce581eab8917d959566f1e4`

## Content

---
name: screenshot-feature-extractor
description: "Analyze product screenshots to extract feature lists and generate development task checklists. Use when: (1) Analyzing competitor product screenshots for feature extraction, (2) Generating PRD/task lists from UI designs, (3) Batch analyzing multiple app screens, (4) Conducting competitive analysis from visual references."
---

# Screenshot Analyzer (Multi-Agent)

Extract product features from UI screenshots using a coordinated multi-agent analysis pipeline.

**Core principle**: Describe WHAT to build (features/interactions), NOT HOW (no tech stack).

## Multi-Agent Architecture

This skill orchestrates 5 specialized agents for comprehensive analysis:

```
                    ┌─────────────────┐
                    │   Coordinator   │
                    │   (this skill)  │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  UI Analyzer    │ │  Interaction    │ │   Business      │
│  (parallel)     │ │   Analyzer      │ │    Analyzer     │
│                 │ │  (parallel)     │ │   (parallel)    │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
                    ┌─────────────────┐
                    │   Synthesizer   │
                    │   (sequential)  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Reviewer     │
                    │   (sequential)  │
                    └─────────────────┘
```

## Process

### Phase 1: Screenshot Collection

Gather all screenshots to analyze:
1. Read the screenshot file(s) provided by the user
2. For each screenshot, note the file path and any context provided
3. If multiple screenshots, determine if they are from the same product

### Phase 2: Parallel Analysis

Launch THREE Task agents IN PARALLEL for each screenshot:

**Agent 1: screenshot-ui-analyzer**
```
Analyze this screenshot for UI components, layout structure, and design patterns.
Screenshot: [file path]
Return your analysis as JSON.
```

**Agent 2: screenshot-interaction-analyzer**
```
Analyze this screenshot for user interactions, navigation flows, and state transitions.
Screenshot: [file path]
Return your analysis as JSON.
```

**Agent 3: screenshot-business-analyzer**
```
Analyze this screenshot for business functions, data entities, and domain logic.
Screenshot: [file path]
Return your analysis as JSON.
```

**IMPORTANT**: Use the Task tool with THREE parallel calls in a single message to maximize efficiency.

### Phase 3: Synthesis

After all parallel analyses complete, launch the synthesizer agent:

**Agent 4: screenshot-synthesizer**
```
Synthesize these analysis results into a unified development task list.

UI Analysis:
[paste UI analyzer result]

Interaction Analysis:
[paste Interaction analyzer result]

Business Analysis:
[paste Business analyzer result]

Product Name: [product name]
Output file: docs/plans/YYYY-MM-DD-<product>-features.md
```

### Phase 4: Review

Launch the reviewer agent to validate the output:

**Agent 5: screenshot-reviewer**
```
Review this task list for completeness and quality.

Original screenshot(s): [file paths]
Task list: [synthesized output]

If issues found, provide corrections.
```

### Phase 5: Output

1. Write final task list to `docs/plans/YYYY-MM-DD-<product>-features.md`
2. Use format from [references/output-format.md](references/output-format.md)
3. Present summary to user

## Key Guidelines

- Use `- [ ]` checkbox format for all tasks
- Break features into small, executable subtasks
- Focus on user interactions, not implementation details
- For multiple screenshots: deduplicate features across all screens
- For competitive analysis: highlight unique features and gaps

## Benefits of Multi-Agent Approach

1. **Thoroughness** - Three specialized perspectives catch more details
2. **Speed** - Parallel analysis reduces total time
3. **Quality** - Synthesis + Review ensures coherent, complete output
4. **Specialization** - Each agent focuses on its domain expertise

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
