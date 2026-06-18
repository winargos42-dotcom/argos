---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/libraries/sorter/sort.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\libraries\sorter\sort.txt
source_ext: .txt
source_sha256: d290e3f6dba53142902e0b489216f83341738c0970513461af12202bb5731ce5
text_sha256: c033bfe7a0cb3c6a4257e76115d3cb2145b1128f54aab9fc59f9c430a62c33cf
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:44
---

# sort.txt

- Source: `tmp/kolibrios/programs/develop/libraries/sorter/sort.txt`
- Extract: `text`
- SHA256: `d290e3f6dba53142902e0b489216f83341738c0970513461af12202bb5731ce5`

## Content

START   DLL_ENTRY = 1.
       SortDir  
 ,        
(   304     70),   
  : 0=,2=,4=  ,6=,
10= ,12=  ,1,3,5,7,11,13 - 
     .
,      ,   
 70   dirdata,   :
	push	2	;  
	push	dword [dirdata+4]	;  
				;   push ebx, 
				;     int 0x40
	push	dirdata+32	;  
	call	[SortDir]
;    dirdata

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
