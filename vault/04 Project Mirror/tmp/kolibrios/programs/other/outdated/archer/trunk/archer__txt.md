---
argos_import: project_file
source_path: tmp/kolibrios/programs/other/outdated/archer/trunk/archer.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\other\outdated\archer\trunk\archer.txt
source_ext: .txt
source_sha256: 46ba1909171e70c2b90f75684a992b2a0f047b4eea3061e503da38bf717e4b0d
text_sha256: 50eec6d163d8591a595e2b4ea5f486fa56e1eb8698d2aadac37f06f464e4fdf3
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:47
---

# archer.txt

- Source: `tmp/kolibrios/programs/other/outdated/archer/trunk/archer.txt`
- Extract: `text`
- SHA256: `46ba1909171e70c2b90f75684a992b2a0f047b4eea3061e503da38bf717e4b0d`

## Content

@RCHER FOR MENUET v1.0        July 14, 2005
 Written in pure assembler by Ivushkin Andrey aka Willow
 
Deflate unpacker

Vivat assembler et MENUETOS!
I tender thanks to everyone who spends his time in feasible effortsfor that 
little OS evolution. Now in my own rating the Mario79's distro named Kolibri4
takes 1th place. It is always pleasant to use modern software. Go on!

@RCHER is intended to view & unpack data compressed by Deflate method 
(including both static and dynamic Huffman). This method (although it isn't the
best already) is used by such file formats as ZIP (modern versions: PKZIP for
MS-DOS can create archives using other, less effective compression methods,
which @RCHER doesn't support), GZIP, JAR, OpenOffice files, SFX ZIP executables
and some others. I couldn't prevent myself to include support of PNG images
(they use the similar compression) and TAR and TAR+GZIP archives.

When the program is started, a little button carrying a @ symbol appears in the
left top corner of screen. Clicking this button opens a SYSXTREE dialog to 
select a file being unpacked. Doubleclick closes the application. @RCHER
outputs its information messages to Debug Board. If an archive contains more
than  one file, the 1st is by default unpacked into /HD/1/OUT.TXT (you may
change the DUMPFILE constant in @RCHER.ASM) and is opened  through TINYPAD
or - if it's a PNG image - in the built-in viewer.

These are unpacking flags that may exist in a commandline before an archive 
filename:

  s - do not close the program after unpacking;
  n - decompress the K-th archive file, where K is the following dword in 
      commandline;
  N - decompress the K-th archive file, where K is ASCII number from the 
      following 6 bytes of commandline;
  R - "raw" Deflate data, without descriptors and headers;
  q - begin file parsing from offset of K, where K is following dword in
      commandline;
  Q - begin file parsing from offset of K, where K is ASCII number from the
      following 6 bytes of commandline.

Commandline example:

cmd_string:
   db  'sN000037q'
   dd  1465
   db  '/hd/1/png.zip',0
  
It means to open the 34th (counting from 0) file of archive /hd/1/png.zip 
and do not terminate. Archive will be parsed starting at offset 1465.
 

To-Do list:

1. Support for interlaced PNG, alpha-channels, gamma-correction, background,
   Significant bits and a lot of cool parts of that format.
2. Output of archive content through IPC or into a built-in window like SYSTREE
   (as we are going to decide with the respected colleagues).
3. Searching of archive files by name and wildcards!
4. Unpacking into a file specified.
5. Means on saving memory space (now @RCHER gorges 8 Mb!): moving RAM areas,
   blocked file output. To do the last thing it is necessary to test carefully
   the reliability of harddisk I/O, directory creation and file deletion. These
   kernel capabilities aren't still documented.
6. Archive contents integration into SYSXTREE & MFAR filemanagers. We have to
   unify the calling format (like a structure in the sysfunc 58).
7. Add comments to source.
8. Correct bugs to be found

Special thanks to:

  Explanation of algorythm of Deflate format decoder with decoding samples
     (evm.narod.ru)
  RFC 1951 DEFLATE Compressed Data Format Specification version 1.3
  ZIP File Format Specification version 4.5 by PKWARE Inc.
  "An Explanation of the Deflate Algorithm" by Antaeus Feldspar
  RFC 1952 GZIP file format specification version 4.3
  TAR Format. Information from File Format List 2.0 by Max Maischein.
  RFC 1950 ZLIB Compressed Data Format Specification version 3.3
  PNG (Portable Network Graphics) Specification version 1.0 
  Michael Dipperstein's Huffman Code Page

I expect your remarks and suggestions on the @RCHER's topic, "Coding" section 
at meos.sysbin.com forum.

See you later!


****************************************
****************************************

@RCHER  MENUET v1.0       14  2005 .
 ᠭ  ⮬ ᥬ 誨 ॥ (Willow)

Deflate ᯠ騪

Vivat assembler et MenuetOS!
ࠦ ७ ୮ ᥬ ⥬,    ᢮ ६,
 ᨫ   ࠧ⨥ ⮩ 쪮 .    ᮡ⢥
३⨭ 1-   ਡ⨢ Mario79 Kolibri4. ᥣ ⭮
짮 ᮢ६ .  ঠ!

@RCHER ।祭  ᬮ  ᯠ , ᦠ   ⮤
Deflate ( ᪨  ᪨ 䬠).  ⮤ ( 
㦥  ⥭   襣)  ଠ 䠩 ZIP 
(ᮢ६ ᨨ: PKZIP  MS-DOS  ᮧ 娢  㣨, 
䥪⨢묨 ⮤ ᦠ,  @RCHER  ন), GZIP, JAR,
䠩 OpenOffice, SFX-ZIP ਫ   㣨.    㤥ঠ  
ᤥ প ࠦ  ଠ PNG (ᯮ த⢥ ⮤
ᦠ)  娢 TAR  TAR+GZIP.

 ᪥ ணࠬ   孥 㣫 ࠭  쪠 
 窮 @.  ⨨   뢠  롮 䠩 (SYSXTREE) 
ᯠ.  饫箪 뢠 ਫ. ଠ樮 ᮮ饭 
@RCHER 뢮   ⫠. ᫨ 娢 ᮤন ᪮쪮 䠩,  
㬮砭    ᯠ뢠  /HD/1/OUT.TXT (  
室 ⠭ DUMPFILE  @RCHER.ASM)  뢠  १ TINYPAD
 -  砥 ⨭ PNG -   ஥ ᬮ騪.

  ப ।  娢   ந쭮 浪 㪠뢠
䫠 ᯠ:

  s -  뢠 ணࠬ ᫥ ᯠ;
  n - ᯠ K- 䠩 娢,  K - ᫥騩 dword   ப;
  N - ᯠ K- 䠩 娢,  K - ASCII ᫮  ᫥ 6 
       ப;
  R - "" Deflate-,  ⥫  ;
  q - ᬮ 䠩   ᬥ饭 K,  K - ᫥騩 dword  
      ப;
  Q - ᬮ 䠩   ᬥ饭 K,  K - ASCII ᫮  ᫥ 6
        ப.

ਬ  ப:

cmd_string:
   db  'sN000037q'
   dd  1465
   db  '/hd/1/png.zip',0
   
 砥,  ᫥  34- (  0) 䠩 娢 /hd/1/png.zip 
   ࠡ. ᬮ 娢 筥  ᬥ饭 1465.
  

  㦭 ᤥ:

1. প  (interlaced) PNG,  ⠪ -, ,
   䮭, Significant bits   㣨 ਬ祪 ⮣ ଠ.
2. 뢮 ᮤন 娢 १ IPC   ஥   SYSTREE
   (  訬  㢠묨 ).
3.  䠩  娢     ᪥!
4. ᯠ  㪠 䠩.
5. ய    (ᥩ @RCHER  8 !): ६饭
   ⪮ ,  뢮  䠩.  ᫥ 室 ⥫쭮
   ஢  -뢮  , ᮧ ⠫  㤠
   䠩.      㬥஢.
6. ⥣ 娢 ⠫  䠩  SYSXTREE, MFAR. 
   ॡ 㭨஢ ଠ 맮 (   58 㭪樨).
7. ⪮஢ .
8. ࠢ , , ᮬ,  ;-)

ᮡ ୮:

  ᠭ ⬠  ଠ Deflate  ਬ ஢ 
     (evm.narod.ru)
  RFC 1951 DEFLATE Compressed Data Format Specification version 1.3
  ZIP File Format Specification version 4.5 by PKWARE Inc.
  "An Explanation of the Deflate Algorithm" by Antaeus Feldspar
  RFC 1952 GZIP file format specification version 4.3
  TAR Format. Information from File Format List 2.0 by Max Maischein.
  RFC 1950 ZLIB Compressed Data Format Specification version 3.3
  PNG (Portable Network Graphics) Specification version 1.0 
  Michael Dipperstein's Huffman Code Page

  砭  ।   ⪥ ࠧ "" 㬠 
meos.sysbin.com

  !

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
