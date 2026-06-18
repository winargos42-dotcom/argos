---
argos_import: project_file
source_path: tmp/kolibrios/data/ru_RU/docs/Config.txt
source_abs: F:\debug\argoss\tmp\kolibrios\data\ru_RU\docs\Config.txt
source_ext: .txt
source_sha256: 3b381ac2a0be939987493418140785407d9825dd4090c281a063b7725972ac81
text_sha256: b561031a2bd5d43ac7ae8de432b749bedce14cc39fd52dda8c4cd951c73b7412
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:39
---

# Config.txt

- Source: `tmp/kolibrios/data/ru_RU/docs/Config.txt`
- Extract: `text`
- SHA256: `3b381ac2a0be939987493418140785407d9825dd4090c281a063b7725972ac81`

## Content

⥬ KolibriOS ᪠  ன  㦤 짮⥫.
 䠩 뢠 ⠪ ன.
 ⮣ ॡ   䠩  ࠬ᪥. ᫨  㦠
 ᪥,  ஡  -  䠩  ᪥. ᫨ 
ᯮ ࠧ ᪥ kolibri.img -    ணࠬ
ࠡ  ࠧ (ਬ, WinImage  DiskExplorer),  ந
      ࠭ ࠬ (ணࠬ rdsave).

1.  ࠡ祣 ⮫.
)  䠩 autorun.dat (⥪⮢ 䠩)   ࠬ  ணࠬ
   kiv ("\S__background.jpg")  䠩   -  ࠢ襩
    JPEG-, BMP-, GIF-  PNG-⨭.  ⮬   ᨬ 
   ଫ: \S (stretch) =  ⨭  ࠭, \T (tile) =
    ⨭ ࠭.  background.jpg  㤠.
)  䠩 autorun.dat  "/SYS/KIV \S__background.jpg" 
   "/sys/PIC4" (஡ ⠢  ). BACKGROUND.JPG
    㤠.  䮭 㤥 ᨬ筠 ⥪.
   ணࠬ⠬  :    ⥪  梥,
    ⮣  䠩 pic4.asm  室 ਡ⨢ :
   *   ⥪: 祭 ६ usearray (ப 585)
      ptarray    ptarray2,ptarray3, ..., ptarray9.
   *   梥:  楤 check_parameters  ப 
     ᮮ⢥騬 ਥ (ப 127)  ਡ  0x40000 1  2.
   ᫥  ४ pic4,   ᮦ kpack'
   ( ਡ⨢ ᤥ ⠪),   ࠬ.
)  । 㭪 ⠭ 䮭  ( ᫥饩
   ⠭).  ⠪ ᫥ 㧪  ⠭ 䮭 
   ᫥饩 १㧪  ணࠬ kiv, iconedit, pic4, tinyfrac.

2. ன ⥬ .
    ⥬  室  ⥪⮢ 䠩 menu.dat.
        ।, ࠭ ଠ.
    ।஢  Kolibri   TINYPAD ᫥ ⪫
    "⨬쭮 ࠭".

3. ன ⮧᪠.
   ᮪ ணࠬ, ᪠  㧪 ⥬, 뢠 
   ⥪⮢ 䠩 autorun.dat.      ।,
   ࠭ ଠ.
   ਬ,  ࢮ ப   startmus ( প 1,
    㬥⮢), ⮡  ࠧ  ᪥  ஥ ᯨ
   ᨫ ࠪୠ .
   ணࠬ⠬  :   ,  ⮣ ।
   䠩 startmus.asm  室 ਡ⨢: ⠬   
        ᢮ - ଠ 모 ᠭ 
   㬥樨  㭪 55 㭪樨 55.

4. ᮪ .
   ᮪  ࠡ祣 ⮫ ࠭  ⥪⮢   䠩
   icons.dat,     ४ ᯮ짮 
    icon (  맢  ⥪⭮  ࠡ祣 ⮫).
   ⨭   ࠭  䠩 iconstrp.gif,  㦭
   ।஢ 譨 ᪨ ।஬.

5. .
     ᬠਢ   ᪨   ਫ
   desktop; ᫥ ⮣,   ࠫ ᪨,   ࠢ  ᥣ,
    ᤥ  ﭭ,   䠩 default.skn,  ண
   ⥬ 㧨 ᪨  㧪. ⠭ ᪨ 祭  ࠬ,
    ୠ⨢ ᪨    ਡ⨢   Skins.
    ⠪ ᮧ ᢮ ᪨, ஡ ਨ ᬮ  室
   ਡ⨢.

6. .
   ࠩ sound.sys, 室騩  ࠬ᪥  㬮砭, 믮 ᢮
   㭪樨   ⮢ Intel ICH, ICH0, ICH2, ICH3, ICH4, ICH5, ICH6, ICH7
    NVidia NForce, NForce 2, NForce 3, NForce 4. ᫨   SB16-ᮢ⨬
   㪮 , 㤠 sound.sys  २ sb16.sys  ⠫
   drivers  sound.sys. ᫨   ஫ sis7012, २ sis.sys 
   ୥ ⠫ ਡ⨢  sound.sys  ᪮   ᪥ 
   ࠧ  ⠫ drivers ( ).  㪮   ᭮
   ஫ ForteMedia FM801   ࠩ fm801.sys  ⠫
   drivers,  稯⮢  VIA - ࠩ vt8235.sys,  㤨
   EMU10K1X - ࠩ emu10k1x.sys,  묨 ᫥ 㯠 筮 -
   ᪮஢   sound.sys,  .

7. Bus Disconnect.
   ணࠬ KBD (Kolibri Bus Disconnect)  ⪫ 設 
    楫 㬥襭  ⥬,  䥪 -  㬠  AC97
   . ணࠬ   ⮬᪮ 맮  㧪
   ⥬,  ⮣   ⮧ (autorun.dat, . .3) ப 
"/SYS/KBD             BOOT       20    # Enable Bus Disconnect for AMD K7 processors".

8. ࠬ .
    㧪 ࠬ  뢠  䨣樮 䠩
   /sys/network/zeroconf.ini.    ⮮। ࠬ஢
     DHCP ("type=zeroconf"),  䨪஢  ("type=static").

9. ன ०   ATI.
   ࠩ  ATI   ᪥ ⠭ 室 ࠧ襭
   ࠭   ࠧ⪨, ᫨  ন. ᮪ ন
   ०   ࠡ ⥬ 뢠 ணࠬ vmode,   
     ४ ० .  ⠭ ०  㧪
   稪 ATIKMS, ᠭ  AUTORUN.DAT, 㦭 । ࠬ
   -m<width>x<height>x<refresh>, ਬ,

/SYS/DRIVERS/ATIKMS -m1024x768x60 -1

    ,  ଠ 䠩 autorun.dat  ।ᬠਢ ஡
     ப, ⠪  㣨 㬥⮢   .
     ⪫  ४祭 ०   易 
   ⨬ ⢨  㧪, 㪠 㬥 -n. ࠩ  ⮬
   -० 㤥 ।⠢  .   ⪫祭
   ࠩ   㤠 ப  ATIKMS  autorun.dat.

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
