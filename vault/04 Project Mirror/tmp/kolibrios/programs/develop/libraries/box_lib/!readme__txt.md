---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/libraries/box_lib/!readme.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\libraries\box_lib\!readme.txt
source_ext: .txt
source_sha256: 6a1fb506607082c551c29e6d13204513bf5ab7c62eef8696e6f2d4e7022836ad
text_sha256: 501b50654fcfb12526e4704dd5bc02a3405981ab7aef28113e41899af083b8fb
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:43
---

# !readme.txt

- Source: `tmp/kolibrios/programs/develop/libraries/box_lib/!readme.txt`
- Extract: `text`
- SHA256: `6a1fb506607082c551c29e6d13204513bf5ab7c62eef8696e6f2d4e7022836ad`

## Content

/
 6  2009.

Copyright (c) 2009, <Lrz>
All rights reserved.

        Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the <organization> nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY Alexey Teplov aka <Lrz> ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE MPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE  DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*****************************************************************************:

 ,     .        .     ,       ,    ,            .:

               ,   ()  .      , ..     .  load_lib.mac        .    ,          ,     ,  ,         .     2- .   ,        (   +  ). 
 :

         load_lib.mac   5  .
       , ,   .     2-       B.   :

A:
sys_load_library
load_library
B:
sys_load_libraries
load_libraries

                  :
library_name, cur_dir_path, library_path, system_path, err_message_found_lib, head_f_l, myimport, err_message_import, head_f_i .         :

sys_load_library library_name, cur_dir_path, library_path, system_path, err_message_found_lib, head_f_l, myimport, err_message_import, head_f_i

 

load_library library_name, cur_dir_path, library_path, system_path, err_message_found_lib, head_f_l, myimport, err_message_import, head_f_i

                   .
sys_load_library -        system_path, ..      system_path     . 

    .
system_path      db '/sys/lib/'
library_name     db 'box_lib.obj',0     ;      

   ,     
system_path      db '/sys/lib/box_lib.obj',0
...      .
library_name     db 'box_lib.obj',0 


 load_library -      , ..      .

library_name -        
library_name     db 'box_lib.obj',0

,      ,     ,     . , :


      ff2,  ,        ,    :

 ,       ,      .
system_path      db '/sys/lib/tread_lib.obj',0
;...      .
library_name     db 'ff2/tread_lib.obj',0
-    ,       .

cur_dir_path -       , :

use32                   ; ,  32  
    org 0x0             ;   ,  0x0
    db 'MENUET01'       ;    (8 )
    dd 0x1              ;     
    dd start            ; ,     
                        ;     
    dd i_end            ;  
    dd mem              ;   ,    0100      4 
    dd mem              ;      ,    .     ,  
    dd 0x0              ;     .
    dd cur_dir_path     ;   ,   ,       .
    DATA  

cur_dir_path    rb 4096 ;  4096    ,       . ..  ,       .

library_path -  ,            . 
library_path    rb 4096

system_path -      . , ,      .
    .
system_path      db '/sys/lib/'
library_name     db 'box_lib.obj',0     ;      

   ,     
system_path      db '/sys/lib/box_lib.obj',0
...      .
library_name     db 'box_lib.obj',0 

err_message_found_lib - ,     ,     .

err_message_found_lib   db 'Sorry I cannot load library box_lib.obj',0

head_f_l -   ,    -   .
head_f_l        db 'System error',0

myimport -       .
myimport:   

edit_box_draw   dd      aEdit_box_draw
edit_box_key    dd      aEdit_box_key
edit_box_mouse  dd      aEdit_box_mouse
version_ed      dd      aVersion_ed

check_box_draw  dd      aCheck_box_draw
check_box_mouse dd      aCheck_box_mouse
version_ch      dd      aVersion_ch

option_box_draw  dd      aOption_box_draw
option_box_mouse dd      aOption_box_mouse
version_op       dd      aVersion_op

                dd      0
                dd      0

aEdit_box_draw  db 'edit_box',0
aEdit_box_key   db 'edit_box_key',0
aEdit_box_mouse db 'edit_box_mouse',0
aVersion_ed     db 'version_ed',0

