---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/nextjs-static/TEMPLATE.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\business-marketing\app-builder\templates\nextjs-static\TEMPLATE.md
source_ext: .md
source_sha256: 6b69ad61c84b9cc18d3c444e09caeaa297e22e64cbbafcafaa855ac677d687bd
text_sha256: 8e9e9437629d9cbc1cfcdf9a64825e4cda782939e75e55bbbe42dc7f0968fa6d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:34
---

# TEMPLATE.md

- Source: `claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/nextjs-static/TEMPLATE.md`
- Extract: `text`
- SHA256: `6b69ad61c84b9cc18d3c444e09caeaa297e22e64cbbafcafaa855ac677d687bd`

## Content

---
name: nextjs-static
description: Next.js static site template principles. Landing pages, portfolios, marketing.
---

# Next.js Static Site Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Next.js 14 (Static Export) |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Animations | Framer Motion |
| Icons | Lucide React |
| SEO | Next SEO |

---

## Directory Structure

```
project-name/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx      # Landing
│   │   ├── about/
│   │   ├── contact/
│   │   └── blog/
│   ├── components/
│   │   ├── layout/       # Header, Footer
│   │   ├── sections/     # Hero, Features, CTA
│   │   └── ui/
│   └── lib/
├── content/              # Markdown content
├── public/
└── next.config.js
```

---

## Static Export Config

```javascript
// next.config.js
const nextConfig = {
  output: 'export',
  images: { unoptimized: true },
  trailingSlash: true,
};
```

---

## Landing Page Sections

| Section | Purpose |
|---------|---------|
| Hero | Main headline, CTA |
| Features | Product benefits |
| Testimonials | Social proof |
| Pricing | Plans |
| CTA | Final conversion |

---

## Animation Patterns

| Pattern | Use |
|---------|-----|
| Fade up | Content entry |
| Stagger | List items |
| Scroll reveal | On viewport |
| Hover | Interactive feedback |

---

## Setup Steps

1. `npx create-next-app {{name}} --typescript --tailwind --app`
2. Install: `npm install framer-motion lucide-react next-seo`
3. Configure static export
4. Create sections
5. `npm run dev`

---

## Deployment

| Platform | Method |
|----------|--------|
| Vercel | Auto |
| Netlify | Auto |
| GitHub Pages | gh-pages branch |
| Any host | Upload `out` folder |

---

## Best Practices

- Static export for maximum performance
- Framer Motion for premium animations
- Responsive mobile-first design
- SEO metadata on every page

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
