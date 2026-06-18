---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/media/speech/references/audio-api.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\media\speech\references\audio-api.md
source_ext: .md
source_sha256: 705e7aa0554e1a505aea18259efdb17d6d7d24ebafa8826df478d2e07f74d5fa
text_sha256: dba58cfc0d5e125cf1ac13875193950233aa948639b268ed7799ca17bca66bfe
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# audio-api.md

- Source: `claude-code-templates/cli-tool/components/skills/media/speech/references/audio-api.md`
- Extract: `text`
- SHA256: `705e7aa0554e1a505aea18259efdb17d6d7d24ebafa8826df478d2e07f74d5fa`

## Content

# Audio Speech API quick reference

## Endpoint
- Create speech: `POST /v1/audio/speech`

## Default model
- `gpt-4o-mini-tts-2025-12-15`

## Other speech models (if requested)
- `gpt-4o-mini-tts`
- `tts-1`
- `tts-1-hd`

## Core parameters
- `model`: speech model
- `input`: text to synthesize (max 4096 characters)
- `voice`: built-in voice name
- `instructions`: optional style directions (not supported for `tts-1` or `tts-1-hd`)
- `response_format`: `mp3`, `opus`, `aac`, `flac`, `wav`, or `pcm`
- `speed`: 0.25 to 4.0

## Built-in voices
- `alloy`, `ash`, `ballad`, `cedar`, `coral`, `echo`, `fable`, `marin`, `nova`, `onyx`, `sage`, `shimmer`, `verse`

## Output notes
- Default format is `mp3`.
- `pcm` is raw 24 kHz 16-bit little-endian samples (no header).
- `wav` includes a header (better for quick playback).

## Compliance note
- Provide a clear disclosure that the voice is AI-generated.

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
