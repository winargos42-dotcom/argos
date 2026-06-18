---
argos_import: project_file
source_path: claude-code-config-main/claude-code-config-main/alternatives/README.md
source_abs: F:\debug\argoss\claude-code-config-main\claude-code-config-main\alternatives\README.md
source_ext: .md
source_sha256: 559b0ded090a17e18f87b876f277e8abb163b10914fdb04eb8f2b94ae33f5f73
text_sha256: 559b0ded090a17e18f87b876f277e8abb163b10914fdb04eb8f2b94ae33f5f73
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:26
---

# README.md

- Source: `claude-code-config-main/claude-code-config-main/alternatives/README.md`
- Extract: `text`
- SHA256: `559b0ded090a17e18f87b876f277e8abb163b10914fdb04eb8f2b94ae33f5f73`

## Content

# Alternatives: Choosing the Right Approach

Not every approach fits every pipeline. These comparisons help you choose.

The skills and patterns in this repository draw from multiple sources -- Anthropic's harness design research, the Proof Loop protocol, Memento's deterministic orchestration, Karpathy's autoresearch, and more. Each solves real problems, but none is universally best. Context matters: team size, task complexity, cost tolerance, and infrastructure all affect which approach wins.

Each document below compares 2-4 approaches to the same problem, with pros, cons, and concrete "when to choose" guidance.

## Comparison Documents

| File | Problem | Approaches Compared |
|------|---------|-------------------|
| [orchestration.md](orchestration.md) | Orchestrating multi-step processes | Harness Design, Proof Loop, Memento, Prompt-only |
| [code-review.md](code-review.md) | Code review strategies | Sequential checklist, Parallel competency, Cross-model adversarial, LLM + static analysis |
| [optimization.md](optimization.md) | Iterative code/prompt optimization | Autoresearch, HyperAgent, Manual iteration, Eval-driven development |
| [context-management.md](context-management.md) | Managing context in long sessions | JIT Loading, Full Context Upfront, Compaction + Re-injection, Fresh Sessions |
| [session-handoff.md](session-handoff.md) | Seamless transitions between sessions | Manual HANDOFF.md, Stop Hook, Session Journal, ContextHarness, Memory Only |

## How to Use These

1. **Identify your problem category** from the table above.
2. **Read the comparison table** at the top of each document for a quick overview.
3. **Check the "When to Choose" section** for each approach to find your match.
4. **Read the Recommendation** at the bottom for the default progression path.

## Contributing

If you discover a new approach or find that one of these comparisons is missing an important trade-off, update the relevant file. Keep the structure consistent: Source, Core Idea, Pros, Cons, When to Choose.

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
