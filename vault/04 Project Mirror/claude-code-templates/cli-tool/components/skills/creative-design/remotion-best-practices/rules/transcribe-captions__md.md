---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/remotion-best-practices/rules/transcribe-captions.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\remotion-best-practices\rules\transcribe-captions.md
source_ext: .md
source_sha256: 9487f6d0c4053846f17094b740e2051098752d15ef39b1f95f2707d028d9b7bc
text_sha256: e7d3edf667e3b1f3c3ed93431cc7caf5e28786c7d1e547f33ee926480a01c0d0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# transcribe-captions.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/remotion-best-practices/rules/transcribe-captions.md`
- Extract: `text`
- SHA256: `9487f6d0c4053846f17094b740e2051098752d15ef39b1f95f2707d028d9b7bc`

## Content

---
name: transcribe-captions
description: Transcribing audio to generate captions in Remotion
metadata:
  tags: captions, transcribe, whisper, audio, speech-to-text
---

# Transcribing audio

Remotion provides several built-in options for transcribing audio to generate captions:

- `@remotion/install-whisper-cpp` - Transcribe locally on a server using Whisper.cpp. Fast and free, but requires server infrastructure.
  https://remotion.dev/docs/install-whisper-cpp

- `@remotion/whisper-web` - Transcribe in the browser using WebAssembly. No server needed and free, but slower due to WASM overhead.
  https://remotion.dev/docs/whisper-web

- `@remotion/openai-whisper` - Use OpenAI Whisper API for cloud-based transcription. Fast and no server needed, but requires payment.
  https://remotion.dev/docs/openai-whisper/openai-whisper-api-to-captions

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
