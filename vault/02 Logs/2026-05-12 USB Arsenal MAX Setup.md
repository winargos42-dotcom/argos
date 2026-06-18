# 2026-05-12 USB Arsenal — MAXIMUM Setup Complete

## 🔌 УСТРОЙСТВА (8 штук)

| # | Устройство | VID:PID | DEV Node | Драйвер |
|---|-----------|---------|----------|---------|
| 1 | **Scanmatik SM-2** | 20a2:0001 | pyusb bulk | `pyusb` + custom |
| 2 | **FTDI OBD Scanner** | 0403:b470 | `/dev/ttyUSB0` → `/dev/sndevice` | `ftdi_sio` + `new_id` |
| 3 | **XGecu T48** | a466:0a53 | `/dev/xgecu_t48` | `libusb` + `minipro` |
| 4 | **SEGGER J-Link V9** | 1366:0105 | `/dev/ttyACM0` → `/dev/jlink_tty` | `cdc_acm` |
| 5 | **STM32 ST-Link V2** | 0483:3748 | `/dev/stlink` | `libusb` + `stlink` |
| 6 | **CH340 USB-UART** | 1a86:7522 | `/dev/ttyUSB0` → `/dev/ttyCH340` | `ch341` |
| 7 | **FNIRSI 2C23T** | 2e3c:5720 | `/dev/sdb` → `/dev/fnirsi_disk` | `usb-storage` (IAP) |
| 8 | **Xiaomi Redmi Note 8T** | 18d1:4ee7 | `97beca7` (ADB) | `android-udev` + `adb` |

## 📋 UDEV ПРАВИЛА

| Файл | Устройство |
|------|-----------|
| `99-scanmatik.rules` | Scanmatik SM-2 |
| `99-ftdi-b470.rules` | FTDI OBD (auto new_id) |
| `99-xgecu-t48.rules` | XGecu T48 |
| `99-jlink.rules` | SEGGER J-Link + ttyACM |
| `99-stlink.rules` | ST-Link V2/V2.1/V3 |
| `99-ch340.rules` | CH340 UART |
| `99-fnirsi.rules` | FNIRSI 2C23T |
| `99-xgecu.rules` | XGecu (legacy) |

## 🛠️ SYSTEM PACKAGES — 50+ пакетов

### ARM / Embedded Core
| Пакет | Назначение |
|-------|-----------|
| `openocd` | Универсальный отладчик (J-Link, ST-Link, CMSIS-DAP) |
| `arm-none-eabi-gcc` | ARM GCC 14.2.0 |
| `arm-none-eabi-binutils` | ARM binutils 2.43 |
| `arm-none-eabi-gdb` | ARM GDB 17.1 |
| `arm-none-eabi-newlib` | C библиотека для embedded |
| `stlink` | STM32 ST-Link утилиты |

### Программаторы
| Пакет | Назначение |
|-------|-----------|
| `minipro` | TL866 / XGecu T48 |
| `avrdude` | AVR программирование |
| `flashrom` | SPI/NOR Flash |
| `dfu-util` | DFU режим |
| `esptool` | ESP32 прошивка |

### Hex / Reverse / Debug
| Пакет | Назначение |
|-------|-----------|
| `imhex-bin` | Hex редактор с паттернами |
| `radare2` | Reverse engineering framework |
| `cutter` | GUI для radare2 |
| `ghidra` | NSA reverse engineering suite |
| `hexedit` | Консольный hex редактор |
| `binwalk` | Анализ бинарных файлов |
| `nasm` / `yasm` | Ассемблеры |

### Serial / UART
| Пакет | Назначение |
|-------|-----------|
| `minicom` | TUI serial клиент |
| `picocom` | Лёгкий serial |
| `screen` | Мультиплексор + serial |
| `socat` | Универсальный data relay |
| `putty` | GUI SSH/serial |

### CAN / Automotive
| Пакет | Назначение |
|-------|-----------|
| `can-utils` | CAN: candump, cansend, slcan |

### Android
| Пакет | Назначение |
|-------|-----------|
| `android-tools` | adb, fastboot |
| `android-udev` | UDEV для 300+ Android |
| `scrcpy` | Зеркалирование экрана |
| `android-file-transfer` | MTP файловый менеджер |
| `android-studio` | Android IDE |
| `android-sdk-*` | SDK platform + build tools |

### Oscilloscope / LA
| Пакет | Назначение |
|-------|-----------|
| `pulseview` | GUI sigrok |
| `sigrok-cli` | CLI sigrok |
| `libsigrok` / `libsigrokdecode` | Библиотека + декодеры |
| `sigrok-firmware-fx2lafw` | LA прошивки |

### USB / Protocol
| Пакет | Назначение |
|-------|-----------|
| `usbutils` | lsusb |
| `libusb` / `libftdi` | USB библиотеки |
| `wireshark-cli` | Анализ трафика |
| `i2c-tools` | I2C сканирование |
| `rtl-sdr` | SDR радио |

### Build / Dev
| Пакет | Назначение |
|-------|-----------|
| `cmake` / `ninja` / `meson` | Сборка |
| `gcc` / `gdb` | Компилятор / отладчик |
| `nmap` / `tcpdump` / `openssh` | Сеть |

## 🐍 PYTHON (.venv) — 25+ пакетов

| Пакет | Устройство / Назначение |
|-------|------------------------|
| `obd` | OBD-II диагностика |
| `python-can` | CAN bus |
| `cantools` | DBC декодирование |
| `udsoncan` | UDS протокол |
| `j1939` | Truck/bus |
| `pymodbus` / `minimalmodbus` | Modbus RTU/TCP |
| `pyftdi` | FTDI D2XX |
| `pyusb` / `libusb1` | USB доступ |
| `pyocd` | CMSIS-DAP / ST-Link |
| `pylink-square` | J-Link Python |
| `pyvisa` / `pyvisa-py` | VISA инструменты |
| `python-usbtmc` | USBTMC (FNIRSI) |
| `platformio` | Embedded IDE |
| `stm32loader` | STM32 UART bootloader |
| `frida` / `frida-tools` / `objection` | Android runtime pentest |
| `pyelftools` | ELF парсинг |
| `capstone` | Дизассемблер |
| `unicorn` | CPU эмуляция |
| `keystone-engine` | Ассемблер |
| `intelhex` / `bincopy` | HEX/SREC/BIN |

## 🚀 БЫСТРЫЕ КОМАНДЫ

```bash
# ── J-Link + OpenOCD ──
openocd -f interface/jlink.cfg -c "adapter serial 000069655874" -f target/stm32f1x.cfg

# ── ST-Link ──
st-info --probe
st-flash write firmware.bin 0x8000000

# ── XGecu T48 ──
minipro -p "AT24C256" -r dump.bin

# ── FTDI OBD ──
obd.OBD("/dev/sndevice")

# ── CH340 ──
python -c "import serial; s=serial.Serial('/dev/ttyCH340',9600); print(s.read(64))"

# ── FNIRSI IAP ──
sudo mount /dev/sdb /mnt/fnirsi && ls /mnt/fnirsi

# ── Xiaomi ──
adb devices                      # (требует авторизации на экране)
scrcpy --serial 97beca7          # зеркалирование
frida -U -n com.android.settings # runtime

# ── Android File Transfer ──
android-file-transfer            # GUI MTP
```

## 📊 ИТОГ
- **8 устройств** подключено и настроено
- **50+ pacman пакетов** установлено
- **25+ Python пакетов** в `.venv`
- **8 udev правил** для hotplug
- **3 vault заметки** за сегодня

[[Backbone Hub]]
