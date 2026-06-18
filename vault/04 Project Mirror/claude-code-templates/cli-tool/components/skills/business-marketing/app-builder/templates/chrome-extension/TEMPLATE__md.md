---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/chrome-extension/TEMPLATE.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\business-marketing\app-builder\templates\chrome-extension\TEMPLATE.md
source_ext: .md
source_sha256: c56294b9837707893586c7a158f6918dee349787a6635d516dc4efd868e47a14
text_sha256: dc8701558732953a5834255066a89bfc0036dd778d5a44d3a39f3066036fe8c2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# TEMPLATE.md

- Source: `claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/chrome-extension/TEMPLATE.md`
- Extract: `text`
- SHA256: `c56294b9837707893586c7a158f6918dee349787a6635d516dc4efd868e47a14`

## Content

---
name: chrome-extension
description: Chrome Extension template principles. Manifest V3, React, TypeScript.
---

# Chrome Extension Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Manifest | V3 |
| UI | React 18 |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Bundler | Vite |
| Storage | Chrome Storage API |

---

## Directory Structure

```
project-name/
├── src/
│   ├── popup/           # Extension popup
│   ├── options/         # Options page
│   ├── background/      # Service worker
│   ├── content/         # Content scripts
│   ├── components/
│   ├── hooks/
│   └── lib/
│       ├── storage.ts   # Chrome storage helpers
│       └── messaging.ts # Message passing
├── public/
│   ├── icons/
│   └── manifest.json
└── package.json
```

---

## Manifest V3 Concepts

| Component | Purpose |
|-----------|---------|
| Service Worker | Background processing |
| Content Scripts | Page injection |
| Popup | User interface |
| Options Page | Settings |

---

## Permissions

| Permission | Use |
|------------|-----|
| storage | Save user data |
| activeTab | Current tab access |
| scripting | Inject scripts |
| host_permissions | Site access |

---

## Setup Steps

1. `npm create vite {{name}} -- --template react-ts`
2. Add Chrome types: `npm install -D @types/chrome`
3. Configure Vite for multi-entry
4. Create manifest.json
5. `npm run dev` (watch mode)
6. Load in Chrome: `chrome://extensions` → Load unpacked

---

## Development Tips

| Task | Method |
|------|--------|
| Debug Popup | Right-click icon → Inspect |
| Debug Background | Extensions page → Service worker |
| Debug Content | DevTools console on page |
| Hot Reload | `npm run dev` with watch |

---

## Best Practices

- Use type-safe messaging
- Wrap Chrome APIs in promises
- Minimize permissions
- Handle offline gracefully

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
