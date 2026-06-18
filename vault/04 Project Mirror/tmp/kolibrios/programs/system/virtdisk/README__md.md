---
argos_import: project_file
source_path: tmp/kolibrios/programs/system/virtdisk/README.md
source_abs: F:\debug\argoss\tmp\kolibrios\programs\system\virtdisk\README.md
source_ext: .md
source_sha256: 4623c6bbc95f2f6bd801015fc695da89f1d829dd8fa340b6e6433a959bde6d75
text_sha256: 7a7b1475d9bbdabe73bc17ea6baa9c09c8ee82326e559cb72c02eac1657f022c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:47
---

# README.md

- Source: `tmp/kolibrios/programs/system/virtdisk/README.md`
- Extract: `text`
- SHA256: `4623c6bbc95f2f6bd801015fc695da89f1d829dd8fa340b6e6433a959bde6d75`

## Content

# VIRT_DISK
Driver for mounting RAW disk images in KolibriOS.

To demonstrate the operation of the driver, the virtdisk program was written. Program allows you to add, delete and view virtual disks.
![foto](https://github.com/Doczom/VIRT_DISK/blob/main/utils/scr_1.png)

## List of virtdisk arguments:
 - Delete command:
 
   <CODE> virtdisk -d <DISK_NUMBER> </CODE>

 - Information from disk:

   <CODE> virtdisk -i <DISK_NUMBER> </CODE>

 - Add disk image in file system:

   <CODE> virtdisk -a <IMAGE_PATH> -s <SECTOR_SIZE> -t <IMAGE_TYPE> -f <ACCESS_FLAGS> </CODE>

 - Input list all virtual disks:

   <CODE> virtdisk -l </CODE>

## List flags:
 - <CODE>ro</CODE> - read only access
 - <CODE>rw</CODE> - read-write access

## List disk image types:
 - <CODE>RAW</CODE> - it is used to mount disk images in "raw", "img" and "iso" formats

## Exemples command:
   <CODE> virtdisk -a /sd0/4/kolibri.img -f ro </CODE>
   
   <CODE> virtdisk -d 3 </CODE>

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
