---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/gepetto/references/interview-protocol.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\gepetto\references\interview-protocol.md
source_ext: .md
source_sha256: c890c49ff05fd85eb01fc6be84c3efc2ed859c122f8322498e24b8845d586985
text_sha256: 6c906a7d093b251c9862157bbcd9618667213fb5fc864e43ebe514f4b1218912
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# interview-protocol.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/gepetto/references/interview-protocol.md`
- Extract: `text`
- SHA256: `c890c49ff05fd85eb01fc6be84c3efc2ed859c122f8322498e24b8845d586985`

## Content

# Interview Protocol

The interview runs directly in this skill (not subagent) because `AskUserQuestion` only works in main conversation context.

## Context

The interview should be informed by:
- **Initial spec** (always available)
- **Research findings** (if step 5 produced `claude-research.md`)

If research was done, use it to:
- Skip questions already answered by research
- Ask clarifying questions about trade-offs or patterns discovered
- Dig deeper into areas where research revealed complexity

## Philosophy

- You are a senior architect accountable for this implementation
- Surface everything the user knows but hasn't mentioned
- Assume the initial spec is incomplete
- Extract context from user's head

## Technique

- Use AskUserQuestion with focused questions (2-4 per round)
- Ask open-ended questions, not yes/no
- Don't ask obvious questions already in spec
- Dig deeper when answers reveal complexity
- Summarize periodically to confirm understanding

## Example Questions

**Good questions:**
- "What happens when X fails? Should we retry, log, or surface to user?"
- "Are there existing patterns in the codebase for Y that we should follow?"
- "What's the expected scale - dozens, thousands, or millions of Z?"

**Bad questions (too vague):**
- "Anything else?"
- "Is that all?"
- "Do you have any other requirements?"

## When to Stop

Stop interviewing when you are confident you can:
1. Write a detailed implementation plan
2. Make no assumptions about requirements
3. Handle all edge cases the user cares about

If uncertain, ask one more round. Better to over-clarify than make wrong assumptions.

If the user predominantly answers with "I don't know" or "Up to you" to most questions, stop and move on.

## Saving the Transcript

After the interview, save the full Q&A to `<planning_dir>/claude-interview.md`:
- Format each question as a markdown heading
- Include the user's full answer below
- Number questions for reference (Q1, Q2, etc.)

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
