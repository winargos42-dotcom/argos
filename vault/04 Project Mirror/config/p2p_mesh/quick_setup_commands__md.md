---
argos_import: project_file
source_path: config/p2p_mesh/quick_setup_commands.md
source_abs: F:\debug\argoss\config\p2p_mesh\quick_setup_commands.md
source_ext: .md
source_sha256: c99cd84506936902a0dfe8e76ac609108e921d1291581d0eb3376941aefe27ea
text_sha256: c99cd84506936902a0dfe8e76ac609108e921d1291581d0eb3376941aefe27ea
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:59
---

# quick_setup_commands.md

- Source: `config/p2p_mesh/quick_setup_commands.md`
- Extract: `text`
- SHA256: `c99cd84506936902a0dfe8e76ac609108e921d1291581d0eb3376941aefe27ea`

## Content

# Быстрые команды для настройки P2P сети ARGOS на Azure

## 1. Настройка Azure VM 1 (20.53.240.36)

### SSH подключение:
```bash
ssh azureuser@20.53.240.36
```

### Установка WireGuard:
```bash
sudo apt update
sudo apt install -y wireguard wireguard-tools
```

### Генерация ключей:
```bash
wg genkey | sudo tee /etc/wireguard/private.key
sudo cat /etc/wireguard/private.key | wg pubkey | sudo tee /etc/wireguard/public.key
```

### Показать публичный ключ:
```bash
sudo cat /etc/wireguard/public.key
```

## 2. Настройка Azure VM 2 (40.81.208.101)

### SSH подключение:
```bash
ssh azureuser@40.81.208.101
```

### Установка WireGuard:
```bash
sudo apt update
sudo apt install -y wireguard wireguard-tools
```

### Генерация ключей:
```bash
wg genkey | sudo tee /etc/wireguard/private.key
sudo cat /etc/wireguard/private.key | wg pubkey | sudo tee /etc/wireguard/public.key
```

### Показать публичный ключ:
```bash
sudo cat /etc/wireguard/public.key
```

## 3. Настройка Japan VM (ARGOS сервис)

### Проверить статус ARGOS:
```powershell
az vm run-command invoke -g RG-ARGOS -n argos-vm-jp_27e38b15 `
  --command-id RunShellScript `
  --scripts "systemctl status argos" `
  --query "value[0].message" -o tsv
```

### Перезапустить ARGOS:
```powershell
az vm run-command invoke -g RG-ARGOS -n argos-vm-jp_27e38b15 `
  --command-id RunShellScript `
  --scripts "systemctl restart argos" `
  --query "value[0].message" -o tsv
```

## 4. Проверка сети с локального Windows

### PowerShell проверка:
```powershell
# Проверить Azure VM 1
Test-NetConnection -ComputerName 20.53.240.36 -Port 22
Test-NetConnection -ComputerName 20.53.240.36 -Port 51820
Test-NetConnection -ComputerName 20.53.240.36 -Port 55771

# Проверить Azure VM 2
Test-NetConnection -ComputerName 40.81.208.101 -Port 22
Test-NetConnection -ComputerName 40.81.208.101 -Port 51821
Test-NetConnection -ComputerName 40.81.208.101 -Port 55771

# Проверить WG-Easy
Invoke-WebRequest -Uri "http://40.81.208.101:51821/" -TimeoutSec 5
```

### Bash проверка (WSL/Git Bash):
```bash
# Проверить порты
nc -zv 20.53.240.36 22
nc -zv 20.53.240.36 51820
nc -zv 20.53.240.36 55771

nc -zv 40.81.208.101 22
nc -zv 40.81.208.101 51821
nc -zv 40.81.208.101 55771
```

## 5. Настройка WireGuard конфигурации

### Конфиг для Azure VM 1 (сохранить как /etc/wireguard/wg0.conf):
```
[Interface]
PrivateKey = <AZURE1_PRIVATE_KEY>
Address = 10.100.0.2/24
ListenPort = 51820
MTU = 1420

[Peer]
# Локальный Windows
PublicKey = <LOCAL_PUBLIC_KEY>
AllowedIPs = 10.100.0.1/32
PersistentKeepalive = 25

[Peer]
# Azure VM 2
PublicKey = <AZURE2_PUBLIC_KEY>
Endpoint = 40.81.208.101:51820
AllowedIPs = 10.100.0.3/32
PersistentKeepalive = 25
```

### Конфиг для Azure VM 2 (сохранить как /etc/wireguard/wg0.conf):
```
[Interface]
PrivateKey = <AZURE2_PRIVATE_KEY>
Address = 10.100.0.3/24
ListenPort = 51820
MTU = 1420

[Peer]
# Локальный Windows
PublicKey = <LOCAL_PUBLIC_KEY>
AllowedIPs = 10.100.0.1/32
PersistentKeepalive = 25

[Peer]
# Azure VM 1
PublicKey = <AZURE1_PUBLIC_KEY>
Endpoint = 20.53.240.36:51820
AllowedIPs = 10.100.0.2/32
PersistentKeepalive = 25
```

## 6. Запуск WireGuard

### На Azure VM:
```bash
# Включить IP forwarding
echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Настроить firewall
sudo ufw allow 51820/udp
sudo ufw allow 55771/tcp
sudo ufw allow 55772/udp
sudo ufw allow 8000/tcp
sudo ufw --force enable

# Запустить WireGuard
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0

# Проверить статус
sudo wg show
```

## 7. Проверка P2P сети

### Проверить подключение между узлами:
```bash
# С Azure VM 1
ping 10.100.0.3  # К Azure VM 2
ping 10.100.0.1  # К локальному Windows

# С Azure VM 2
ping 10.100.0.2  # К Azure VM 1
ping 10.100.0.1  # К локальному Windows
```

### Проверить P2P порты:
```bash
# Проверить, что порты слушают
ss -tulpn | grep -E '(55771|55772|8000)'

# Проверить подключение к Japan VM
curl http://argos-vm-jp_27e38b15:8000/status 2>/dev/null || echo "ARGOS сервис не отвечает"
```

## 8. Быстрые команды для копирования

### Копировать конфиги на Azure VM:
```bash
# На Azure VM 1
scp wireguard_azure1.conf azureuser@20.53.240.36:/tmp/wg0.conf
ssh azureuser@20.53.240.36 "sudo cp /tmp/wg0.conf /etc/wireguard/"

# На Azure VM 2
scp wireguard_azure2.conf azureuser@40.81.208.101:/tmp/wg0.conf
ssh azureuser@40.81.208.101 "sudo cp /tmp/wg0.conf /etc/wireguard/"
```

### Проверить всю сеть одной командой:
```powershell
.\check_azure_p2p.ps1
```

## 9. Устранение неполадок

### Если порты не открыты:
```powershell
# Проверить NSG правила
az network nsg rule list -g rg-argos --nsg-name argos-vm-nsg --query "[].{Name:name, Port:destinationPortRange, Protocol:protocol}" -o table
az network nsg rule list -g rg-argos --nsg-name basicNsgvnet-japaneast-nic01 --query "[].{Name:name, Port:destinationPortRange, Protocol:protocol}" -o table
```

### Если WireGuard не запускается:
```bash
# Проверить журналы
sudo journalctl -u wg-quick@wg0 -f

# Проверить конфиг
sudo wg-quick strip wg0
```

### Если ARGOS не отвечает:
```powershell
# Проверить Japan VM
az vm run-command invoke -g RG-ARGOS -n argos-vm-jp_27e38b15 `
  --command-id RunShellScript `
  --scripts "ps aux | grep python | grep -v grep" `
  --query "value[0].message" -o tsv
```

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
