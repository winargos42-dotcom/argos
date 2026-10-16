# Аудит ZhengPengqiao/QtStudy — `芯片平台/SPR2801S`

Дата: 2026-10-10. GitHub: https://github.com/ZhengPengqiao/QtStudy/tree/master/%E8%8A%AF%E7%89%87%E5%B9%B3%E5%8F%B0/SPR2801S

## Полнота инвентаризации

Построен **полный рекурсивный Git tree** для всех четырёх каталогов, `truncated=false` во всех ответах. **346 файлов**, около 213.2 МБ. Каждый файл зарегистрирован по **пути, размеру, Git blob SHA1**, включая изображения, 5 бинарных BGR/RGB файлов, 2 готовые модели и бинарные библиотеки. Полный манифест `SPR2801_QTSTUDY_MASTER_ALL_FILES_20261010.json` сохранён через ARGOS X230 MCP.

| Directory | Files | Bytes | Git tree SHA |
|---|---:|---:|---|
| `1_0_Demo` | 13 | 2,014,510 | `dafabb1eb343983bbb4920215ec08d32de6230df` |
| `doc` | 100 | 101,977,751 | `76749446c9b97b558a471a8159f374607be6f552` |
| `include` | 2 | 26,985 | `70a00fcb2859ecee3861afbb4d0ab332e758c3ab` |
| `libs` | 231 | 109,222,181 | `ee647180208d429f7e77590f4f600a241a3e94e9` |

**Важное разграничение:** все 346 файлов проиндексированы, но нельзя утверждать, что каждый байт всех бинарников, видео/картинок и OpenCV headers просмотрен человеком. Прикладные исходники, SDK API и udev правила прочитаны; два оригинальных `.model` и SDK `.so` уже были подвергнуты отдельному программному реверсу на X230 в более ранних этапах.

## Что на самом деле содержит QtStudy

1. `1_0_Demo/spr2801s.cpp`: приложение Qt использует вызовы **`GtiCreateModel(modelName)`** и **`GtiEvaluate(model,&input)`**. Конвертирует входную картинку из OpenCV в три планарных BGR массива, стандартный размер `224x224x3`. Ответ читает как JSON из `output->buffer` и рисует класс с FPS. В приложении **нет** управления BAR0, H2C/C2H, AXI/FIP, выбором U4/U5/U9/U10, аппаратным IRQ или kernel ioctl.
2. `1_0_Demo/mainwindow.cpp`: по умолчанию загружает `gti_gnet3_fc20_2801.model`, вызовом `spr2801s.initModel(...)`.
3. `1_0_Demo/1_0_Demo.pro`: qmake Qt/C++11; подключает SDK `-lGTILibrary-static`, `-lftd3xx-static`, OpenCV. Однако в данном каталоге бинарник `libGTILibrary-static.a.4.5.1` есть, а `libftd3xx-static.a` **не найден** — сборка из ZIP «как есть» может потребовать изменения linker flags или отдельных vendor dependencies.
4. `include/GTILib.h`: публичный API различает `GTI_DEVICE_USB_FTDI`, `GTI_DEVICE_USB_EUSB`, `GTI_DEVICE_PCIE`, `GTI_DEVICE_VIRTUAL`; содержит `GtiGetAvailableDevice`, `GtiDeviceRead/Write`, `GtiLoadModel`, `GtiCreateModel`, `GtiEvaluate`. **Это API библиотеки, а не драйвер PCIe для XC7A35T.**
5. `doc/rules/70-gti.rules`: `gti0-0..3` → `gti2800-0..3`, права 0666. **Только udev symlinks**, они НЕ создают ядровый драйвер и НЕ описывают физическую разводку четырех ASIC.
6. `doc/rules/51-ftd3xx.rules`: USB FTDI VID 0403, product IDs; `52-gtiusb.rules`: USB VID 300c PID 5801; `50-eusb.rules`: Generic USB SCSI devices. Карту PCIe 10ee:7022 ни одно из этих правил не программирует.
7. `libs/libGTILibrary.so.4.5.1` (2,035,968 B), `libGTILibrary-static.a.4.5.1` (3,969,234 B) — SDK готовые бинарники. **В исходниках проекта нет реализации `gti::DevicePcie`**; при прошлых изолированных трассах SDK использовал проприетарный GTI2800 `ioctl 0x40044701/02`, отличающийся от Xilinx XDMA.
8. `libs/libftd3xx.so.0.5.21` (~4.9 MB) обслуживает альтернативный USB FTDI путь, а не FPGA XC7A35T PCIe.
9. `doc/Modules/`: **ровно две** заводские модели — `gti_gnet3_fc20_2801.model` (9,282,331 B) и `gti_gnet18_dog40_2801.model` (4,689,239 B). Их заводские model-load stages ранее восстановлены с оригинальным SDK побайтово; оба есть в ветви X230 восстановления.
10. `doc/Data`: датасеты 21 BMP, 63 JPG, JPEG, 5 raw BIN по **150,528 bytes = 224×224×3**, 3 видео, README. Это точные входные тестовые изображения для восстановления тракта `GtiEvaluate` — **не драйверные FPGA регистры**.
11. `libs/OpenCV`: 158 `.hpp` и 52 `.h`, набор динамических OpenCV 3.2 для x86_64. Большинство остальных 231 файлов в `libs` — вендорные OpenCV зависимые headers / shared libraries.
12. `1_0_Demo/cscope.out` — индекс ссылок для поиска по C/C++ (1.3 MB), не дополнительный драйверный исходник.

## Практический вывод для ARGOS

**В данном дереве отсутствуют**: исходник kernel `gti0`/`gti2800`, AXIPCIE BAR register map для 10ee:7022, SC4 XC7A35T проект Vivado/RTL, XDMA→четыре физические U4/U5/U9/U10 селекторы и подтверждаемые ACK. Не смешивать номера `/dev/gti2800-0..3` с physical FPGA bank 0x10/0x20/0x30/0x40 — это пока гипотеза.

**Что полезно прямо сейчас:** QtStudy даёт два byte-verified `.model` + готовые тестовые RGB/BGR planar raw inputs по 150,528 B. Это основа для независимого проверки `GtiEvaluate` на хостовом уровне; загружать их на физический SC4 через generic XDMA **без подтверждённого mapping** нельзя. Публичный Qt-проект — frontend вызовов SDK, а не полное руководство по фабричной четырехчиповой карте SC4.

## Следующий инженерный шаг

В уже рабочем X230 C-драйвере `argos-sc4` реальный BAR status PASS, 55/55 локальных тестов PASS, живой H2C staged diagnostic был ранее отдельно испытан Python. Отдельный C H2C тест ждёт подтверждения RootGuard в Telegram, request `f929152cffa7`; без подтверждения его не называть выполненным. Чтобы добиться NPU inference, разбирать бинарный PCIe backend `libGTILibrary.so` с точным семантическим драйвером `gti0`, либо писать **собственный FPGA битстрим** и FIP sequencer (изолированная сборка ARGOS уже есть, но не залита на карту).

**Нельзя заявлять «прочитаны 346 файлов по байтам»; корректная формулировка — все 346 инвентаризированы, прикладной исходный код и API изучены, бинарники/датасеты идентифицированы по типу/размеру/sha.**