aCheck_box_draw  db 'check_box_draw',0
aCheck_box_mouse db 'check_box_mouse',0
aVersion_ch      db 'version_ch',0

aOption_box_draw  db 'option_box_draw',0
aOption_box_mouse db 'option_box_mouse',0
aVersion_op       db 'version_op',0

err_message_import - ,     ,      .

err_message_import      db 'Error on load import library box_lib.obj',0

head_f_i -  ,    -   .
head_f_i        db 'System error',0

         ,         ,        ,  .   ax  0     ,  -1,        .       .
        cmp     eax,-1
        jz      exit

  B

            ,   B   ()     .  ,       . ,      ,   2   :
  
   .

B:
sys_load_libraries
load_libraries

           B       :
      load_libraries l_libs_start,end_l_libs,  

l_libs_start:
library01  l_libs boxlib_name, path, file_name, system_dir, \
er_message_found_lib, ihead_f_l, myimport, er_message_import, ihead_f_i

library02  l_libs plugin_BMP_name, path, file_name, system_dir1,\
er_message_found_lib2, ihead_f_l, myimport, er_message_import2, ihead_f_i
end_l_libs:

  
library01  l_libs boxlib_name, path, file_name, system_dir, \
er_message_found_lib, ihead_f_l, myimport, er_message_import, ihead_f_i
  :

.library_name   dd library_name
.cur_dir_path   dd cur_dir_path
.library_path   dd library_path
.system_path    dd system_path
.err_message_found_lib   dd err_message_found_lib
.head_f_l       dd head_f_l
.my_import      dd my_import
.err_message_import      dd err_message_import
.head_f_i       dd head_f_i
;        .
.adr_load_lib   dd 0x0          ;    
.status_lib     dd 0x0          ;status of load library -      0 - , 01 -   , 02 -   .

   ,   ,   :

;      
        mov     ebp,library01 -  
        cmp     dword [ebp+ll_struc_size-4],0 ;     
        jnz     exit ;  0,  .


;   
        mov     ebp,library01 -  
        cmp     dword [ebp+ll_struc_size-4],0 ;     
        jnz     exit ;  0,  .
        mov     ebp, dword [ebp+ll_struc_size-8] -  ebp  .

 @use_library

    ,         B.      .             @use_library_mem.


 @use_library_mem mem_alloc,mem_free,mem_realloc,dll_load

    @use_library,            'lib_init'  4 .            ,        .


      /   ? 

     :

use32                ; ,  32  
    org 0x0                ;   ,  0x0
    db 'MENUET01'        ;    (8 )
    dd 0x1                ;     
    dd start                ; ,     
                        ;     
    dd i_end                ;  
    dd mem                  ;   ,    0100      4 
    dd mem                  ;      ,    .     ,  
    dd 0x0              ;     .
    dd cur_dir_path
include 'macros.inc'
include 'box_lib.mac'
include 'load_lib.mac'
        @use_library    ;use load lib macros
start:
;universal load library/librarys
sys_load_library  library_name, cur_dir_path, library_path, system_path, \
err_message_found_lib, head_f_l, myimport, err_message_import, head_f_i
;if return code =-1 then exit, else nornary work
        cmp     eax,-1
        jz      exit
        mcall   40,0x27         ;    
red_win:
    call draw_window            ;   
align 4
still:                          ; 
        mcall   10              ; 
        dec  eax
        jz   red_win
        dec  eax
        jz   key
        dec  eax
        jz   button

        push    dword edit1
        call    [edit_box_mouse]

        push    dword edit2
        call    [edit_box_mouse]

        push    dword check1
        call    [check_box_mouse]

        push    dword check2
        call    [check_box_mouse]

        push    dword Option_boxs
        call    [option_box_mouse]

        push    dword Option_boxs2
        call    [option_box_mouse]

        jmp still    ;       
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
button:
        mcall   17      ;   
        test ah,ah      ;  ah 0,      still
        jz  still
exit:   mcall   -1
key:
        mcall   2       ;  2   eax     

        push    dword edit1
        call    [edit_box_key]

        push    dword edit2
        call    [edit_box_key]

        jmp still

