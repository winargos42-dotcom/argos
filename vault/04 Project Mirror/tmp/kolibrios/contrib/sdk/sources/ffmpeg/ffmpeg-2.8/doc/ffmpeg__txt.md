---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/ffmpeg/ffmpeg-2.8/doc/ffmpeg.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\ffmpeg\ffmpeg-2.8\doc\ffmpeg.txt
source_ext: .txt
source_sha256: 47f81843339fe13fcb60524c68ea0b202678530a4900b67cb2acf1e0ab662524
text_sha256: a5e5fd18eca4edf1efaab1ab9daf68d8de1fb1d36410862eb8fdf2d5764813b0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:29
---

# ffmpeg.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/ffmpeg/ffmpeg-2.8/doc/ffmpeg.txt`
- Extract: `text`
- SHA256: `47f81843339fe13fcb60524c68ea0b202678530a4900b67cb2acf1e0ab662524`

## Content

:
                                             ffmpeg.c                                                                                  :       libav*
                                             ========                                                                                  :       ======
                                                                                                                                       :
                                                                                                                                       :
                                                                                                       --------------------------------:---> AVStream...
                                                                    InputStream input_streams[]      /                                 :
                                                                                                    /                                  :
                    InputFile input_files[]                         +==========================+   /   ^                               :
                                                          ------> 0 |      : st ---:-----------:--/    :                               :
                 ^  +------+-----------+-----+          /           +--------------------------+       :                               :
                 :  |      :ist_index--:-----:---------/          1 |      : st    :           |       :                               :
                 :  +------+-----------+-----+                      +==========================+       :                               :
 nb_input_files  :  |      :ist_index--:-----:------------------> 2 |      : st    :           |       :                               :
                 :  +------+-----------+-----+                      +--------------------------+       :  nb_input_streams             :
                 :  |      :ist_index  :     |                    3 |            ...           |       :                               :
                 v  +------+-----------+-----+                      +--------------------------+       :                               :
                                                              --> 4 |                          |       :                               :
                                                             |      +--------------------------+       :                               :
                                                             |    5 |                          |       :                               :
                                                             |      +==========================+       v                               :
                                                             |                                                                         :
                                                             |                                                                         :
                                                             |                                                                         :
                                                             |                                                                         :
                                                              ---------                                --------------------------------:---> AVStream...
                                                                        \                            /                                 :
                                                                    OutputStream output_streams[]   /                                  :
                                                                          \                        /                                   :
                                                                    +======\======================/======+      ^                      :
                                                          ------> 0 |   : source_index  : st-:---        |      :                      :
                    OutputFile output_files[]           /           +------------------------------------+      :                      :
                                                       /          1 |   :               :    :           |      :                      :
                 ^  +------+------------+-----+       /             +------------------------------------+      :                      :
                 :  |      : ost_index -:-----:------/            2 |   :               :    :           |      :                      :
 nb_output_files :  +------+------------+-----+                     +====================================+      :                      :
                 :  |      : ost_index -:-----|-----------------> 3 |   :               :    :           |      :                      :
                 :  +------+------------+-----+                     +------------------------------------+      : nb_output_streams    :
                 :  |      :            :     |                   4 |                                    |      :                      :
                 :  +------+------------+-----+                     +------------------------------------+      :                      :
                 :  |      :            :     |                   5 |                                    |      :                      :
                 v  +------+------------+-----+                     +------------------------------------+      :                      :
                                                                  6 |                                    |      :                      :
                                                                    +------------------------------------+      :                      :
                                                                  7 |                                    |      :                      :
                                                                    +====================================+      v                      :
                                                                                                                                       :

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
