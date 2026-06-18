---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/productivity/deadline-prep/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\productivity\deadline-prep\SKILL.md
source_ext: .md
source_sha256: 38358a28068ff9636731cf4bef989d9d785c4fd054cfd0a4c618dd894e9c127f
text_sha256: a5a2fe0b2aadcfeb9d792a723b5617719ed428299ea9a7a301ca05b89ec168f2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/productivity/deadline-prep/SKILL.md`
- Extract: `text`
- SHA256: `38358a28068ff9636731cf4bef989d9d785c4fd054cfd0a4c618dd894e9c127f`

## Content

---
name: deadline-prep
description: Generate a structured demo outline from your session's change log and git history. Reads .claude/critical_log_changes.csv and git log to produce presentation-ready talking points for end-of-day demos, standups, or delivery deadlines.
---

# Deadline Prep

Generate a structured demo outline from your work session. Combines the change log CSV (from the change-logger hook) with git history to create presentation-ready talking points.

## Workflow

### Step 1: Gather data sources

**Change log** (primary source if available):
- Read `.claude/critical_log_changes.csv` if it exists
- Parse columns: timestamp, tool, file_path, action, details
- Group by: files created, files modified, commands executed

**Git history** (always available):
```bash
git log --oneline --since="today 00:00"
git diff --stat HEAD~10 2>/dev/null || git diff --stat
```

If the CSV doesn't exist, fall back to git-only mode and note this in the output.

### Step 2: Analyze and categorize changes

Group all changes into categories:

| Category | Signals |
|----------|---------|
| **Features shipped** | New files, new routes, new components, `feat` commits |
| **Bug fixes** | Modified files with `fix` commits, error handling changes |
| **Refactors** | Renamed files, structural changes, `refactor` commits |
| **Config/Setup** | package.json, tsconfig, CI/CD, Docker changes |
| **Tests** | Test files created or modified |
| **Documentation** | README, docs, comments |

### Step 3: Generate the demo outline

Create a structured markdown document:

```markdown
# Demo Outline — [Date]

## What I Shipped
- **[Feature/Fix name]**: One sentence explaining what it does and why it matters
- **[Feature/Fix name]**: One sentence explaining what it does and why it matters
- **[Feature/Fix name]**: One sentence explaining what it does and why it matters

## Architecture Decisions
- **[Decision]**: Why I chose this approach over alternatives
- **[Decision]**: Tradeoff I made and the reasoning

## What I Would Do Next
1. **[Priority 1]**: Why this is the most important next step
2. **[Priority 2]**: What this would unlock
3. **[Priority 3]**: Nice-to-have improvement

## Session Metrics
- Files changed: X
- Lines: +Y / -Z
- Commits: N
- Key files: `path/to/important/file.ts`, `path/to/other.ts`
- Time window: HH:MM - HH:MM
```

### Step 4: Save and present

Save the outline to `.claude/demo-outline.md`.

Print the full outline to the terminal so the user can review it immediately.

## Tips

- Run this 30 minutes before your deadline to have time to review and add personal context
- The "Architecture Decisions" section is what reviewers care about most — add context about tradeoffs
- "What I Would Do Next" shows you think beyond the immediate task
- Edit the generated outline to add your own voice and any context the log missed
- Works best with the `change-logger` hook installed, but functions with git history alone

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
