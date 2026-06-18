---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/video/sora/references/video-api.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\video\sora\references\video-api.md
source_ext: .md
source_sha256: e0fdbd6473a1bf8c7b5eb2a398fc6b18483f1f2001380096cf7d85d8058f22f9
text_sha256: 01a2e01f4d595e9e5b7de24dfe4943e227a3c59b1513215acfaee68912870587
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# video-api.md

- Source: `claude-code-templates/cli-tool/components/skills/video/sora/references/video-api.md`
- Extract: `text`
- SHA256: `e0fdbd6473a1bf8c7b5eb2a398fc6b18483f1f2001380096cf7d85d8058f22f9`

## Content

# Sora Video API quick reference

Keep this file short; the full docs live in the OpenAI platform docs.

## Models
- sora-2: faster, flexible iteration
- sora-2-pro: higher fidelity, slower, more expensive

## Sizes (by model)
- sora-2: 1280x720, 720x1280
- sora-2-pro: 1280x720, 720x1280, 1024x1792, 1792x1024
Note: higher resolutions generally yield better detail, texture, and motion consistency.

## Duration
- seconds: "4", "8", "12" (string enum; set via API param; prose will not change clip length)
Shorter clips tend to follow instructions more reliably; consider stitching multiple 4s clips for precision.

## Input reference
- Optional `input_reference` image (jpg/png/webp).
- Input reference should match the target size.

## Jobs and status
- Create is async. Status values: queued, in_progress, completed, failed.
- Prefer polling every 10-20s or use webhooks in production.

## Endpoints (conceptual)
- POST /videos: create a job
- GET /videos/{id}: retrieve status
- GET /videos/{id}/content: download video data
- GET /videos: list
- DELETE /videos/{id}: delete
- POST /videos/{id}/remix: remix a completed job

## Download variants
- video (mp4)
- thumbnail (webp)
- spritesheet (jpg)

Download URLs expire after about 1 hour; copy files to your own storage for retention.

## Guardrails (content restrictions)
- Only content suitable for audiences under 18
- No copyrighted characters or copyrighted music
- No real people (including public figures)
- Input images with human faces are currently rejected

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
