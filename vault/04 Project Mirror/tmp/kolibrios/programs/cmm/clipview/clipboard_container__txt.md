---
argos_import: project_file
source_path: tmp/kolibrios/programs/cmm/clipview/clipboard_container.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\cmm\clipview\clipboard_container.txt
source_ext: .txt
source_sha256: c416b51c375716eac0fab229cd9e166f36c57490976d04e3ea8b5139f22847ce
text_sha256: a41afaf006b1821b01d7286e3e7152e595209cdf4566711e53cdf845f55febe9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:42
---

# clipboard_container.txt

- Source: `tmp/kolibrios/programs/cmm/clipview/clipboard_container.txt`
- Extract: `text`
- SHA256: `c416b51c375716eac0fab229cd9e166f36c57490976d04e3ea8b5139f22847ce`

## Content

Содержимое контейнера буфера обмена

1. Первый dword содержит общую длину данных в контейнере

2. Второй dword указывает тип данныx:
   0 = Текст
   1 = Изображение
   2 = RAW
   4 и выше зарезервировано

2.1 Текст
    Данные в третьем dword содержат тип кодировки:
    0 = UTF
    1 = 0866    
    2 = 1251
    3 и выше зарезервировано

2.2 Изображение
    Третий dword - размер по X
    Четвертый dword - размер по Y
    Пятый dword - глубина цвета в битах (8, 16, 24, 32, 48, 64)
    Шестой dword - Указатель на палитру (смещение от начала файла).
                   Если палитры нет то значение 0
    Седьмой dword - Размер области палитры, максимальное значение 256*4=1024байт.
                   Если палитры нет то значение 0
    Восьмой dword - Указатель на данные пикселей для R, G, B.
    Девятый dword - Размер области данных для пикселей.
    
2.3 RAW
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
