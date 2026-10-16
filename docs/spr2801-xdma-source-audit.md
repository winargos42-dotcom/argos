# ARGOS SPR2801S: восстановление GTI/XDMA-моста по официальному исходному драйверу

**Дата:** 2026-10-10. Исходник: <https://github.com/Xilinx/dma_ip_drivers/tree/master/XDMA/linux-kernel> (Xilinx / AMD XDMA GPLv2).

## Что взято из реального кода производителя

| Файл XDMA | Проверено | Практическое следствие для X230 |
|---|---|---|
| `xdma/cdev_ctrl.c` | `char_ctrl_read` всегда вызывает `ioread32`, копирует ровно 4 байта и возвращает `4`. BAR offset — `*pos`. | Считывать `sc4_xdma` двумя отдельными `pread(fd,4,0)` и `pread(fd,4,4)`; 8-байтный `pread` неверен. |
| `xdma/cdev_sgdma.c` | `char_sgdma_read_write` выставляет `cb.ep_addr=*pos` и вызывает `xdma_xfer_submit`. | `pwrite(fd, data, 0x10000)` означает AXI-MM цель `0x10000` — подтверждает интерпретацию выполненного H2C теста. |
| `xdma/libxdma.c` | `engine->streaming = 1` при `identifier & 0x8000`; иначе MM. | У H2C0 и C2H0 на X230 ID `0x1fc00006`, `0x1fc10006`, бит AXI-ST **не** установлен. |
| `xdma/cdev_sgdma.h` | XDMA SGDMA ioctl `_IOW('q',...)`, `_IOR('q',...)`. | ioctl на GTI2800 `0x40044701/02` имеет другой magic `'G'`. |
| `xdma/cdev_ctrl.h` | XDMA control ioctl magic `'x'`; обрабатываются Xilinx version / online / offline. | Старые GTI команды `ioctl(0x40044702, opcode 5)` **не** являются XDMA control ioctl. |
| `xdma/libxdma.c` | `user_bar_idx` и `config_bar_idx` обнаруживаются отдельно. | На текущей плате Linux user BAR0 и control BAR2 нельзя переставлять местами. |

**Важная заводская оговорка:** в `XDMA/linux-kernel/readme.txt` Xilinx явно предупреждает, что его `tests/run_test.sh`, `dma_memory_mapped_test.sh` и сопутствующие скрипты предназначены **только для демонстрационного FPGA example design**. Не запускать их на фабричной SC4 без проверки AXI address map.

## Реально восстановленные файлы ARGOS

- `src/connectivity/gti_pcie_bridge.py` — строгий разбор заводской GTITXN01, последовательности всех восьми этапов GtiCreateModel и 4 логических устройств; работает с **настоящим** `/dev/gti2800-{0..3}` только если установлен подлинный драйвер GTI, а иначе честно отказывает. Тестовый fake-backend не выдаёт себя за физический NPU.
- `src/connectivity/xdma_transport.py` — безопасный `O_RDONLY` preflight Linux XDMA: проверяет PCI `10ee:7022`, подпись `sc4_xdma`, два engine ID и 16 слов четырёх логических регистровых блоков. **Нулевые аппаратные записи и нулевые DMA**.
- `tests/test_spr2801_gti_xdma.py` — автономные unittest тесты синтетической последовательности GTI и 4 банков SC4 в обычных временных файлах, проверки magic ioctl, неправильного PCI/AXI-ST, запрета неподтверждённых адресов и выбора чипов.
- `.github/workflows/spr2801-gti-bridge-test.yml` — отдельная CI-проверка только кода, без железа и секретов.

Публичный исходный Windows XDMA/BAR доступ из старого ARGOS: `poilopr57-a11y/Argos/src/connectivity/xilinx_fpga.py`, коммит `5c363584928562f648f78bc686dde2a1948c3999`. Этот модуль под Windows использует `cfgmgr32` и `CreateFile`, но не содержит полного интерфейса четырёх NPU.

## Аппаратная граница — не путать с готовым инференсом

На физическом X230 уже выполнено (отдельная локальная история ARGOS):
- H2C `0x10000`, 256 нулевых байт: **256/256 PASS**.
- H2C `0x10000`, 88 байт оригинального GTI model-control stage4: **88/88 PASS**, все четыре блока BAR0 без изменений.
- C2H `0x10000`, 256 байт без загрузки модели: **ETIMEDOUT**, после чего дальнейшие запросы остановлены.
- Полные хостовые `GtiCreateModel` GNet3 и GNet18 воспроизведены побайтово, но **на реальном FPGA модель не загружена**, NPU-ACK не наблюдался.

Официальный исходный XDMA драйвер подтверждает транспорт и режим MM, **но не содержит регистра выбора U4/U5/U9/U10, внутреннего FIP и фабричной карты SC4**. Новый код эту недостающую логику не выдумывает, не меняет битстрим, не пишет в BAR0 и не отправляет много-МБ моделей по неподтверждённым адресам.

## Запуск без риска

```bash
python3 -m unittest discover -s tests -p 'test_spr2801_gti_xdma.py' -v
python3 src/connectivity/xdma_transport.py
python3 src/connectivity/gti_pcie_bridge.py --status
```

Первый запуск проверяет модель и BAR на **фиктивных файлах**, второй и третий только **читают** реальное состояние карты X230.

Понадобится достоверная цепочка `GTI ioctl → AXI command region → FIP → chip select/ACK`. Только после неё можно разрешить реальную многомегабайтную загрузку и следующий C2H запрос. Наличие официального Xilinx XDMA не означает, что этот второй, **заводской SC4** компонент уже восстановлен.
