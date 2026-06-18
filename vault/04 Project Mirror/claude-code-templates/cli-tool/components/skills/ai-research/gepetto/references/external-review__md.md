---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/gepetto/references/external-review.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\gepetto\references\external-review.md
source_ext: .md
source_sha256: ce156e4aa2b64adc4e7abcd7f5f86eac7a8aa6600c583b17cdd3e378293eae33
text_sha256: ec9e2f47c6cd91193403045dfbc1d2e5bf49bb0145754ab333f50ba36c46d6a8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# external-review.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/gepetto/references/external-review.md`
- Extract: `text`
- SHA256: `ce156e4aa2b64adc4e7abcd7f5f86eac7a8aa6600c583b17cdd3e378293eae33`

## Content

# External Review Protocol

This step sends `claude-plan.md` to external LLMs (Gemini and Codex) for independent review using CLI subagents.

## Overview

Launch TWO parallel Bash commands to get external reviews:
1. **Gemini CLI** - Google's Gemini 3 Pro
2. **Codex CLI** - OpenAI's GPT-5.2

Both reviewers receive the same plan and return their analysis.

## Review Prompt

Use this prompt for both reviewers:

```
You are a senior software architect reviewing an implementation plan.

The plan is self-contained - it includes all background, context, and requirements.

Identify:
- Potential footguns and edge cases
- Missing considerations
- Security vulnerabilities
- Performance issues
- Architectural problems
- Unclear or ambiguous requirements
- Anything else worth adding to the plan

Be specific and actionable. Reference specific sections. Give your honest, unconstrained assessment.

Here is the plan to review:

{PLAN_CONTENT}
```

## Execution

### Step 1: Read the Plan

```bash
plan_content=$(cat "<planning_dir>/claude-plan.md")
```

### Step 2: Launch Both Reviews in Parallel

Use TWO Bash tool calls in a single message:

**Gemini Review:**
```bash
gemini -m gemini-3-pro-preview --approval-mode yolo "You are a senior software architect reviewing an implementation plan.

The plan is self-contained - it includes all background, context, and requirements.

Identify:
- Potential footguns and edge cases
- Missing considerations
- Security vulnerabilities
- Performance issues
- Architectural problems
- Unclear or ambiguous requirements
- Anything else worth adding to the plan

Be specific and actionable. Reference specific sections. Give your honest, unconstrained assessment.

Here is the plan to review:

$(cat '<planning_dir>/claude-plan.md')"
```

**Codex Review:**
```bash
echo "You are a senior software architect reviewing an implementation plan.

The plan is self-contained - it includes all background, context, and requirements.

Identify:
- Potential footguns and edge cases
- Missing considerations
- Security vulnerabilities
- Performance issues
- Architectural problems
- Unclear or ambiguous requirements
- Anything else worth adding to the plan

Be specific and actionable. Reference specific sections. Give your honest, unconstrained assessment.

Here is the plan to review:

$(cat '<planning_dir>/claude-plan.md')" | codex exec -m gpt-5.2 --sandbox read-only --skip-git-repo-check --full-auto 2>/dev/null
```

### Step 3: Write Review Files

Create `<planning_dir>/reviews/` directory and write:
- `gemini-review.md` - Gemini's analysis
- `codex-review.md` - Codex's analysis

Format each file:
```markdown
# {Provider} Review

**Model:** {model_name}
**Generated:** {timestamp}

---

{review_content}
```

## Handling Failures

| Scenario | Action |
|----------|--------|
| Gemini fails, Codex succeeds | Write only codex-review.md, note Gemini failure |
| Codex fails, Gemini succeeds | Write only gemini-review.md, note Codex failure |
| Both fail | Ask user if they want to retry or skip external review |
| CLI not installed | Skip that reviewer, note in output |

## Notes

- **Gemini**: Uses `--approval-mode yolo` for non-interactive execution
- **Codex**: Uses `--full-auto` and `2>/dev/null` to suppress thinking tokens
- Both CLIs must be installed and configured separately by the user
- If a CLI is not available, skip that reviewer and continue with the other

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
