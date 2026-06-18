---
argos_import: project_file
source_path: tmp/kolibrios/programs/emulator/dgen-sdl-1.33/dz80/README.TXT
source_abs: F:\debug\argoss\tmp\kolibrios\programs\emulator\dgen-sdl-1.33\dz80\README.TXT
source_ext: .txt
source_sha256: 3ec51609abe11b01b571d8c98a9925d07088bf4c8c0e8b257d80f5fdfaedc145
text_sha256: 3ae7fd98ec1faf922e6e890f2ecf8e1b92f71066097d0f0297f5d719fd0de64a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:45
---

# README.TXT

- Source: `tmp/kolibrios/programs/emulator/dgen-sdl-1.33/dz80/README.TXT`
- Extract: `text`
- SHA256: `3ec51609abe11b01b571d8c98a9925d07088bf4c8c0e8b257d80f5fdfaedc145`

## Content

dZ80 Version 2.0 Source Code

                       Copyright 1996-2002 Mark Incley.

                           E-mail: dz80@inkland.org
                            http://www.inkland.org


Serious Bit
-----------

I have made this source code available so that it may be compiled on platforms
other than MS-DOS and Windows. You may compile it and distribute the resulting
executable only if no monies are charged for it.

      ** YOU ARE NOT ALLOWED TO DISTRIBUTE THIS SOFTWARE COMMERICIALLY **


Not So Serious Bit
------------------

If you make any feature modifications to the dZ80 source code, please let me
know, so that I can make them to my source too. I didn't intend for dZ80 to
grow into an all singing and dancin' disassembler, but, if features are added,
I would like to add them to my base version too.


Source Code Notes
-----------------

Please note that as of dZ80 2.0, you will also require the Lua 4.0
source code download from http://www.lua.org. It should be unzipped so that
the lua folder appears within the dZ80 folder as "Lua".


File            Purpose
----            -------
types.h         Sets up the typedefs
tables.c        Miscellaenous tables used by dZ80
dz80.c / h      The "front end" for the disassembler core
dissz80.c / h   The disassembler core
dissz80p.h      Private dZ80 header file - check out EXAMPLE.C
parsecmd.c/h    Command line parser for the front end.
loadfile.c      File loader and memory allocator

example.c       An example of how to drop dZ80 into your own programs to gain
		a disassembler.

makefile        A simple makefile for dZ80
dz80ns.mak      A simple makefile for dZ80 without scripting support
example.mak     Makefile for the example code

skip.c          A self-contained dZ80 opcode map file generator by
                Raffaele Sena


If you have any problems, just e-mail me at dz80@inkland.org

Cheers,

        Mark

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
