---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/examples/simple-todo-app.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\loki-mode\examples\simple-todo-app.md
source_ext: .md
source_sha256: 2d5b19c9863f1dd38a4d93cb2480f744ac5ad041fd1ff4acb8d567f93c665830
text_sha256: 1589aebc3bc09e277ed9e0c4cd004ae65b48ed0c787cc2b7418b92fa8f071201
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:32
---

# simple-todo-app.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/examples/simple-todo-app.md`
- Extract: `text`
- SHA256: `2d5b19c9863f1dd38a4d93cb2480f744ac5ad041fd1ff4acb8d567f93c665830`

## Content

# PRD: Simple Todo App

## Overview
A minimal todo application for testing Loki Mode with a simple, well-defined scope.

## Target Users
Individual users who want a simple way to track tasks.

## Features

### MVP Features
1. **Add Todo** - Users can add a new todo item with a title
2. **View Todos** - Display list of all todos
3. **Complete Todo** - Mark a todo as done
4. **Delete Todo** - Remove a todo from the list

### Tech Stack (Suggested)
- Frontend: React + TypeScript
- Backend: Node.js + Express
- Database: SQLite (local file)
- No deployment (local testing only)

## Acceptance Criteria

### Add Todo
- [ ] Input field for todo title
- [ ] Submit button
- [ ] New todo appears in list
- [ ] Input clears after submit

### View Todos
- [ ] Shows all todos in a list
- [ ] Shows completion status
- [ ] Empty state when no todos

### Complete Todo
- [ ] Checkbox or button to mark complete
- [ ] Visual indicator for completed items
- [ ] Persists after refresh

### Delete Todo
- [ ] Delete button on each todo
- [ ] Confirmation before delete
- [ ] Removes from list and database

## Out of Scope
- User authentication
- Due dates
- Categories/tags
- Mobile app
- Cloud deployment

## Success Metrics
- All features functional
- Tests passing
- No console errors

---

**Purpose:** This PRD is intentionally simple to allow quick testing of Loki Mode's core functionality without waiting for complex builds or deployments.

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
