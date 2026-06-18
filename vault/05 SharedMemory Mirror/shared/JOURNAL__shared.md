---
argos_import: sharedmemory_mirror
source_path: shared/JOURNAL.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\shared\JOURNAL.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: shared/JOURNAL.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\shared\JOURNAL.md`
- Category: [[SharedMemory Hub]]

## Content

# Журнал сессий

---

## 2026-05-04 — Сессия 7 (ARGOS полный функционал + Orange Pi CAN + фиксы)

### ARGOS функционал X230 — полный стек ✅

#### Системные пакеты (установлено)
- `mosquitto` MQTT брокер — `localhost:1883`, сервис enabled ✅
- `valkey` Redis — `localhost:6379`, сервис enabled ✅
- `docker` — сервис enabled, ava в группе docker ✅
- `rtl-sdr` — RTL-SDR/AirSnitch 433/868MHz ✅
- `libnfc` — NFC поддержка ✅
- `openocd` — прошивка STM32/ARM ✅
- `hostapd` — WiFi AP (wlp3s0 поддерживает AP режим) ✅
- `picocom` — UART терминал ✅
- `esptool` — прошивка ESP32/ESP8266 ✅
- `rsync` — синхронизация файлов ✅

#### Python пакеты в venv
- `keystone-engine` + `capstone` — ColibriAsmEngine (ASM/дизассемблер) ✅
- `asyncua` — OPC UA промышленный протокол ✅
- `pyrtlsdr` 0.3.0 — SDR (совместима с rtl-sdr v2 API) ✅
- `zigpy` — Zigbee ✅
- `nfcpy` — NFC ✅
- `uptime` ✅
- `~iohttp` битый dist-info — удалён (sudo rm), aiohttp 3.13.5 исправлен ✅

#### NOPASSWD sudo восстановлен
- `/etc/sudoers.d/ava` — `ava ALL=(ALL) NOPASSWD: ALL`

### Orange Pi — CAN bus ✅ (новое)
- Устройство: `1d50:606f` OpenMoko/Geschwister Schneider candleLight (gs_usb)
- Интерфейс: `can0` UP, bitrate 500000
- `can-utils` установлен: cansend/candump/cansniffer
- Автозапуск: `/etc/systemd/system/can0.service` enabled ✅
- Актуальные устройства OPi:

| Устройство | Порт | Статус |
|-----------|------|--------|
| CAN adapter (candleLight) | can0 | ✅ UP 500kbps |
| NodeMCU v3 ESP8266 | /dev/ttyUSB0 | ✅ MicroPython, WiFi |
| Raspberry Pi Pico | /dev/ttyACM0 | ✅ |
| CH340 converter | /dev/ttyUSB0 | ✅ |

- Armbian обновлён (apt upgrade) ✅

### Фиксы

#### Telegram polling — ИСПРАВЛЕН
- Файл: `src/connectivity/telegram_bot.py:1125`
- Проблема: `set_wakeup_fd only works in main thread` (retry 164+)
- Фикс: добавлен `stop_signals=None` в `app.run_polling()`
- Результат: `[TG] Telegram бот запущен` без ошибок ✅

#### thinkfan — ИСПРАВЛЕН
- Проблема: конфиг указывал на `hwmon4` (coretemp), нужен `thinkpad-isa-0000`
- Фикс: переключён на `chip: thinkpad-isa-0000`, агрессивная кривая (вентилятор стартует с 52°C)
- Результат: CPU 89°C → 84°C, вентилятор 5679 → 6396 RPM ✅

#### openclaw перегрев
- `openclaw` ×2 процесса занимали 200% CPU → CPU 89°C
- Применён `nice +19` + `taskset` (CPU 0 и 1), ARGOS на CPU 2,3
- Температура стабилизировалась ниже порога 87°C

### Неопознанное устройство
- `20a2:0001` на X230 Bus 001, Port 2 (xHCI)
- Vendor Specific class, 2 bulk endpoint, нет дескрипторов
- Не отключается при попытке вытащить → скорее всего внутренний чип ноутбука
- Требует дальнейшего исследования

### Лог синхронизирован на ПК
- `~/Projects/argoss/logs/argos_laptop.log` → `F:/debug/argoss/logs/argos_laptop_x230.log`

---

## 2026-05-04 — Сессия 6 (завершение настройки X230 + синхронизация)

### Настройка ноутбука X230 — ЗАВЕРШЕНА ✅
- Ребут выполнен: ядро 7.0.3-arch1-2, thinkfan active (64-68°C → норма)
- ch341 загружен: /dev/ttyUSB0, /dev/ttyUSB1 → CH340 адаптеры доступны
- TLP пороги 70/80% работают через natacpi (thinkpad_acpi)
- Bluetooth, PipeWire/wireplumber — все сервисы active
- Дисплей от сети: xset s off + autostart обновлён (проверка AC перед отключением)
- gh (GitHub CLI) установлен, нужна авторизация: `! gh auth login`

### Синхронизация Obsidian ✅
- Таймер sync-obsidian-memory.timer: active, каждые ~3 мин
- Синхронизировано 24 файла ноутбук↔ПК
- Добавлен project_3gpu.md (ПК→ноутбук): RX580/Vega11/RX560 fast/code/smart

### ARGOS main.py запущен ✅
- PID 29087, режим --no-gui --dashboard
- Ollama ✅, ChromaDB ✅, Kimi ✅, VectorStore ✅
- Предупреждения: TG polling (set_wakeup_fd), OpenClaw port 47392 недоступен
- Лог: /tmp/argos_main.log

### Осталось
- [ ] Orange Pi One — прошивка Armbian (подключить в FEL режим)
- [ ] GitHub sigtrip — сделать публичным (`! gh auth login` → gh repo edit sigtrip/... --visibility public)
- [ ] Colab LoRA обучение — открыть colab/ARGOS_Train_Colab.ipynb

---

## 2026-05-03 — Сессия 5 (обучение ARGOS модели — подготовка)

### Создан Colab ноутбук для LoRA обучения
- Файл: `colab/ARGOS_Train_Colab.ipynb` (14 ячеек)
- Модель: `Qwen2.5-7B-Instruct-bnb-4bit` (Unsloth, 4-bit, T4 GPU)
- LoRA: rank=16, alpha=32, target_modules=q/k/v/o/gate/up/down_proj, RSLoRA
- Параметры: 2 эпохи, batch 4×4=16, packing=True, adamw_8bit

### Датасет подготовлен
- Скрипт: `colab/prepare_dataset.py`
- Вход: `data/evolver_dataset.jsonl` — 3610 записей, 283 MB
- Выход: `data/argos_train_clean.jsonl` — **1230 чистых примеров**, 1.0 MB
- Фильтры: системные, code artifacts, дубликаты, не-русские (MIN 25% кириллицы)

### HuggingFace — статус
- Аккаунт: `AvaSiG` (авторизован через Claude MCP)
- Все токены в .env истекли (401 Unauthorized)
- **Нужно:** зайти на `huggingface.co/settings/tokens` → New token → Write → вставить в .env
- Целевой репо: `AvaSiG/argos-dataset` (dataset), `AvaSiG/argos-v2-lora` (model)

### Команда загрузки датасета (после нового токена)
```bash
cd ~/Projects/argoss
source .venv/bin/activate
python colab/prepare_dataset.py --upload --hf-repo AvaSiG/argos-dataset --hf-token hf_NEW_TOKEN
```

### После обучения — интеграция в ARGOS
```bash
# Скачать с HF или из Colab: argos-v2.gguf + Modelfile
cd ~/Projects/argoss/models/argos-gguf/
ollama create argos-v2 -f Modelfile
ollama run argos-v2 "Кто ты?"  # проверка
# В .env:
# OLLAMA_MODEL=argos-v2
# OLLAMA_FAST_MODEL=argos-v2
```

---

## 2026-05-03 — Сессия 4 (настройка железа + ARGOS запуск)

### X230 — завершение настройки
- `bluetooth`, `wireplumber`, `pipewire-pulse`, `fwupd-refresh.timer` — включены и работают
- `/etc/modprobe.d/thinkpad_acpi.conf` — fan_control=1 записан (применится после ребута)
- `/etc/thinkfan.conf` — кривая охлаждения для hwmon4 (coretemp) записана
- `mkinitcpio -P` — initramfs для 7.0.3-arch1-2 готов
- **Осталось: `sudo reboot`** — после этого thinkfan заработает, все USB модули появятся

### ARGOS на ноутбуке — запущен
- ~251 pip пакет установлен в `.venv` (Python 3.14)
- Исправлен баг: `main.py:685` `orchestrator.shutdown()` → `self.shutdown()`
- Исправлен баг: `aiohttp` 1.0.5 → 3.13.5 (Python 3.14 совместимость)
- MCP `http://127.0.0.1:8000/mcp` — работает
- Навык `evolved_system_health_monitor` — создан и загружен (команда "хелс")

