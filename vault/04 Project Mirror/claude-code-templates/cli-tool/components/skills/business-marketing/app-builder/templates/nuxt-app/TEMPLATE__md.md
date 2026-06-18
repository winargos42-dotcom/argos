---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/nuxt-app/TEMPLATE.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\business-marketing\app-builder\templates\nuxt-app\TEMPLATE.md
source_ext: .md
source_sha256: bb2ba04d96edc71bdef8b7d3fea83869f1a84e9d493bfd0004ea642a1354682e
text_sha256: 5b265e4c64d31429e3e64e436fd4eb5a140e6a8918f67926dd3169a7ca197c46
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:34
---

# TEMPLATE.md

- Source: `claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/nuxt-app/TEMPLATE.md`
- Extract: `text`
- SHA256: `bb2ba04d96edc71bdef8b7d3fea83869f1a84e9d493bfd0004ea642a1354682e`

## Content

---
name: nuxt-app
description: Nuxt 3 full-stack template. Vue 3, Pinia, Tailwind, Prisma.
---

# Nuxt 3 Full-Stack Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Nuxt 3 |
| Language | TypeScript |
| UI | Vue 3 (Composition API) |
| State | Pinia |
| Database | PostgreSQL + Prisma |
| Styling | Tailwind CSS |
| Validation | Zod |

---

## Directory Structure

```
project-name/
├── prisma/
│   └── schema.prisma
├── server/
│   ├── api/
│   │   └── [resource]/
│   │       └── index.ts
│   └── utils/
│       └── db.ts         # Prisma client
├── composables/
│   └── useAuth.ts
├── stores/
│   └── user.ts           # Pinia store
├── components/
│   └── ui/
├── pages/
│   ├── index.vue
│   └── [...slug].vue
├── layouts/
│   └── default.vue
├── assets/
│   └── css/
│       └── main.css
├── .env.example
├── nuxt.config.ts
└── package.json
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| Auto-imports | Components, composables, utils |
| File-based routing | pages/ → routes |
| Server Routes | server/api/ → API endpoints |
| Composables | Reusable reactive logic |
| Pinia | State management |

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| DATABASE_URL | Prisma connection |
| NUXT_PUBLIC_APP_URL | Public URL |

---

## Setup Steps

1. `npx nuxi@latest init {{name}}`
2. `cd {{name}}`
3. `npm install @pinia/nuxt @prisma/client prisma zod`
4. `npm install -D @nuxtjs/tailwindcss`
5. Add modules to `nuxt.config.ts`:
   ```ts
   modules: ['@pinia/nuxt', '@nuxtjs/tailwindcss']
   ```
6. `npx prisma init`
7. Configure schema
8. `npx prisma db push`
9. `npm run dev`

---

## Best Practices

- Use `<script setup>` for components
- Composables for reusable logic
- Pinia stores in `stores/` folder
- Server routes for API logic
- Auto-import for clean code
- TypeScript for type safety
- See `@[skills/vue-expert]` for Vue patterns

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
