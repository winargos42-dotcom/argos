# 2026-05-12 Scanmatik SM-2 Linux Setup

## Устройство
- **Scanmatik SM-2** — USB автомобильный сканер (J2534)
- VID: `20a2`, PID: `0001`
- Bus 1 Device 2, Full Speed (12 Mbps)
- Endpoints: Bulk IN `0x81`, Bulk OUT `0x02`, maxsize 64

## Установлено
- `udev`-правило `/etc/udev/rules.d/99-scanmatik.rules` → доступ без root
- Python-драйвер `/home/ava/scanmatik_driver/scanmatik_linux.py`
- `pyusb`, `pyftdi` в ARGOS `.venv`
- `obd`, `python-can`, `cantools`, `udsoncan`, `j1939` в `.venv`

## Системный софт
| Пакет | Назначение |
|-------|-----------|
| usbutils | lsusb |
| minicom | UART терминал |
| picocom | Лёгкий UART клиент |
| screen | Универсальный терминал |
| socat | Создание виртуальных COM-портов |
| putty | GUI клиент |
| wireshark-cli | Анализ трафика |
| can-utils | CAN-bus: candump, cansend, slcan |
| openocd | JTAG/SWD отладка |
| avrdude | Прошивка AVR |
| stlink | ST-Link программатор |
| dfu-util | DFU режим |
| flashrom | SPI/NOR Flash |
| i2c-tools | I2C сканирование |
| spi-tools | SPI тесты |
| pymodbus / minimalmodbus | Modbus RTU/TCP |

## Драйвер
- Путь: `/home/ava/scanmatik_driver/`
- `scanmatik_linux.py` — базовый pyusb wrapper
- `99-scanmatik.rules` — udev (mode 0666)

## Тест
- Устройство найдено: Bus 1 Device 2 ✅
- Устройство открыто: pyusb claim_interface ✅
- Ответ на `0x01` первой сессии: `01000056` (firmware 0x0056) ✅
- Последующие bulk-read → timeout (требуется control-transfer инициализация)

## Следующий шаг
- Разобрать инициализационный control-transfer протокол SM-2
- Использовать `usb_control_msg` для setup-packet
- Интегрировать в ARGOS модуль `src/connectivity/scanmatik.py`

## Связи
- [[Scanmatik]]
- [[OTG]]
- [[Orange Pi One]]
- [[ARGOS]]

[[Backbone Hub]]
