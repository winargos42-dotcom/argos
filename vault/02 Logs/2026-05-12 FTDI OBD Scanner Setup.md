# 2026-05-12 FTDI OBD Scanner Setup

## Устройство
- **FTDI OBD-II / J2534 Scanner** на чипе FT232R
- VID: `0403`, PID: `b470` (кастомный)
- Серийник: `SNDEVICE`
- Bus 1 Device 3, Full Speed (12 Mbps)
- Чип: FT232R (type 0x0600), EEPROM VCP режим

## Драйвер
- Ядро: `ftdi_sio` + `usbserial` загружены
- `/dev/ttyUSB0` создан через `new_id`:
  ```bash
  echo '0403 b470' > /sys/bus/usb-serial/drivers/ftdi_sio/new_id
  ```
- udev-правило: `/etc/udev/rules.d/99-ftdi-b470.rules`
  - Автоподключение new_id при hotplug
  - Права `0666`, symlink `/dev/sndevice`

## Установленный софт
| Категория | Пакеты |
|-----------|--------|
| **OBD-II** | `obd` (python-OBD), `python-can`, `cantools`, `udsoncan`, `j1939` |
| **CAN bus** | `can-utils` (candump, cansend, slcan_attach) |
| **UART / Serial** | `minicom`, `picocom`, `screen`, `socat`, `putty` |
| **USB / FTDI** | `pyftdi`, `pyusb`, `ftdi_sio`, `usbserial` |
| **Modbus** | `pymodbus`, `minimalmodbus` |
| **Прошивка** | `openocd`, `avrdude`, `stlink`, `dfu-util`, `flashrom` |
| **I2C** | `i2c-tools` |
| **Сканирование** | `usbutils`, `wireshark-cli` |

## Тест
- Устройство найдено: Bus 1 Device 3 ✅
- pyftdi EEPROM прочитан ✅ (FT232R, VCP mode)
- `/dev/ttyUSB0` создан ✅
- Serial silent — нормально для OBD-адаптера без подключённого авто

## Использование
```python
import obd
connection = obd.OBD("/dev/ttyUSB0")  # или "/dev/sndevice"
cmd = obd.commands.RPM
response = connection.query(cmd)
print(response.value)
```

## Примечание
Устройство не отвечает на AT-команды без питания от OBD-порта автомобиля. Это стандартное поведение для J2534-адаптеров.

## Связи
- [[Scanmatik SM-2]] — предыдущее устройство (20a2:0001)
- [[OBD-II]]
- [[FTDI]]
- [[ARGOS]]

[[Backbone Hub]]
