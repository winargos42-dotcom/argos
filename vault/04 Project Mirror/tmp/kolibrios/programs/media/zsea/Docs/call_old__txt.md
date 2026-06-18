---
argos_import: project_file
source_path: tmp/kolibrios/programs/media/zsea/Docs/call_old.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\media\zsea\Docs\call_old.txt
source_ext: .txt
source_sha256: 10ba21255d4072237e0c11d91efa38111f2ff67fc8166e4a0638b3f02c2608c2
text_sha256: 6bd6cd02573c0732e0aeb6458e40481d044894b65f600c147ca3498b30d69571
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# call_old.txt

- Source: `tmp/kolibrios/programs/media/zsea/Docs/call_old.txt`
- Extract: `text`
- SHA256: `10ba21255d4072237e0c11d91efa38111f2ff67fc8166e4a0638b3f02c2608c2`

## Content

The block is passed to the plugin:
;---------------------------------------------------------------------
; not change this section!!!
; start section
;---------------------------------------------------------------------
align 4
image_file     dd 0 ;+0
raw_pointer    dd 0 ;+4
return_code    dd 0 ;+8
img_size       dd 0 ;+12
deflate_unpack dd 0 ;+16
raw_pointer_2  dd 0 ;+20
;---------------------------------------------------------------------
; end section
;---------------------------------------------------------------------


Calling plugins:



;---------------------------------------------------------------------
convert:
    xor  eax,eax
	cmp  [error_fs],eax
	jnz   .error
    mov  [return_code],eax
	mov eax,image_file
    call  [plugin]
    cmp   [return_code],dword 0
    je   @f
    cmp   [return_code],dword 2
    je   @f
;-------------------------------    
    xor  eax,eax
    mov  [return_code],eax
	mov eax,image_file
    call  [plugin_1]
    cmp   [return_code],dword 0
    je   @f
    cmp   [return_code],dword 2
    je   @f
;-------------------------------
    xor  eax,eax
    mov  [return_code],eax
	mov eax,image_file
    call  [plugin_2]
    cmp   [return_code],dword 0
    je   @f
    cmp   [return_code],dword 2
    je   @f
;-------------------------------
    xor  eax,eax
    mov  [return_code],eax
	mov eax,image_file
    call  [plugin_3] 
;-------------------------------
@@:
    mov   ecx,[image_file]
    mcall 68, 13,

    cmp   [return_code],dword 0
    je   .all_ok
    xor  eax,eax
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
