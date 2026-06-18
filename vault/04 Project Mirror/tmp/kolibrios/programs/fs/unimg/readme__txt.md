---
argos_import: project_file
source_path: tmp/kolibrios/programs/fs/unimg/readme.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\fs\unimg\readme.txt
source_ext: .txt
source_sha256: 976fca480acdd5b8f0d918ff3330eb62cb4cd361a25d2ff6b7c12a02dd48cea7
text_sha256: e81e68027b5b5f7fc884a84f8ba49fe69c764502949444ac521c21d337e8081d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:45
---

# readme.txt

- Source: `tmp/kolibrios/programs/fs/unimg/readme.txt`
- Extract: `text`
- SHA256: `976fca480acdd5b8f0d918ff3330eb62cb4cd361a25d2ff6b7c12a02dd48cea7`

## Content

# KolibriOS Image Unpacker
## Summary

Extracts files from FAT12 KolibriOS image to specified folder.

## How to use

unimg path/to/img [output/folder] [-e]

If output folder is skipped, the image will be unpacked at /TMP0/1/KOLIBRI.IMG

Options:
-e: Exit on success

## How to build

kos32-tcc fat12.c -lck -o unimg.kex

## Toolchain

Default toolchain for TCC on Kolibri, got from KolibriISO/develop/tcc

## Authors

- Magomed Kostoev (Boppan, mkostoevr): FAT12 file system, driver.

## Contributors

- Kirill Lypatov (Leency): Coding style, driver working protocol.

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
