---
argos_import: project_file
source_path: tmp/kolibrios/data/common/drivers/i915/readme.txt
source_abs: F:\debug\argoss\tmp\kolibrios\data\common\drivers\i915\readme.txt
source_ext: .txt
source_sha256: ee608e48ee454558956718ffc4e0ba57fed4b239f73d709ab2fd83d56089a375
text_sha256: 799cbd12169b6fd6bd7daf80a7d39ce4b2a02dfea8f3d9586d45b105f3d0fa36
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:39
---

# readme.txt

- Source: `tmp/kolibrios/data/common/drivers/i915/readme.txt`
- Extract: `text`
- SHA256: `ee608e48ee454558956718ffc4e0ba57fed4b239f73d709ab2fd83d56089a375`

## Content

PCI Express  Intel  i915  Skylake.

    :  i915    i915.dll.
       .

 : <>/i915 < >

  :
 -l
 --log 	<   ->
    	    ,   .
    	  /rd/1/drivers/i915.log 
 --fbc 	<-1,0,1>   .   
	     . 
 --rc6 	<-1,0-7>     C-state 6
 -m
 --m <WxHxHz>      .

 -v
 --video <CONNECTOR>:<xres>x<yres>[M][R][-<bpp>][@<refresh>][i][m][eDd]
	    CONNECTOR

   autorun.dat      . 

:
/SYS/DRIVERS/I915 -l/hd0/2/i915.log 1    # 

   .

 --list-connectors    
 --list-connector-modes <CONNECTOR>
	     
	 CONNECTOR 
:
   
i915 --list-connectors

   
i915 --list-connector-modes HDMI-A-1

  1600x900 60Hz   HDMI-A-1
i915 -v HDMI-A-1:1600x900

  1280x1024 75Hz   VGA-1
i915 -v VGA-1:1280x1024@75

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
