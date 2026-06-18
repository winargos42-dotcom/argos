---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/tinypy/tp_kolibri.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\tinypy\tp_kolibri.txt
source_ext: .txt
source_sha256: ba9a2662dbd5dfa19b72bd0124af6f88eabffc814ef686063609cdb309453cab
text_sha256: e8ff4a53408f5b9040d95046528f9ab43ca2d2f69a3897ffe044bd09e95783f7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:45
---

# tp_kolibri.txt

- Source: `tmp/kolibrios/programs/develop/tinypy/tp_kolibri.txt`
- Extract: `text`
- SHA256: `ba9a2662dbd5dfa19b72bd0124af6f88eabffc814ef686063609cdb309453cab`

## Content

TinyPy  ⪨   樨  ࠡ  ਎.

1.  ⠪ TinyPy  祬     ஢

 TinyPy -  Python- 몠, ᮧ 
 (Phil Hassey), ⫨騩 祭 訬 ࠧࠬ: 롮஬ 権
樨   ࠧ஢ ᯮ塞   । 64 .

  ࠧࠡ⪥ ਫ    㣨 樮 ⥬
㯥 쭮 ப 롮 -஢.  । ࠧࠡ⪨ 
ᠬ    ६  ࠭祭 FASM.  ।, 
 ᮧ ணࠬ  ᠬ ⥬  ⠪ 砥 
࠭񭭮 몥,  Python, 蠥 ਢ⥫쭮 ⥬ 
짮⥫, 񪮣  ணࠬ஢  ᥬ.

TinyPy  񣮪  ஢: ⥫쭠   ᠭ  ᠬ
Python,  ⠫쭠  -  C, 室 ⥪    200 .
 樨 㦭 ⮫쪮 ⠭⭠ ⥪ libc.   ᯮ
ᥣ   ⪮ 㭪権 (vsnprintf/vsprintf, malloc/memcpy/memmove/free,
fopen/fread/fwrite/fclose).

  ⮣ ࠡ  ஢ TinyPy 﫠  ᫥ ⥩:
 1. ᠭ Makefile  ᡮન ஬ GCC  ᯮ짮
 menuetlibc.
 2.   menuetlibc  㭪権 vsnprintf/vsprintf.
 3. 祭 ⥪   ࠡ  ᮫.
 4.  筮, ⫮ ࠧࠧ   (   ⮣!).

2.  TinyPy.

2.1.  .

 ꥪ  । TinyPy ।⠢ 16-⮢ ன tp_obj.
 4   ⨯,  祭 ᫥ 12    .
㯭 ᫥騥 ⨯: TP_NONE, TP_NUMBER, TP_STRING, TP_DICT, TP_LIST, 
TP_FNC, TP_DATA.

 TP_NONE - ᮮ⢥ ⢥ ꥪ None.    ᪠
 祣.

 TP_NUMBER - ᫮, ࠭  float. ᫨ ᫮ ⫨砥  襣
 楫 , 祬  10^(-6),  ⠥ 楫,    뢮
  楫.   ⮬ ⨯ ⭮ ᪨ True  False.
 ন 䬥᪨ 樨 +,-,*,/,%, ⮢ <<  >>, ᪨
 |, &.

 ਬ:
 print(2+2*2, 7/3, (-7)%3, 1==True, 0==False)

 뢮:
 6 2.333333 -1 1 1

 ⨬ ࠧ,  print  㭪樥 (  Python 3),   ࠬ
 易⥫쭮 㪠뢠  ᪮.

 TP_STRING - ப. ন: ஢ઠ 宦 ("str1" in "str2"), १ s[:b], s[a:b],
 s[a:], 㭪樨 len, index, join, split, find, strip, replace.

 TP_DICT - ᫮,   樠⨢ ᨢ. ন 
     ⮢ 㣮 ᫮. ॡ  ᥬ 砬 
 㤠 ⮢   ন.  ⠪  㤮 ᯮᮡ
 ।⠢ ꥪ⮢,  ⭮, ᫨ d ᫮,   d.key 
 d['key'] ࠢ.  ⮬ TinyPy   JavaScript.

 TP_LIST - ᯨ᮪. ন: ॡ  ⠬ (for el in list),
 㭪樨 len, append/appendx, extend, insert/insertx, pop, find, index, sort.
 ন 㭪 range. reverse()   ন.

 TP_FNC - 㭪. 뢠 2 ⨯ - 筠 㭪  ⮤, ⫨
 浪 맮.

 TP_DATA - ७  TinyPy.

2.  TinyPy  ࠢ  "訬" Python

"what tinypy won't be:
- a full implementation of Python;
- totally compatible with Python"
        "roadmap.txt", tinypy sources

 ⠪ 몠 TinyPy 祭 宦  Python,   ⢥
  Python  ন:

 -   ᮯணࠬ;
 - ᨭ⠪᪨ ""   ᯨ᪮  ᫮३, 
 odd_squares = [a*a for a in range(100) if a%2];
 - ࠪ⨢ ᮫.

  筮,  墠⠥ ᭮ ᨫ Python -  ⠭⭮ ⥪.

3. ७ TinyPy.

  ஥ 㭪権  TinyPy 筮 ,    
 㫥 筮 . ᬮਬ ᮧ 㫥  ᠬ TinyPy, 
 C   FASM.

 3.1. 㫨  TinyPy.

 TinyPy ন 쭮 ணࠬ஢, ᮧ 㫥
 ਭ樯쭮 祬  ⫨砥  Python. ,    
 ணࠬ   䠩:

 math.py:
 def square(a):
     return a*a

 prog.py:
import math

if __name__=="__main__":
    math.square(12)

 砫 㦭 ᪮஢  math.py  -   ணࠬ
 py2bc.py,  ࠡ⠥   Python, ⠪   TinyPy. ᪠ shell  믮塞 
 # tinypy py2bc.py math.py math.tpc
 
 ᫥ ⮣   prog.py  TinyPy.
 
 # tinypy prog.py
 144
 
 砭: ᨭ⠪ "from module import function"   ন.

 3.2 㫨  C.

 ਬ ᮧ 㫥  C  ᬮ  ⠫ modules/kolibri. 
 㫨 ᪨   ᠬ ஬ , ᮮ⢥⢥,
 㢥稢  ࠧ.  ᭨  室  TinyPy
    ꥪ ,  䠩 室 ⥪⮢  
  ४⨢ #include. ⥫ 㫨  ஢  
 ⤥ ꥪ 䠩,  ⮬ 砥 㦭    Makefile, 
 筮 ⠪   ४⨢ include.

  㫥  ⢮ 㭪 樠樨 筮  뢠
 <modname>_init.  뢠  tpmain ࠧ ᫥ 樠樨 㠫쭮
 設, ᮧ ᫮  ᯮ㥬 ꥪ⮢     ।। ᫮ modules.

 ⮡ । TinyPy-㭪, 㦭 ᮧ  㭪  C 

tp_obj myfunc(tp_vm *tp);

 3.3 㫨  FASM.

  FASM  筮,  ᥣ   ⤥
ꥪ 䠩. ਬ  ᬮ  ⠫ fasm_modules. 
kolibri_dbg ᯮ  㭪 debug_print, 뢮 ப  
⫠.

 4.   kolibri.

 த ᫥.

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
