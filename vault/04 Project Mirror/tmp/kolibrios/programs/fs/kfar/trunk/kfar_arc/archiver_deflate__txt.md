---
argos_import: project_file
source_path: tmp/kolibrios/programs/fs/kfar/trunk/kfar_arc/archiver_deflate.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\fs\kfar\trunk\kfar_arc\archiver_deflate.txt
source_ext: .txt
source_sha256: 9739cc4c28d29e0549e8af75bea12f7459133986f92e12af86455d0958ca4085
text_sha256: 29666c91dc0b4bde8e842d926e7e4bfa2b893713a2af04a578fcc4dfb937c43f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:45
---

# archiver_deflate.txt

- Source: `tmp/kolibrios/programs/fs/kfar/trunk/kfar_arc/archiver_deflate.txt`
- Extract: `text`
- SHA256: `9739cc4c28d29e0549e8af75bea12f7459133986f92e12af86455d0958ca4085`

## Content

archiver.obj      deflate-.
	  : deflateInit, deflateInit2, deflateReset, deflate,
	deflateEnd   deflate-,    
	  zlib.

: deflate_unpack
   : void* __stdcall deflate_unpack(const void* data, unsigned* pLength);
:
	data -    
	pLength -    :
		  *pLength      data,
		  *pLength    
 :
	   , NULL   
	   ,    
		 68.13
    :
;  esi =   , ecx =   
	push	ecx	;  *pLength   
	push	esp	;       pLength
	push	esi	;   
	call	[deflate_unpack]
	pop	ecx	;     *pLength
			;     deflate_unpack
;  eax =    , ecx =  

: deflate_unpack2
   : void* __stdcall deflate_unpack2(const void* get_next_chunk, void* parameter, unsigned* pUnpackedLength);
	void* __stdcall get_next_chunk(void* parameter, unsigned* pLength);
:
	get_next_chunk -   ,    
		   ;  
		,   NULL ( 
		        ,
		      NULL, 
		   )
	parameter - ,     
		     get_next_chunk
		( callback-    ,  
		   ,  )
	pUnpackedLength -   ,   
		  
 :
	   , NULL   
	   ,    
		 68.13
    :
	push	eax	;      *pUnpackedLength
			;   ,    
			;    push <>
	push	esp	;      pUnpackedLength
	push	esi	; - 
	push	deflate_callback
	call	[deflate_unpack2]
	pop	ecx	;  UnpackedLength
;     , eax =    , ecx = 

...

;        
deflate_callback:
;   ,     :
;	mov	esi, [esp+4]	; esi = 
;  - 
;   
	mov	ecx, [esp+8]	;  [ecx]   
	mov	[ecx], length
	mov	eax, buffer
	ret	8

   :
	1)   deflateInit  deflateInit2.
	2)        64 .
		    64        deflate.
		    deflate      16 .
		. .     16 ,        deflate.
		    64 ,          deflate.
		    64 ,          deflate.
	3)   deflateEnd   .
:
	      .
	 deflate      Z_NO_FLUSH.
	(       Z_FINISH)

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
