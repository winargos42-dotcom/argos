---
argos_import: project_file
source_path: tmp/kolibrios/programs/demos/life2/compile.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\demos\life2\compile.txt
source_ext: .txt
source_sha256: dedee3918e002ca5aae61d73fea258f5af2a4c52c1d6fb27f5e4cf67dc110341
text_sha256: 40aafce003ce95c84bed064e68ce87bf61d0abb16cbc2747ff279f7d8a1ed1bc
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:42
---

# compile.txt

- Source: `tmp/kolibrios/programs/demos/life2/compile.txt`
- Extract: `text`
- SHA256: `dedee3918e002ca5aae61d73fea258f5af2a4c52c1d6fb27f5e4cf67dc110341`

## Content

Для компиляции необходим kos32-bcc (патч в папке kos32-bcc примененный к Borland C++), а также FASM.
life_bmp.bat создаёт необходимый для компиляции h-файл с картинками.
cpp2asm.bat компилирует С++-исходник в TASM-исходник,
	а потом превращает его в FASM-исходник.
После этого, возможно, понадобится перенести в f_life2.asm строки с equ из файла f_life2.asm в его начало.
Компиляция бинарника - как обычно, fasm f_life2.asm life2.

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
