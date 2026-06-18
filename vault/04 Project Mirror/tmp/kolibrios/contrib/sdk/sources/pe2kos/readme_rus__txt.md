---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/pe2kos/readme_rus.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\pe2kos\readme_rus.txt
source_ext: .txt
source_sha256: 3503e2d1f22cfedd544513073ac0a61ad5604bfc38a3a2f8676416e3b2b0276b
text_sha256: 5d0c78f738ccdaf488759650bb656cefefcd45c36814b3d22e116f1c75304732
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:37
---

# readme_rus.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/pe2kos/readme_rus.txt`
- Extract: `text`
- SHA256: `3503e2d1f22cfedd544513073ac0a61ad5604bfc38a3a2f8676416e3b2b0276b`

## Content

Утилита pe2kos написана by Rabid Rabbit и немного подправлена мной,
diamond'ом. Она используется в проектах xonix и fara (автор - Rabid Rabbit),
написанных на Visual C++, на завершающем шаге после компиляции, когда
требуется по программе в формате Windows-exe получить настоящую
Kolibri-программу. Утилита всего лишь изменяет формат exe-шника, так что,
чтобы действительно получилась работающая программа, нужно выполнение
определённых условий. Понятно, что требуется, чтобы программа общалась
с внешним миром средствами КолибриОС (т.е. int 0x40) и не использовала
никаких Windows-библиотек. Помимо этого, требуется также, чтобы программа
размещалась по нулевому адресу (ключ линкера "/base:0"). Как писать такие
программы - смотрите в уже упомянутых проектах xonix и fara.
Есть две версии программы, для программ, использующих путь к исполняемому
файлу (последнее слово в MENUET01-заголовке), и остальных.
Выберите нужную версию.
Использование: (в командной строке) "pe2kos <файл-источник> <файл-приёмник>".
Например, "pe2kos xonix.exe xonix".

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
