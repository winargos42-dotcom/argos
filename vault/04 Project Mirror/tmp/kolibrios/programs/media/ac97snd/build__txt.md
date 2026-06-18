---
argos_import: project_file
source_path: tmp/kolibrios/programs/media/ac97snd/build.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\media\ac97snd\build.txt
source_ext: .txt
source_sha256: f9c1b477fe987b5d8e47409acde0ea0d9e1a693426727ddbc7d1dc8c04f4415e
text_sha256: bfcc94dd941c1c3479d153f4c9879358ce812c636746b1e083433eff5d14f6d2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# build.txt

- Source: `tmp/kolibrios/programs/media/ac97snd/build.txt`
- Extract: `text`
- SHA256: `f9c1b477fe987b5d8e47409acde0ea0d9e1a693426727ddbc7d1dc8c04f4415e`

## Content

Building AC97SND on windows.

1. Tools required:

- Microsoft Visual Studio (version 2005 or later)

- Flat assembler
Download and install fasm for windows from http://www.flatassembler.net
Add fasm directory to windows PATH variable.
(To check if this worked, open CMD and type fasm. Fasm's help messages should be visible now.)

- pe2kos.exe
Can be found in some subdirectories of SVN, official location unknown.
This file will need to be placed in the same directory as dependencies, to build the final KolibriOS executable

2. Collecting the dependencies:

- sound.lib
Source code can be found at \programs\develop\sdk\trunk\sound\src
Building this is beyond the scope of this document for now.
Alternatively, you can download latest compiled version from the autobuild server.
http://builds.kolibrios.org/eng/data/programs/develop/sdk/trunk/sound/src/sound.lib

- ufmod.obj
Source code is at \programs\develop\libraries\ufmod
Build using makeobj.bat
Or as above, download from:
http://builds.kolibrios.org/eng/data/programs/develop/libraries/ufmod/ufmod.obj

- mpg.obj
Open ac97snd solution in visual studio, select mpg project and click build -> build mpg


3. Building AC97SND binary

You will need to copy all previously mentioned dependencies into the folder that Visual Studio expects to find them.
This can be for example: \programs\media\ac97snd\release\
Alternatively, you can add another directory to 'Additional Library Directories' in Projects Linker options.
Now select AC97SND project, and click build -> build AC97SND


Good luck!

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
