---
argos_import: project_file
source_path: tmp/kolibrios/data/ru_RU/docs/Install.txt
source_abs: F:\debug\argoss\tmp\kolibrios\data\ru_RU\docs\Install.txt
source_ext: .txt
source_sha256: 3839f701218f1151b19983d2fd12e1f52f7fca41d0ed492205869db8d8625a19
text_sha256: f8e2f4d6fc9e194c67b76589f495547a44b6db413a3e4604bc4c6d231bbf3ec2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:40
---

# Install.txt

- Source: `tmp/kolibrios/data/ru_RU/docs/Install.txt`
- Extract: `text`
- SHA256: `3839f701218f1151b19983d2fd12e1f52f7fca41d0ed492205869db8d8625a19`

## Content

⥬ ॡ ਎:
* CPU 5x86: Pentium I, AMD  Cyrix  MMX  ⮩ 90 MHz
* RAM: 8 Mb
* : ন VGA (० 640*480*16)  VESA
* : AT
* : COM, PS/2  USB

⥬  㦠    ᫥ ன:
- Floppy 3.5
- CD/DVD
- USB Flash
- HDD LBA
- 筠 ⠭ 稪

I. ⠭  ᪥.
  1) ⠢  ᪥  ᡮ ᥪ஢  ᪮.
  2)    ࠧ kolibri.img   㯭 ᯮᮡ:
    ) (᫨  㦥 㧨 - ࠧ )  ணࠬ
       rdsave  롥 ᮮ⢥騩 ᪥  । ਠ⮢
    )  DOS ᯮ ⨫⮩ DskImage
    )  Windows  ணࠬ WinImage, RawWrite for Windows  
    )  Linux  :
       `dd if=/pathto/kolibri.img of=/dev/fd0 bs=512 count=2880` 
       । 祭 ᪥    ࠧ஢.

  ᪥  㦠 (⠢   ᪮, १㧨,
  ⠭  BIOS'  㧪  ᪥).

II. ⠭  USB-Flash-⥫.
ISO ࠧ   ⨫⮩ Rufus https://rufus.ie
   ४ ᯮ짮 ᯥ樠 ⠭騪  FAT32-⮬
 ⠫ HD_load\USB_Boot.
 ᮡ  砥  , ࠧ񭭠  ⠫ HD_load\USB_Boot_old.

III. ⠭  CD  DVD.
 ᯥ樠쭠  Kolibri  LiveCD,    ⠭⭮
⠢ 室 "" ( ⠭⠬ ) ணࠬ.
 ⠪  ᮧ 㧮 CD  DVD   ⠭⭮ ⠢
(   ,  㣮)  ० 樨 㧪 
᪥. 室  ⮣ ⢨ । ᯮ㥬 
ணࠬ  CD/DVD
(ਥ  ᫮ " 㧪  ᪥").

IV. ⠭  ⪨ .
 ᪮쪮 稪  ⪮ ᪠.   ⠭ 
짮⥫ DOS  Windows.    ᯮ짮 ⠭
Linux-㧪  GRUB.   ⮤ ࠡ  䠩 kolibri.img. ᫨
  Kolibri 㦥 ⠭  ᯮ짮 -  
稪,   kolibri.img  . ᫨  㧨 
LiveCD,  ஬  䠩 kolibri.img  ⠪,   ᮧ
 ᠬ⥫쭮,  ⮣  ணࠬ rdsave,   䠩
 ࠭  롥 ᮮ⢥騩 ਠ. 㬥,  ᮧ
ࠧ -  ⥬  㬥   䠩 ⥬ ࠧ.
1)  ᥣ ⥩  稪 mtldr ( - Diamond) - ࠡ 
   DOS/Win95/98/NT/2k/XP/Vista, প FAT32  NTFS, 稥 ⠫,
   ⠭  ந   ᪥.
    ⠭   䠩 HD_load\mtldr_install.exe  㪠
   䠩 ࠧ.  , ⠪ ᯮᮡ  ⠭ ᪮쪮
   ࠧ.  ⠪ ਠ ⠭  -  ,  
   筮 ,  ந室  ⠭: 樨  HD_load\mtldr
2)   稪 MeOSLoad ( - Trans, ࠡ⠫ Mario79) -
   ࠡ  DOS/Win95/98, প FAT32,
   室騩   樥   HD_load\MeOSLoad.
3) ஬ ⮣,  ணࠬ,  㦠 Kolibri ।⢥
    Windows 95/98/Me (⢥, 㦠 ᫥) -  9x2klbr
   ( - Diamond), প FAT32  NTFS.
4) ᫨   ⠭ Linux,  ந 㧪 १ GRUB.
    ਡ⨢ ਫ 䠩 'memdisk',    ⠫ 'boot'
     ࠧ, ᯮ㥬  Kolibri.
   a)  GRUB2,   /etc/grub.d     䠩 :

menuentry 'KolibriOS' {
      linux16 (hd[ ⪮ ᪠],[ ࠧ])[  䠩]/memdisk
      initrd16 (hd[ ⪮ ᪠],[ ࠧ])[  䠩]/kolibri.img
      }

      ਬ:

menuentry 'KolibriOS' {
      linux16 (hd0,msdos1)/boot/memdisk
      initrd16 (hd0,msdos1)/boot/kolibri.img
      }

      ᫥ 祣  ନ 믮  sudo update-grub.

   )  ண GRUB,   䠩 䨣樨 'menu.lst' :

      title KolibriOS
      kernel (hd[ ⪮ ᪠],[ ࠧ])[  䠩]/memdisk
      initrd (hd[ ⪮ ᪠],[ ࠧ])[  䠩]/kolibri.img

       ,  㬥  GRUB 稭  0. ਬ:

      title KolibriOS
      kernel (hd0,0)/boot/memdisk
      initrd (hd0,3)/kolibri/kolibri.img

=================================================================================

筠 ⠭ 稪 ⢫ ᫥騬  ᯮᮡ:
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

1.     ࠡ⠥  䠩 ⥬ NTFS  FAT32. 

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