;>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
align 4
draw_window:            ;  
        mcall   12,1
        mcall   0,(50*65536+390),(30*65536+200),0x33AABBCC,0x805080DD,hed

        push    dword edit1
        call    [edit_box_draw]

        push    dword edit2
        call    [edit_box_draw]

        push    dword check1
        call    [check_box_draw]

        push    dword check2
        call    [check_box_draw]

        push    dword Option_boxs
        call    [option_box_draw]        

        push    dword Option_boxs2
        call    [option_box_draw]

        mcall   12,2
    ret
;>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
;DATA 
;    .
system_path      db '/sys/lib/'
library_name     db 'box_lib.obj',0
;    ,     
;system_path      db '/sys/lib/box_lib.obj',0
;...      .
;library_name     db 'box_lib.obj',0
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

err_message_found_lib   db 'Sorry I cannot load library box_lib.obj',0
head_f_i:
head_f_l        db 'System error',0
err_message_import      db 'Error on load import library box_lib.obj',0

myimport:   

edit_box_draw   dd      aEdit_box_draw
edit_box_key    dd      aEdit_box_key
edit_box_mouse  dd      aEdit_box_mouse
version_ed      dd      aVersion_ed

check_box_draw  dd      aCheck_box_draw
check_box_mouse dd      aCheck_box_mouse
version_ch      dd      aVersion_ch

option_box_draw  dd      aOption_box_draw
option_box_mouse dd      aOption_box_mouse
version_op       dd      aVersion_op

                dd      0
                dd      0

aEdit_box_draw  db 'edit_box',0
aEdit_box_key   db 'edit_box_key',0
aEdit_box_mouse db 'edit_box_mouse',0
aVersion_ed     db 'version_ed',0

aCheck_box_draw  db 'check_box_draw',0
aCheck_box_mouse db 'check_box_mouse',0
aVersion_ch      db 'version_ch',0

aOption_box_draw  db 'option_box_draw',0
aOption_box_mouse db 'option_box_mouse',0
aVersion_op       db 'version_op',0




check1 check_box 10,45,6,12,0x80AABBCC,0,0,check_text,14,ch_flag_en
check2 check_box 10,60,6,12,0x80AABBCC,0,0,check_text2,15

edit1 edit_box 350,3,5,0xffffff,0x6f9480,0,0xAABBCC,0,308,hed,ed_focus,hed_end-hed-1,hed_end-hed-1
edit2 edit_box 350,3,25,0xffffff,0x6a9480,0,0,0,99,ed_buffer,ed_figure_only

op1 option_box option_group1,10,90,6,12,0xffffff,0,0,op_text.1,op_text.e1-op_text.1
op2 option_box option_group1,10,105,6,12,0xFFFFFF,0,0,op_text.2,op_text.e2-op_text.2
op3 option_box option_group1,10,120,6,12,0xffffff,0,0,op_text.3,op_text.e3-op_text.3
op11 option_box option_group2,120,90,6,12,0xffffff,0,0,op_text.1,op_text.e1-op_text.1
op12 option_box option_group2,120,105,6,12,0xffffff,0,0,op_text.2,op_text.e2-op_text.2
op13 option_box option_group2,120,120,6,12,0xffffff,0,0,op_text.3,op_text.e3-op_text.3

option_group1   dd op1  ;,    ,   
option_group2   dd op12 ;
Option_boxs     dd  op1,op2,op3,0
Option_boxs2    dd  op11,op12,op13,0
hed db   'BOXs load from lib <Lrz> date 27.04.2009',0
hed_end:
rb  256
check_text db 'First checkbox'
check_text2 db 'Second checkbox'
op_text:                ;     
.1 db 'Option_Box #1' 
.e1:
.2 db 'Option_Box #2'
.e2:
.3 db 'Option_Box #3'
.e3:
ed_buffer       rb 100
;-----------------------
;sc      system_colors
p_info  process_information
cur_dir_path    rb 4096
library_path    rb 4096
i_end:
rb 1024
mem:

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
