---
argos_import: project_file
source_path: openai-chatkit-advanced-samples/examples/cat-lounge/README.md
source_abs: F:\debug\argoss\openai-chatkit-advanced-samples\examples\cat-lounge\README.md
source_ext: .md
source_sha256: 727928799214c5c6433ab3d835954950b819cd2cde79d79aaaff46ea2a84981c
text_sha256: 63eeeddd9f78d58f0532a7ef0c705ade11c2aa888424caba829e467667194ef4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:25
---

# README.md

- Source: `openai-chatkit-advanced-samples/examples/cat-lounge/README.md`
- Extract: `text`
- SHA256: `727928799214c5c6433ab3d835954950b819cd2cde79d79aaaff46ea2a84981c`

## Content

# Cat Lounge

Virtual cat caretaker demo built with ChatKit (FastAPI backend + Vite/React frontend).

## Quickstart

1. Export `OPENAI_API_KEY`.
2. From the repo root run `npm run cat-lounge` (or `cd examples/cat-lounge && npm install && npm run start`).
3. Go to http://localhost:5170

## Example prompts

- "Feed the cat a tuna treat."
- "The cat looks a little messy—give them a bath."
- "What should I name the cat?"
- "Can I see the cat's profile card?"
- "Hello, cat! How are you feeling?"

## Features

- Server tools to read and mutate per-thread cat state: `get_cat_status`, `feed_cat`, `play_with_cat`, `clean_cat`, `set_cat_name`, `speak_as_cat`.
- Name suggestion workflow with a selectable widget and client-handled actions (`cats.select_name`, `cats.more_names`) plus server reconciliation for chosen names.
- Profile card widget (`show_cat_profile`) streamed from the server with presentation-only content.
- One-way client effects (`update_cat_status`, `cat_say`) are streamed from the server to keep the UI stats in sync and surface speech bubbles after each server tool invocation.
- Hidden context tags track recent actions (<FED_CAT>, <PLAYED_WITH_CAT>, <CLEANED_CAT>, <CAT_NAME_SELECTED>) so the agent remembers what already happened.
- Quick actions call `chatkit.sendUserMessage` to send canned requests without typing ([App.tsx](frontend/src/App.tsx)).
- Image generation for cat pictures with partials using `ImageGenerationTool`

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
