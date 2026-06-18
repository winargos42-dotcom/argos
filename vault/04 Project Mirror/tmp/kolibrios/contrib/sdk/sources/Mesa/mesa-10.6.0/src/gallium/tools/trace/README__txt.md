---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-10.6.0/src/gallium/tools/trace/README.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-10.6.0\src\gallium\tools\trace\README.txt
source_ext: .txt
source_sha256: 89d2b52ddf45965f4035dd3616b6e56c3857c45eb861d5f69504e23c198b8d27
text_sha256: 4280addb940d43ea8c44eb4772ceda01253affb37890a376478e191c674bd608
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:33
---

# README.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-10.6.0/src/gallium/tools/trace/README.txt`
- Extract: `text`
- SHA256: `89d2b52ddf45965f4035dd3616b6e56c3857c45eb861d5f69504e23c198b8d27`

## Content

These directory contains tools for manipulating traces produced by the trace
pipe driver.


Most debug builds of state trackers already load the trace driver by default.
To produce a trace do

  export GALLIUM_TRACE=foo.gtrace

and run the application.  You can choose any name, but the .gtrace is
recommended to avoid confusion with the .trace produced by apitrace.


You can dump a trace by doing

  ./dump.py foo.gtrace | less


You can dump a JSON file describing the static state at any given draw call
(e.g., 12345) by
doing

  ./dump_state.py -v -c 12345 foo.gtrace > foo.json

or by specifying the n-th (e.g, 1st) draw call by doing

  ./dump_state.py -v -d 1 foo.gtrace > foo.json

The state is derived from the call sequence in the trace file, so no dynamic
(eg. rendered textures) is included.


You can compare two JSON files by doing

  ./diff_state.py foo.json boo.json | less

If you're investigating a regression in a state tracker, you can obtain a good
and bad trace, dump respective state in JSON, and then compare the states to
identify the problem.

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
