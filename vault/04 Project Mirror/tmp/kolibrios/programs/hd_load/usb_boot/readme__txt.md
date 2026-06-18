---
argos_import: project_file
source_path: tmp/kolibrios/programs/hd_load/usb_boot/readme.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\hd_load\usb_boot\readme.txt
source_ext: .txt
source_sha256: 65e82ff0d894135891cb230081ec1b6bcaba66d59f7629eee453548e6a049fc6
text_sha256: 2244e78586c568c2ff382dcd6155558280b0c1bbbaa8faf8db972749d2a81673
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# readme.txt

- Source: `tmp/kolibrios/programs/hd_load/usb_boot/readme.txt`
- Extract: `text`
- SHA256: `65e82ff0d894135891cb230081ec1b6bcaba66d59f7629eee453548e6a049fc6`

## Content

:
BOOT_F32.BIN -   FAT32;
MTLD_F32 -   ;
inst.exe -    WinNT+;
setmbr.exe -   MBR ( );
readme.txt -  .

       FAT32,  
      kolibri.img     
 .

   WinNT+:
 inst.exe,    , 
,    ,     .   
.   (  /     
 FAT32-) - .
    kolibri.img    
. (       .)
    .

   ,  ( )  
,   "Pen drive Without Operating System.Remove
Pen Drive And Reboot."    
    ,  ,  setmbr.exe.
     .    
     ,   .
     .

     :
 -   .      
,    : inst.exe   
:
-  , ,    FAT32;
-     MTLD_F32,    
"","","  " (   
  ,          );
-   BOOT_F32.BIN;     
   3   0x5A (0x57 )   ;
- ,  ,     ,
     ,    (   2 
  0x32) (      ,
       ).

,  Linux     /dev/sdb1 (  ,
 FAT32-)      :
dd if=/dev/sdb1 of=BOOT_F32.BIN bs=1 skip=3 seek=3 count=87 conv=notrunc
dd if=BOOT_F32.BIN of=/dev/sdb1 bs=512 count=1 conv=notrunc
  mtld_f32  kolibri.img   .

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
