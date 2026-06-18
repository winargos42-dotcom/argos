---
argos_import: project_file
source_path: tmp/kolibrios/programs/hd_load/9x2klbr/readme.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\hd_load\9x2klbr\readme.txt
source_ext: .txt
source_sha256: ea3c22ad2589ec2cf7ceea8a8f844294074f2077e0c4e4f13808c9b7e4d9ed47
text_sha256: d03c83e14ded147dd5dc677f2dca3315d555e337a9d2eca642b7ed41759a195c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# readme.txt

- Source: `tmp/kolibrios/programs/hd_load/9x2klbr/readme.txt`
- Extract: `text`
- SHA256: `ea3c22ad2589ec2cf7ceea8a8f844294074f2077e0c4e4f13808c9b7e4d9ed47`

## Content

Purpose: when it is started (from Win95/98/ME), (correctly) unloads Windows
and loads KolibriOS instead.

Installation is not required.

Start:
	9x2klbr \[\[drive:]\[path\][image_name\]\]
Image file must be situated on hard disk.
Default values: drive C:, root folder, image kolibri.img.
Path and image name must contain only characters from first half of
ASCII-table. In particular, there must be no russian letters.

FAT: Only short names of folders and file are accepted, i.e. progra~1 instead
of Program Files; for names such as kolibri and menuet.075 (no more than
8 characters in name, no more than 3 characters in extension, no special
characters) this is satisfied automatically, in general case short name can be
found out, for example, in Explorer dialog "Properties" (in column
"MS-DOS name").

If this requirements are not satisfied, loader will not format drive :-)
but simply says 'not found'.

Examples:
	9x2klbr d:\download\kolibri\kolibri1.img
	9x2klbr c:\progra~1\kolibri\
	9x2klbr \progra~1\kolibri\
		(will load from kolibri.img)
	9x2klbr e:\
		(equivalent to 9x2klbr e:\kolibri.img)
	9x2klbr
		(without parameters; equivalent to 9x2klbr c:\kolibri.img)

						diamond
						mailto: diamondz@land.ru

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