### Эволюция ARGOS
- Запущено 3 цикла эволюции через MCP
- Итог: 1 принят (sklearn TF-IDF, но логическая ошибка), 2 отклонены Code Review (заглушки)
- Написан рабочий навык вручную (`evolved_system_health_monitor.py`) → загружен в ARGOS

### Подключённые устройства (все на USB хабе)
- **Orange Pi One** (Allwinner H3) — FEL режим работает (`AWUSBFEX soc=00001680(H3)`)
  - plugdev группа создана, udev правило `/etc/udev/rules.d/99-sunxi.rules` записано
  - Armbian 26.2.1 скачан: `~/Downloads/orangepi/Armbian_26.2.1_Orangepione_noble_current_6.12.74_minimal.img`
  - U-Boot извлечён: `~/Downloads/orangepi/u-boot-sunxi-with-spl.bin`
  - boot.scr (UMS) создан: `~/Downloads/orangepi/boot.scr`
  - Блокирует: нет ch341 модуля (нужен ребут)
- **Raspberry Pi Pico** (RP2040, 2e8a:0009) — подключён, LED потух (прога завершилась)
  - Блокирует: нет cdc-acm модуля (нужен ребут)
- **CH340 ×2** (1a86:7523) — UART адаптеры (вероятно к Orange Pi UART)
  - Блокирует: нет ch341 модуля (нужен ребут)

