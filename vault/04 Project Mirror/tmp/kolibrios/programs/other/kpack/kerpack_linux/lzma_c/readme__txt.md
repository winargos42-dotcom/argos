---
argos_import: project_file
source_path: tmp/kolibrios/programs/other/kpack/kerpack_linux/lzma_c/readme.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\other\kpack\kerpack_linux\lzma_c\readme.txt
source_ext: .txt
source_sha256: 342dcb44940ccd947c8ea13117770e33c9b966c27644e3ead3acf9868f8157fd
text_sha256: 8337e14da0b1b61d2f1b7fe88e71d9862b830e8bae07e0401c9dc73f6c82400d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:47
---

# readme.txt

- Source: `tmp/kolibrios/programs/other/kpack/kerpack_linux/lzma_c/readme.txt`
- Extract: `text`
- SHA256: `342dcb44940ccd947c8ea13117770e33c9b966c27644e3ead3acf9868f8157fd`

## Content

C , diamond', 
LZMA-.  LZMA SDK 4.32  copyright (c) 1999-2005
Igor Pavlov,      http://www.7-zip.org/sdk.html,
,  ,     C++,C#  Java   
,  LZMA-  ANSI-C,   7z.

       ,  
bt4 match-finder,     (,  
  ),     
 . (     LZMA
SDK.)       ,   
 VC++,       ANSI C  
 VC-  #pragma intrinsic(memcpy), ,
 memcpy      -     
     C run-time library. (  , 
     MtApPack,  
RTL        Windows,   Kolibri.)

 ,    LZMA SDK,     
       (  ) GNU LGPL 
GNU CPL. ( SDK    
        
 ,      .)

  :  C++-   :
extern "C" __stdcall void lzma_set_dict_size(unsigned logdictsize);
extern "C" __stdcall unsigned lzma_compress(
	const void* source,
	void* destination,
	unsigned length,
	void* workmem);

         ,
    2  
(.. dictsize == (1<<logdictsize)).     256Mb,
   logdictsize    28.   
   ,       ,
..    12345       16384  
 1  .
      . source -  
 , destination -      ,
length -   , workmem -    ,
 ;      0x509000+dictsize*19/2
.        0x10 + length*9/8 .

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
