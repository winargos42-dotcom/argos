---
argos_import: project_file
source_path: tmp/kolibrios/programs/network/ftpc/README.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\network\ftpc\README.txt
source_ext: .txt
source_sha256: c864ecf0eb0962f00b7f095b6cf772bd9916d527d1efcf21c7ef982612a8b23e
text_sha256: 5ee4a4699736338dfd57d6d6704142f84f547fd0bd49089482a9193b52f43eb0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# README.txt

- Source: `tmp/kolibrios/programs/network/ftpc/README.txt`
- Extract: `text`
- SHA256: `c864ecf0eb0962f00b7f095b6cf772bd9916d527d1efcf21c7ef982612a8b23e`

## Content

Usage instructions -

1) By default log file is created in /usbhd0/1. If the folder is uavailable,
the program will throw an error. Configure the folder from ftpc.ini

2) Browse the local and remote folders using UP/DOWN arrow keys and press ENTER
to download/upload the file. Scrolling might not work due to lack of support
from the boxlib library

3) It might be difficult to read log file contents using certain text editors.
gedit works fine


Known issues -

1) Uploading large files may not work. I do not know whether this is an FTPC
issue or a network-stack realted issue

2) FTPC may freeze on rare occasions. Simply close and restart it

3) Download may fail abruptly if disk becomes full. Unfortunately, as of now,
there is no support for checking available disk space beforehand from kernel
itself

4) Text in console and log file is not properly formatted


Future improvements -

1) Display more informative error messages (especially in GUI)

2) Allow resizing of GUI window and align GUI elements automatically

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
