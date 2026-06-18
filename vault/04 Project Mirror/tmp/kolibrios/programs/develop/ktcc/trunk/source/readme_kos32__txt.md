---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/ktcc/trunk/source/readme_kos32.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\ktcc\trunk\source\readme_kos32.txt
source_ext: .txt
source_sha256: f4e2cecf2b5e884b1390e6631f4b2f073c5c1c2e6af67568bf7b322ffb26ed56
text_sha256: 7c72cd0e89a67dc2343fce102e751d6a9a83f5c743edbb7a470e5c260534f590
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:43
---

# readme_kos32.txt

- Source: `tmp/kolibrios/programs/develop/ktcc/trunk/source/readme_kos32.txt`
- Extract: `text`
- SHA256: `f4e2cecf2b5e884b1390e6631f4b2f073c5c1c2e6af67568bf7b322ffb26ed56`

## Content

Siemargl port comments 

Used github branch https://github.com/TinyCC/tinycc
It have a vesion 0.9.26 with heads up to 0.9.27 - see ChangeLog

Kolibri version specifics
errata/changelog - moved to trunk/readme.txt

-added TCC_TARGET_MEOS as needed
-leading_underscore by default is 0 (can use -f[no-]leading-underscore), 
otherwise (error) underscoring all symbols, not only cdecl
-added message in tccmeos.c about missed symbols when linking KOS executable
-start.o added automatically, when -nostdlib not used
-to use standard ktcc lib must add -lck at commandline
-default search paths are ./include ./lib from executable (under KOS need to 
 use -Bpath_to_ktcc and put start.o in current dir)
-when config.h is ready, compiler can be easy builded as [kos32-]gcc tcc.c libtcc.c
 see also makefile.kos32
-impossible using with mingw-gcc compiled lib, incompatible library format:
 .o is PE-format from gcc but ELF from tcc, may be linux-gcc does it ok
-__fastcall incompatible with other compilers. now stack freed by caller. 
 must fix i386-gen.c@490,572 (fixed in other branch https://github.com/mirror/tinycc)


-using __attribute__((packed)) see test82. need naming struct twice as in kos32sys1.h
-using __attribute__ ((alias xxx)) restricted only for non "static inline" functions 
-erroneous or "non TCC" member using in nested structs or unions can lead to compiler internal error
-bench timing coarse (0s or 1s), no usec in newlib gettimeofday. OK

Tests status:
asmtest +
abitest not tested (embedding compiler)
libtcctest not tested (embedding compiler)
boundtest ----- alloca removed from tcc  libtcc.c:945 (really not worked)
tcctest most test ok, some problems with long double
vla_test.c +

pp/* +  (minor comment error in 13.s)

tests2/* : see below

// errata
skippin' tests
test76 fail dollars in identifiers
test34 fail (array assignment not supported)
test73 fail compile (no stdint.h), printfloat, ARM specific
test46 no stdin - removed funtionality read from console, but file ops works

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
