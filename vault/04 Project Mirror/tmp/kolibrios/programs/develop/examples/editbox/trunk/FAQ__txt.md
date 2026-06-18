---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/examples/editbox/trunk/FAQ.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\examples\editbox\trunk\FAQ.txt
source_ext: .txt
source_sha256: 8d9665ba5e497e4e904c7e0049c90eb22517b4615facb6d0ea752eababfcc236
text_sha256: c728ed30d67e15800160a02923ecec655ceff5b6f2128ec4ffa30c1c32c2778b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:42
---

# FAQ.txt

- Source: `tmp/kolibrios/programs/develop/examples/editbox/trunk/FAQ.txt`
- Extract: `text`
- SHA256: `8d9665ba5e497e4e904c7e0049c90eb22517b4615facb6d0ea752eababfcc236`

## Content

EDITBOX   macroc.inc   ,     
 , struct.inc         
!! 


  
;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;       .
;;;;;;;;;;;;;;;;;;;;;;;;;;;
        use_edit_box,
       .
  :
   edit_box.draw -  ;
   edit_box.key -  ;
   edit_box.mouse -  ;
   edit_box.focus -  ;
   edit_box.blur -  ;
   edit_box.get_n -    .
          edi 
   .
   :
some_edit edit_box 100,10,30,0x00ffffff,0,0x00aaaaaa,0,255,some_edit_text
, , ,  ,  ,  ,
 ,   ,   ,
  ,    .  
 ,     255:
  some_edit_text:
       rb      256 ;255+1
    :
       mov     edi,some_edit
       call    edit_box.draw
     edit_box.key   
  ah,        
 2-  , :
       mov     eax,2
       int     0x40
       mov     edi,some_edit1
       call    edit_box.key
       mov     edi,some_edit2
       call    edit_box.key
       ,   
.
         edit box
 .
:::::::::::::::::::::::::
;;;,    
;;;;;;;;;;;;;;;;;;;;;;;;;
***********
use_edit_box
     editbox 
procinfo -     9  -  

      
        mcall   0,(50*65536+390),(30*65536+200),0xb3AABBCC,0x805080DD,hed
 0xb3AABBCC -   -        ,        
       
scr_h -      22 
scr_w -      5 
***********
mouse_edit_boxes 
  ,       
 
editboxes -     
editboxes_end -    

    
mouse_edit_box -      
 
editboxes -     
     .
**********
key_edit_boxes -    ,          
 
editboxes -     
editboxes_end -    

    
key_edit_box -      
 
editboxes -     
     .
**********
draw_edit_boxes -        
 
editboxes -     
editboxes_end -    


    
draw_edit_box -      
 
editboxes -     
     .
**********
default_box -         ..    
  KFM :))       yes or no  .      -      
         KFM






Q:
  : 
1)       ,        ,      ,    . 
2)   ,       . ,    ,        .

A:
1)    ,  : 
edit2 edit_box 250,5,30,0xffffff,0,0,0,308,hed,ed_focus,53 -    editbox 
,  : 
    
struc edit_box width,left,top,color,focus_border_color,blur_border_color,text_color,max,text,flags,size 
{ 
.width dd width 
.left dd left 
.top dd top 
.color dd color 
.focus_border_color dd focus_border_color 
.blur_border_color dd blur_border_color 
.text_color dd text_color 
.max dd max 
.text dd text 
.flags dd flags+0 
.size dd size+0 
.pos dd 0 -     
.offset dd 0 
.cl_curs_x dd 0 
.cl_curs_y dd 0 
.shift dd 0 
.shift_old dd 0 
} 
250 -   editbox width 
5 -     left 
30 -    top 
0xffffff -   editbox 
0x6a9480 -       shift
0 - focus_border_color   editbox,    ..  editbox 
0 - blur_border_color   editbox,     ..   editbox 
0 - text_color   editbox. 
308 - max  - ,    (   ,    ,        2,   !!      2    !) 
hed - tex     
ed_focus - (0       Editbox' - flags 
53 -    size.   ,       .     ,  ,   ,     ,  0, ,     ,      . 
53 -   - ,          ,      , ..   :)))
<DATA> -    , + . 
hed db 'EDITBOX optimization and retype <Lrz> date 09.03.2007',0 ;  54  
rb 256 ; 256+54 =310     308 - 2     (    ,   -     ) 

2)      .     editbox,     , 
.width dd width 
.left dd left 
.top dd top 
  . 

;>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
;DATA  
editboxes:
edit1 edit_box 168,5,10,0xffffff,0x6a9480,0,0,0,99,ed_buffer.2,ed_figure_only
edit2 edit_box 250,5,30,0xffffff,0x6a9480,0,0xAABBCC,0,308,hed,ed_focus,53,53
edit3 edit_box 35,5,50,0xffffff,0x6a9480,0,0,0,9,ed_buffer.3,ed_figure_only
edit4 edit_box 16,5,70,0xffffff,0x6a9480,0,0,0,1,ed_buffer.4,ed_figure_only
editboxes_end:


    
  
lea eax, editboxes -      . 
    
mov dword [eax],   width 
mov dword [eax+4],   left 
mov dword [eax+8],   top 

    editbox 
  
add eax,ed_struc_size 
;        editbox 
  
mov dword [eax],   width 
mov dword [eax+4],   left 
mov dword [eax+8],   top 
    editbox 

   ))). 
,

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
