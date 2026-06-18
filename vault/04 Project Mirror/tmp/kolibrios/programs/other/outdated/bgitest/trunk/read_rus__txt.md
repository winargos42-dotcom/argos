---
argos_import: project_file
source_path: tmp/kolibrios/programs/other/outdated/bgitest/trunk/read_rus.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\other\outdated\bgitest\trunk\read_rus.txt
source_ext: .txt
source_sha256: d51c79303bbfccdd3f5b5453b92689792f62ea70e8507d18bcda7952929c08b3
text_sha256: d9e64067bd0d97745b5c8b5771e835225435bbbe2debfcb039a45945bd598ff2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:47
---

# read_rus.txt

- Source: `tmp/kolibrios/programs/other/outdated/bgitest/trunk/read_rus.txt`
- Extract: `text`
- SHA256: `d51c79303bbfccdd3f5b5453b92689792f62ea70e8507d18bcda7952929c08b3`

## Content

BGIFONT.INC v1.0 beta for MenuetOS
   ࠡ  묨 ⠬ ଠ BGI

 ᠭ  ⮬ ᥬ 誨 ॥ aka Willow

   饥 ६ 樮 ⥬ Menuet  㤭묨 ।⢠
⮡ࠦ ᨬ.  ਡ⨢  2 ஢  (䠩 CHAR.MT 
CHAR2.MT).    ⪮   . । ᨫ  ७
⠡㥬 ⮢ TTF- ଠ ।ਭ Jarek Pelczar, 
஬ MenuetOS C Library  稫    让 ୮ 
ᥬ୮ . ᪮  Menuet  ⪨ ந  
⨩ ⠡㥬 , , ᪮쪮  ⭮,  ᨬ 室 
⠤ .  ࠧ, ࠧࠡ⪠    ।⠢ 業
 冷 짮⥫. 祢,  ⠡㥬  
ࠧࠡ⪥ ⠪  ⥣਩ ணࠬ த⮢,  㧥 
⥪⮢ ,   ஫ ࠥ ଠ஢ ᨬ.
  ।⠢  ⢥ 짮 砥 䠩 BGIFONT.INC  ࠡ 
묨 ⠬ *.CHR, ࠧࠡ⠭ ⮩ ମ Borland 
ᯮ짮   Turbo Pascal, Turbo C  Borland C++   । MS-
DOS.  ᮦ,     㤠 ᯥ প BGI-⮢ 
஢  - 㦭 㡦   ।   맮
⥬ 㭪権.  ,  ⥬騪 Menuet  ⮢  .
   ⠢  ।  ᯮ짮 ⠭
BGI_LEVEL equ KERNEL.  ᫮ 樨   㤥
ᯮ짮  ⥫묨 ﬨ  ஢  , ⠪  ਫ.
 ᠥ ࠡ   ஢ ਫ.

  BGI-  ᯮ   ⠫ HD  RD.  
⢫  祭 ⠭ BGI_PATH. ᫨ ⠭ BGI_WINDOW_CLIP
⠭  1, 楤ࠬ    뢮 ஢ 
⢫ ஢ઠ 室  ࠭ , ⮡  䠪⮢.
ᯮ , ᫨   㢥७,      . 
⮬ 砥 室 ⥫쭮 । ⠭ BGI_PRC_INFO - 
  (1024 ), 㤠 ਫ   ଠ  ᢮ 
१ 9- ⥬ 㭪.  楤  BGIFONT.INC  
, .. 뢠  call.  㧪 11 ⮢  ᭮
࠭⢮ ਫ 室 뢭 ⮪ ࠧ஬  120 .
 㧪 ⢫ ६饭   楫  . 奬
ࠧ饭 ⮢:

| 稪 |  | |  ||   ||  | |  ||
| ⮢ |  |  BGIrec  |  ||   | BGIrec  |  | |  | BGIrec  |   ...
| (1 )|          |                  |    |                  |    |
     |               ------------->------    -------------->-----    ----------
     -  뫠 [BGIfont_Ptr]

    BGIrec  ᫥饥 祭:

 +00 dword .FontName     㪢  
 +04 byte  .CharsCount   ⢮ ᨬ  
 +05 byte  .FirstChar     ࢮ ॠ ᨬ
 +06 byte  .UpperMargin   ࠭ ᨬ
 +07 byte  .LowerMargin   ࠭ ᨬ
 +08 dword .Widths       ᬥ饭 ᨢ ਭ ᨬ
 +12 dword .FirstData    ᬥ饭 ⠡ ஢
 +16 dword .EOF	         㪠⥫  ᫥騩 BGIrec
 +20 dword .font_data     稭  

  ⢥ 㧪  䨪  ⢫ 楤
