---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/enterprise-communication/session-handoff/references/resume-checklist.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\enterprise-communication\session-handoff\references\resume-checklist.md
source_ext: .md
source_sha256: d195c3d9ff04a1161decb9805fa60a3d4a901d8767b8420476dd96361b412b68
text_sha256: bd64d36be5e68f361038ab7465b7f0c6bd47f4d3e43c925cc38a3868356f19e4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:47
---

# resume-checklist.md

- Source: `claude-code-templates/cli-tool/components/skills/enterprise-communication/session-handoff/references/resume-checklist.md`
- Extract: `text`
- SHA256: `d195c3d9ff04a1161decb9805fa60a3d4a901d8767b8420476dd96361b412b68`

## Content

# Resume Checklist

Follow this checklist when resuming work from a handoff document to ensure zero-ambiguity continuation.

## Pre-Resume Verification

- [ ] Read the entire handoff document before taking any action
- [ ] Verify you are in the correct project directory
- [ ] Confirm the git branch matches (or understand why it might differ)
- [ ] Check the handoff timestamp - how stale is this context?

## Context Validation

- [ ] Review "Important Context" section thoroughly
- [ ] Understand all assumptions listed - are they still valid?
- [ ] Check if any blockers have been resolved since handoff
- [ ] Review "Potential Gotchas" to avoid known pitfalls

## State Verification

- [ ] Run `git status` to see current file state
- [ ] Compare modified files list in handoff vs current state
- [ ] Check if any environment variables need to be set
- [ ] Verify any required services/processes are running

## Resume Execution

- [ ] Start with "Immediate Next Steps" item #1
- [ ] Reference "Files Modified" table for context on recent changes
- [ ] Apply patterns documented in "Key Patterns Discovered"
- [ ] Follow architectural insights from "Architecture Overview"

## During Work

- [ ] Update handoff document if major new context is discovered
- [ ] Mark completed items in "Pending Work" as you finish them
- [ ] Add new blockers/questions as they arise
- [ ] Consider creating a new handoff if session becomes long

## Red Flags - Stop and Verify

If you encounter any of these, pause and verify context before proceeding:

1. **Files mentioned in handoff don't exist** - codebase may have changed significantly
2. **Branch has diverged substantially** - check git log for recent commits
3. **Assumptions are clearly invalid** - reassess the approach
4. **Blockers marked as unresolved are now blocking you** - escalate to user
5. **Architecture has changed** - re-explore before continuing

## Quick Start Commands

After reading the handoff, these commands help verify state:

```bash
# Check current branch and status
git branch --show-current
git status

# See recent commits (compare with handoff)
git log --oneline -10

# Check for any running processes mentioned
ps aux | grep [process-name]

# Verify environment
env | grep [relevant-var]
```

## Handoff Quality Assessment

Rate the handoff quality to identify if more exploration is needed:

| Aspect | Good | Needs Exploration |
|--------|------|-------------------|
| Next steps | Clear, actionable | Vague or missing |
| File references | Specific paths/lines | General descriptions |
| Decisions | Rationale included | Just outcomes |
| Context | Complete picture | Gaps or assumptions |

If multiple aspects "Need Exploration", spend time re-exploring the codebase before continuing implementation.

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
