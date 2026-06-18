---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/docs/ARB_color_buffer_float.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-9.2.5\docs\ARB_color_buffer_float.txt
source_ext: .txt
source_sha256: c52ec9eda5822cda3ae83a7bc944acf5a1f8f49ca94029e2ec880ed31854ade7
text_sha256: 21534750ddd73179eb5adf4d4b1f0eb1fde1eb3600eb223fbe0c749e310634d1
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:34
---

# ARB_color_buffer_float.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/docs/ARB_color_buffer_float.txt`
- Extract: `text`
- SHA256: `c52ec9eda5822cda3ae83a7bc944acf5a1f8f49ca94029e2ec880ed31854ade7`

## Content

Known issues in the ARB_color_buffer_float implementation:
- Rendering to multiple render targets, some fixed-point, some floating-point, with FIXED_ONLY fragment clamping and polygon smooth enabled may write incorrect values to the fixed point buffers (depends on spec interpretation)
- For fragment programs with ARB_fog_* options, colors are clamped before fog application regardless of the fragment clamping setting (this depends on spec interpretation)

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
