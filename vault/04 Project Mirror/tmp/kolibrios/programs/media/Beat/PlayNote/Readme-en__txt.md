---
argos_import: project_file
source_path: tmp/kolibrios/programs/media/Beat/PlayNote/Readme-en.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\media\Beat\PlayNote\Readme-en.txt
source_ext: .txt
source_sha256: dc56f5a2db9dcd7b9e08cba4b88425f88877283e3b88923e6ef0a85ebe5a55cd
text_sha256: c8ec612b4973192caa1aa0fd149ed4a4fa654be513aea8dfed545162bb104698
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# Readme-en.txt

- Source: `tmp/kolibrios/programs/media/Beat/PlayNote/Readme-en.txt`
- Extract: `text`
- SHA256: `dc56f5a2db9dcd7b9e08cba4b88425f88877283e3b88923e6ef0a85ebe5a55cd`

## Content

PlayNote (release date 2020.05.17)

PlayNote is a program to play a note. Sound plays through a sound driver.

Usage: PlayNote <path>
 path - path to a file to be played.

Examples:
 PlayNote note.raw
 PlayNote /tmp0/1/note.raw

===========================
To generate a note in a .wav format with a sox (to listening):
 sox -n -L -c 1 -b 16 -r 48000 Note_C6.wav synth 1 sine 1046.4
To generate a note in a .raw format with a sox (to PlayNote):
 sox -n -L -c 1 -b 16 -r 48000 Note_C6.raw synth 1 sine 1046.4

To install a sox in Ubuntu:
 sudo apt install sox
===========================

//--------------------------------------//
  The program: 
   - Compiled with KTCC compiler.
   - Written in KolibriOS NB svn7768.
   - Designed and written by JohnXenox
     aka Aleksandr Igorevich.
//--------------------------------------//

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
