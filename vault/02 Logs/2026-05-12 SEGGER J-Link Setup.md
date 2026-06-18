# 2026-05-12 SEGGER J-Link Setup

## Устройство
- **SEGGER J-Link V9** — отладчик / программатор ARM Cortex
- VID: `1366`, PID: `0105`
- Серийник: `000069655874`
- Bus 1 Device 6, Full Speed (12 Mbps)
- 3 интерфейса: CDC ACM (ttyACM0), HID, Bulk

## Драйвер
- Ядро: `cdc_acm` → `/dev/ttyACM0` ✅
- udev-правило: `/etc/udev/rules.d/99-jlink.rules`
  - Права `0666`, symlink `/dev/jlink`, `/dev/jlink_tty`

## Тест openocd
```bash
openocd -c "adapter driver jlink; adapter serial 000069655874; transport select swd"
```
Результат:
- J-Link V9 compiled May 7 2021 ✅
- Hardware version: 9.60 ✅
- VTarget = 3.221 V ✅
- clock speed 100 kHz ✅

## Установленный софт
| Категория | Пакеты |
|-----------|--------|
| **OpenOCD** | `openocd` (J-Link, ST-Link, CMSIS-DAP поддержка) |
| **ARM GCC** | `arm-none-eabi-gcc`, `arm-none-eabi-binutils`, `arm-none-eabi-gdb`, `arm-none-eabi-newlib` |
| **Python embedded** | `pyocd`, `pylink-square`, `pyelftools`, `capstone`, `unicorn`, `keystone-engine` |
| **Программаторы** | `minipro`, `avrdude`, `stlink`, `flashrom`, `dfu-util` |
| **Ассемблер** | `nasm`, `yasm` |
| **Hex/Bin** | `hexedit`, `binwalk`, `intelhex`, `bincopy` |
| **Serial/UART** | `minicom`, `picocom`, `screen`, `socat` |
| **CAN** | `can-utils` |
| **I2C** | `i2c-tools` |

## pyocd
- Найден внутренний STM32 STLink: `37FF71064E573436D3CB1943` ✅
- J-Link через pyocd требует SEGGER DLL (не установлена)

## Использование openocd + J-Link
```bash
# Подключение к STM32 через SWD
openocd -f interface/jlink.cfg -c "adapter serial 000069655874" -f target/stm32f1x.cfg

# В другом терминале — GDB
gdb-multiarch firmware.elf
(gdb) target remote localhost:3333
```

## Связи
- [[XGecu T48]] — предыдущее устройство (a466:0a53)
- [[FTDI OBD Scanner]] — (0403:b470)
- [[Scanmatik SM-2]] — (20a2:0001)
- [[ARGOS]]

[[Backbone Hub]]
