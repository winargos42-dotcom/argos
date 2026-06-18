---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/libraries/console/console_ru.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\libraries\console\console_ru.txt
source_ext: .txt
source_sha256: 36cee5a1a458593ff28c14a93c1c2f03640dd2585a027abfe8c6108cc8f30631
text_sha256: 66481e855e58f30b2421b3bf78900405730d56ea5b5ef9177830631ee05f23b5
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:43
---

# console_ru.txt

- Source: `tmp/kolibrios/programs/develop/libraries/console/console_ru.txt`
- Extract: `text`
- SHA256: `36cee5a1a458593ff28c14a93c1c2f03640dd2585a027abfe8c6108cc8f30631`

## Content

console.dll   :

typedef unsigned long dword; /* 32-   */
typedef unsigned short word; /* 16-   */

void __stdcall con_init(dword wnd_width, dword wnd_height,
	dword scr_width, dword scr_height, const char* title);
 .      .
wnd_width, wnd_height -    ( )    
	;
scr_width, scr_height -    ( )  ;
   4      -1 (=0xFFFFFFFF)
	-    ;
title -   .

void __stdcall con_exit(bool bCloseWindow);
   .  ()  bCloseWindow
,         ,  
  ,       " [Finished]".

void __stdcall con_set_title(const char* title);
    .

void __stdcall con_write_asciiz(const char* string);
 ASCIIZ-     ,   .

void __stdcall con_write_string(const char* string, dword length);
 con_write_asciiz,    length .

int __cdecl con_printf(const char* format, ...)
 printf  ANSI C.

dword __stdcall con_get_flags(void);
   .
dword __stdcall con_set_flags(dword new_flags);
   .   .
 ( ):
/*   */
#define CON_COLOR_BLUE		1
#define CON_COLOR_GREEN		2
#define CON_COLOR_RED		4
#define CON_COLOR_BRIGHT	8
/*   */
#define CON_BGR_BLUE		0x10
#define CON_BGR_GREEN		0x20
#define CON_BGR_RED		0x40
#define CON_BGR_BRIGHT		0x80
/*   */
#define CON_IGNORE_SPECIALS	0x100
/*   ,    :
	10 ('\n') -     
	13 ('\r') -     
	8 ('\b') -  (  )
	9 ('\t') - 
	27 ('\033'='\x1B') -  Esc-;
     . */
/*  Esc-:
	Esc[<number1>;<number2>;<number3>m -   :
		  ,       ;
		0 =   (    )
		1 =  
		5 =  
		7 =   (    )
		30 =  
		31 =  
		32 =  
		33 =  
		34 =  
		35 =  
		36 =  
		37 =  
		40 =  
		41 =  
		42 =  
		43 =  
		44 =  
		45 =  
		46 =  
		47 =  
	     5 :
	Esc[2J -  ,      
	Esc[<number1>;<number2>H = Esc[<number1>;<number2>f -
		      <number1>,<number2>
	Esc[<number>A -    <number>  
	Esc[<number>B -    <number>  
	Esc[<number>C -    <number>  
	Esc[<number>D -    <number>  
*/
/*     ;    6 ;
	   con_set_flags */
#define CON_WINDOW_CLOSED 0x200
     = 7.

int __stdcall con_get_font_height(void);
   .

int __stdcall con_get_cursor_height(void);
   .
int __stdcall con_set_cursor_height(int new_height);
   .   .
      ( 0  font_height-1)
.
  0    .
    - 15%   .

int __stdcall con_getch(void);
    .
    ASCII-.   
(, Fx  )     0,
      ( DOS- ).
   7 ,     
 0.

word __stdcall con_getch2(void);
    .    ASCII- 
(0   ),  -  
( BIOS- ).
   7 ,     
 0.

int __stdcall con_kbhit(void);
 1,  -   , 0 .  
    con_getch  con_getch2.
   6 ,       1.

char* __stdcall con_gets(char* str, int n);
   .     
 ,     n-1  (   , 
 ).         
str.     .
   6 ,     
     NULL,     .  
6    .

typedef int (__stdcall * con_gets2_callback)(int keycode, char** pstr, int* pn, int* ppos);
char* __stdcall con_gets2(con_gets2_callback callback, char* str, int n);
    4 .
  con_gets   ,   
  ,   callback-
( , ,  up/down     tab 
).        -  ,
       .    
      (,   
 ), ,    -     .
 : 0=  ; 1= , 
    ; 2= ,   ;
3=   .
   6 ,     
     NULL,     .  
6    .

void __stdcall con_cls();
    5 .
        .

void __stdcall con_get_cursor_pos(int* px, int* py);
    5 .
  *px      x,  *py -   y.

void __stdcall con_set_cursor_pos(int x, int y);
    5 .
      .  - 
      ( 0  scr_width-1
 x,  0  scr_height-1  y, scr_width  scr_height   
 con_init),      .

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
