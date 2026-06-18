# 2026-05-12 USB Arsenal — Full System Setup

## Устройства (все подключены сегодня)

| # | Устройство | VID:PID | Тип | Порт | Статус |
|---|-----------|---------|-----|------|--------|
| 1 | Scanmatik SM-2 | 20a2:0001 | Автосканер J2534 | pyusb bulk | ✅ Драйвер pyusb |
| 2 | FTDI OBD Scanner | 0403:b470 | FT232R OBD-II | /dev/ttyUSB0 | ✅ ftdi_sio + new_id |
| 3 | XGecu T48 | a466:0a53 | Программатор микросхем | libusb | ✅ minipro |
| 4 | SEGGER J-Link V9 | 1366:0105 | ARM отладчик | /dev/ttyACM0 | ✅ cdc_acm + openocd |
| 5 | STM32 ST-Link V2 | 0483:3748 | STM32 программатор | libusb | ✅ stlink + openocd |

## UDEV правила (все в `/etc/udev/rules.d/`)

| Файл | Размер | Статус |
|------|--------|--------|
| `99-ftdi-b470.rules` | 305 B | ✅ FTDI OBD auto-binding |
| `99-jlink.rules` | 346 B | ✅ J-Link + ttyACM |
| `99-stlink.rules` | 372 B | ✅ ST-Link V2/V2.1/V3 |
| `99-xgecu-t48.rules` | 145 B | ✅ XGecu programmer |
| `99-scanmatik.rules` | 317 B | ✅ Scanmatik SM-2 |
| `99-nfc.rules` | 216 B | (было) |
| `99-sunxi.rules` | 96 B | (было) |
| `99-cc2531.rules` | 0 B | пустое |

## DEV nodes

```
/dev/jlink       -> bus/usb/001/006   (J-Link USB)
/dev/jlink_tty   -> ttyACM0           (J-Link CDC)
/dev/stlink      -> bus/usb/001/008   (ST-Link USB)
/dev/stlinkv2_1  -> bus/usb/001/008   (alias)
/dev/ttyACM0     (J-Link CDC ACM)
/dev/ttyUSB0     (FTDI OBD — отключён сейчас)
```

## Системный софт — Full Package

### ARM / Embedded
| Пакет | Версия |
|-------|--------|
| `openocd` | 0.12.0 |
| `arm-none-eabi-gcc` | 14.2.0 |
| `arm-none-eabi-binutils` | 2.43 |
| `arm-none-eabi-gdb` | 17.1 |
| `arm-none-eabi-newlib` | 4.5.0 |
| `stlink` | 1.8.0.r121 |

### Программаторы
| Пакет | Версия |
|-------|--------|
| `minipro` | 0.7.4 |
| `avrdude` | 8.1 |
| `flashrom` | 1.7.0 |
| `dfu-util` | 0.11 |
| `esptool` | 5.2.0 |

### Serial / UART
| Пакет | Версия |
|-------|--------|
| `minicom` | 2.11.1 |
| `picocom` | 3.1 |
| `screen` | 5.0.1 |
| `socat` | 1.8.1.1 |
| `putty` | 0.83 |

### Python embedded (system)
| Пакет | Версия |
|-------|--------|
| `python-pyserial` | 3.5 |
| `python-pyusb` | 1.3.1 |
| `python-pyelftools` | 0.32 |

### CAN / Fieldbus
| Пакет | Версия |
|-------|--------|
| `can-utils` | 2025.01 |

### Анализ / Reverse
| Пакет | Версия |
|-------|--------|
| `binwalk` | 3.1.0 |
| `hexedit` | 1.6 |
| `nasm` | 3.01 |
| `yasm` | 1.3.0 |

### USB infra
| Пакет | Версия |
|-------|--------|
| `usbutils` | 019 |
| `libusb` | 1.0.29 |
| `libftdi` | 1.5 |
| `wireshark-cli` | 4.6.5 |
| `i2c-tools` | 4.4 |
| `rtl-sdr` | 2.0.2 |

## Python .venv (ARGOS)
| Пакет | Назначение |
|-------|-----------|
| `obd` | OBD-II диагностика |
| `python-can` | CAN bus |
| `cantools` | DBC / CAN декодирование |
| `udsoncan` | UDS протокол |
| `j1939` | J1939 truck/bus |
| `pymodbus` | Modbus RTU/TCP |
| `minimalmodbus` | Modbus лёгкий |
| `pyftdi` | FTDI D2XX |
| `pyusb` | libusb wrapper |
| `pyocd` | CMSIS-DAP / ST-Link |
| `pylink-square` | J-Link (требует SEGGER DLL) |
| `pyelftools` | ELF parsing |
| `capstone` | Дизассемблер |
| `unicorn` | CPU эмуляция |
| `keystone-engine` | Ассемблер |
| `intelhex` | Intel HEX |
| `bincopy` | SREC / HEX / BIN |
| `stm32loader` | STM32 UART bootloader |

## Проверка цепочки
```bash
# J-Link + OpenOCD
openocd -f interface/jlink.cfg -c "adapter serial 000069655874" -f target/stm32f1x.cfg

# ST-Link + OpenOCD
openocd -f interface/stlink.cfg -f target/stm32f1x.cfg

# ST-Link info
st-info --probe

# XGecu programmer
minipro -p "AT24C256" -r dump.bin

# FTDI OBD (когда подключён)
obd.OBD("/dev/sndevice")

# Scanmatik (через драйвер)
python3 /home/ava/scanmatik_driver/scanmatik_linux.py
```

## Связи
- [[Scanmatik SM-2 Setup]]
- [[FTDI OBD Scanner Setup]]
- [[XGecu T48 Setup]]
- [[SEGGER J-Link Setup]]
- [[STM32 ST-Link V2 Setup]]
- [[ARGOS]]

[[Backbone Hub]]
