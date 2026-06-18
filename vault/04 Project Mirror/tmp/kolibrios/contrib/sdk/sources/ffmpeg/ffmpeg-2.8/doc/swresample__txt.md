---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/ffmpeg/ffmpeg-2.8/doc/swresample.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\ffmpeg\ffmpeg-2.8\doc\swresample.txt
source_ext: .txt
source_sha256: 801e3358ff9b88b23d8195affc535a2bed160c08cc1ab58a6a3aa40808a703f4
text_sha256: 452fb7b3384327cbf70f5d9c45d55d15d76df0fca1a477ea63f926c069f954cb
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:29
---

# swresample.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/ffmpeg/ffmpeg-2.8/doc/swresample.txt`
- Extract: `text`
- SHA256: `801e3358ff9b88b23d8195affc535a2bed160c08cc1ab58a6a3aa40808a703f4`

## Content

The official guide to swresample for confused developers.
   =========================================================

Current (simplified) Architecture:
---------------------------------
                        Input
                          v
       __________________/|\___________
      /                   |            \
     /    input sample format convert   v
    /                     | ___________/
    |                     |/
    |                     v
    |         ___________/|\___________              _____________
    |        /            |            \            |             |
    |   Rematrix          |          resample <---->|   Buffers   |
    |        \___________ | ___________/            |_____________|
    v                    \|/
Special Converter         v
    v         ___________/|\___________              _____________
    |        /            |            \            |             |
    |   Rematrix          |          resample <---->|   Buffers   |
    |        \___________ | ___________/            |_____________|
    |                    \|/
    |                     v
    |                     |\___________
    \                     |            \
     \   output sample format convert   v
      \_________________  | ___________/
                         \|/
                          v
                        Output

Planar/Packed conversion is done when needed during sample format conversion.
Every step can be skipped without memcpy when it is not needed.
Either Resampling and Rematrixing can be performed first depending on which
way it is faster.
The Buffers are needed for resampling due to resamplng being a process that
requires future and past data, it thus also introduces inevitably a delay when
used.
Internally 32bit float and 16bit int is supported currently, other formats can
easily be added.
Externally all sample formats in packed and planar configuration are supported
It's also trivial to add special converters for common cases.
If only sample format and/or packed/planar conversion is needed, it
is performed from input to output directly in a single pass with no intermediates.

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
