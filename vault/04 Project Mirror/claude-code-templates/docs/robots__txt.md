---
argos_import: project_file
source_path: claude-code-templates/docs/robots.txt
source_abs: F:\debug\argoss\claude-code-templates\docs\robots.txt
source_ext: .txt
source_sha256: cd3fd2d25bf8328c9fd2f58015f06d7807636d2a0a4976884ee435df0b0fde25
text_sha256: f33875346b1a85c4c25bc2c7281d01c437bbfe7b58a93984e241bb84d5b775dd
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# robots.txt

- Source: `claude-code-templates/docs/robots.txt`
- Extract: `text`
- SHA256: `cd3fd2d25bf8328c9fd2f58015f06d7807636d2a0a4976884ee435df0b0fde25`

## Content

User-agent: *
Allow: /

# Filter pages - high priority for crawling
Allow: /agents
Allow: /commands
Allow: /settings
Allow: /hooks
Allow: /mcps
Allow: /templates
Allow: /skills

# Blog content
Allow: /blog/

# Component pages
Allow: /component/

# Important pages
Allow: /trending.html

# Disallow temporary or admin files
Disallow: /node_modules/
Disallow: /.git/
Disallow: /.vercel/
Disallow: /dev-server.js

# Sitemap location (fixed: was pointing to GitHub Pages instead of aitmpl.com)
Sitemap: https://aitmpl.com/sitemap.xml

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
