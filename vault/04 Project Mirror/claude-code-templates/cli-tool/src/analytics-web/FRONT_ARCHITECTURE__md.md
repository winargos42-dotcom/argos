---
argos_import: project_file
source_path: claude-code-templates/cli-tool/src/analytics-web/FRONT_ARCHITECTURE.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\src\analytics-web\FRONT_ARCHITECTURE.md
source_ext: .md
source_sha256: c61affc8d70d013431e820c232247760fc626d2cd5344eca3ac8378c663b3220
text_sha256: 2a5497e58b6b98a8154c1785b126417b8e6d6bae5c93cb03e198426986837c4b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# FRONT_ARCHITECTURE.md

- Source: `claude-code-templates/cli-tool/src/analytics-web/FRONT_ARCHITECTURE.md`
- Extract: `text`
- SHA256: `c61affc8d70d013431e820c232247760fc626d2cd5344eca3ac8378c663b3220`

## Content

# Analytics Web Architecture

## Current Architecture (Active)

### Main Components:
- **App.js** - Main application orchestrator with sidebar navigation
- **Sidebar.js** - Navigation sidebar component
- **DashboardPage.js** - Dashboard page with metrics and charts
- **AgentsPage.js** - Agents/conversations page

### Services:
- **WebSocketService.js** - Real-time communication
- **DataService.js** - API data fetching and caching
- **StateService.js** - Application state management

### Layout Structure:
```
App.js
├── Sidebar.js (navigation)
└── Page Components
    ├── DashboardPage.js
    └── AgentsPage.js
```

## Deprecated Architecture (Removed)

### Deprecated Files:
- **main.js** → `main.js.deprecated` - Old initialization system
- **Dashboard.js** → `Dashboard.js.deprecated` - Old monolithic dashboard

### Reason for Deprecation:
The old architecture used a single Dashboard.js component without navigation, while the new architecture uses App.js with proper routing and a sidebar navigation system.

## WebSocket Integration

The WebSocket system is fully functional and provides real-time updates for:
- Conversation state changes
- Data refresh events
- System status updates

## Loading State Fix

Fixed issue where loading states weren't clearing properly by:
1. Reordering DOM rendering before setting loading states
2. Adding proper error handling and fallback mechanisms
3. Ensuring `setLoading(false)` is called in finally blocks

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
