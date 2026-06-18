---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/gepetto/references/section-splitting.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\gepetto\references\section-splitting.md
source_ext: .md
source_sha256: 02242cd47fb1157664f4be32a20e2206c1f87408c9df90f11ed6eaffaaa67a2d
text_sha256: 088267309761afe84401e16cd168485c3aa4633374c45b8e9a58ea2678f51aaf
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# section-splitting.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/gepetto/references/section-splitting.md`
- Extract: `text`
- SHA256: `02242cd47fb1157664f4be32a20e2206c1f87408c9df90f11ed6eaffaaa67a2d`

## Content

# Section File Writing

Write individual section files from the plan using **parallel subagents** for efficiency.

This step assumes `sections/index.md` already exists.

## Input Files

- `<planning_dir>/claude-plan.md` - implementation details
- `<planning_dir>/sections/index.md` - section definitions and dependencies

## Output

```
<planning_dir>/sections/
├── index.md (already exists)
├── section-01-<name>.md
├── section-02-<name>.md
└── ...
```

## Parallel Execution Strategy

**Launch one subagent per section in a single message** for maximum parallelization:

```
┌─────────────────────────────────────────────────────┐
│  PARALLEL SUBAGENT APPROACH                         │
│                                                     │
│  1. Parse index.md to get SECTION_MANIFEST list     │
│  2. Check which sections already exist              │
│  3. Launch ALL missing sections as parallel Tasks:  │
│                                                     │
│     Task(prompt="Write section-01-...")             │
│     Task(prompt="Write section-02-...")             │
│     Task(prompt="Write section-03-...")             │
│     ... (all in ONE message)                        │
│                                                     │
│  4. Wait for all subagents to complete              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Parse SECTION_MANIFEST

Extract section list from index.md:

```markdown
<!-- SECTION_MANIFEST
section-01-foundation
section-02-config
section-03-api
END_MANIFEST -->
```

### Launch Parallel Tasks

For each section in the manifest, include a Task in a single message:

```python
Task(
  subagent_type="general-purpose",
  prompt="""
  Write section file: section-01-foundation

  Inputs:
  - <planning_dir>/claude-plan.md
  - <planning_dir>/sections/index.md

  Output: <planning_dir>/sections/section-01-foundation.md

  Requirements: [see Section File Template below]
  """
)

Task(
  subagent_type="general-purpose",
  prompt="Write section file: section-02-config ..."
)

# ... one Task per section
```

**Why parallel?** Each section is independent - they all read from the same source files (`claude-plan.md`, `index.md`) but write to different output files.

### Resume Handling

If some sections already exist:
1. Only launch Tasks for MISSING sections
2. Skip sections that have corresponding `section-*.md` files

## Section File Requirements

**CRITICAL: Each section file must be completely self-contained.**

The implementer reading a section file should NOT need to reference `claude-plan.md` or any other document. They should be able to:
1. Read the single section file
2. Create a TODO list
3. Start implementing immediately

Include all necessary background, requirements, and implementation details within each section.

### Section File Template

```markdown
# Section NN: {Section Name}

## Background

{Why this section exists, what problem it solves}

## Requirements

{What must be true when this section is complete}

## Dependencies

- Requires: {list of prior sections that must be complete}
- Blocks: {list of sections that depend on this one}

## Implementation Details

{Detailed implementation guidance}

### {Subsection 1}

{Details}

### {Subsection 2}

{Details}

## Acceptance Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Files to Create/Modify

- `path/to/file1.ts` - {description}
- `path/to/file2.ts` - {description}
```

## Completion

All sections are complete when every section in the SECTION_MANIFEST has a corresponding `section-NN-name.md` file.

After all parallel Tasks complete, update the main TODO list to mark section writing as done.

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
