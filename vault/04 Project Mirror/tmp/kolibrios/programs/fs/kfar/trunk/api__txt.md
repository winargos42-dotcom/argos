---
argos_import: project_file
source_path: tmp/kolibrios/programs/fs/kfar/trunk/api.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\fs\kfar\trunk\api.txt
source_ext: .txt
source_sha256: fa9b4bfc5f5e93e4d8d0a5495fa5d92b4e5e84e82bf41cc40534bbd33a4db8d2
text_sha256: 0b78c18d532089c746d27e8b536bc8305c2590aae610775e8eaaa4dd19846048
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:45
---

# api.txt

- Source: `tmp/kolibrios/programs/fs/kfar/trunk/api.txt`
- Extract: `text`
- SHA256: `fa9b4bfc5f5e93e4d8d0a5495fa5d92b4e5e84e82bf41cc40534bbd33a4db8d2`

## Content

।⠢ ᮡ ⠭    ⥪ (ଠ COFF),
ᯮ ᫥騥 㭪樨  ६ ( 㭪樨  ⢮).
㭪樨  ࠧ  ॣ. kfar ࠭ 襭 䫠 ࠢ DF
 맮 ᯮ㥬 㭪権   ⮣   callback-㭪権.

int version;
 䥩 kfar,   ⠭ .    2.

int __stdcall plugin_load(kfar_info* info);
뢠  㧪 .
typedef struct
{
        int StructSize; // = sizeof(kfar_info)
        int kfar_ver;   // 10000h*major + minor
/*  callback-㭪樨 ࠭  ॣ,  ᪫祭 eax. */
/* 㭪樨 ࠡ  䠩: */
        void* open;     // HANDLE __stdcall open(const char* name, int mode);
                        // mode -  ⮢ 䫠
                        // O_READ = 1 -   ⥭
                        // O_WRITE = 2 -   
                        // O_CREATE = 4 - ᫨ 䠩  , ᮧ 
                        // O_TRUNCATE = 8 -  䠩  㫥 
        void* open2;    // HANDLE __stdcall open2(int plugin_id, HANDLE plugin_instance,
                        //                      const char* name, int mode);
                        // 筮 open,  뢠 䠩   
                        // open2(0,<anything>,name,mode) = open(name,mode)
        void* read;     // unsigned __stdcall read(HANDLE hFile, void* buf, unsigned size);
        void* write;    //   ॠ
        void* seek;     // void __stdcall seek(HANDLE hFile, int method, __int64 newpos);
        void* tell;     // __int64 __stdcall tell(HANDLE hFile);
        void* flush;    //   ॠ
        void* filesize; // __int64 __stdcall filesize(HANDLE hFile);
        void* close;    // void __stdcall close(HANDLE hFile);
/* 㭪樨 ࠡ   (࠭筮): */
        void* pgalloc;  // in: ecx=size, out: eax=pointer or NULL
                        //  墠⪥  ᮮ頥 짮⥫  頥 NULL
        void* pgrealloc; // in: edx=pointer, ecx=new size, out: eax=pointer or NULL
                        //  墠⪥  ᮮ頥 짮⥫  頥 NULL
        void* pgfree;   // in: ecx=pointer
        void* getfreemem;       // unsigned __stdcall getfreemem(void);
                                // 頥 ࠧ ᢮ ⨢   
        void* pgalloc2;         // void* __stdcall pgalloc2(unsigned size);
        void* pgrealloc2;       // void* __stdcall pgrealloc2(void* pointer, unsigned size);
        void* pgfree2;          // void __stdcall pgfree2(void* pointer);
/* 㭪樨 ࠡ  : */
        void* menu;     // int __stdcall menu(void* variants, const char* title, unsigned flags);
                        // variants 㪠뢠  ⥪騩   吝 ᯨ᪥
        void* menu_centered_in; // int __stdcall menu_centered_in(unsigned left, unsigned top,
                                // unsigned width, unsigned height,
                                // void* variants, const char* title, unsigned flags);
        void* DialogBox;        // int __stdcall DialogBox(DLGDATA* dlg);
        void* SayErr;           // int __stdcall SayErr(int num_strings, const char** strings,
                                //                      int num_buttons, const char** buttons);
        void* Message;          // int __stdcall Message(const char* title,
                                //                      int num_strings, const char** strings,
                                //                      int num_buttons, const char** buttons);
                                // may be x=-1 and/or y=-1
        struct {unsigned width;unsigned height;}* cur_console_size;
} kfar_info;
頥 祭:
0 = ᯥ譠 樠
1 = 訡 樠樨 (kfar 뤠 ᮮ饭 짮⥫)
2 = 訡 樠樨 (kfar த  ᮮ饭)

void __stdcall plugin_unload(void);
뢠  㧪  (  襭 ࠡ kfar).

HANDLE __stdcall OpenFilePlugin(HANDLE basefile,
        const void* attr, const void* data, int datasize,
        int baseplugin_id, HANDLE baseplugin_instance, const char* name);
