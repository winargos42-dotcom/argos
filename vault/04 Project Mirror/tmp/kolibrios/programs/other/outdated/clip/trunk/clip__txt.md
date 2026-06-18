---
argos_import: project_file
source_path: tmp/kolibrios/programs/other/outdated/clip/trunk/clip.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\other\outdated\clip\trunk\clip.txt
source_ext: .txt
source_sha256: f71b39e2e316f747f300707613ed28bcefb90153d4087992005396ac65c9db4b
text_sha256: 47b12b7e61f8c20f6618b55e815d5655c24016393c8172408ec4d0c2fd181547
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:47
---

# clip.txt

- Source: `tmp/kolibrios/programs/other/outdated/clip/trunk/clip.txt`
- Extract: `text`
- SHA256: `f71b39e2e316f747f300707613ed28bcefb90153d4087992005396ac65c9db4b`

## Content

⥬     . 
ଠ  ࠧࠡ稪.

⪮:  ॠ १ -  IPC-ᮮ饭.
 ஢ન 㦭  @clip()  
(cliptest   ⫠)  test2( ᪮쪮).

1.  @clip   .

 @clip ॠ  ,  ᮧ騩  (祬  ), 
 ⮫쪮 騩 IPC-ᮮ饭.  ন  16 (MAX_FORMAT) ஢ 
ࠧ ଠ⮢ ,   16,7  (MAX_SIZE)     
( ⢮ ᪨).
Id ଠ  - ᫮  0  65534 (祭 65535 १ࢨ஢).

 ᪥  蠥  㣨  @clip.

, । ,  ଠ:

[ Cmd: word | Format: word | Reserved: Dword | Data: ...]

 Cmd -  ,
Format - id ଠ ,
Reserved -  㣮 ( ᯮ),
 Data - ,     .

 ਭ ᫥騥 :

 1. Set Size.  室 ࠧ   ਥ .  ⮩
   室  ᢮   IPC-ᮮ饭
(ᯮᮡ 㬥   ⥪饩 ॠ樨 ).
ࠬ Data: 1 Dword, ᮤঠ騩 ࠧ   ।.
 : 12 .

 2. Set. । .  ⮩      .
ࠬ Data: ,  㦭 ᪮஢.
 : 8 + ( ) .

 3. Get Size.  ࠧ , ࠭    㪠 id
ଠ.  ⮩   ࠢ ⢥⭮ IPC-ᮮ饭  4
, ᮤঠ饥 ࠧ   . ᫨    ,
 ᮮ饭 㪠뢠 ࠧ 0.
 : 8 .

 4. Get.      㪠 id ଠ.  ⮩ 
 ࠢ ⢥⭮ IPC-ᮮ饭 㦭   묨  .
᫨    , ⢥⭮ ᮮ饭  ࠢ.
 : 8 .

 5. Delete.    㪠 id ଠ. ᫨ 㪠 
id ଠ = 0xFFFF,  饭  .
 : 8 .

室 䠩 - @clip.asm. ᫨ ᪮஢ 
;define DEBUG TRUE 
 ஢ ᫥,   筥   㪮  
⫠,     㤥 -    訡.
DEFAULT_SIZE - 砫 ࠧ IPC-
MAX_SIZE - ࠭祭  
MAX_FORMAT - ᫮ ࠧ ଠ⮢,     
६ ( ᫨ , ᣫ.   䨪).
DELAY - প  ⪠ ࠢ ᮮ饭, /100 ᥪ.
ATTEMPT - ⢮ ⮪ ࠢ ᮮ饭 ⮬   ⮢
. 
 

2. clip.inc -  㭪権   ᮪஢ 饭   @clip.
 ⥭     .

ਬ ᯮ짮 -  cliptest.asm (뢮   ⫠) 
test2.asm.

 ᯮ짮 clip.inc 室 㪠 ᫥騥 祭 (᫠,
⢥,   㣨):
DEFAULT_MASK = 7	; ᪠ ᮡ⨩ (. 㭪 40)  㬮砭  
			; ⥪饣 ⮪. 㦭, ⮡ ᫥ ਥ 
			; IPC-ᮮ饭 ( ᪠   01000000b)
			; ⠭   (    ).