### Память
- Синхронизировано в `/root/.claude/projects/-home-ava/memory/` и `/home/ava/.claude/projects/-home-ava/memory/`
- Obsidian sync запущен вручную — данные пошли на ПК

---

## 2026-05-02 — Сессия 3 (продолжение)

### ARGOS на ноутбуке — подготовка

#### Файлы
- Синхронизировано с ПК: ~7.4 ГБ (src/, config/, scripts/, deploy/ и др.)
- Исключено: llama.cpp, models, comfyui, .venv, node_modules (бинарники, не нужны)
- Ключевые файлы: main.py, genesis.py, health_check.py, launch.sh, requirements.txt — есть

#### venv
- Создан: `~/Projects/argoss/.venv`
- Python: 3.14.4
- Установка: fastapi, ollama, telegram-bot, chromadb, sentence-transformers, IoT libs, etc.

#### .env изменения для ноутбука
- `OBSIDIAN_VAULT_PATH` → `/home/ava/Documents/MyObsidianVault`
- `OLLAMA_ENABLED=true`
- Добавлены GPU серверы ПК через сеть: 192.168.1.66:8082-8084

#### Системные пакеты (нужна установка вручную)
```
sudo pacman -S portaudio ffmpeg nmap espeak-ng redis
```

#### Статус
- [x] Файлы скопированы
- [x] venv создан
- [ ] Пакеты устанавливаются (pip install ~60 пакетов)
- [ ] Системные зависимости — нужен sudo
- [ ] health_check.py — после установки

---

## 2026-05-02 — Сессия 2

### Что сделано

#### Синхронизация проекта ARGOS
- Скопирован `F:\debug\argoss\` с ПК на ноутбук → `~/Projects/argoss/` (~7.4 ГБ через tar/SSH)
- Исключены: `.venv`, `venv`, `node_modules`, `__pycache__`, `.buildozer`, `.npm-cache`

#### Общая память SharedMemory
- Создана структура папок для всех агентов:
  - `SharedMemory/claude/` — Claude Code
  - `SharedMemory/argos/` — ARGOS
  - `SharedMemory/opencode/` — OpenCode  
  - `SharedMemory/ollama/` — Ollama
  - `SharedMemory/shared/` — общее (читают все)
- Настроена двусторонняя синхронизация ноутбук ↔ ПК каждые 2 минуты
  - Скрипт: `~/.local/bin/sync-obsidian-memory.py`
  - Таймер: `systemd --user sync-obsidian-memory.timer`
  - Путь на ПК: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\`

#### Claude Code конфиг
- `~/.claude/settings.json` — добавлены MCP серверы:
  - `argos-pc`: `http://192.168.1.66:8000/mcp` (ARGOS на ПК)
  - `argos-local`: `http://127.0.0.1:8000/mcp` (ARGOS локально)
