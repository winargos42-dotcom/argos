---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/electron-desktop/TEMPLATE.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\business-marketing\app-builder\templates\electron-desktop\TEMPLATE.md
source_ext: .md
source_sha256: c36b89725403d3883619b1e1d8b723aa99d7ed93f28cf3a52195817d44068298
text_sha256: b495860b7ab3a38d0541729933178cc49b7f05d08d02ac06541cb1b3eacbb7ce
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# TEMPLATE.md

- Source: `claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/electron-desktop/TEMPLATE.md`
- Extract: `text`
- SHA256: `c36b89725403d3883619b1e1d8b723aa99d7ed93f28cf3a52195817d44068298`

## Content

---
name: electron-desktop
description: Electron desktop app template principles. Cross-platform, React, TypeScript.
---

# Electron Desktop App Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Electron 28+ |
| UI | React 18 |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Bundler | Vite + electron-builder |
| IPC | Type-safe communication |

---

## Directory Structure

```
project-name/
├── electron/
│   ├── main.ts          # Main process
│   ├── preload.ts       # Preload script
│   └── ipc/             # IPC handlers
├── src/
│   ├── App.tsx
│   ├── components/
│   │   ├── TitleBar.tsx # Custom title bar
│   │   └── ...
│   └── hooks/
├── public/
└── package.json
```

---

## Process Model

| Process | Role |
|---------|------|
| Main | Node.js, system access |
| Renderer | Chromium, React UI |
| Preload | Bridge, context isolation |

---

## Key Concepts

| Concept | Purpose |
|---------|---------|
| contextBridge | Safe API exposure |
| ipcMain/ipcRenderer | Process communication |
| nodeIntegration: false | Security |
| contextIsolation: true | Security |

---

## Setup Steps

1. `npm create vite {{name}} -- --template react-ts`
2. Install: `npm install -D electron electron-builder vite-plugin-electron`
3. Create electron/ directory
4. Configure main process
5. `npm run electron:dev`

---

## Build Targets

| Platform | Output |
|----------|--------|
| Windows | NSIS, Portable |
| macOS | DMG, ZIP |
| Linux | AppImage, DEB |

---

## Best Practices

- Use preload script for main/renderer bridge
- Type-safe IPC with typed handlers
- Custom title bar for native feel
- Handle window state (maximize, minimize)
- Auto-updates with electron-updater

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
