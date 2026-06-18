---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/mtdbg/mtdbg.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\mtdbg\mtdbg.txt
source_ext: .txt
source_sha256: 3cf71d4fd4c7a5d6ee31338d1d5ad382c6a6e7fc1930863048f7b25035e3984f
text_sha256: bd54c5d33ca2173bd092c8d7ce1d57728096d1f730381ecd3ab381ad6d2ab198
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:44
---

# mtdbg.txt

- Source: `tmp/kolibrios/programs/develop/mtdbg/mtdbg.txt`
- Extract: `text`
- SHA256: `3cf71d4fd4c7a5d6ee31338d1d5ad382c6a6e7fc1930863048f7b25035e3984f`

## Content

.

mtdbg        KolibriOS.   -   (Diamond).         .     -        -  ,   ,    board.kolibrios.org    - http://board.kolibrios.org/viewtopic.php?f=45&t=358,     - mailto:diamondz@land.ru.

 .

    mtdbg     .      .     ,      .

mtdbg   ,   .        .     Backspace, Delete, Home, End,  /,  / (  ).     .        .

       "quit" ( ). ,            .

        ,     .  mtdbg    
,         ,      ,  ,  
 (  ).

    ,      load:
load <   > [<>]
:
load /sys/example
LOAD   /sys/aclock w200 h200
 LoaD  /hd0/1/menuetos/dosbox/dosbox
,         ,       .
 load       (    ).    ,      ;   ,       .   - "file not found",     .

          (,  ) -  ,      0x<hex__> <> (,    , ).             fasm'.
    load-symbols:
load-symbols <   >
 ,    load        ,   ,   .dbg (/sys/example.dbg     ),    ,    (  "Symbols loaded",   
).

  ,    .     :     (-  ),      ,      ,     ,     .   ,   ""           . mtdbg     (mxp, mxp_lzo, mxp_nrv, mtappack)         "" .   ( 'y'  <Enter>),    .     ,    - ,    "unpack" ( ).     ,
  ,            ! [   Kolibri 0.6.5.0,     ,          kpack'             .]

     "terminate" ( ).  "detach" ( )   ,      ,      .        .

       "reload" ( ).     ,    
 (  )   (    ),      :
terminate
load <last program name> <last program arguments>
     ,    (     mtdbg) (    ), ..    ,   load <last program name> <last program arguments>,   reload      ;  , load ,    ,     (. )   ,  reload   .

   "help",     "h".
    .
help      .
help          
.
help        .
:
help
help control
h LoaD

     ,   :
-  .          ("Running"/"Paused"),    "No program loaded".
-   -     ,  eip,     FPU/MMX.     :  hex-    : CF,PF,AF,ZF,SF,DF,OF:   ,    ,  ,  . ,    ,  .
-   ( ) -     
-   ( ) -       
-  
-   

     ,    ,    :
d <>
 d      .          u <>   u.
:
d esi -  ,    esi (,     rep movsb)
d esp -  
u eip -  ,   

  mtdbg  
-  
-      (8 32-, 8 16-  8 8-)   eip;  16-  8-  
    32 
-    +,-,*,/ (  )  
- [    ] ,   dbg-
     2^32.
 :
eax
eip+2
ecx-esi-1F
al+AH*bl
ax + 2* bH*(eip+a73)
3*esi*di/EAX

? <>    .

       r,     :
r <> <>
r <>=<>
(       ).         - 24     eip.


,  load     .        .
 F7 (   -  "s")      ,     ,       .   int 40h (   sysenter  syscall)     .
 F8 (   -  "p")      ,     ,   
 rep/repz/repnz   loop    .
   ,  ,    ,  , ,     / -   .
 g <>     ,     eip= ,      .  "g"      .

     "stop" ( ).

 ,    ,           .     , breakpoint(s),   - .     -   , ..    eip=< >.     :
bp <>
.       ,      "g"  .

    -      .         ( 
   x86,    4  ).
bpm <> -         
bpm w <> -       
bpmb/bpmw/bpmd <> -      ,       . bpm  bpmb - .   bpmw/bpmd         (..  )      (..   4).
bpmb,bpmw,bpmd w <> -     .

       "bl",          "bl <>".      "bc <>",      "bd <>",     ,   "be <>".

.

1.          int3 (    !).       ,     ,         (  "int3 command at xxx").      ,      g / bp.           ,          "g"  "bp",   "u","d","?"     /.
2.        16-  .
3.   ,      ,     ;       . ,  "d"     ,     .

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
