---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/examples/clipboard/clipboard_container_eng.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\examples\clipboard\clipboard_container_eng.txt
source_ext: .txt
source_sha256: 2496ae16ed6b55ddba3855d536b3cefa622e32ee3128f275ee86b79ac951b637
text_sha256: e47d25a86d8832df7b396e9e236415b695933771ec38476fe0816d9b61078725
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:42
---

# clipboard_container_eng.txt

- Source: `tmp/kolibrios/programs/develop/examples/clipboard/clipboard_container_eng.txt`
- Extract: `text`
- SHA256: `2496ae16ed6b55ddba3855d536b3cefa622e32ee3128f275ee86b79ac951b637`

## Content

Сontents of container from clipboard

1. First dword - contains the total length of data in the container

2. Second dword - indicates the type of data:
   0 = Text
   1 = Highlighted text block
   2 = Image
   3 = RAW
   4 and above reserved

2.1 Text
    Data in the third dword contain type:
    0 = UTF
    1 = 0866    
    2 = 1251
    3 and above reserved
    
2.2 Highlighted text block
    Differs from 2.1 - that all rows have the same length.

2.3 Image
    Third dword - X size
    Fourth dword - Y size
    Fifth dword - bit color depth (8, 16, 24, 32, 48, 64)
    Sixth dword - Pointer to the palette (the offset from the beginning of the file).
                   If the palette is not set then value 0
    Seventh dword - The size of the palette, the maximum value of 256 * 4 = 1024 bytes.
                   If the palette is not set then value 0
    Eighth dword - A pointer to the pixel data for the R, G, B.
    Ninth dword - The size of the data for pixels.
    
2.4 RAW
    Can contain any data, because content at the discretion of the programmer

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
