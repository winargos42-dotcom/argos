---
argos_import: project_file
source_path: wg/README_SE_FIX.md
source_abs: F:\debug\argoss\wg\README_SE_FIX.md
source_ext: .md
source_sha256: 9215eaa4b18f2c9dbd6a35fc1fe7587029e611bd9e2a07ed71ea2d384c655c5f
text_sha256: 9215eaa4b18f2c9dbd6a35fc1fe7587029e611bd9e2a07ed71ea2d384c655c5f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:48
---

# README_SE_FIX.md

- Source: `wg/README_SE_FIX.md`
- Extract: `text`
- SHA256: `9215eaa4b18f2c9dbd6a35fc1fe7587029e611bd9e2a07ed71ea2d384c655c5f`

## Content

# README - Исправление WireGuard на SE VM

## Проблема
SE (Sweden) VM показывает OFFLINE в dashboard. Конфигурация WireGuard неполная.

## Исправлено
✅ Добавлен публичный ключ PC в конфиг SE VM
✅ Создан скрипт настройки `setup_se_wg.sh`

## Развёртывание

### Вариант 1: Через EXT VM (Jump Host)
```powershell
# Копируем скрипт на EXT VM
scp -i ~/.ssh/argos_key F:\debug\argoss\wg\setup_se_wg.sh azureuser@47.237.24.124:/tmp/

# Подключаемся к EXT и запускаем на SE через него
ssh -i ~/.ssh/argos_key azureuser@47.237.24.124
# На EXT VM:
ssh -i ~/.ssh/argos_key azureuser@10.200.0.4 "sudo bash /tmp/setup_se_wg.sh"
```

### Вариант 2: Через Azure Portal
1. Открыть Azure Portal → SE VM → Serial console
2. Выполнить команды:
```bash
sudo su
curl -o /tmp/setup_se_wg.sh https://raw.githubusercontent.com/.../setup_se_wg.sh
sudo bash /tmp/setup_se_wg.sh
```

### Вариант 3: Локально на SE
1. Подключиться к SE через Azure Bastion или Serial Console
2. Выполнить:
```bash
cd /tmp
cat > setup_se_wg.sh << 'ENDOFSCRIPT'
[PASTE SCRIPT CONTENT HERE]
ENDOFSCRIPT
sudo bash setup_se_wg.sh
```

## Проверка после настройки
```bash
# На SE VM
wg show
ping 10.200.0.1  # AU
ping 10.200.0.6  # PC
```

## Ключи
- **PC Public Key:** `Uk2qGQwBtpbee+FZrdbVIBuSitiAUL5kzt9hxe+1xxY=`
- **SE IP:** `10.200.0.4`
- **SE Endpoint:** `20.240.192.35:51822`

## Статус нод
После исправления mesh должен показывать:
- ✅ AU (10.200.0.1) - Master
- ✅ JP1 (10.200.0.2) - Tokyo  
- ✅ JP2 (10.200.0.3) - Tokyo
- ✅ SE (10.200.0.4) - Stockholm
- ✅ EXT (10.200.0.5) - External
- ✅ PC (10.200.0.6) - Desktop

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