SEND_DELAY = 10		; 㧠  ⪠  ࠢ ᮮ饭 

RECV_DELAY = 100	; ६  ⢥   (᫨   ६
			;  襫 ⢥,  訡)
			; ६ -   ᥪ㭤 (  㭪樨 5).

ATTEMPT = 5		; ⢮ ⮪ ࠢ ᮮ饭, ᫨  
			; 

᫥ 祭 clip.inc ⠭ 㯭묨 㭪樨:

clipboard_init() -   @clip.  㭪
 뢠 ⭮ (ਬ, ᫨   襫   
१饭),  1 ࠧ 맢 易⥫쭮 㦭.
頥 1  ᯥ  0  㤠 (  ).

clipboard_write(esi 㪠뢠    ଠ CLIP_BUFFER (. ),
ax (᫮) - id ଠ ) -     . 
믮  1  2. 頥 1  ᯥ  0  㤠 
(稭 뢠 ࠧ:        ..).

clipboard_read(esi 㪠뢠    ଠ CLIP_BUFFER (. ),
ax (᫮) - id ଠ ) - ⥭    . 믮
 3  4. 頥  eax 1  ᯥ, -1  墠⪥   
-ਥ(  ⮬ 砥  )  0   訡.
 edx( eax=1  -1) 頥 ⢨⥫ ࠧ   .

砭. ᫨ ਫ ᯮ 室騥 IPC  ⮫쪮  ࠡ  
஬ , ᫥ ࠡ뢠 ᮮ饭  @clip , .. 
   ⠪ : ᮮ饭  㣮 ਫ
   ⮣ ਫ  ᮮ饭   , 
 㤥 ந஢.

  ᯮ짮(᫥ 맮 clipboard_init) ᫥騥 㭪樨  
 ஢:
_ipc_send (esi 㪠뢠   , edx - ⢮ ).
ࠢ IPC-ᮮ饭 . ⫨稥  㭪樨 60/2  ⮬,  _ipc_send
 ᪮쪮 (筥, ATTEMPTS) ࠧ  ࠢ, ᫨  
 ( 2)  ९ ( 3),  㧮  SEND_DELAY/100 ᥪ㭤.
頥 1  ᯥ, 0  訡.

_ipc_recv(esi 㪠뢠    ଠ CLIP_BUFFER (. ),
edx = ᪠ ᮡ⨩ ⮪  㬮砭).
 ᮮ饭    祭 RECV_DELAY/100 ᥪ㭤.  ᯥ
१ ࠭  esi. 
頥 1  ᯥ, 0  訡.

ଠ   ࠡ  ஬ :
CLIP_BUFFER
(+0)	.size	dd	?	;    ᠭ ࠧ
				; ᮡ⢥  (N)
				;     , ᫨ 㦭
				; ࠢ 襥 ⢮ ,
				; ६   ⢮ 
				; (. ਬ test2)

(+4)	.sys1	dd	?	; \    ᯮ 㫥 clip.inc
				;  -  ७ 楫   
(+8)	.sys2	dd	?       ; /  ஢ ਫ

(+12)	.data	db	N dup(?); ᮡ⢥  

  ணࠬ஢  ⫠!

; barsuk, 21.08.2008




@CLIP - .  0.2.

  ⠢ ⥪  ਫ,  ন騥 ࠡ 
 @clip,   㭪樨 72.1. , - ᮡ⥩ ॠ樨, 
ਫ 室   edx, ᨬ  ० (ascii/scancode). 
 訫,  設⢮ ਫ,  ,  ० ascii,  ⮬ 
ࠫ    @clip (  ਫ,  ᯮ ० ᪠-, 
  ).
뫮       (   㧭 㦮 
० ).

⠢ ⢫ ⨥ 祩  ctrl-alt-v. 砫 㦭 
 ਫ, ࠡ饥  @clip (ਬ, test2),  ᪮஢ 
  id = 1 ( ⥪) - ⥪.

 :   eolite (    kfar) ஢   
⥪饣    䠩  ஬.   fasm  ᦠ⨥  
kpack ⠭ 㤮.

; 08.09.2008

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
