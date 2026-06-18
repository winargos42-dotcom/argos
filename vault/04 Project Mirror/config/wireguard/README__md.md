---
argos_import: project_file
source_path: config/wireguard/README.md
source_abs: F:\debug\argoss\config\wireguard\README.md
source_ext: .md
source_sha256: 3034ea876b53794d44b0720b591bcf1329cedfbdb1079ad0e8cbdb5eb2013756
text_sha256: 3034ea876b53794d44b0720b591bcf1329cedfbdb1079ad0e8cbdb5eb2013756
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:59
---

# README.md

- Source: `config/wireguard/README.md`
- Extract: `text`
- SHA256: `3034ea876b53794d44b0720b591bcf1329cedfbdb1079ad0e8cbdb5eb2013756`

## Content

# P2P СЕТЬ ARGOS - ГОТОВЫЕ КОНФИГУРАЦИИ

## АРХИТЕКТУРА СЕТИ (5 УЗЛОВ)

1. **Australia VM** (`argos-vm`): `20.53.240.36` → WireGuard: `10.100.0.1`
2. **Japan VM 1** (`argos-vm-jp_079c3df3`): `172.207.209.134` → WireGuard: `10.100.0.2`
3. **Japan VM 2** (`argos-vm-jp_27e38b15`): `40.81.208.101` → WireGuard: `10.100.0.3`
4. **Windows PC**: → WireGuard: `10.100.0.4`
5. **Google Cloud**: → WireGuard: `10.100.0.5`

**Подсеть:** `10.100.0.0/20`
**Порт WireGuard:** `51820/UDP`

## КОМАНДЫ ДЛЯ РАЗВЁРТЫВАНИЯ

### 1. Australia VM
```bash
# Установка WireGuard
az vm run-command invoke --resource-group RG-ARGOS --name argos-vm --command-id RunShellScript --scripts "sudo apt update && sudo apt install -y wireguard wireguard-tools"

# Применение конфига
az vm run-command invoke --resource-group RG-ARGOS --name argos-vm --command-id RunShellScript --scripts "cat > /etc/wireguard/wg0.conf << 'EOF'
$(cat australia-vm.conf)
EOF && sudo chmod 600 /etc/wireguard/wg0.conf"

# Запуск
az vm run-command invoke --resource-group RG-ARGOS --name argos-vm --command-id RunShellScript --scripts "echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf && sudo sysctl -p && sudo wg-quick up wg0 && sudo systemctl enable wg-quick@wg0"
```

### 2. Japan VM 1
```bash
# Установка
az vm run-command invoke --resource-group RG-ARGOS --name argos-vm-jp_079c3df3 --command-id RunShellScript --scripts "sudo apt update && sudo apt install -y wireguard wireguard-tools"

# Конфиг (создать файл japan-vm-1.conf на основе australia-vm.conf с изменениями)
```

### 3. Japan VM 2
```bash
# Установка
az vm run-command invoke --resource-group RG-ARGOS --name argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "sudo apt update && sudo apt install -y wireguard wireguard-tools"

# Конфиг (создать файл japan-vm-2.conf)
```

### 4. Windows PC
1. Установите WireGuard: https://www.wireguard.com/install/
2. Импортируйте файл `windows-pc.conf`
3. Активируйте туннель

### 5. Google Cloud
1. Установите WireGuard на GCP VM
2. Используйте файл `google-cloud.conf`

## ПРОВЕРКА СЕТИ

```bash
# Из Windows
ping 10.100.0.1
ping 10.100.0.2
ping 10.100.0.3

# Из Australia VM
ping 10.100.0.4
ping 10.100.0.5
```

## КЛЮЧИ (одинаковые для всех узлов)
- **PrivateKey:** `5M1sUk7Wm0NDtIJOLK/aXcZZd/fAiNrMgImxWDYPrtY=`
- **PublicKey:** `5M1sUk7Wm0NDtIJOLK/aXcZZd/fAiNrMgImxWDYPrtY=`

**Внимание:** В реальной сети используйте уникальные ключи для каждого узла!

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
