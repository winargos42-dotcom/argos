---
argos_import: project_file
source_path: openai-chatkit-advanced-samples/examples/cat-lounge/frontend/README.md
source_abs: F:\debug\argoss\openai-chatkit-advanced-samples\examples\cat-lounge\frontend\README.md
source_ext: .md
source_sha256: ff38b474001c5e7c958450d2b0c266063bb60b4b3450ba0321c2bde0d79afaee
text_sha256: b0f570bd86856ceeeb10858236ccaa4874a4ac473977a2637b4a9abbf30872b8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:25
---

# README.md

- Source: `openai-chatkit-advanced-samples/examples/cat-lounge/frontend/README.md`
- Extract: `text`
- SHA256: `ff38b474001c5e7c958450d2b0c266063bb60b4b3450ba0321c2bde0d79afaee`

## Content

# ChatKit Frontend

This Vite + React client wraps the ChatKit web component in a slim list UI so you can focus on iterating with the backend agent. It mirrors the root README tone while surfacing the project paths and configuration you need day to day.

## Quick Reference
- App entry point: `src/main.tsx`
- ChatKit config helper: `src/lib/config.ts`
- Cat dashboard UI: `src/App.tsx` and `src/components`
- Styling: `src/index.css` (Tailwind layers)

## Requirements
- Node.js 20+
- Backend API running locally (defaults to `http://127.0.0.1:8000`).

## Environment Variables

Optional overrides include `VITE_CHATKIT_API_URL`, `VITE_CAT_STATE_API_URL`, and `VITE_CHATKIT_API_DOMAIN_KEY`. If you change them, restart `npm run dev` so Vite reloads the new values.

## Install & Run

```bash
npm install
npm run dev
```

The dev server is available at `http://127.0.0.1:5170`, which works for local development. To test remote access flows, you can temporarily expose the app with a tunnel (for example `ngrok http 5170`) after allowlisting that hostname.

For production deployments, host the app on infrastructure you control behind a managed domain. Register that domain on the [domain allowlist page](https://platform.openai.com/settings/organization/security/domain-allowlist), add it to `frontend/vite.config.ts` under `server.allowedHosts`, and set the resulting key via `VITE_CHATKIT_API_DOMAIN_KEY`.

Need backend guidance? See the root README for FastAPI setup and domain allowlisting steps.

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
