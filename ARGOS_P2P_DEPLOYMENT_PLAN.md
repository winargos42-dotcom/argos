# ПЛАН РАЗВЁРТЫВАНИЯ P2P СЕТИ ARGOS

## ТЕКУЩЕЕ СОСТОЯНИЕ

### ✅ Australia VM (`argos-vm`, `20.53.240.36`)
- ARGOS установлен в `/home/argos/Argos/`
- P2P включён: `ARGOS_P2P_ENABLED=true`
- P2P порт: `8000` (работает)
- MCP порт: `8000` (работает)
- Network secret: `argos_net_secret_2026`

### 🚧 Japan VM (`argos-vm-jp_27e38b15`, `40.81.208.101`)
- Создан `.env` с P2P настройками
- Запускается MCP сервер на порту 8000
- ARGOS нужно установить из `src.zip`

### 🔧 Japan VM 2 (`argos-vm-jp_079c3df3`, `172.207.209.134`)
- Не настроена
- Можно использовать как резервный узел

## ПЛАН РАЗВЁРТЫВАНИЯ

### ФАЗА 1: УСТАНОВКА ARGOS НА JAPAN VM

```powershell
# 1. Скачать ARGOS
az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "
cd /home/ava/argoss &&
wget https://argdeploy6683.blob.core.windows.net/deploy/src.zip -O src.zip &&
unzip -o src.zip &&
echo 'ARGOS скачан'"

# 2. Проверить структуру
az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "
ls -la /home/ava/argoss/ &&
ls -la /home/ava/argoss/src/"

# 3. Запустить ARGOS
az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "
cd /home/ava/argoss &&
python3 main.py --no-gui > argos.log 2>&1 &
sleep 3 &&
ps aux | grep python"

# 4. Проверить P2P соединение
az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "
curl -s http://localhost:8000/health &&
curl -s http://20.53.240.36:8000/health"
```

### ФАЗА 2: НАСТРОЙКА WIREGUARD ДЛЯ НАДЁЖНОСТИ

```powershell
# 1. Установить WireGuard на обе VM
az vm run-command invoke -g rg-argos -n argos-vm --command-id RunShellScript --scripts "
sudo apt update &&
sudo apt install -y wireguard wireguard-tools &&
wg genkey | tee /tmp/private.key &&
wg pubkey < /tmp/private.key > /tmp/public.key &&
echo 'Australia VM ключи сгенерированы'"

az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "
sudo apt update &&
sudo apt install -y wireguard wireguard-tools &&
wg genkey | tee /tmp/private.key &&
wg pubkey < /tmp/private.key > /tmp/public.key &&
echo 'Japan VM ключи сгенерированы'"

# 2. Получить ключи
# Australia VM private key
az vm run-command invoke -g rg-argos -n argos-vm --command-id RunShellScript --scripts "cat /tmp/private.key"

# Australia VM public key  
az vm run-command invoke -g rg-argos -n argos-vm --command-id RunShellScript --scripts "cat /tmp/public.key"

# Japan VM private key
az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "cat /tmp/private.key"

# Japan VM public key
az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "cat /tmp/public.key"
```

### ФАЗА 3: СОЗДАНИЕ КОНФИГОВ WIREGUARD

**Australia VM конфиг:**
```bash
[Interface]
Address = 10.100.0.1/20
PrivateKey = <AUS_PRIVATE_KEY>
ListenPort = 51820
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# Japan VM
PublicKey = <JP_PUBLIC_KEY>
Endpoint = 40.81.208.101:51820
AllowedIPs = 10.100.0.2/32
PersistentKeepalive = 25
```

**Japan VM конфиг:**
```bash
[Interface]
Address = 10.100.0.2/20
PrivateKey = <JP_PRIVATE_KEY>
ListenPort = 51820
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# Australia VM
PublicKey = <AUS_PUBLIC_KEY>
Endpoint = 20.53.240.36:51820
AllowedIPs = 10.100.0.1/32
PersistentKeepalive = 25
```

### ФАЗА 4: ЗАПУСК WIREGUARD И ПРОВЕРКА

