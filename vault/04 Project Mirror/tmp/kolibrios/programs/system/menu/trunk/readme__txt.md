---
argos_import: project_file
source_path: tmp/kolibrios/programs/system/menu/trunk/readme.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\system\menu\trunk\readme.txt
source_ext: .txt
source_sha256: 001e62a2811e231619788f8e1a19469d11a72c48edff86aa9db055f0f91d8781
text_sha256: c1c7ef16e667a3db0440d5a6f54271e7677f2f069f7895add5727097f3267260
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:47
---

# readme.txt

- Source: `tmp/kolibrios/programs/system/menu/trunk/readme.txt`
- Extract: `text`
- SHA256: `001e62a2811e231619788f8e1a19469d11a72c48edff86aa9db055f0f91d8781`

## Content

English text is below
  .
:     MENUET   0.76
   (    )

   :
1..   ,   
   MENU.DAT. 
 :
-/    .   
        . 
       ,   -
.    ,    
  .
-    ,    .
-    58- ,   -
    .
2.,     ,  
   .  ,  
       .    -
  MENU, SELECT1, SELECT2  .. - MENU
     .
3.          
4.,       (  
  ).
5. .  , , Enter  Esc.
 ,     .

    MENU.DAT:
  MENU.DAT-  2
 #0- .
 -  10 -  #0  #9
       ,    
,  /@5
  ##  (! TINYPAD   )
       20   
   ENTER, ..    -
  0x0d,0x0a

  ,    ,  -  
.   MENU.DAT    . TINYPAD
  .    !
     MENU. ( )
        .
        lisovin@26.ru
     mutny@rambler.ru
 ,
 

11.07.06 - Mario79,    70.

NEW MAIN MENU
Requirements: MENUET 0.76, color monitor
WHAT'S NEW?
1.Self-configuring menu. All the configurational data is in MENU.DAT
You may add/remove menu positions, translate menu to any language,
run menu applications from HDD without source code change.
2.Multi-thread application. There're two files only: MENU and MENU.DAT
instead of MENU, SELECT1, SELECT2, SELECT3 etc.
3.Self-closing when running application or clicking out of menu.
4.Button highlight
5.Keyboard support (keys Up, Dn, Enter, Esc.)
So, it's just like Windows menu ;)
NOTES ON MENU.DAT:
Size of MENU.DAT should be not more than 2K
Number of menus-not more than 10 (from #0 to #9). #0 is always main menu
## is an end file marker - always required.
First 20 positions of any string reserved for button text
Any string contains file path or link to submenu, for example /@4.
You may edit MENU.DAT by any text editor, but be careful when using
TINYPAD (sometimes it cuts end marker).
It is recommended to compile MMENU.ASM as MENU. So, you can run it from
standard panel.
All the comments and bugreports send to lisovin@26.ru
Michail Lisovin.  

11.07.06 - Mario79, application used function 70.

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
