---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/express-api/TEMPLATE.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\business-marketing\app-builder\templates\express-api\TEMPLATE.md
source_ext: .md
source_sha256: b3225717d60dd7bbe742f8a9c3a5c5d476bae4f2eb84ccacb35f859bd0f95353
text_sha256: e06f166902ccca2943775faac0198c77cc52eca50ec7dde41aa90d9e16ee0990
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# TEMPLATE.md

- Source: `claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/express-api/TEMPLATE.md`
- Extract: `text`
- SHA256: `b3225717d60dd7bbe742f8a9c3a5c5d476bae4f2eb84ccacb35f859bd0f95353`

## Content

---
name: express-api
description: Express.js REST API template principles. TypeScript, Prisma, JWT.
---

# Express.js API Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Runtime | Node.js 20+ |
| Framework | Express.js |
| Language | TypeScript |
| Database | PostgreSQL + Prisma |
| Validation | Zod |
| Auth | JWT + bcrypt |

---

## Directory Structure

```
project-name/
├── prisma/
│   └── schema.prisma
├── src/
│   ├── app.ts           # Express setup
│   ├── config/          # Environment
│   ├── routes/          # Route handlers
│   ├── controllers/     # Business logic
│   ├── services/        # Data access
│   ├── middleware/
│   │   ├── auth.ts      # JWT verify
│   │   ├── error.ts     # Error handler
│   │   └── validate.ts  # Zod validation
│   ├── schemas/         # Zod schemas
│   └── utils/
└── package.json
```

---

## Middleware Stack

| Order | Middleware |
|-------|------------|
| 1 | helmet (security) |
| 2 | cors |
| 3 | morgan (logging) |
| 4 | body parsing |
| 5 | routes |
| 6 | error handler |

---

## API Response Format

| Type | Structure |
|------|-----------|
| Success | `{ success: true, data: {...} }` |
| Error | `{ error: "message", details: [...] }` |

---

## Setup Steps

1. Create project directory
2. `npm init -y`
3. Install deps: `npm install express prisma zod bcrypt jsonwebtoken`
4. Configure Prisma
5. `npm run db:push`
6. `npm run dev`

---

## Best Practices

- Layer architecture (routes → controllers → services)
- Validate all inputs with Zod
- Centralized error handling
- Environment-based config
- Use Prisma for type-safe DB access

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