- `autoMemoryDirectory` → `SharedMemory/claude/`

#### ARGOS MCP (ПК)
- Подтверждено: ARGOS работает на ПК, порт 8000
- MCP endpoint: `http://192.168.1.66:8000/mcp` → `{"name":"argos","ok":true}`
- Порты ПК: 5010 (API), 6379 (Redis), 8000 (main), 8082-8084 (GPU LLM), 11434 (Ollama)

#### Claude Code на ПК
- Запущена установка: `npm install -g @anthropic-ai/claude-code`
- Конфиг подготовлен: `autoMemoryDirectory` → SharedMemory, MCP → argos-local + argos-laptop

#### Cloudflare туннели
- Ноутбук (`laptop`): активен, 4 соединения
- ПК (`Argos`): активен, 4 соединения  
- SSH через туннель: требует `cloudflared access login ssh-pc.argosssss.win`

### Статус
- [x] SharedMemory синхронизируется
- [x] ARGOS MCP доступен с ноутбука
- [x] Claude Code знает о ПК через MCP
- [ ] Claude Code на ПК — установка в процессе
- [ ] SSH через Cloudflare Access — нужен `cloudflared access login`

### Orange Pi One — прошивка Armbian ✅ (2026-05-04)
- Образ: `Armbian_26.2.1_Orangepione_noble_current_6.12.74_minimal.img` (1.3 ГБ)
- Устройство: `/dev/sdb` (USB кардридер — встроенный Ricoh слот нестабилен)
- Записано: 311 блоков × 4МБ = 1.3 ГБ, 12.6 МБ/с, без ошибок
- Партиция: sdb1 1.2G Linux (ext4)
- U-Boot: `sun8i-h3-orangepi-one` SPL 2024.01 подтверждён
- Проблема встроенного слота: Ricoh [1180:e822], I/O errors, recovery failed — обходим через USB
- Следующий шаг: вставить SD в Orange Pi, подключить питание, найти IP (DHCP), ssh root@<ip>

### Orange Pi One — первый запуск ✅ (2026-05-04 ~03:40 UTC)
- IP: `192.168.2.168` (DHCP от ноутбука, MAC: `02:81:21:28:5e:69`)
- Hostname: `orangepione`, интерфейс: `end0`
- ОС: Armbian 6.12.74-current-sunxi, armv7l
- Диск: 29G, FS расширена, 27G свободно
- RAM: 485 МБ, температура ~58°C
- SSH: `ssh orangepione` (ключ скопирован)
- Подключение: прямой LAN кабель ноутбук↔OPi, DHCP через dnsmasq на enp0s25 (192.168.2.1/24)

### Orange Pi One — полная настройка ✅ (2026-05-04 ~04:15 UTC)

#### Пользователи
- root: пароль `argos2024`
- ava: пароль `argos2024`, sudo, SSH ключ скопирован

#### Сеть
- LAN: `192.168.2.168/24` (DHCP от ноутбука через dnsmasq)
- Интернет: NAT через wlp3s0 ноутбука (`iptables MASQUERADE`)
- SSH локально: `ssh orangepione`
- SSH из интернета: `ssh orangepi-tunnel` → `ssh-orangepi.argosssss.win`

#### Cloudflare туннель
- Туннель: `orangepi` (ID: `bf451038-e9d0-4a55-8bfd-95f6af283c59`)
- DNS: `ssh-orangepi.argosssss.win`
- Сервис: `cloudflared.service` active ✅

