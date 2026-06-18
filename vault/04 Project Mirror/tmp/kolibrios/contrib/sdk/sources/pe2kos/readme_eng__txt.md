---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/pe2kos/readme_eng.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\pe2kos\readme_eng.txt
source_ext: .txt
source_sha256: 1f0f4ebdb8f18d0f40b7fd2b4c187d6f595e59ce2fad867a58d99eb1cde109c4
text_sha256: 87586e83746c0137dbb2f122becf9eaf4d8830c656347df942bfb7132000742d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:37
---

# readme_eng.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/pe2kos/readme_eng.txt`
- Extract: `text`
- SHA256: `1f0f4ebdb8f18d0f40b7fd2b4c187d6f595e59ce2fad867a58d99eb1cde109c4`

## Content

The tool pe2kos is written by Rabid Rabbit and slightly rectified by me,
diamond. It is used in projects xonix and fara (the author is Rabid Rabbit),
written in Visual C++, at last step after a compilation, when it is needed
to get from a program in the Windows-exe format a true Kolibri-program.
The tool only converts the format of executable, so to get working program
one must satisfy to certain conditions. Of course, a program must
communicate with the outer world by Kolibri facilities (i.e. int 0x40)
and must not use any Windows-libraries. In addition program is required
to be placed on zero address (linker option "/base:0"). How to write
such programs - look to already mentioned projects xonix and fara.
There is two versions of the tool: for programs which use path to executable
file (last dword in MENUET01-header), and others.
Select wanted version.
Usage: (in command line) "pe2kos <source file> <destination file>".
For example, "pe2kos xonix.exe xonix".

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
