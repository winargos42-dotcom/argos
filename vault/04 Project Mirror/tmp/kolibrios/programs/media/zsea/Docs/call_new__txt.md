---
argos_import: project_file
source_path: tmp/kolibrios/programs/media/zsea/Docs/call_new.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\media\zsea\Docs\call_new.txt
source_ext: .txt
source_sha256: 8a09509211892b72bc7ad1a8754f4547b63ba10225c80eeba0503f64069f4d25
text_sha256: fe849b32ff57601e80f95fec0e60570a3740e7733a6d45c18abc44b1456e7001
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# call_new.txt

- Source: `tmp/kolibrios/programs/media/zsea/Docs/call_new.txt`
- Extract: `text`
- SHA256: `8a09509211892b72bc7ad1a8754f4547b63ba10225c80eeba0503f64069f4d25`

## Content

The block is passed to the plugin:
;---------------------------------------------------------------------
; not change this section!!!
; start section
;---------------------------------------------------------------------
align	4
image_file		dd 0	;+0
raw_pointer		dd 0	;+4
return_code		dd 0	;+8
img_size		dd 0	;+12
deflate_unpack	dd 0	;+16
raw_pointer_2	dd 0	;+20
;---------------------------------------------------------------------
; end section
;---------------------------------------------------------------------


Calling plugins:

;---------------------------------------------------------------------
convert:
	xor	eax,eax
	cmp	[error_fs],eax
	jnz	.error
	mov	[return_code],eax
;	mov	eax,image_file
	push	image_file
	call	[plugin]
	cmp	[return_code],dword 0
	je	@f
	cmp	[return_code],dword 2
	je	@f
;-------------------------------	
	xor	eax,eax
	mov	[return_code],eax
;	mov	eax,image_file
	push	image_file
	call	[plugin_1]
	cmp	[return_code],dword 0
	je	@f
	cmp	[return_code],dword 2
	je	@f
;-------------------------------
	xor	eax,eax
	mov	[return_code],eax
;	mov	eax,image_file
	push	image_file
	call	[plugin_2]
	cmp	[return_code],dword 0
	je	@f
	cmp	[return_code],dword 2
	je	@f
;-------------------------------
	xor	eax,eax
	mov	[return_code],eax
;	mov	eax,image_file
	push	image_file
	call	[plugin_3]	
;-------------------------------
@@:
	mov	ecx,[image_file]
	mcall	68,13

	cmp	[return_code],dword 0
	je	.all_ok
	xor	eax,eax
;-------------------------------

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
