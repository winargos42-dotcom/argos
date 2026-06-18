---
argos_import: project_file
source_path: tmp/kolibrios/programs/hd_load/usb_boot_old/usb_boot_1251.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\hd_load\usb_boot_old\usb_boot_1251.txt
source_ext: .txt
source_sha256: c2af6dee2e1effb76938bd079d11226348152e3a95ea9c9b98da4120f5acc31a
text_sha256: 8f5f769f307164556cb4852afb375902a6965b245b18cf5080276214424127bd
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# usb_boot_1251.txt

- Source: `tmp/kolibrios/programs/hd_load/usb_boot_old/usb_boot_1251.txt`
- Extract: `text`
- SHA256: `c2af6dee2e1effb76938bd079d11226348152e3a95ea9c9b98da4120f5acc31a`

## Content

: Mario79
xx.01.2006 -  
20.03.2006 -  
23.03.2006 -    
26.02.2007 -        

   USB Flash Drive
       USB     ,       USB Flash      .
 2      .

1)     BIOS.
       IMG ,   ,   0  IMG   0  ,            .            1,44 .      ,      .
       :
)  Linux   ,     man dd
)  Windows       WinHex ( ),  2880    A (floppy disk)  ,   Flash ,   0 .
) DOS     , ,    BIOS   .

2)  Flash      BIOS.
   :    BIOS         ,       FAT12,              4 .
   ,    FAT16           2 .  ,         FAT32,        USB Flash    2 ,   .

   .
         ,        .     ,     (    )    .
      2 : meosload.com  mtldr.
     DOS.
          DOS  ,   , -     . ,            DOS,      ,     ,       .

 DOS     :
)  Windows        ,  ,        .  ,       9,  2  ,      .
) DOS             .      sys X:     ,       Flash  ( ,      ,          ).   DOS, ,   ,         F (),         ,     DOS  .
     USB Flash    DOS.

  ,        Command.com, Io.sys, Msdos.sys -   ,      .            ,    .        DOS  .    ,       DOS,       .
             : Config.sys, Autoexec.bat -  ,         ,         .

,    .    ,     (      ).
   ,          IMG    (    ),  ,     .   , ,        ,    USB     .

    -        ,        . ! (  !)    DOS,     (Real mode)  ,       1 ,          ,         .
  ? ! DOS            (         ),     ,      . (    ).

           .   86    ,      (Unreal mode)  .
,      ,        ,      .
           4 ,       .

     meosload.com (       ),       ,    .
         ,   <http://www.wasm.ru>      enable.exe
      FASM (   TASM),  Serge,     ,           .

,    ,             .
       enable.exe  meosload.com,     Autoexec.bat   (Autoexec.bat     ) , ,           kolibri.img.

    .        USB Flash .            3-   .

P.S.
1)           (NoName),  (DoomEdArchangel)   (Serge).
2)          enable.exe  meosload.com    .

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
