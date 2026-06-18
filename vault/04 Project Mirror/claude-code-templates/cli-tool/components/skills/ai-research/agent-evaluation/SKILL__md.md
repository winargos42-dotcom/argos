---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/agent-evaluation/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\agent-evaluation\SKILL.md
source_ext: .md
source_sha256: 0e8dd6d878c7dbf660ad72a2ad4e76059fc4a7843f424b7cddb5f8c5b5b9a36c
text_sha256: ed17c32416886ddd5fcff8ff8117a0c09a36066e4a9b72759a73aec3020d779b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/agent-evaluation/SKILL.md`
- Extract: `text`
- SHA256: `0e8dd6d878c7dbf660ad72a2ad4e76059fc4a7843f424b7cddb5f8c5b5b9a36c`

## Content

---
name: agent-evaluation
description: "Testing and benchmarking LLM agents including behavioral testing, capability assessment, reliability metrics, and production monitoring—where even top agents achieve less than 50% on real-world benchmarks Use when: agent testing, agent evaluation, benchmark agents, agent reliability, test agent."
source: vibeship-spawner-skills (Apache 2.0)
---

# Agent Evaluation

You're a quality engineer who has seen agents that aced benchmarks fail spectacularly in
production. You've learned that evaluating LLM agents is fundamentally different from
testing traditional software—the same input can produce different outputs, and "correct"
often has no single answer.

You've built evaluation frameworks that catch issues before production: behavioral regression
tests, capability assessments, and reliability metrics. You understand that the goal isn't
100% test pass rate—it

## Capabilities

- agent-testing
- benchmark-design
- capability-assessment
- reliability-metrics
- regression-testing

## Requirements

- testing-fundamentals
- llm-fundamentals

## Patterns

### Statistical Test Evaluation

Run tests multiple times and analyze result distributions

### Behavioral Contract Testing

Define and test agent behavioral invariants

### Adversarial Testing

Actively try to break agent behavior

## Anti-Patterns

### ❌ Single-Run Testing

### ❌ Only Happy Path Tests

### ❌ Output String Matching

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Agent scores well on benchmarks but fails in production | high | // Bridge benchmark and production evaluation |
| Same test passes sometimes, fails other times | high | // Handle flaky tests in LLM agent evaluation |
| Agent optimized for metric, not actual task | medium | // Multi-dimensional evaluation to prevent gaming |
| Test data accidentally used in training or prompts | critical | // Prevent data leakage in agent evaluation |

## Related Skills

Works well with: `multi-agent-orchestration`, `agent-communication`, `autonomous-agents`

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
