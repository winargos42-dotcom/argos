---
argos_import: project_file
source_path: tmp/kolibrios/programs/games/soko/RULES.TXT
source_abs: F:\debug\argoss\tmp\kolibrios\programs\games\soko\RULES.TXT
source_ext: .txt
source_sha256: 5081985faf317ba78e2c4b8c22714ae0f7bf15f8b90aed2b710c8cd55dee3d19
text_sha256: 106c3c77f2dd3d3d8613b5a0336ae061232d34362b1ad4c77ff656d577851935
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# RULES.TXT

- Source: `tmp/kolibrios/programs/games/soko/RULES.TXT`
- Extract: `text`
- SHA256: `5081985faf317ba78e2c4b8c22714ae0f7bf15f8b90aed2b710c8cd55dee3d19`

## Content

SOKOBAN FOR MENUET v0.1        July 2, 2004
 Written in pure assembler by Ivushkin Andrey aka Willow
 Main idea, art & graphics
   Sokofun for Windows 95 by Games 4 Brains
   and Sokoban 2.3 by Bjrn Kllmark

 Level designers:

   Alberto Garcia, Aymeric du Peloux, Brian Kent, David Holland, 
   David W Skinner, Erim Sever, Evgeniy Grigoriev, Franois Marques, 
   Frantisek Pokorny, Howard Abed,J franklin Mentzer, Jaques Duthen, 
   John C Davis, John Polhemus, Kobus Theron, Lee Haywood, Mario Bonenfant,
   Martin P Holland, Mic (Jan Reineke), Phil Shapiro, Richard Weston,
   Sven Egevad, Ken'ichiro Takahashi (takaken), Thinking Rabbit,
   Yoshio Murase, ZICO (Zbigniew Kornas)

 Special thanks to Hirohiko Nakamiya

 More credits:
   Masato Hiramatsu, Kazuo Fukushima, Klaus Clemens

 Game uses its own format of levelset files *.LEV
   with simple run-length compression
   
!!!!NB!!!!
It is strongly recommended that you place application files into C:\menuetos
directory. Otherwise you should change CUR_DIR (SOKO.ASM, line 30) to the
appropriate value!

Interface

When loaded, application opens skin file SKIN.RAW in the current directory.
It is an image 16x240 pt. Then so-named "standard" levels SOKO-?.LEV are 
read in the same dir. ? means a number within 0 and 9.
You can navigate along the level list pressing PgUp and PgDn keys. User 
selects the level desired by pressing keys 0-9. Space key moves focus to the 
text field below, so you can enter filename there.
Additional levels are in program subfolder LEV. For example, you wish to load
a levelset file /HD/1/MENUETOS/LEV/AENIGMA.LEV. Then you should enter 
lev/aenigma.lev
Within the textbox user can press Backspace. There's no cursor yet :-( 
Pressing Enter in the text field is equvalent for button "Load file".

When in game, pressing Esc restarts the level, pressing Home returns back to 
the levelset selection mode.

Game Rules

You have a little PUSHER. You will guide him using the cursor-keys.

SOKOBAN (same as SOKOBLUE or SOKOWAHN)
    The pink pyramids have to be pushed onto the marked places. 
    The problem is: You can only push things, but not pull them.
    A level is solved when every pyramid stands on a marked place.

SOKOLOR 
    Tiles of the same colour need to be pushed together.

SOKONEX 
    Push all CONNECTOR-TILES together! 

    Game-items of SOKONEX and their properties:
    
    PLATE: undestructable, movable, covers holes
    HOLE: you can push LASERS and BROKEN PLATES into them
    BROKEN PLATE: destructable, movable
    CONNECTOR: undestructable, movable
    FIXED CONNECTOR: undestructable, not movable
    LASER: destructable, movable
    BEAM: eleminates LASERS and BROKEN PLATES, paralyses PUSHERS

The objective is always the same: You must push boxes the right way. 
Sometimes tasks seem to be impossible. 
But, be sure: There is always a solution!

To-Do list:

1. Better interface - I saw XTREE and understood that it's really possible to 
   write wonderful programs for MenuetOS easily.
