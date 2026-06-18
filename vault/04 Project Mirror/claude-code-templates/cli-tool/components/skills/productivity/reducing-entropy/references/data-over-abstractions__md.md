---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/productivity/reducing-entropy/references/data-over-abstractions.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\productivity\reducing-entropy\references\data-over-abstractions.md
source_ext: .md
source_sha256: 49e6995173cd708c4cf35d33d9090bae0604e91d8fdf08fb267495eaf6638834
text_sha256: fdfa218c0fea9726fa6276b32c3407e1995a21d99f5f00c45f6e2200fdb6f213
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# data-over-abstractions.md

- Source: `claude-code-templates/cli-tool/components/skills/productivity/reducing-entropy/references/data-over-abstractions.md`
- Extract: `text`
- SHA256: `49e6995173cd708c4cf35d33d9090bae0604e91d8fdf08fb267495eaf6638834`

## Content

---
description: 100 functions on one data structure beats 10 functions on 10 structures. Generic data and operations enable composition.
---

# Data-Oriented Design

## The Core Principle

> "It is better to have 100 functions operate on one data structure than 10 functions on 10 data structures."

Generic operations on generic data structures beat specialized operations on specialized structures.

## Why Custom Abstractions Hurt

Every custom type, wrapper class, or specialized structure:
- Adds a concept to understand
- Requires its own operations
- Limits composition with other code
- Creates maintenance burden

A `Map<String, Value>` can be processed by hundreds of existing functions. A `SettingsManager` class can only be processed by the methods you write for it.

## Information Over Objects

Model the information domain, not the behavior.

- What data exists?
- What are the essential relationships?
- What transformations do you need?

Then use generic structures (maps, vectors, sets) to represent that information. The behavior comes from functions that operate on data - not from methods bound to custom objects.

## Practical Application

Before creating a new class/type, ask:
- Could this be a map/dict with well-known keys?
- Could this be a simple tuple/record?
- Do I need custom behavior, or just data?

If you just need data, use data structures. Save custom types for when you genuinely need custom behavior that can't be a function.

**The power is in the combinations, not the custom constructs.**

## External References

- [The Value of Values](https://www.infoq.com/presentations/Value-Values/) - Rich Hickey on data vs objects
- [Data-Oriented Design](https://www.dataorienteddesign.com/dodbook/) - Richard Fabian's book on DOD
- [CppCon 2014: Mike Acton "Data-Oriented Design"](https://www.youtube.com/watch?v=rX0ItVEVjHc) - Practical DOD in game engines

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
