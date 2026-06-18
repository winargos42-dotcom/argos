# 2026-05-12 STM32 ST-Link V2 Setup

## Устройство
- **STMicroelectronics ST-LINK/V2** — отладчик / программатор STM32
- VID: `0483`, PID: `3748`
- Версия прошивки: V2J37S7
- Серийник: `37FF71064E573436D3CB1943`
- Bus 1 Device 8

## Драйвер
- Ядро: не требует драйвера (через libusb)
- udev-правило: `/etc/udev/rules.d/99-stlink.rules`
  - Права `0666`, symlink `/dev/stlink`

## Тест
- `st-info --probe` ✅ — ST-Link V2J37S7 обнаружен
- `Failed to enter SWD mode` — ожидаемо, нет подключённого STM32 MCU

## Установленный софт
| Категория | Пакеты |
|-----------|--------|
| **OpenOCD** | `openocd` (ST-Link, J-Link, CMSIS-DAP) |
| **ST-Link** | `stlink` (st-info, st-flash, st-util) |
| **STM32 загрузчики** | `stm32flash`, `stm32loader` |
| **ARM GCC** | `arm-none-eabi-gcc`, `binutils`, `gdb`, `newlib` |
| **Python embedded** | `pyocd`, `pylink-square`, `pyelftools`, `capstone`, `unicorn`, `keystone-engine` |
| **Программаторы** | `minipro`, `avrdude`, `flashrom`, `dfu-util` |
| **Serial/UART** | `minicom`, `picocom`, `screen`, `socat` |

## Использование
```bash
# Инфо о подключённом STM32
st-info --probe

# Прошивка через ST-Link
st-flash write firmware.bin 0x8000000

# OpenOCD с ST-Link
openocd -f interface/stlink.cfg -f target/stm32f1x.cfg
```

## Связи
- [[SEGGER J-Link]] — (1366:0105)
- [[XGecu T48]] — (a466:0a53)
- [[FTDI OBD Scanner]] — (0403:b470)
- [[Scanmatik SM-2]] — (20a2:0001)
- [[ARGOS]]

[[Backbone Hub]]