#### GPIO/I2C/UART/SPI
- Overlays в `/boot/armbianEnv.txt`: `i2c0 i2c1 spi-spidev uart1 uart2`
- `/dev/i2c-0` — уже доступен ✅
- `/dev/ttyUSB0`, `/dev/ttyUSB1` — NodeMCU v3 и CC2350 (CH340) ✅
- `/dev/ttyS0-7` — аппаратные UART ✅
- SPI: будет после ребута

#### USB устройства на Orange Pi
- Hub: Terminus Technology 1a40:0101
- CH340 ×2 (1a86:7523) — NodeMCU v3 + CC2350 Zigbee
- WiFi адаптер — не определён (нужны драйвера или перезагрузка)

#### ARGOS IoT агент
- Путь: `/opt/argos-iot/argos_agent.py`
- Порт: `:7777` → JSON статус (temp, serial, I2C)
- Сервис: `argos-iot.service` active ✅
- ARGOS bridge: `/root/orangepi_bridge.py`

#### Нужно
- [ ] Ребут Orange Pi (активирует SPI overlays)
- [ ] Найти и подключить WiFi адаптер (driver?)
- [ ] Настроить NodeMCU v3 прошивку
- [ ] Интеграция CC2350 Zigbee → Home Assistant или ARGOS

### NodeMCU v3 (ESP8266) — WiFi мост ✅ (2026-05-04 ~06:55 UTC)
- Чип: ESP8266EX, 4MB flash, MAC: `8c:4f:00:58:3a:fd`
- Порт: `/dev/ttyUSB0` на Orange Pi
- Прошивка: **MicroPython v1.24.1** (2024-11-29)
- WiFi: подключён к **SiG** → IP `192.168.1.181`
- boot.py записан → автоподключение при старте
- Инструменты: esptool v5.2.0, mpremote v1.28.0 (на Orange Pi)

### EDUP WiFi адаптер — не работает
- USB enumeration fails: `device not accepting address, error -71`
- Причина: нехватка питания или неисправность
- Решение: NodeMCU v3 ESP8266 используется вместо него

### Устройства Orange Pi — итоговый список
| Устройство | Порт | Статус |
|-----------|------|--------|
| NodeMCU v3 ESP8266 | /dev/ttyUSB0 | ✅ MicroPython, WiFi SiG |
| CC2350 Zigbee | /dev/ttyUSB1 | ✅ подключён |
| Raspberry Pi Pico | /dev/ttyACM0 | ✅ подключён |
| I2C x3 | /dev/i2c-0,1,2 | ✅ |
| SPI | нет | ждёт ребута OPi |

### PB_MCU01_H503A (STM32H503) — диагностика (2026-05-04)
- Плата: Одноплатный компьютер PB_MCU01_H503A от Полярного Медведя (pb-embedded.ru)
- Чип: STM32H503 Cortex-M33, 250 МГц, 128KB flash
- USB DFU: не работает (error -71/-32 на xhci/ehci при энумерации)
- ST-Link V2: VTarget=3.23V ✅, IDCODE=0x6ba02477 считан однократно
- J-Link V9: "cannot read IDR" — неверное подключение проводов
- Итог: чип признан нерабочим, плата отложена
- Инструменты установлены: dfu-util, stlink, stm32flash, pyocd, openocd

### ESP32-2432S024 — настройка и прошивка ✅ (2026-05-05)
- Чип: ESP32-D0WD-V3 rev3.1, 240MHz, 4MB flash, MAC: b0:cb:d8:c2:6b:d8
- Дисплей: ILI9341 320x240 TFT (SPI: MOSI=13,CLK=14,CS=15,DC=2,RST=12,BL=27)
- Сенсор: встроенный датчик температуры ESP32 (~52°C)
- Прошивка: MicroPython v1.24.1 + boot.py (WiFi SiG, HTTP сервер :80)
- IP: 192.168.1.211 (WiFi SiG)
- ARGOS: `curl http://192.168.1.211/msg?text=...` / `esp32_2432_send(text)`
- Порт: /dev/ttyUSB0 на ноутбуке (CH340, 115200 baud)

### Cloudflare туннели — обновление (2026-05-08)

