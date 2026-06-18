---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/productivity/reducing-entropy/references/design-is-taking-apart.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\productivity\reducing-entropy\references\design-is-taking-apart.md
source_ext: .md
source_sha256: c27ac808e8858b4f0213f41e4f64c778a107d8d43ca9d78bb943a91cc7d9ed2b
text_sha256: 62694edb44965c50b7a88fc1f891ae38948b2acd1b872d25c2adc988f352ebe0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# design-is-taking-apart.md

- Source: `claude-code-templates/cli-tool/components/skills/productivity/reducing-entropy/references/design-is-taking-apart.md`
- Extract: `text`
- SHA256: `c27ac808e8858b4f0213f41e4f64c778a107d8d43ca9d78bb943a91cc7d9ed2b`

## Content

---
description: Design is taking things apart, not adding features. Separate concerns, remove dependencies, compose simple pieces.
---

# Composition Over Construction

## The Core Insight

> "Design is about taking things apart."

Good design is not about adding features. It's about removing dependencies. It's about separating concerns so cleanly that each piece can be understood, tested, and changed independently.

## Taking Things Apart

When you see a complex system, the instinct is to understand how the pieces fit together. But the real skill is seeing how to *pull them apart*.

- What different concerns are mixed here?
- Which responsibilities could be separate?
- Where are we conflating different concepts?

Each separation reduces complexity. Each coupling increases it.

## Building from Simple Parts

Once you have simple, independent pieces:
- They compose freely
- They test trivially
- They change safely

Inheritance complects. Composition liberates.

A system built from small, focused functions that transform data is:
- Easier to understand (each piece does one thing)
- Easier to test (pure functions, clear inputs/outputs)
- Easier to change (modify one piece without touching others)

## The Anti-Pattern

The opposite of composition is the "god object" or "kitchen sink" - one thing that knows about everything, does everything, and can't be changed without breaking everything else.

Every helper method you add to a class is a small step toward the kitchen sink. Every layer of abstraction is a coupling waiting to cause pain.

## Practical Application

Before adding a method, wrapper, or abstraction:
- Does this *separate* concerns, or *combine* them?
- Am I making pieces more independent, or more coupled?
- Could I solve this with a function that takes data and returns data?

**Separate, don't combine. Compose, don't construct.**

## External References

- [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/) - Rich Hickey on complecting vs composing
- [Out of the Tar Pit](https://curtclifton.net/papers/MosesleyMarks06a.pdf) - Moseley & Marks on essential vs accidental complexity
- [A Philosophy of Software Design](https://www.amazon.com/dp/173210221X) - John Ousterhout on deep vs shallow modules

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
