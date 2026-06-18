# 2026-05-12 FNIRSI 2C23T Setup

## Устройство
- **FNIRSI 2C23T** — портативный 3-в-1 осциллограф / мультиметр / генератор
- Процессор: Artery AT32 (китайский аналог STM32)
- Режим USB: Mass Storage IAP (In-Application Programming)
- VID: `2e3c`, PID: `5720`
- Bus 001 Device 018
- Product: `AT32 Mass Storage`
- Manufacturer: `Artery`
- Серийник: `080E686F58A4`

## Режимы работы
| Режим | USB класс | Назначение |
|-------|-----------|------------|
| IAP (сейчас) | Mass Storage | Обновление прошивки |
| Рабочий | USBTMC / CDC | Осциллограф + данные |

## Mass Storage IAP
- `/dev/sdb` — 1 MiB диск
- Содержимое: `Ready.TXT` (пустой, флаг IAP режима)
- Диск смонтирован: `/mnt/fnirsi`

## Драйвер
- Ядро: `usb-storage` автоматически ✅
- udev-правило: `/etc/udev/rules.d/99-fnirsi.rules`
  - Права `0666`, symlink `/dev/fnirsi`, `/dev/fnirsi_disk`

## Установленный софт
| Пакет | Назначение |
|-------|-----------|
| `pulseview` | GUI для sigrok — универсальный осциллограф |
| `sigrok-cli` | CLI для sigrok |
| `libsigrok` | Библиотека sigrok |
| `libsigrokdecode` | Декодеры протоколов |
| `sigrok-firmware-fx2lafw` | Прошивки для FX2 LA |
| `python-usbtmc` | USBTMC протокол (Test & Measurement) |
| `pyvisa` / `pyvisa-py` | VISA инструменты |
| `gnuplot` | Построение графиков |
| `qt5-serialbus` | Qt serial bus |

## Sigrok
```bash
# Скан устройств
sigrok-cli --scan

# Захват с demo (тест)
sigrok-cli --driver demo --samples 100

# Захват с fx2lafw (Logic Analyzer)
sigrok-cli --driver fx2lafw --samples 1000
```

## FNIRSI протокол
FNIRSI 2C23T использует закрытый протокол. Для Linux:
- **Scoppy** — Android app + Raspberry Pi Pico bridge (не нативно)
- **IAP режим** — копирование firmware на `/dev/sdb`
- **Скриншоты** — через mass storage (когда устройство в режиме сохранения)

## Прошивка (IAP)
```bash
# Скопировать .bin файл на диск FNIRSI
sudo mount /dev/sdb /mnt/fnirsi
sudo cp firmware_v2.0.2.bin /mnt/fnirsi/
sudo umount /mnt/fnirsi
# Устройство перезагрузится и прошьётся
```

## Связи
- [[USB Arsenal Full Setup]]
- [[CH340 USB-UART]]
- [[ARGOS]]

[[Backbone Hub]]
