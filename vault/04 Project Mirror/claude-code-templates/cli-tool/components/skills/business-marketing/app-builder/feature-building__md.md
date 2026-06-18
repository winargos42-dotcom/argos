---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/feature-building.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\business-marketing\app-builder\feature-building.md
source_ext: .md
source_sha256: 9cb5dcdd3cf519759ddf8269c1418fd99f70e6920af4936cc1f02ff9e911ed40
text_sha256: e717306dfca771266b42b582a69ed67b02883d3a3604b6d6118841ae1369207c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# feature-building.md

- Source: `claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/feature-building.md`
- Extract: `text`
- SHA256: `9cb5dcdd3cf519759ddf8269c1418fd99f70e6920af4936cc1f02ff9e911ed40`

## Content

# Feature Building

> How to analyze and implement new features.

## Feature Analysis

```
Request: "add payment system"

Analysis:
├── Required Changes:
│   ├── Database: orders, payments tables
│   ├── Backend: /api/checkout, /api/webhooks/stripe
│   ├── Frontend: CheckoutForm, PaymentSuccess
│   └── Config: Stripe API keys
│
├── Dependencies:
│   ├── stripe package
│   └── Existing user authentication
│
└── Estimated Time: 15-20 minutes
```

## Iterative Enhancement Process

```
1. Analyze existing project
2. Create change plan
3. Present plan to user
4. Get approval
5. Apply changes
6. Test
7. Show preview
```

## Error Handling

| Error Type | Solution Strategy |
|------------|-------------------|
| TypeScript Error | Fix type, add missing import |
| Missing Dependency | Run npm install |
| Port Conflict | Suggest alternative port |
| Database Error | Check migration, validate connection |

## Recovery Strategy

```
1. Detect error
2. Try automatic fix
3. If failed, report to user
4. Suggest alternative
5. Rollback if necessary
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
