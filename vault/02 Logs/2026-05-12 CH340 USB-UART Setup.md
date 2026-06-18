# 2026-05-12 CH340 USB-UART Setup

## Устройство
- **QinHeng CH340 serial converter** — USB-UART мост (китайская альтернатива FTDI)
- VID: `1a86`, PID: `7522`
- Bus 002 Device 5 (порт 2-1.2), Full Speed
- Product: `USB Serial`

## Драйвер
- Ядро: `ch341` автоматически загружен ✅
- `/dev/ttyUSB0` создан автоматически ✅
- udev-правило: `/etc/udev/rules.d/99-ch340.rules`
  - Права `0666`, symlink `/dev/ch340`, `/dev/ttyCH340`

## Тест
- `stty -F /dev/ttyUSB0 9600` → OK ✅
- `pyserial` → open `/dev/ttyUSB0` @ 9600 ✅

## Установленный дополнительный софт
| Пакет | Назначение |
|-------|-----------|
| `pyserial-asyncio` | Async serial для Python |
| `python-pyserial` | Serial (уже был) |

## Использование
```python
import serial
s = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
s.write(b"Hello\r\n")
print(s.read(64))
s.close()
```

## Связи
- [[USB Arsenal Full Setup]]
- [[ARGOS]]

[[Backbone Hub]]
