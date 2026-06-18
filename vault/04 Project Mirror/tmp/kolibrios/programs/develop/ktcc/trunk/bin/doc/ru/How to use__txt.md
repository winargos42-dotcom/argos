---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/ktcc/trunk/bin/doc/ru/How to use.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\ktcc\trunk\bin\doc\ru\How to use.txt
source_ext: .txt
source_sha256: 0295e7c85e1d1cbefd26fcfbf17ce2ce42855cfab7636ad06f3cdb227176a73d
text_sha256: 3efab629f93472e4870879a4ed923f4fafb32d2ba681752c1513ed345380cb92
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:43
---

# How to use.txt

- Source: `tmp/kolibrios/programs/develop/ktcc/trunk/bin/doc/ru/How to use.txt`
- Extract: `text`
- SHA256: `0295e7c85e1d1cbefd26fcfbf17ce2ce42855cfab7636ad06f3cdb227176a73d`

## Content

tcc    (.  tcc).  KX 
     (*.def)    ( *.o,
   ,  -  *.o,     
  ).
  
     .   /samples
   
  :
   -nobss  ,       ( 
  bss         ,  
            
    )
  
    /lib   *.def (  
  ), crt0.o (  )  *libtcc.a ( 
  tcc),      *.a.  , 
   tiny.o        ,
         .  
  
        
    KX    
     [++,      
  ].     ,
          . , 
     
  
    -llibc
  
  tcc     : libc.def, liblibc.def, liblibc.a
   ,         
    .   ,   
      KX     
     *.def

  

   KX     (*.def).  *.def
           
    .   *.def  .
  
    ;         
    ;
    ;        LIBRARY  
    ;   c  (  3   )
    LIBRARY libname.obj

    ;       EXPORTS 
    ;   prefix 
    EXPORTS [prefix]
    
    ;    prefix,      
    ;     ( )     
    ; .       
    ; ,   http.obj    http_
    ;   http_get       get 
    [libname_]entry1
    [libname_]entry2
    
    ;    
    
   
         :
  -     (   ).
         .
    
    __attribute__((dllimport)) void foo(int);
    
  -        ( , 
           )
  
    extern int (*foo)(const char*);
    
    : 
            
    extern  ,  tcc   ,   
           
     
    int (*foo)(const char*); => !!!
    
      __attribute__((dllimport))
        
  
    void foo(int); => !!!,  .  
 
   KX

   ,  tcc   KX:
    1.    
       tcc -v
         ,     KX  
       tcc version 0.9.26 (i386 KolibriOS/KX extension 0.4.6)
    
    2.        
          __KX__, 
       #ifdef __KX__
         //        KX
       #else
         // ,      KX 
       #endif
       
        ,       , 
          KX.     
        ,         
         .   
               
          .

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
