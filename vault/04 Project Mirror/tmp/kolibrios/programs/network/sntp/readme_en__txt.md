---
argos_import: project_file
source_path: tmp/kolibrios/programs/network/sntp/readme_en.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\network\sntp\readme_en.txt
source_ext: .txt
source_sha256: 0b3aa7a6f9d02865dfa00a1a13f11cd37f12b6386ce7960b8ea0aca1a28955a4
text_sha256: 0eb7ba186ce60cfdf6652046d3c8bb6ab5b0d3272a88cf2d9694446dccc55ff2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# readme_en.txt

- Source: `tmp/kolibrios/programs/network/sntp/readme_en.txt`
- Extract: `text`
- SHA256: `0b3aa7a6f9d02865dfa00a1a13f11cd37f12b6386ce7960b8ea0aca1a28955a4`

## Content

Command line:
sntp host [-tz [-[+\]\]hh[:ss\]\] [-s]|[-st]|[-ss\]\]
host  Name of SNTP server
-tz - set time zone, default is GMT +0:00

Synchronization, default is disabled 
-s  - system date and time
-st - system time (hours, minutes and seconds) only
-ss - preserve current hour (synchronize minutes and seconds only)

Eg:
sntp pool.ntp.org -tz 1 -s
sntp 88.147.254.227 -tz 1 -ss

History

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
