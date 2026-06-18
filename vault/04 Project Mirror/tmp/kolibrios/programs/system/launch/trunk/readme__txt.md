---
argos_import: project_file
source_path: tmp/kolibrios/programs/system/launch/trunk/readme.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\system\launch\trunk\readme.txt
source_ext: .txt
source_sha256: e8ebf8ce9fe902e40c5560a0184b8637ab7ea91a2bac61ea15029ab0df45d45a
text_sha256: 5f2502d4099b65fbf1c8b6835d8ea5ca6a86719b197f45bf5e142ba76c25229e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:47
---

# readme.txt

- Source: `tmp/kolibrios/programs/system/launch/trunk/readme.txt`
- Extract: `text`
- SHA256: `e8ebf8ce9fe902e40c5560a0184b8637ab7ea91a2bac61ea15029ab0df45d45a`

## Content

==================== ᪨ ====================
: 0.1.80.1 (0.2 beta)
Launch - ணࠬ  ᪠ ਫ  ४਩ ᪠.
 ᪥ ⠥ 䠩 launch.cfg  /sys/etc, ⥬  ४ਨ ᪠.
᫥ ⮣ ᬮ ࠬ  ப. ਮ ࠬ஢ - 
浪 뢠.
 ࠬ஢  ப  ॠ ⮫쪮  ணࠬ  㬥, । .
 񭭮 ᯮ짮 Kobra  ᮢ (室騥  㯯 launch_reactive) ਫ 
 砥 ᯥ譮 ᪠ (뫠 ᮮ饭 dword 1 dword tid, tid - 䨪 饭 ).
ன:
main.path -   ४ ᪠
debug.debug - 樨 ⫠ (no -  ⫠  console - 뢮 १ ᮫)
debug.level - ஢ ⫠ (0 - ⮫쪮 ᮮ饭 㤠筮/㤠筮, 1 - 뢮 ᮮ饭   ४ਨ)
kobra.use - ᯮ짮 Kobra

:
 ࠡ 㦭 libconfig.

==================== English ====================
Version: 0.1.80.1 (0.2 beta)
Launch is a programme that launches applications from search dirictories.
On the start it reads file launch.cfg in /sys/etc and in current dirictory.
Than it reads command line arguments. Priority of arguments is as reading.
Now there are only few command line arguments: the name of application and its arguments.
If using Kobra is enabled all intrested (members of launch_reactive group) applications are notified if
application is launched (sending message dword 1 dword tid, tid - identifier of launched process).
Configuration:
main.path - path to search dirictories
debug.debug - debug options (no or console)
debug.level - debug level (0 - show only ok/error messages, 1 - show for each directory)
kobra.use - using of Kobra
ATTENTION:
you need libconfig to use launch.

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
