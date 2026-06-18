---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/ktcc/trunk/bin/doc/en/Features.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\ktcc\trunk\bin\doc\en\Features.txt
source_ext: .txt
source_sha256: 445f0aac9f3eb760c3eb02db93b71d64a9b96f8adb0639a6b4f55b65bd917ace
text_sha256: faba865c34da869b62b889bf5ad2f5408ebe80c7df98c0b3161c236654bc4c21
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:43
---

# Features.txt

- Source: `tmp/kolibrios/programs/develop/ktcc/trunk/bin/doc/en/Features.txt`
- Extract: `text`
- SHA256: `445f0aac9f3eb760c3eb02db93b71d64a9b96f8adb0639a6b4f55b65bd917ace`

## Content

+ Library autoload
  Now you don't need to think about having to load dependent libraries.
  The most of this work will be done by TCC and Dll.obj

+ Easy linking using *.def files
  All you need to do is connect the files describing the symbols
  of the used libraries. This files have plain text format and may 
  easy created in any text editor. If one or more libraries use the same
  symbols you may use name prefix to solve symbols conflicts 
  No more complicated of creating *.o and/or *.a files
  
+ Reduced image size
  Since the library loader no longer needs to be placed in every application,
  this reduces the size of the image. No more C layer neded, all dependent
  libraries loading and also initialized automatically.
  The compact format of the import table is also used.
  
+ Backward compatible
  You don't need change your project. But the features described above will
  require reconfiguration. Once you have tried it, you do not want to come back.

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
