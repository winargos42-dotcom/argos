# 2026-05-12 XGecu T48 / TL866II Plus Programmer Setup

## Устройство
- **XGecu T48** — универсальный программатор микросхем
- Также известен как TL866II Plus (MiniPRO)
- VID: `a466`, PID: `0a53`
- Manufacturer: `XGecu.com`
- Bus 1 Device 4, High Speed (480 Mbps)
- 4 endpoint (Vendor Specific Class)

## Драйвер
- Ядро: Vendor Specific, драйвер не требуется
- Доступ через libusb (pyusb / minipro)
- udev-правило: `/etc/udev/rules.d/99-xgecu-t48.rules`
  - Права `0666`, symlink `/dev/xgecu_t48`

## Установленный софт
| Пакет | Назначение |
|-------|-----------|
| **minipro** | CLI для TL866II / T48 — чтение/запись микросхем |
| **srecord** | Motorola S-record формат (зависимость minipro) |
| **hexedit** | Hex-редактор |
| **binwalk** | Анализ бинарных файлов, извлечение прошивок |
| **nasm / yasm** | Ассемблеры |
| **flashrom** | SPI/NOR Flash программирование |
| **avrdude** | AVR прошивка |
| **openocd** | JTAG/SWD отладка |
| **stlink** | ST-Link программатор |
| **dfu-util** | DFU режим |
| **pyusb** | Python USB доступ |
| **intelhex / bincopy** | Python HEX/SREC библиотеки |

## Тест
- minipro запускается: `minipro version 0.2-dev` ✅
- Устройство доступно через libusb ✅

## Использование
```bash
# Список поддерживаемых микросхем
minipro -l | grep AT24C256

# Чтение EEPROM AT24C256
minipro -p "AT24C256" -r eeprom_dump.bin

# Запись
minipro -p "AT24C256" -w firmware.bin

# Только ID
minipro -p "AT24C256" -d
```

## Связи
- [[FTDI OBD Scanner]] — предыдущее устройство (0403:b470)
- [[Scanmatik SM-2]] — первое устройство (20a2:0001)
- [[ARGOS]]

[[Backbone Hub]]