뢠 , 㫨騩 䠩 ⥬   䠩 (ਬ, 娢).

basefile -  䠩 ( ஬ ਬ 㭪樨 read  seek  kfar_info)
attr - 㪠⥫    ਡ⠬ 䠩  ଠ ⥬ 㭪樨 70.1
data - , ᮤঠ騩   砫 䠩 ( ᯮ짮  । ⨯ 䠩)
datasize - ࠧ   data.  ⥪饩 ॠ樨 min(1024,ࠧ 䠩)
baseplugin_id - 䨪 ,   ண ᯮ 뢠 䠩;
                0  砥  
baseplugin_instance - ,   㭪樨 GetOpenPluginInfo ,
                ।塞  baseplugin_id
name -  䠩 ( ६ ) (  ⭮⥫쭮 baseplugin)

᫨  ࠡ뢠 । 䠩,      ⥫,
  쭥襬 㤥 ᯮ짮 kfar  饭  .  ⮬ 砥
  ᠬ⥫쭮  basefile 㭪樥 close  kfar_info (ਬ,
 ⨨ ⥫   ClosePlugin  ।⢥  OpenFilePlugin,
᫨ basefile  ᫥⢨  㦥).
᫨   ࠡ뢠 । 䠩,   0.
᫨  ࢠ 짮⥫,   祭 -1.

void __stdcall ClosePlugin(HANDLE hPlugin);
뢠 ᮧ  OpenFilePlugin ⥫.

void __stdcall GetOpenPluginInfo(HANDLE hPlugin, OpenPluginInfo* Info);
 ଠ  ⮬  .
typedef struct
{
        unsigned flags; //  0:   '..', ᫨  
                        //  1: ஢ ࠡ뢠 㭪樥 GetFiles
} OpenPluginInfo;

void __stdcall GetPanelTitle(HANDLE hPlugin, char title[1024],
        const char* host_file, const char* curdir);
   . ࠬ host_file ᮢ   䠩, ।
 OpenFilePlugin. ࠬ curdir ᮢ  ⥪饩 , ⠭  SetFolder.

int __stdcall ReadFolder(HANDLE hPlugin, unsigned dirinfo_start,
        unsigned dirinfo_size, void* dirdata);
⠥ ⥪ . hPlugin -   OpenFilePlugin ⥫.
dirinfo_start -   䠩 , dirinfo_size - ᪮쪮 䠩 .
頥 祭  頥  dirdata   ᮮ⢥⢮ 㭪樨 70.1.

bool __stdcall SetFolder(HANDLE hPlugin, const char* relative_path, const char* absolute_path);
⠭ ⥪ . relative_path - ⭮⥫  (".."   ),
absolute_path - ᮫  ( 㫨㥬  䠩 ⥬).

void __stdcall GetFiles(HANDLE hPlugin, int NumItems, void* items[], void* addfile, void* adddir);
        bool __stdcall addfile(const char* name, void* bdfe_info, HANDLE hFile);
        bool __stdcall adddir(const char* name, void* bdfe_info);
뢠  ஢, ᫨  䫠, 頥 GetOpenPluginInfo, ⠭  1.
 㭪 ४ ॠ뢠  砥, ᫨ ⠭ ४ᨢ 室 
㤮.
hPlugin - ⥫, ᮧ  OpenFilePlugin.
NumItems - ᫮ 㥬 ⮢.
items - ᨢ 㥬 ⮢,     㪠⥫   BDFE.
樠 砩 NumItems=-1, items=NULL 砥 " 䠩" ( ⥪饩   ).
addfile, adddir - callback-㭪樨 kfar'.  false 砥 "ࢠ ஢".
ࠬ name    ⭮⥫쭮 ⥪饩 . ࠬ bdfe_info -
㪠⥫  ᮪ (40 )   ଠ 㭪樨 70.5.
⨥  ⨥ ⥫ hFile   . 㭪 addfile 㤥
뢠 ⮫쪮 㭪 read.

int __stdcall getattr(HANDLE hPlugin, const char* filename, void* info);
 ଠ  䠩. 頥 祭    info  ᮮ⢥⢮
㭪樨 70.5.

HANDLE __stdcall open(HANDLE hPlugin, const char* filename, int mode);
 䠩 filename. ࠬ mode १ࢨ஢   ⥪饩 ᨨ kfar ᥣ ࠢ 1.

unsigned __stdcall read(HANDLE hFile, void* buf, unsigned size);
⥭ size    buf  䠩 hFile, ࠭ ⮣ १ open.
kfar ࠭,  size ⥭ 512 .
頥 祭: ᫮ ⠭ , -1  訡.

void __stdcall setpos(HANDLE hFile, __int64 pos);
⠭ ⥪   䠩 hFile, ࠭ ⮣ १ open,  pos.
࠭,  pos ⭮ 512 .

void __stdcall close(HANDLE hFile);

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
