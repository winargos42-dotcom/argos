---
argos_import: project_file
source_path: tmp/kolibrios/data/common/drivers/acpi/readme.txt
source_abs: F:\debug\argoss\tmp\kolibrios\data\common\drivers\acpi\readme.txt
source_ext: .txt
source_sha256: cfe51ca22d965ae8bdfa1e5452ca7068ff9205c21e87447e3693bf291fed6de2
text_sha256: 0c0347834f00d6307137fa6f40cae9311f60e30635ce6c6724bd9a5ca908fa5c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:39
---

# readme.txt

- Source: `tmp/kolibrios/data/common/drivers/acpi/readme.txt`
- Extract: `text`
- SHA256: `cfe51ca22d965ae8bdfa1e5452ca7068ff9205c21e87447e3693bf291fed6de2`

## Content

================================ ENG ================================

Current driver installation is semi-manual. 
To turn on APIC you have to:

1) Run Installer (install.kex)
2) Wait 3 seconds and get sure that there is a message about succesfull
   file generation /sys/drivers/devices.dat
   Note: log can be found in /tmp0/1/acpi.log
3) Make kernel restart (MENU -> END -> HOME key)
4) Check that kernel and drivers are working well.
5) Save kolibri.img. Now each time you boot APIC would be turned on automatically.

================================ RUS ================================

      ,   .
  APIC :

1)   (install.kex)
2)  3   ,   
      /sys/drivers/devices.dat
       /tmp0/1/acpi.log
3)    ( ->   -> )
4)     
5)  .  APIC      .

 .

   ,       ,   ACPI     IOAPIC  Local APIC.     APIC_init       devices.dat.    ,   IOAPIC  Local APIC,      APIC     IRQ    PCI   devices.dat.

 https://board.kolibrios.org/viewtopic.php?f=1&t=1195&hilit=devices.dat&start=105#p37822

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
