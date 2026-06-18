---
argos_import: project_file
source_path: tmp/kolibrios/programs/media/Beat/PlayNote/Readme-ru.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\media\Beat\PlayNote\Readme-ru.txt
source_ext: .txt
source_sha256: 07ca6e5eb286cdbb9d4cd67a710aacbf0f7a493cbccfae11ff669895e96ec3f4
text_sha256: 66d71d6c3e79ffb52bfa144b17890fa273134ba7186bb3712c5dc218453e50f3
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# Readme-ru.txt

- Source: `tmp/kolibrios/programs/media/Beat/PlayNote/Readme-ru.txt`
- Extract: `text`
- SHA256: `07ca6e5eb286cdbb9d4cd67a710aacbf0f7a493cbccfae11ff669895e96ec3f4`

## Content

PlayNote (дата выпуска 2020.05.17)

PlayNote - простая программа для проигрывания ноты. Звук проигрывается через звуковой драйвер.

Использование: PlayNote <path>
                path - путь к файлу, который будет проигран.

Примеры:
 PlayNote note.raw
 PlayNote /tmp0/1/note.raw

===========================
Для генерирования ноты в формате .wav при помощи sox (для прослушивания результата:
 sox -n -L -c 1 -b 16 -r 48000 Note_C6.wav synth 1 sine 1046.4
Для генерирования ноты в формате .raw при помощи sox (для программы PlayNote):
 sox -n -L -c 1 -b 16 -r 48000 Note_C6.raw synth 1 sine 1046.4

Для установки программы sox в Ubuntu:
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
