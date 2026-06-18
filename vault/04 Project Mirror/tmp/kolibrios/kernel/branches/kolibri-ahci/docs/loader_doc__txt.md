---
argos_import: project_file
source_path: tmp/kolibrios/kernel/branches/kolibri-ahci/docs/loader_doc.txt
source_abs: F:\debug\argoss\tmp\kolibrios\kernel\branches\kolibri-ahci\docs\loader_doc.txt
source_ext: .txt
source_sha256: 63622454fbac93ee1cbbe1ca5ea99c231ecba7660bdac9dd95788aaf2f39d348
text_sha256: b4ad4b07be4b9c09ff077477ec23ddaaf8e2b49cb640668cc4455b38695fa558
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:41
---

# loader_doc.txt

- Source: `tmp/kolibrios/kernel/branches/kolibri-ahci/docs/loader_doc.txt`
- Extract: `text`
- SHA256: `63622454fbac93ee1cbbe1ca5ea99c231ecba7660bdac9dd95788aaf2f39d348`

## Content

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;                                                              ;;
;; Copyright (C) KolibriOS team 2004-2011. All rights reserved. ;;
;; Distributed under terms of the GNU General Public License    ;;
;;                                                              ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; (english text below)

;------------------------------------------
; Интерфейс сохранения параметров
;------------------------------------------
Если при передаче управления ядру загрузчик устанавливает AX='KL',
то в DS:SI ядро ожидает дальнего указателя на следующую структуру:
        db      версия структуры, должна быть 1
        dw      флаги:
                бит 0 установлен = присутствует образ рамдиска в памяти
        dd      дальний указатель на процедуру сохранения параметров
                может быть 0, если загрузчик не поддерживает
Процедура сохранения параметров должна записать первый сектор ядра
kernel.mnt назад на то место, откуда она его считала; возврат из
процедуры осуществляется по retf.

;------------------------------------------
; Указание загрузчиком системного каталога
;------------------------------------------
Перед передачей управления ядру могут быть установлены следующие регистры:
CX='HA'
DX='RD'
Это указывает на то, что регистр BX указывает на системный раздел. Каталог /kolibri/ на
этом разделе является системным, к нему можно обращаться как к /sys/

Возможные значения регистра BL (указывает на устройство):
'a' - Primary   Master
'b' - Primary   Slave
'c' - Secondary Master
'd' - Secondary Slave
'r' - RAM диск
'm' - Приводы CD-ROM

Возможные значения регистра BH (указывает на раздел):
для BL='a','b','c','d','r' - указывает на раздел, где расположен системный каталог
для BL='m',указывает на номер физического устройства, с которого надо начинать поиск системного каталога.

примеры значений регистра BX:
'a1' - /hd0/1/
'a2' - /hd0/2/
'b1' - /hd1/1/
'd4' - /hd3/4/
'm0' - поиск по сидюкам каталога kolibri
'r1' - /rd/1/


;------------------------------------------
; Interface for saving boot-screen settings
;------------------------------------------
If a loader sets AX='KL' when transferring control to the kernel,
the kernel expects in DS:SI far pointer to the following structure:
        db      structure version, must be 1
        dw      flags
                bit 0 set = ramdisk image in memory is present
        dd      far pointer to save settings procedure
                may be 0 if such procedure is not supported by loader
Procedure for saving settings must write the first sector of the kernel
kernel.mnt back to the place, from where it has been read; return from
this procedure must be with retf.

;------------------------------------------ 
; System directory information from loader
;------------------------------------------ 
Before transfer of control to the kernel following registers can be set:
CX = 'HA'
DX = 'RD'
This indicates that the register BX identifies system partition. The folder /kolibri/ in
this partition is system folder, it can be referenced as /sys/

Possible values for register BL (indicates the device):
'a' - Primary Master
'b' - Primary Slave
'c' - Secondary Master
'd' - Secondary Slave
'r' - RAM disc
'm' - ROM drives

Possible values for register BH (indicates section):
for BL = 'a', 'b', 'c', 'd', 'r' to denote partition where the system folder
for BL = 'm', indicates the number of physical devices, which must begin a systematic search directory.

Examples of register BX:
'a1' - /hd0/1/
'a2' - /hd0/2/
'b1' - /hd1/1/
'd4' - /hd3/4/
'm0' - search directory 'kolibri' by all CD-ROMs
'r1' - /rd/1/

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
