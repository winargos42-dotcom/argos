---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/project-detection.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\business-marketing\app-builder\project-detection.md
source_ext: .md
source_sha256: 7d727d85947a5f89e81b59f1ab21f0bfe9108c91818f059ea2ca6d25f1352c56
text_sha256: 65f41fd5bc87b8022b609cfef5ac0a372f57df872a939bcb8705dbe9294edd2f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# project-detection.md

- Source: `claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/project-detection.md`
- Extract: `text`
- SHA256: `7d727d85947a5f89e81b59f1ab21f0bfe9108c91818f059ea2ca6d25f1352c56`

## Content

# Project Type Detection

> Analyze user requests to determine project type and template.

## Keyword Matrix

| Keywords | Project Type | Template |
|----------|--------------|----------|
| blog, post, article | Blog | astro-static |
| e-commerce, product, cart, payment | E-commerce | nextjs-saas |
| dashboard, panel, management | Admin Dashboard | nextjs-fullstack |
| api, backend, service, rest | API Service | express-api |
| python, fastapi, django | Python API | python-fastapi |
| mobile, android, ios, react native | Mobile App (RN) | react-native-app |
| flutter, dart | Mobile App (Flutter) | flutter-app |
| portfolio, personal, cv | Portfolio | nextjs-static |
| crm, customer, sales | CRM | nextjs-fullstack |
| saas, subscription, stripe | SaaS | nextjs-saas |
| landing, promotional, marketing | Landing Page | nextjs-static |
| docs, documentation | Documentation | astro-static |
| extension, plugin, chrome | Browser Extension | chrome-extension |
| desktop, electron | Desktop App | electron-desktop |
| cli, command line, terminal | CLI Tool | cli-tool |
| monorepo, workspace | Monorepo | monorepo-turborepo |

## Detection Process

```
1. Tokenize user request
2. Extract keywords
3. Determine project type
4. Detect missing information → forward to conversation-manager
5. Suggest tech stack
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
