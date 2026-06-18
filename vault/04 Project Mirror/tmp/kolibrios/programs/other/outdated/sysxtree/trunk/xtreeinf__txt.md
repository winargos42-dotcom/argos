---
argos_import: project_file
source_path: tmp/kolibrios/programs/other/outdated/sysxtree/trunk/xtreeinf.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\other\outdated\sysxtree\trunk\xtreeinf.txt
source_ext: .txt
source_sha256: 3eca1dad3aead01ab76213dc7233146fcb4157e78c41b6b19a76a55826705d7b
text_sha256: 7404238044d2066dea7b12a6b057b7bc0b68f3b1508dfa302e50921b8ccbaf78
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:47
---

# xtreeinf.txt

- Source: `tmp/kolibrios/programs/other/outdated/sysxtree/trunk/xtreeinf.txt`
- Extract: `text`
- SHA256: `3eca1dad3aead01ab76213dc7233146fcb4157e78c41b6b19a76a55826705d7b`

## Content

SYSTEM X-TREE

The new file browser with support sorting file by name, extension, size, date
Develop by Pavlushin Evgeni for Menuet OS e-mail: waptap@mail.ru
                                           site (slow update) : www.deck4.narod.ru 

~~~Manuals~~~

Copy program COPYR to ramdisk !!! for work feuters - copy and paste file's

~~~Keys~~~
PageUp\PageDown , Up Arrow/Down Arrow -Navigation
Blackspace - goto to previous folder
Enter - enter to folder or run/view/edit file
F2 - change sort mode (name,extension,size,date,sohw/fade del files)
F3 - view file in notepad
F5 - copy file to clipboard
F6 - paste file from clipboard
F12 - update source

SYSTEM X-TREE

       ,
,   .
    Menuet OS e-mail: waptap@mail.ru
                                     ( ) : www.deck4.narod.ru 

~~~~~~

  COPYR  ramdisk !!!      

~~~~~~
PageUp\PageDown , Up Arrow/Down Arrow - 
Blackspace -    
Enter -     // 
F2 -    ( ,,,, . )
F3 -     
F5 -    clipboard 
F6 -    clipboard'
F12 -   

Translate of russian documentation for xtree
Sorry i'm write in English very poor.

The new concept of dialogues, now dialogues
is made do not use file system for an exchange
with the client, and use IPC - Inter process comunication
(Support since 52 Versions).
52 Version support IPC of dialogues
53 Version is added protection dialogs from
external processes.
Test with TESTOPDG 54 Version IPC protection it is
improved Test with TESTOPD2 That testing dialogues
copy SYSTRE54 on ramdisk under name SYSXTREE and start TESTOPD2 

In window TESTOPD2 the following information is displayed:
In heading at the left???
Below parameters transferred SYSTEM XTREE,
namely PID TESTOPD2, the blank and
type of dialogue of one byte (O-Open, S-Save)
is even lower PID SYSTEM XTREE and current num of the
started processes After file will be open in dialogue,
it will be displayed in window TESTOPD2 below heading,
and dialogue will be closed. 

Protection TESTOPD2:
1) If at start SYSTEM XTREE from XTREE don't it is
received it PID during 2 sec, 54 version XTREE or 
not XTREE at all means on ramdisk not, TESTOPD2
comes to the end. 
2) If worked SYSTEM XTREE it was closed not
having sent path to file (itself or from CPU programs)
TESTOPD2 comes to the end since parameters from XTREE
have not been received and since XTREE is closed
that already and don't are received. 

;78Ver input in dir whith extension (for example TEST.DIR\XT\) bug deleted
;64Ver Run file from HD bug deleted.
;65Ver The bad scroll realization
;66Ver The good scroll realization, url line anti-flick
;67Ver Url line monolith procedure
;68Ver Mini icon on left of file name
;69Ver Getimg proc size minus 900 bytes
;70Ver Del data area ramsize minus 140000 bytes
;72Ver Quick sort, ramsize minus 200000 bytes
;73Ver Url flick and out bugs delete
;sort type in headmenu bug del

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
