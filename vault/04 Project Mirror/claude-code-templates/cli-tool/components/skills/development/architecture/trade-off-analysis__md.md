---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/architecture/trade-off-analysis.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\architecture\trade-off-analysis.md
source_ext: .md
source_sha256: b61528d9558583ce063ff32ee8a45fdf0b22ca1208b095e9081a075154f90dd6
text_sha256: 14a0ceb22e88af2d39b24f06a9095312aa04bc72e8980f244bf2b42f8260abaa
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# trade-off-analysis.md

- Source: `claude-code-templates/cli-tool/components/skills/development/architecture/trade-off-analysis.md`
- Extract: `text`
- SHA256: `b61528d9558583ce063ff32ee8a45fdf0b22ca1208b095e9081a075154f90dd6`

## Content

# Trade-off Analysis & ADR

> Document every architectural decision with trade-offs.

## Decision Framework

For EACH architectural component, document:

```markdown
## Architecture Decision Record

### Context
- **Problem**: [What problem are we solving?]
- **Constraints**: [Team size, scale, timeline, budget]

### Options Considered

| Option | Pros | Cons | Complexity | When Valid |
|--------|------|------|------------|-----------|
| Option A | Benefit 1 | Cost 1 | Low | [Conditions] |
| Option B | Benefit 2 | Cost 2 | High | [Conditions] |

### Decision
**Chosen**: [Option B]

### Rationale
1. [Reason 1 - tied to constraints]
2. [Reason 2 - tied to requirements]

### Trade-offs Accepted
- [What we're giving up]
- [Why this is acceptable]

### Consequences
- **Positive**: [Benefits we gain]
- **Negative**: [Costs/risks we accept]
- **Mitigation**: [How we'll address negatives]

### Revisit Trigger
- [When to reconsider this decision]
```

## ADR Template

```markdown
# ADR-[XXX]: [Decision Title]

## Status
Proposed | Accepted | Deprecated | Superseded by [ADR-YYY]

## Context
[What problem? What constraints?]

## Decision
[What we chose - be specific]

## Rationale
[Why - tie to requirements and constraints]

## Trade-offs
[What we're giving up - be honest]

## Consequences
- **Positive**: [Benefits]
- **Negative**: [Costs]
- **Mitigation**: [How to address]
```

## ADR Storage

```
docs/
└── architecture/
    ├── adr-001-use-nextjs.md
    ├── adr-002-postgresql-over-mongodb.md
    └── adr-003-adopt-repository-pattern.md
```

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
