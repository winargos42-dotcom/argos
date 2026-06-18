---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/astro-static/TEMPLATE.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\business-marketing\app-builder\templates\astro-static\TEMPLATE.md
source_ext: .md
source_sha256: 3be154d9b75e2f974d358bdbe5211f20490728f5e6b122babb0b39977ba1f2df
text_sha256: b603190c6f2d0a453d8fb9156532fd314722e0404635453858a278bc50bd6428
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# TEMPLATE.md

- Source: `claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/astro-static/TEMPLATE.md`
- Extract: `text`
- SHA256: `3be154d9b75e2f974d358bdbe5211f20490728f5e6b122babb0b39977ba1f2df`

## Content

---
name: astro-static
description: Astro static site template principles. Content-focused websites, blogs, documentation.
---

# Astro Static Site Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Astro 4.x |
| Content | MDX + Content Collections |
| Styling | Tailwind CSS |
| Integrations | Sitemap, RSS, SEO |
| Output | Static/SSG |

---

## Directory Structure

```
project-name/
├── src/
│   ├── components/      # .astro components
│   ├── content/         # MDX content
│   │   ├── blog/
│   │   └── config.ts    # Collection schemas
│   ├── layouts/         # Page layouts
│   ├── pages/           # File-based routing
│   └── styles/
├── public/              # Static assets
├── astro.config.mjs
└── package.json
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| Content Collections | Type-safe content with Zod schemas |
| Islands Architecture | Partial hydration for interactivity |
| Zero JS by default | Static HTML unless needed |
| MDX Support | Markdown with components |

---

## Setup Steps

1. `npm create astro@latest {{name}}`
2. Add integrations: `npx astro add mdx tailwind sitemap`
3. Configure `astro.config.mjs`
4. Create content collections
5. `npm run dev`

---

## Deployment

| Platform | Method |
|----------|--------|
| Vercel | Auto-detected |
| Netlify | Auto-detected |
| Cloudflare Pages | Auto-detected |
| GitHub Pages | Build + deploy action |

---

## Best Practices

- Use Content Collections for type safety
- Leverage static generation
- Add islands only where needed
- Optimize images with Astro Image

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
