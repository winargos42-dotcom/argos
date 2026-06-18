---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/examples/api-only.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\loki-mode\examples\api-only.md
source_ext: .md
source_sha256: d075e9066caeb90104bdb35d3c68a91981e3969707c7f71005763a64876062b1
text_sha256: 4342d60386b225c12132053e6c29ef3c5bf1d53ef38c0bee5fdd5cb275282793
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:32
---

# api-only.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/examples/api-only.md`
- Extract: `text`
- SHA256: `d075e9066caeb90104bdb35d3c68a91981e3969707c7f71005763a64876062b1`

## Content

# PRD: REST API Service

## Overview
A simple REST API for managing notes. Tests Loki Mode's backend-only capabilities.

## Target Users
Developers who need a notes API.

## API Endpoints

### Notes Resource

#### GET /api/notes
- Returns list of all notes
- Response: `[{ id, title, content, createdAt }]`

#### GET /api/notes/:id
- Returns single note
- Response: `{ id, title, content, createdAt }`
- Error: 404 if not found

#### POST /api/notes
- Creates new note
- Body: `{ title, content }`
- Response: `{ id, title, content, createdAt }`
- Error: 400 if validation fails

#### PUT /api/notes/:id
- Updates existing note
- Body: `{ title?, content? }`
- Response: `{ id, title, content, updatedAt }`
- Error: 404 if not found

#### DELETE /api/notes/:id
- Deletes note
- Response: 204 No Content
- Error: 404 if not found

### Health Check

#### GET /health
- Returns `{ status: "ok", timestamp }`

## Tech Stack
- Runtime: Node.js 18+
- Framework: Express.js
- Database: In-memory (array) for simplicity
- Validation: zod or joi
- Testing: Jest + supertest

## Requirements
- Input validation on all endpoints
- Proper HTTP status codes
- JSON error responses
- Request logging
- Unit tests for each endpoint

## Out of Scope
- Authentication
- Database persistence
- Rate limiting
- API documentation (OpenAPI)
- Deployment

## Test Cases
```
POST /api/notes with valid data → 201 + note object
POST /api/notes with missing title → 400 + error
GET /api/notes → 200 + array
GET /api/notes/:id with valid id → 200 + note
GET /api/notes/:id with invalid id → 404
PUT /api/notes/:id with valid data → 200 + updated note
DELETE /api/notes/:id → 204
GET /health → 200 + status object
```

---

**Purpose:** Tests backend agent capabilities, code review, and QA without frontend complexity.

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
