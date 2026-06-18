---
argos_import: project_file
source_path: tmp/kolibrios/programs/hd_load/mtldr/install.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\hd_load\mtldr\install.txt
source_ext: .txt
source_sha256: f0b6036775bfe7be4922bc4983314640f4b3337d60b505e07ceab60246897256
text_sha256: a511df6ab0af3776472ca9b6d34aa3c1d12f2925239558bcf5b37cd3e6b205fc
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# install.txt

- Source: `tmp/kolibrios/programs/hd_load/mtldr/install.txt`
- Extract: `text`
- SHA256: `f0b6036775bfe7be4922bc4983314640f4b3337d60b505e07ceab60246897256`

## Content

⠭ ⢫ ᫥騬  ᯮᮡ:
 1.  䠩 mtldr  kolibri.img  C:\
	( ࠢ C:\? ⠩ 砭 .)

 2)  짮⥫ NT-ᥬ⢠  Vista (NT/2k/XP/2003 Server (?)):
	  boot.ini  ࠧ [operating systems] ப
c:\mtldr="KolibriOS"
	(   ⥪⮢ ।஬ c:\boot.ini,
	  १ Control Panel -> System -> Advanced -> Startup and Recovery
	-> Edit).   窠    ,   ࠢ,
	 ⨬  ⥬ 㤥   ᯨ᪥ 㧪.
  㧪 㤥 뤠 ࠭ 롮 樮 ⥬.

 2)  짮⥫ 9x-ᥬ⢠ (95/98)
(  ,  㤥 ࠡ    DOS):
	  config.sys ப
install=c:\mtldr
	ࢮ ப, ᫨   ⮩  config.sys,
	ࢮ ப  ᮮ⢥饩 ᥪ樨, ᫨ config.sys
	ࠧ  ᥪ樨 ( 稭  [menu])
  㧪 mtldr 㤥 訢: "Load KolibriOS? [y/n]: "  
   'y','Y','n','N'.

 Windows Millenium   ࠡ⠥, .. Me' 稪 
㦠 譥   config.sys. (ᨡ camper'  㪠
  ᪮࡭ 䠪.) ᯮ 9x2klbr.

 2)  짮⥫ Vista:
	ன  ப  ᪨ ਢﬨ
		(㭪 "Run as administrator"  ⥪⭮ );
	᫨    ⠭ ᪮쪨 ਠ⮢ 
	 ᠭ  砭,   ਫ vista_install.bat;
	 믮 ᫥騥 :
bcdedit /create /d "KolibriOS" /application BOOTSECTOR
	(  窠    ,   ࠢ,
	 ⨬  ⥬ 㤥   ᯨ᪥ 㧪.)
	  ᮮ饭 ⨯
" {xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx} ᯥ譮 ᮧ."
	   ⠢ 祭 祭 (,  ,
	ࠧ  ࠧ ).
bcdedit /set {xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx} DEVICE PARTITION=C:
bcdedit /set {xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx} PATH \mtldr
bcdedit /displayorder {xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx} /addlast

   2)  2) ⢫ 㤠   
boot.ini  config.sys ᮮ⢥⢥.   砥 2)  ⠪:

vista_remove.bat, ᫨ ⠭ 뫠 १ vista_install.bat;
bcdedit /delete {xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}  饬 砥

᫨    祭  ⠭ GUID ( ଠ쭮 ),
 㧭  , 믮  bcdedit  㬥⮢  
 뢥 ᯨ᪥ ᮮ⢥騩 .

    ࠭ 롮 ࠬ஢ KolibriOS   ,
㤠 㧨 ࠧ (㭪 d, "ࠧ ᪥"),
⢥ "3" (ᯮ짮 㦥 㦥 ࠧ).

砭:

1.     ࠡ⠥  䠩 ⥬ NTFS  FAT32, প FAT16
 ॠ  裡   㡮 㡥,  ᥩ FAT16 - ꥪ
 ᪨. ᫨  ᯮ FAT16,   ⮨ Windows   
- 稭   室  FAT32 -  
-  ,  㤠  㡥.

2.  稪 mtldr 易⥫쭮   C:\.  9x  Vista  
ࠧ  㣮,  NT/2k/XP -  ᪥ C:,  易⥫쭮
 ୥ . (㬥,  ⠭ 㦭 㪠뢠 
c:\mtldr ॠ   ॠ쭮  䠩.)

3. ࠧ kolibri.img ⮦ 易⥫쭮   C:\.   直
  ⠭ ᯮ짮 ୥   ᪮ ᪠,
ࠧ饣  ࢮ 䨧᪮.

4. ᫨  ᯮ짮 ᪨   㣮 䨧᪮ ᪥?
   ᫥ ਠ⮢:
a) (᫨  㬥 ࠡ  FASM')  室 (  ᪠
    http://diamondz.land.ru, ⠬ ,   ᠬ 稪) 
   ⠭ boot_drive (  mtldr.asm)  80h  䨪 ᪠,
   80h ᮮ⢥ ࢮ, 81h - ஬  .. ४.
) (᫨  㬥 ࠡ  hex-।஬)    ᬥ饭 0xD98
    80h  䨪 ᪠ (  㭪 ).
) ᯮ ⠭騪 mtldr_install (᪠   ⠬ ).
    ந 稪  ᠬ    ⠭.

5. ᫨ 祬-  ࠢ ୥ ?    ਠ:
)  室  ப kolibri_img_name (  mtldr.asm)
      䠩. ਬ,  C:\Program Files\kolibri\kolibri.img 
   'progra~1\kolibri\kolibri.img' ( ⮬ 㦭  8.3). ४.
) ᯮ ⠭騪 mtldr_install.

6. ᫨ ᯮ짮 ४ﬨ 㭪⮢ 2  5   ⠭
   ᪮쪮 ࠧ  ࠧ ᯮ 離 mtldr+kolibri.img,
      㧮筮  ᪮쪮 室  ࠧ ᨩ
    (  ᨩ  ࠧ묨 ன).

7. , 砭, । 뫠  뫮, 㪠 .

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
