---
argos_import: project_file
source_path: openai-chatkit-advanced-samples/examples/metro-map/README.md
source_abs: F:\debug\argoss\openai-chatkit-advanced-samples\examples\metro-map\README.md
source_ext: .md
source_sha256: a82eef6f94bbb87b2df04d48dbff75e6c814fc75a5ec438ed7b6f04b33b684ed
text_sha256: 3a4ccf12b4089b61ffbf10ad470b4918aa02258730ded4bae735d02644f4d5e6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:25
---

# README.md

- Source: `openai-chatkit-advanced-samples/examples/metro-map/README.md`
- Extract: `text`
- SHA256: `a82eef6f94bbb87b2df04d48dbff75e6c814fc75a5ec438ed7b6f04b33b684ed`

## Content

# Metro Map

Chat-driven GUI updates for a metro map using a React Flow canvas that lets the user extend lines with new stations.

## Quickstart

1. Export `OPENAI_API_KEY` (and `VITE_CHATKIT_API_DOMAIN_KEY=domain_pk_local_dev` for local).
2. From the repo root run `npm run metro-map` (or `cd examples/metro-map && npm install && npm run start`).
3. Go to http://localhost:5173

## Example prompts

- "Add a new station named Aurora" (line picker widget will appear)
- "Plan a route from Titan Border to Lyra Verge."
- "Tell me about @Cinderia station." (@-mention stations; need to type @ manually, copy paste won't work)
- "Tell me about the stations I've selected." (lasso some stations on the canvas first)

## Features

- Map sync + lookup tools: `get_map`, `list_lines`, `list_stations`, `get_line_route`, `get_station` keep the agent grounded in the latest network data.
- Selection-aware replies: the agent calls the `get_selected_stations` client tool to pull the user’s current canvas selection before continuing a response, handled in `onClientTool` ([ChatKitPanel.tsx](frontend/src/components/ChatKitPanel.tsx), [metro_map_agent.py](backend/app/agents/metro_map_agent.py)).
- Plan-a-route responses attach entity sources that are shown as inline annotations for each station in the recommended path so ChatKit can keep the canvas focused on the stops being discussed.
- Station creation flow: `show_line_selector` streams a clickable `line.select` widget, the server stashes `<LINE_SELECTED>`, and `add_station` triggers a widget update and a client tool call to refresh the canvas and focus the new stop.
- Location placement helper: after a line is chosen, a `location_select_mode` client effect flips the UI into placement mode so users pick start/end of line for insertion.
- Progress updates: initial map fetch streams a quick progress event while loading line data.
- Entity tags: station @-mentions in the composer add `<STATION_TAG>` content for the agent and can be clicked to focus the station on the canvas. Users can trigger tag search by typing "@" in the composer or clicking the "@" button.
- Custom header action: a right-side icon toggles dark/light themes in the ChatKit header.

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
