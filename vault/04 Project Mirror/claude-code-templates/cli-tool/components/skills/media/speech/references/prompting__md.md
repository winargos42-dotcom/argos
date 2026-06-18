---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/media/speech/references/prompting.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\media\speech\references\prompting.md
source_ext: .md
source_sha256: 86937d5640981d6368b952b6a20ec69baca84d4c96a763c3d2ca6938648c2e94
text_sha256: 2adcb001813be04e56918eb0d34d9a45f9326aa0fb240526ae74a926522b6554
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# prompting.md

- Source: `claude-code-templates/cli-tool/components/skills/media/speech/references/prompting.md`
- Extract: `text`
- SHA256: `86937d5640981d6368b952b6a20ec69baca84d4c96a763c3d2ca6938648c2e94`

## Content

# Instructioning best practices (TTS)

## Contents
- Structure
- Specificity
- Avoiding conflicts
- Pronunciation and names
- Pauses and pacing
- Iterate deliberately
- Where to find copy/paste recipes

## Structure
- Use a consistent order: affect -> tone -> pacing -> emotion -> pronunciation/pauses -> emphasis -> delivery.
- For complex requests, use short labeled lines instead of a long paragraph.

## Specificity
- Name the delivery you want ("calm and steady" vs "friendly").
- If you need a specific cadence, call it out explicitly ("slow and measured", "brisk and energetic").

## Avoiding conflicts
- Do not mix opposing instructions ("fast and slow", "formal and casual").
- Keep instructions short: 4 to 8 lines are usually enough.

## Pronunciation and names
- For acronyms, write the pronunciation hint in text ("A-I" instead of "AI").
- For names or brands, add a simple phonetic guide in the input text if clarity matters.
- If a word must be emphasized, add an Emphasis line and repeat the word exactly.

## Pauses and pacing
- Use punctuation or short line breaks in the input text to create natural pauses.
- Use the Pauses line for intentional pauses ("pause after the greeting").

## Iterate deliberately
- Start with a clean base instruction set, then make one change at a time.
- Repeat critical constraints on each iteration ("keep pacing steady").

## Where to find copy/paste recipes
For copy/paste instruction templates, see `references/sample-prompts.md`. This file focuses on principles, structure, and iteration patterns.

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