#### Ноутбук (laptop tunnel 525a)
- ssh-laptop.argosssss.win → ssh://localhost:22 ✅
- ollama-laptop.argosssss.win → localhost:11434 (⚠️ WAF блокирует API)
- ollama-pc.argosssss.win → localhost:12434/SSH туннель (⚠️ WAF)
- mcp-laptop.argosssss.win → localhost:8000 (⚠️ WAF)
- iot.argosssss.win → 192.168.2.168:7777 (⚠️ WAF + OPi недоступен)
- `/etc/cloudflared/config.yml` обновлён

#### Orange Pi (orangepi tunnel bf45)
- ssh-orangepi.argosssss.win → ssh://localhost:22 ✅
- iot.argosssss.win добавлен в конфиг (IoT агент :7777)

#### ПК (argos tunnel d400)
- Все старые маршруты сохранены
- ollama-pc.argosssss.win → localhost:11434 (исправлен WSL IP)

#### Рабочие Ollama эндпоинты (без WAF)
- `https://myollama123.ngrok.io` — Ollama ПК ✅ (ngrok)
- `http://localhost:12434` — Ollama ПК ✅ (SSH туннель)
- `http://localhost:11434` — Ollama ноутбук ✅ (локально)

#### Ollama helper
- `/home/ava/.local/bin/ask_ollama.py` — авто-роутинг через ngrok/SSH

### Сессия 2026-05-08 — Итог дня

#### Обучение модели (A100 / Mistral NeMo 12B)
- Датасет v2: 940 уникальных + 145 синтетических ARGOS примеров
- Загружено на HF: `AvaSiG/argos-dataset` → argos_train_v2.jsonl + val
- HF токен актуальный: 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
- Colab готов: `colab/ARGOS_A100_Train_Final.ipynb` (9 ячеек, авто-HF, GGUF)
- Целевая модель: `AvaSiG/argos-mistral-12b` → GGUF Q4_K_M для V100

#### Ollama / GPU доступ
- SSH туннель: localhost:12434 → ПК:11434
- ngrok: https://myollama123.ngrok.io (llama3.1:8b на ПК)
- Хелпер: `/home/ava/.local/bin/ask_ollama.py`
- ПК модели (через ngrok/SSH): ds-coder-v2, deepseek-v2:16b, qwen2.5:3b

#### Cloudflare обновление
- /etc/cloudflared/config.yml исправлен (был orangepi, стал laptop 525a)
- Новые маршруты: ollama-laptop, mcp-laptop, iot (через LAN к OPi)
- WAF блокирует API запросы к *.argosssss.win — нужно отключить в дашборде

#### Устройства (актуальный статус)
- ESP32-2432S024: 192.168.1.211 | ILI9341 TFT | ARGOS UI | HTTP :80 ✅
- ESP8266 NodeMCU: 192.168.1.181 | OLED SDA=GPIO14 SCL=GPIO12 | HTTP :80 ✅
- Orange Pi: 192.168.2.168 | Armbian | IoT агент :7777 | cloudflared ✅
- Pico: /dev/ttyACM0 | MicroPython v1.24.1 ✅
- XGecu T48: USB программатор ✅ (udev настроен)
- PB_MCU01 H503A: STM32H503 — нерабочий, отложен

#### Итог 2 месяца кода
- ARGOS v2.1.4: 51 навык, P2P, 10+ AI провайдеров, Telegram, IoT, GPU кластер
- Железо: X230 + ПК (3 GPU) + OPi + ESP32 + ESP8266 + Pico + NodeMCU
- Своя модель: датасет 940 примеров, пайплайн на A100 готов
- Инфра: Cloudflare + ngrok + SSH туннели + dnsmasq

**Спать. Продолжение завтра.**

---

## 2026-05-09 — Сессия 8 (Zigbee + HA + STM32)

### Zigbee2MQTT — запущен ✅
- **CC2531** (Texas Instruments ZStack12) — `/dev/ttyACM0` на ноутбуке
- Z2M 2.10.1 в Docker, adapter: zstack, 115200 baud
- Фронтенд: http://localhost:8099, MQTT → HA → 34 entity

### ZB-GW04 v1.2 (ZYZBP008, EFR32MG21)
- Прошивка: EmberZNet 7.4.5.0, протокол EZSP, 115200 baud
- Требует `rts_dtr` reset для инициализации (RTS+DTR HIGH → release RTS → release DTR)
- Работал на ноутбуке через Z2M Docker (ember adapter + патч ash.js)
- Сейчас подключён к Orange Pi — пробуем на ПК (Windows)