```powershell
# Australia VM
az vm run-command invoke -g rg-argos -n argos-vm --command-id RunShellScript --scripts "
echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf &&
sudo sysctl -p &&
sudo cp /tmp/wg0.conf /etc/wireguard/wg0.conf &&
sudo chmod 600 /etc/wireguard/wg0.conf &&
sudo wg-quick up wg0 &&
sudo systemctl enable wg-quick@wg0 &&
sudo wg show"

# Japan VM
az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "
echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf &&
sudo sysctl -p &&
sudo cp /tmp/wg0.conf /etc/wireguard/wg0.conf &&
sudo chmod 600 /etc/wireguard/wg0.conf &&
sudo wg-quick up wg0 &&
sudo systemctl enable wg-quick@wg0 &&
sudo wg show"

# Проверка связи
az vm run-command invoke -g rg-argos -n argos-vm --command-id RunShellScript --scripts "ping -c 3 10.100.0.2"
az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "ping -c 3 10.100.0.1"
```

### ФАЗА 5: ИНТЕГРАЦИЯ ARGOS P2P С WIREGUARD

```powershell
# Australia VM - обновить .env для использования WireGuard IP
az vm run-command invoke -g rg-argos -n argos-vm --command-id RunShellScript --scripts "
sed -i 's/ARGOS_P2P_PUBLIC_IP=20.53.240.36/ARGOS_P2P_PUBLIC_IP=10.100.0.1/g' /home/argos/Argos/.env &&
echo 'ARGOS_P2P_PEERS=10.100.0.2' >> /home/argos/Argos/.env"

# Japan VM - обновить .env
az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "
sed -i 's/ARGOS_P2P_PEERS=20.53.240.36/ARGOS_P2P_PEERS=10.100.0.1/g' /home/ava/argoss/.env &&
echo 'ARGOS_P2P_PUBLIC_IP=10.100.0.2' >> /home/ava/argoss/.env"

# Перезапустить ARGOS
az vm run-command invoke -g rg-argos -n argos-vm --command-id RunShellScript --scripts "
pkill -f 'python.*main.py' &&
cd /home/argos/Argos &&
python3 main.py --no-gui > argos.log 2>&1 &"

az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "
pkill -f 'python.*main.py' &&
cd /home/ava/argoss &&
python3 main.py --no-gui > argos.log 2>&1 &"
```

## АРХИТЕКТУРА ПОСЛЕ РАЗВЁРТЫВАНИЯ

```
Australia VM (20.53.240.36)
├── Public IP: 20.53.240.36
├── WireGuard IP: 10.100.0.1
├── ARGOS P2P порт: 8000
├── MCP порт: 8000
└── WireGuard порт: 51820
    │
    └── Japan VM (40.81.208.101)
        ├── Public IP: 40.81.208.101
        ├── WireGuard IP: 10.100.0.2
        ├── ARGOS P2P порт: 8000
        ├── MCP порт: 8000
        └── WireGuard порт: 51820
```

## ПРЕИМУЩЕСТВА ТАКОЙ АРХИТЕКТУРЫ

1. **Надёжность**: WireGuard обеспечивает стабильный туннель поверх интернета
2. **Безопасность**: Все данные шифруются
3. **Производительность**: Прямое P2P соединение
4. **Гибкость**: Можно добавлять новые узлы
5. **Резервирование**: Если публичный IP изменится, WireGuard туннель останется

## СЛЕДУЮЩИЕ ШАГИ

1. **Добавить Japan VM 2** (`argos-vm-jp_079c3df3`) в сеть
2. **Добавить Windows PC** через WireGuard
3. **Добавить Google Cloud** VM
4. **Настроить мониторинг** сети
5. **Реализовать автоматическое восстановление**

## КОМАНДЫ ДЛЯ БЫСТРОГО СТАРТА

```powershell
# Просто запустить ARGOS на Japan VM
az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "cd /home/ava/argoss && python3 main.py --no-gui &"

# Проверить соединение
az vm run-command invoke -g rg-argos -n argos-vm --command-id RunShellScript --scripts "curl -s http://40.81.208.101:8000/health"
az vm run-command invoke -g rg-argos -n argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "curl -s http://20.53.240.36:8000/health"
```