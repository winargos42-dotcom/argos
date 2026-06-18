---
argos_import: project_file
source_path: tmp/kolibrios/kernel/branches/kolibri_pe/docs/loader_doc.txt
source_abs: F:\debug\argoss\tmp\kolibrios\kernel\branches\kolibri_pe\docs\loader_doc.txt
source_ext: .txt
source_sha256: eba8ac753212eaa3e5848509f95ac2b05c147eda115f9e7b738d5702188fc9c7
text_sha256: 1ffdc93d15197eccfb5f5718c5d40d9685e92b629fcfd18ceba46b88c09b8f4b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:41
---

# loader_doc.txt

- Source: `tmp/kolibrios/kernel/branches/kolibri_pe/docs/loader_doc.txt`
- Extract: `text`
- SHA256: `eba8ac753212eaa3e5848509f95ac2b05c147eda115f9e7b738d5702188fc9c7`

## Content

; (english text below)

;------------------------------------------
;   
;------------------------------------------
       AX='KL',
  DS:SI       :
        db       ,   1
        dw      :
                 0  =     
        dd           
                  0,    
       
kernel.mnt    ,    ;  
   retf.

;------------------------------------------
;    
;------------------------------------------
        :
CX='HA'
DX='RD'
   ,   BX    .  /kolibri/ 
   ,       /sys/

   BL (  ):
'a' - Primary   Master
'b' - Primary   Slave
'c' - Secondary Master
'd' - Secondary Slave
'r' - RAM 
'm' -  CD-ROM

   BH (  ):
 BL='a','b','c','d','r' -   ,    
 BL='m',    ,       .

   BX:
'a1' - /hd0/1/
'a2' - /hd0/2/
'b1' - /hd1/1/
'd4' - /hd3/4/
'm0' -     kolibri
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
