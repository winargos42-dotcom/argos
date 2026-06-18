# 2026-05-14 — Hardware Deploy + Mini-Tron-50 Fallback

**Время:** 19:35  
**Статус:** Конфиги развёрнуты, ожидают запуска  

---

## 🖥️ Windows PC (argos-pc, 192.168.1.66)

### Донгл (COM14)
- **Обнаружен:** USB Serial устройство на COM14
- **Статус:** Точная идентификация невозможна удалённо (encoding issues в PowerShell через SSH)
- **Рекомендация:** `devmgmt.msc` → порты → посмотреть Vendor ID для точной идентификации
- **Скрипт:** `windows_dongle_setup.ps1` — уже на ПК, лог в `windows_dongle.log`

### Spaced Repetition — установлен ✅
- Плагин файлы в `F:\debug\аргос\.obsidian\plugins\obsidian-spaced-repetition\`
- Следующий шаг: restart Obsidian → enable plugin

### Mini-Tron-50 — Python API wrapper ✅ (GGUF не удался)
**Почему GGUF не работает:** модель использует кастомный BPE-токенайзер (tiktoken-совместимый), который llama.cpp не поддерживает напрямую. `convert_hf_to_gguf.py` падает на парсинге `tokenizer.model`.

**Решение:** Python API wrapper (`argos_minitron_api.py`) — предоставляет OpenAI-compatible API на `localhost:11435`.

**Запуск на Windows (WSL или Python):**
```bash
# WSL:
cd /mnt/c/Users/AvA/Downloads/argos_scripts
python3 argos_minitron_api.py --preload

# Или нативный Python на Windows (если установлен):
cd C:\Users\AvA\Downloads\argos_scripts
python argos_minitron_api.py --preload
```

**Интеграция в Brain API:** добавить endpoint `http://192.168.1.66:11435` как provider `argos-classic`.

### Файлы на ПК
```
C:\Users\AvA\Downloads\argos_scripts\
├── argos_install_sr.ps1              (Spaced Repetition installer)
├── argos_setup_mini_tron_windows.ps1 (загрузка модели с HF)
├── argos_minitron_api.py              (Python inference API)
├── windows_dongle_setup.ps1          (детекция донгла)
├── mini-tron-50-model\                (модель 129MB + конфиги)
│   ├── model\pytorch_model.bin
│   └── Modelfile
└── windows_dongle.log               (результат сканирования)
```

---

## 🍊 Orange Pi (orangepi-one, 192.168.2.168:7777)

### Zigbee донгл + 2 ESP
- **API:** IoT Agent v2.1 работает, uptime 98+ часов
- **USB serial:** не обнаружены через API (`/dev/ttyUSB*` отсутствуют в ответе)
- **Причина:** либо донглы не подключены физически, либо нужен драйвер/перезагрузка

### Деплой-скрипт готов
**`orangepi_deploy_all.sh`** — создан, нужно запустить на Orange Pi:
```bash
# На Orange Pi (root):
curl -O http://192.168.1.53:8000/orangepi_deploy_all.sh  # или скопировать через USB/SD
bash orangepi_deploy_all.sh
```

**Что скрипт делает:**
1. Сканирует `/dev/ttyUSB*` и `/dev/ttyACM*`
2. Идентифицирует Zigbee координатор (CC253/CC265/Silabs)
3. Пишет `configuration.yaml` для Zigbee2MQTT с mqtt://192.168.1.53:1883
4. Создаёт конфиги ESPHome для ESP8266 (сенсор) и ESP32 (актуатор)
5. Включает UART overlays в `/boot/armbianEnv.txt`

### Проверка перед деплоем
```bash
# На Orange Pi:
lsusb                          # должны быть USB устройства
dmesg | tail -30               # свежие USB-подключения
ls /dev/ttyUSB* /dev/ttyACM*   # должны быть порты
```

Если портов нет — нужны драйверы:
```bash
# CH340/CH341
modprobe ch341-uart

# CP210x
modprobe cp210x

# FTDI
modprobe ftdi_sio
```

---

## 🔧 Скрипты на laptop (доступны для копирования)

| Скрипт | Назначение | Путь |
|--------|-----------|------|
| `orangepi_deploy_all.sh` | Orange Pi: Z2M + ESPHome + UART | `/home/ava/Projects/argoss/scripts/` |
| `argos_minitron_api.py` | Python inference API (OpenAI-compatible) | `/home/ava/Projects/argoss/scripts/` |
| `vault-sync.sh` v2 | Синхронизация vault + защита от дублей | `/home/ava/.local/bin/` |
| `sync-obsidian-memory.py` v2 | Python sync с exclude `.obsidian/.git` | `/home/ava/.local/bin/` |

---

## 📝 Чеклист для пользователя

### Windows PC
- [ ] Restart Obsidian → Settings → Community plugins → Enable «Spaced Repetition»
- [ ] Проверить COM14 донгл: `devmgmt.msc` → COM14 → свойства → Details → Hardware IDs
- [ ] Если донгл = Zigbee: настроить ZHA/Z2M через WSL Docker
- [ ] Если донгл = WiFi/SDR/etc: установить соответствующие драйверы
- [ ] Запустить mini-tron API:
  ```bash
  wsl bash -c "cd /mnt/c/Users/AvA/Downloads/argos_scripts && python3 argos_minitron_api.py --preload"
  ```

### Orange Pi
- [ ] Проверить USB порты: `lsusb`, `ls /dev/ttyUSB*`
- [ ] Если портов нет: `modprobe ch341-uart cp210x ftdi_sio`
- [ ] Скопировать `orangepi_deploy_all.sh` и запустить
- [ ] Перезагрузить если изменён `/boot/armbianEnv.txt`
- [ ] Стартовать Z2M: `cd /opt/zigbee2mqtt && npm start`
- [ ] Флеш ESP через ESPHome: `esphome run /root/esphome/esp-usb-sensor.yaml`

---

[[2026-05-14]]
[[ARGOS Spaced Repetition + Mini-Tron-50 Integration]]
[[Backbone Hub]]
