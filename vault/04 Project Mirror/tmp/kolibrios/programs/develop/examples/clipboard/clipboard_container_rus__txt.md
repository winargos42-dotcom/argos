---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/examples/clipboard/clipboard_container_rus.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\examples\clipboard\clipboard_container_rus.txt
source_ext: .txt
source_sha256: f74f8aa9e58fb6a47ebed5a8157a2b70a9b218f01b900962d276ba547186463f
text_sha256: e3c537b8d3ec4af83a16d914f6804490669f4f4c664d66c40c3b67be0e477713
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:42
---

# clipboard_container_rus.txt

- Source: `tmp/kolibrios/programs/develop/examples/clipboard/clipboard_container_rus.txt`
- Extract: `text`
- SHA256: `f74f8aa9e58fb6a47ebed5a8157a2b70a9b218f01b900962d276ba547186463f`

## Content

Содержимое контейнера буфера обмена

1. Первый dword содержит общую длину данных в контейнере

2. Второй dword указывает тип данныx:
   0 = Текст
   1 = Текст с блочным выделением
   2 = Изображение
   3 = RAW
   4 и выше зарезервировано

2.1 Текст
    Данные в третьем dword содержат тип:
    0 = UTF
    1 = 0866    
    2 = 1251
    3 и выше зарезервировано

2.2 Текст с блочным выделением
    Отличается от п.2.1 только тем, что все строки имеют одинаковую длинну.

2.3 Изображение
    Третий dword - размер по X
    Четвертый dword - размер по Y
    Пятый dword - глубина цвета в битах (8, 16, 24, 32, 48, 64)
    Шестой dword - Указатель на палитру (смещение от начала файла).
                   Если палитры нет то значение 0
    Седьмой dword - Размер области палитры, максимальное значение 256*4=1024байт.
                   Если палитры нет то значение 0
    Восьмой dword - Указатель на данные пикселей для R, G, B.
    Девятый dword - Размер области данных для пикселей.
    
2.4 RAW
    Может содержать любые данные, т.к. содержимое на усмотрение программиста

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