BGIfont_Prepare.

  BGIfont_Prepare
     室:  EDX - 㪢  , 饣 㧪. 
            ᮢ   䠩  ( ७)
            EDI -  ⪠ , 㤠 ᫥   .
            ᯮ ⮫쪮  㧪 ࢮ .  祭
              [BGIfont_Ptr]
     室: EAX=0, ᫨ ந諠 訡,   EAX - 䨪 (ID)
            㦥 . ᫥⢨ ID   㭪ﬨ
            BGIfont_GetID  BGIfont_GetName.

   ६ 㧪 ᪮쪨 ⮢  ᯮ짮 楤
BGIfont_Init.

  BGIfont_Init
     室:  ESI - 㪠⥫  ᯨ᮪  ⮢ (ਬ db 'TRIPSIMPEURO')
            ECX - ⢮ ⮢  㧪
            EDI - . BGIfont_Prepare
     室: 祣.

   㧪 10 ⠭ ⮢  㫥 । ᨢ BGIfont_names
(ᯮ짮 .  BGITEST).

   楫 ᮢ⨬  ᫥饣 ७    । 2
楤  뢮 ᨬ 묨 ⠬.    ᯮ
ॣ ( 4- ⥬ 㭪樨), 㣠 - .

  BGIfont_Outtext
     室:  EAX - "窠 "  뢮 ப [x] shl 16+[y]
            ECX - 梥 ⥪  ࠧ  0xXYRRGGBB,
               X - ID ୮  (4..F),
                  Y - 稭 ᨬ/4, ਬ 0x1 - 1/4 筮 ࠧ,
                      0xC - ன ࠧ.
            EDX - 㪠⥫  ப
            ESI -  ப + 䫠 ଠ஢ (. ). 
              BGI_ITALIC  BGI_NODRAW .
     室: EAX - न   [x] shl 16+[y].

   , BGIfont_Outtext  ᢮ ࠬࠬ 宦  4- ⥬ 㭪樥,
 ᪠ ७ ࠢ 뢮 ᨬ.

    ᯮ짮  ⮢ ᯥ稢 㭪
BGIfont_Freetext. ࠬ 뢮 ப ।   BGIfree.

    BGIfree  ᫥饥 祭:

 +00 dword   㪢  
 +04 dword   "窠 "  뢮 ப [x] shl 16+[y]
 +08 dword   㣮  (0 - ਧ⠫,   ᮢ ५)
 +12 dword   ⠡   X (祭  饩 窮!)
 +16 dword   ⠡   Y (祭  饩 窮!)
 +20 dword   㪠⥫  ப
 +24 dword    ப  䫠 ଠ஢
 +28 dword   梥 ⥪ 0x00RRGGBB
 +32 dword   䫠 ଠ஢

   । ᫥騥 䫠 ଠ஢:
BGI_NODRAW     -  ᮢ ᨬ
BGI_ITALIC     - ᨢ
BGI_BOLD       - 㦨 
BGI_HALEFT     - ஢   
BGI_HARIGHT    - ஢  ࠢ 
BGI_HACENTER   - ஢  業
BGI_VABOTTOM   - ஢   
BGI_VATOP      - ஢  孥 
BGI_VACENTER   - ஢  ।

   䫠 ࠧ  ᫮  樥 OR.

  BGIfont_Freetext
     室:  EBX - 㪠⥫   BGIfree
     室: EAX - न   [x] shl 16+[y].

  㭪 BGIfont_GetID 頥 ID    .

  BGIfont_GetID
     室:  EDX - 㪢  
     室: EAX - ID 
            EDI - 㪠⥫  BGIrec .

  ᯮ짮 㭪権  BGIFONT.INC  ணࠬ BGITEST.

    㦭 ᤥ:
1.  ⢥ 㧪 ⮢ (  BGITEST)  
    , 騩 ᪮쪮 ᨬ.   浪 㧪
   ⮢  祧... :-(
2. ࠢ 㤮ந     ᯨ ⮢.
3. ᮢ襭⢮ ᮢ 㦨 ⮢.
4.  㭪樨 뢮 ᥫ.

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