### STM32H503 (PB MCU01 H503A) — мёртвый USB
- ARM Cortex-M33, 250MHz
- USB не перечисляется (error -71/-32) — повреждена USB схема (D+/D- или часовой кристалл)
- Чип ЖИВ — диод реагирует, ошибка EPIPE означает ответ от устройства
- **Восстановление**: UART загрузчик через CH340 → PA9/PA10 + BOOT0=HIGH
- Инструмент: `stm32flash` или STM32CubeProgrammer через COM порт

### Home Assistant
- JWT токен: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3...
- Ollama AI: conversation.argos_ai_llama3_1_8b (ngrok: myollama123.ngrok.io)
- ARGOS сенсоры X230+OPi в HA через MQTT

### ARGOS Railway деплой ✅ (2026-05-09)
- URL: https://argos-v2-production.up.railway.app
- Проект: patient-spontaneity | Сервис: argos-v2
- GitHub: winargos42-dotcom/argos (main)
- Эндпоинты: / /health /mcp /ask /status
- Env: ARGOS_PC_URL, OLLAMA_URL, HF_TOKEN
- Токены Railway: 3464571a... (workspace), 7b22c292... (account)
- GitHub winargos42-dotcom: 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

---

## 2026-05-10 — Сессия 9 (Zigbee на ПК + Smart Life)

### Обновления
- **Ноутбук**: pacman -Syu ✅ (code/telegram-desktop пропущены — медленное зеркало)
- **Orange Pi**: apt upgrade ✅

### Zigbee2MQTT на ПК (Windows)
- **CC2531** подключён к ПК: COM14 (VID_0451:PID_16A8)
- Z2M 2.10.1 установлен глобально: `npm install -g zigbee2mqtt`
- Запуск: `set ZIGBEE2MQTT_DATA=C:\Users\AvA\zigbee2mqtt\data && set Z2M_ONBOARD_NO_SERVER=1 && zigbee2mqtt`
- MQTT: mqtt://192.168.1.53:1883 (ноутбук, mosquitto)
- Фронтенд: http://192.168.1.66:8099
- Автозапуск: Task Scheduler "Zigbee2MQTT" при входе AvA
- HA видит Bridge: binary_sensor.zigbee2mqtt_bridge_connection_state = on ✅

### Устройства (мёртвые/не подключены)
- **STM32H503 (PB MCU01 H503A)**: ARM Cortex-M33 — USB не работает (error -71/-32), чип жив (LED реагирует). Восстановление через UART: PA9/PA10 + BOOT0=HIGH + `stm32flash`
- **ZB-GW04 v1.2 (ZYZBP008/EFR32MG21)**: EFR32 не отвечает на OPi. На ноутбуке работал (EZSP 7.4.5 при 115200, rts_dtr reset). Отложен.

### Smart Life / Tuya
- Нужна авторизация через браузер: http://localhost:8123 → Settings → Devices & Services → Add Integration → Tuya → QR код → Smart Life app
- Или через iot.tuya.com: Access ID + Secret

### Текущая сеть устройств
| Устройство | Подключение | Статус |
|-----------|-------------|--------|
| CC2531 | ПК COM14 → Z2M → MQTT | ✅ координатор |
| Orange Pi One | LAN 192.168.2.168 | ✅ IoT агент :7777, can0 |
| ZB-GW04 (EFR32MG21) | Orange Pi ttyUSB0 | ⚠️ Z2M не стартует |
| Home Assistant | localhost:8123 | ✅ 72 entity |
| ARGOS | localhost:8000 MCP | ✅ Kimi+DeepSeek |
| Ollama | myollama123.ngrok.io | ✅ llama3.1:8b в HA |

### P2P Mesh ARGOS (2026-05-10)
- Token: `b3ca6dc602a6738b1d643f5010ee0751...`
- Ноды: ПК, Ноутбук, Orange Pi, Railway
- Peers: ws://192.168.1.66:8000 | ws://192.168.1.53:8000 | ws://192.168.2.168:8000 | wss://argos-v2-production.up.railway.app

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[SharedMemory Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `shared/JOURNAL.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[SharedMemory Hub]]
