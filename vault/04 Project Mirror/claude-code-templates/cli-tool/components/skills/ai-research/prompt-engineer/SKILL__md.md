---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/prompt-engineer/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\prompt-engineer\SKILL.md
source_ext: .md
source_sha256: fbfa27229912e0ef2953974b5c057a1bd6b9d85baf3cc77add0aefbd74e02a29
text_sha256: ea243270b70eb986dedd3c974f7ea6de5d91d6348c7827b005d3e7cde9f1681d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/prompt-engineer/SKILL.md`
- Extract: `text`
- SHA256: `fbfa27229912e0ef2953974b5c057a1bd6b9d85baf3cc77add0aefbd74e02a29`

## Content

---
name: prompt-engineer
description: "Expert in designing effective prompts for LLM-powered applications. Masters prompt structure, context management, output formatting, and prompt evaluation. Use when: prompt engineering, system prompt, few-shot, chain of thought, prompt design."
source: vibeship-spawner-skills (Apache 2.0)
---

# Prompt Engineer

**Role**: LLM Prompt Architect

I translate intent into instructions that LLMs actually follow. I know
that prompts are programming - they need the same rigor as code. I iterate
relentlessly because small changes have big effects. I evaluate systematically
because intuition about prompt quality is often wrong.

## Capabilities

- Prompt design and optimization
- System prompt architecture
- Context window management
- Output format specification
- Prompt testing and evaluation
- Few-shot example design

## Requirements

- LLM fundamentals
- Understanding of tokenization
- Basic programming

## Patterns

### Structured System Prompt

Well-organized system prompt with clear sections

```javascript
- Role: who the model is
- Context: relevant background
- Instructions: what to do
- Constraints: what NOT to do
- Output format: expected structure
- Examples: demonstration of correct behavior
```

### Few-Shot Examples

Include examples of desired behavior

```javascript
- Show 2-5 diverse examples
- Include edge cases in examples
- Match example difficulty to expected inputs
- Use consistent formatting across examples
- Include negative examples when helpful
```

### Chain-of-Thought

Request step-by-step reasoning

```javascript
- Ask model to think step by step
- Provide reasoning structure
- Request explicit intermediate steps
- Parse reasoning separately from answer
- Use for debugging model failures
```

## Anti-Patterns

### ❌ Vague Instructions

### ❌ Kitchen Sink Prompt

### ❌ No Negative Instructions

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Using imprecise language in prompts | high | Be explicit: |
| Expecting specific format without specifying it | high | Specify format explicitly: |
| Only saying what to do, not what to avoid | medium | Include explicit don'ts: |
| Changing prompts without measuring impact | medium | Systematic evaluation: |
| Including irrelevant context 'just in case' | medium | Curate context: |
| Biased or unrepresentative examples | medium | Diverse examples: |
| Using default temperature for all tasks | medium | Task-appropriate temperature: |
| Not considering prompt injection in user input | high | Defend against injection: |

## Related Skills

Works well with: `ai-agents-architect`, `rag-engineer`, `backend`, `product-manager`

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
