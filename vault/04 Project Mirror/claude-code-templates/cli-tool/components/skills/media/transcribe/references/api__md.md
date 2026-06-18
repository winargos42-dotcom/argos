---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/media/transcribe/references/api.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\media\transcribe\references\api.md
source_ext: .md
source_sha256: eaa5637c90273e053ed5aaf48c90219cfff826fcde907bbdd1a7177217d463fc
text_sha256: a2bf7e59d69aa127b176255c5c01afbafda4e3029b12b4413e75074233ffb36d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# api.md

- Source: `claude-code-templates/cli-tool/components/skills/media/transcribe/references/api.md`
- Extract: `text`
- SHA256: `eaa5637c90273e053ed5aaf48c90219cfff826fcde907bbdd1a7177217d463fc`

## Content

# gpt-4o-transcribe-diarize quick reference

- Input formats: mp3, mp4, mpeg, mpga, m4a, wav, webm.
- Max file size: 25 MB per request.
- response_format options: text, json, diarized_json.
- For audio longer than ~30 seconds, pass chunking_strategy (use "auto" to split into chunks).
- Known speakers: up to 4 references via extra_body known_speaker_names + known_speaker_references (data URLs).
- Prompting is not supported for gpt-4o-transcribe-diarize.

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