2. More skins. And lesser file size...
3. Improve user interaction, I think.
4. Level Editor. Having a great wish you may compose levelsets by yourself and
   compile them with FASM - see files CNF.ASM and CNF.
5. Correct bugs, make improvements from opinions of you, respective users of 
   this application ;-)
6. Include support for XTREE dialogs.

****************************************
****************************************

  MENUET v0.1        2  2004 .

 ᠭ  ⮬ ᥬ 誨 ॥ (Willow)
  , 㭪  䨪
   Sokofun for Windows 95  Games 4 Brains
    Sokoban 2.3  Bjrn Kllmark

  ஢:

   Alberto Garcia, Aymeric du Peloux, Brian Kent, David Holland, 
   David W Skinner, Erim Sever, Evgeniy Grigoriev, Franois Marques, 
   Frantisek Pokorny, Howard Abed,J franklin Mentzer, Jaques Duthen, 
   John C Davis, John Polhemus, Kobus Theron, Lee Haywood, Mario Bonenfant,
   Martin P Holland, Mic (Jan Reineke), Phil Shapiro, Richard Weston,
   Sven Egevad, Ken'ichiro Takahashi (takaken), Thinking Rabbit,
   Yoshio Murase, ZICO (Zbigniew Kornas)

 ᮡ ୮ Hirohiko Nakamiya

  ୮:
   Masato Hiramatsu, Kazuo Fukushima, Klaus Clemens

   ᯮ ᯥ樠 ଠ 䠩 ஢ *.LEV
    ਢ ᦠ⨥ ଠ樨

!!!!NB!!!!
⥫쭮 ४  䠩 ணࠬ  ⠫ C:\menuetos.
 ⨢ 砥  ਤ  ⠭ CUR_DIR  䠩
SOKO.ASM  ப 30 ᮮ⢥騬 祭!

䥩

 ᪥ ணࠬ 뢠 䠩 ᪨  ஢ ꥪ⮢ SKIN.RAW
 ᮡ⢥ ⠫.  ⨭ ࠧ஬ 16240 祪. ⥬  ⮬ 
 ⠫  ⠪ 뢠 "⠭" ஢ SOKO-?.LEV, 
? - ᫮  0  9.
 ᯨ ஢  । 蠬 PgUp  PgDn.  ஢
롨ࠥ ⨥   0  9.
⨥ ஡ ७ 䮪  ⥪⮢    䠩 ஢.
⥫ ஢ 室  ⠫ LEV ணࠬ. ⨬,  
 㧨 䠩 ஢ /HD/1/MENUETOS/LEV/AENIGMA.LEV.  ᫥
 ப lev/aenigma.lev 
    Backspace.    ॠ :-( ⨥ 
Enter  ப  ⭮  '㧨'.

 ०  ⨥ Esc ந  ஢, ⨥ Home 뢮 
  ⭮  ᯨ ஢.

ࠢ 

 ⮩     ,   ࠢ 蠬 ५.

 (  :-)  )
     ࠬ 㦭 ।  ᯥ樠 ⪨.
    ஡  ⮬,   ⮫쪮 ⮫ ।,    .
    ஢ 襭,   ࠬ 室  થ୮ ⪥.
    

      梥 㦭 ⮫   .
    

     - 㦭 ⮫   .
    
    ꥪ      ᢮⢠:
    
    : 㭨⮦, , 뢠 
    : 㤠  ⠫    
     : 㭨⮦, 
    : 㭨⮦, 
    -: 㭨⮦, 
    : 㭨⮦, 
     : 㭨⮦    , ࠫ  (!)
    
  ᥣ :   ࠢ쭮 ⠢ .
   믮.
  㢥७: ᥣ  襭!  

   ᤥ:

1. ᨢ 䥩 - ᫥ XTREE  ,   Menuet 
   ⭮⥫쭮   祭 ᨢ ணࠬ.
2. ⥫ ᪨ -  ଠ.   ࠧ 䠩 ᤥ:
   11  -  ண  
3.  ࠢ -  ⠪ .
4.  ஢.  ᮡ  䠩 ஢    
   ஢ FASM' - . 䠩 CNF.ASM  CNF.
5. ࠢ ,  襭    , 㢠 
   짮⥫  ணࠬ ;-)
6.  প   XTREE.

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
