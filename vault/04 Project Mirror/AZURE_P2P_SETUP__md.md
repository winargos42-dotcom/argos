---
argos_import: project_file
source_path: AZURE_P2P_SETUP.md
source_abs: F:\debug\argoss\AZURE_P2P_SETUP.md
source_ext: .md
source_sha256: 6527d4950f3c9c4a7edbab0428a4178593bd8a43905f84fcee9dd8c646f29c29
text_sha256: 6527d4950f3c9c4a7edbab0428a4178593bd8a43905f84fcee9dd8c646f29c29
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# AZURE_P2P_SETUP.md

- Source: `AZURE_P2P_SETUP.md`
- Extract: `text`
- SHA256: `6527d4950f3c9c4a7edbab0428a4178593bd8a43905f84fcee9dd8c646f29c29`

## Content

# Azure VPN + P2P Network Setup

**Дата:** 2026-04-17 00:33  
**Проект:** ARGOS v2.1.3  
**Статус:** ✅ ГОТОВО

## 🎯 Что сделано

### 1. Созданы навыки для управления Azure и P2P сетями

**Azure VPN P2P Manager** (`src/skills/generated/azure_vpn_p2p_manager.py`):
- Управление VPN-сервером WireGuard на Azure VM
- Проверка подключения к Azure (`20.53.240.36`)
- Генерация команд для установки WireGuard
- Настройка Cloudflare DNS
- Создание конфигураций клиентов WireGuard
- Генерация QR-кодов для быстрого подключения
- Интеграция с P2P сетями

**P2P Network Manager** (`src/skills/generated/p2p_network_manager.py`):
- Управление P2P сетями (libp2p, mDNS, Kademlia)
- Проверка доступности пиров
- Сканирование сети на наличие узлов
- Генерация конфигураций libp2p
- Настройка WireGuard mesh сетей
- Интеграция с ZeroTier
- Создание P2P навыков

### 2. Интеграция с существующей системой

- Навыки используют конфигурацию из `.env` файла
- Автоматически определяют пиры из `ARGOS_P2P_PEERS`
- Работают с Azure VM из `ARGOS_VPN_SERVER_IP`
- Интегрируются с Evolution через AI Coder Bridge

### 3. Создана инфраструктура

```
config/
├── vpn/                    # Конфиги WireGuard
├── p2p/                    # Конфиги libp2p и P2P
└── integration/            # Совместные конфигурации
```

## 🚀 Как использовать

### Azure VPN Manager

```python
from src.skills.generated.azure_vpn_p2p_manager import AzureVpnP2pManager

manager = AzureVpnP2pManager()

# Проверить подключение к Azure VM
result = manager.execute("check")
print(result)

# Получить команды для установки WireGuard на Azure
commands = manager.execute("setup_wireguard")
print(commands)

# Настроить P2P сеть
result = manager.execute("p2p_setup")
print(result)

# Создать конфиг клиента
result = manager.execute("create_client", client_name="my_phone")
print(result)

# Получить статус
print(manager.report())
```

### P2P Network Manager

```python
from src.skills.generated.p2p_network_manager import P2PNetworkManager

manager = P2PNetworkManager()

# Проверить статус сети
result = manager.execute("status")
print(result)

# Сканировать сеть на наличие узлов
result = manager.execute("scan", subnet="192.168.1.0/24")
print(result)

# Создать конфиг libp2p
result = manager.execute("libp2p_config")
print(result)

# Создать P2P навык
result = manager.execute("create_skill", skill_name="ChatBroadcaster")
print(result)

# Получить статус
print(manager.report())
```

## 🔧 Конфигурация из .env

Навыки автоматически читают конфигурацию:

```bash
# Azure VM
ARGOS_VPN_SERVER_IP=20.53.240.36
ARGOS_VPN_PORT=51820

# P2P сеть
ARGOS_P2P_ENABLED=true
ARGOS_P2P_PEERS=20.53.240.36,40.81.208.101

# Cloudflare DNS
Cloudflaretoken=cfut_YUPHVEVQ7UXFMadd4drU8uq6xdtNQfv9VCXuFQ9sfe02c734
```

## 📋 Пошаговая настройка Azure VPN

### 1. Подключиться к Azure VM
```bash
ssh azureuser@20.53.240.36
```

### 2. Установить WireGuard (через менеджер)
```python
manager = AzureVpnP2pManager()
commands = manager.execute("setup_wireguard")
# Скопировать команды и выполнить на сервере
```

### 3. Настроить Cloudflare DNS
```python
result = manager.execute("cloudflare_dns", subdomain="vpn")
print(result)  # Получить команду curl для Cloudflare API
```

### 4. Создать клиентские конфиги
```python
# Для телефона
manager.execute("create_client", client_name="phone")

# Для роутера
manager.execute("create_client", client_name="router")

# Сгенерировать QR-код
manager.execute("qr", client_name="phone")
```

### 5. Настроить P2P сеть
```python
# На Azure VM
azure_manager.execute("p2p_setup")

# На локальной машине
p2p_manager.execute("libp2p_config")
```

## 🌐 P2P Network Architecture

```
Локальная машина (ARGOS) ←→ Azure VM (WireGuard VPN)
        │                            │
        ├── libp2p (порт 8000)       ├── libp2p (порт 8000)
        ├── mDNS discovery           ├── Kademlia DHT
        └── WireGuard mesh           └── WireGuard server
```

**Протоколы:**
- **Discovery**: mDNS (локальная сеть) + Kademlia DHT (глобальная)
- **Transport**: TCP + WebSocket + WireGuard UDP
- **Security**: Noise protocol + WireGuard encryption
- **Messaging**: gossipsub (pub/sub) + request-response

## 🛠️ Дополнительные возможности

### WireGuard Mesh Network
```python
peers = [
    {"name": "node1", "public_key": "...", "endpoint": "10.0.0.1:51830", "allowed_ips": "10.100.0.2/32"},
    {"name": "node2", "public_key": "...", "endpoint": "10.0.0.2:51830", "allowed_ips": "10.100.0.3/32"}
]
result = p2p_manager.execute("wireguard_mesh", peers=peers)
```

### ZeroTier (альтернатива)
```python
commands = p2p_manager.execute("zerotier", network_id="YOUR_NETWORK_ID")
```

### Создание кастомных P2P навыков
```python
result = p2p_manager.execute("create_skill", skill_name="FileSharer")
# Создаёт навык для обмена файлами через P2P
```

## 📊 Мониторинг

### Проверка состояния
```python
# Azure VPN статус
azure_status = azure_manager.execute("check")

# P2P сеть статус
p2p_status = p2p_manager.execute("status")

# Сканирование сети
scan_results = p2p_manager.execute("scan", subnet="192.168.1.0/24")
```

### Логи
```
logs/argos.azure_vpn_p2p_manager.log
logs/argos.p2p_network_manager.log
```

## 🔐 Безопасность

1. **WireGuard**: современная криптография (Curve25519, ChaCha20)
2. **libp2p**: Noise protocol для P2P соединений
3. **Ключи**: автоматическая генерация, хранение в защищённых файлах
4. **Доступ**: только авторизованные пиры из `.env`

## 🚨 Устранение неполадок

### Проблема: Не подключается к Azure VM
```python
# Проверить SSH доступ
manager.execute("check")

# Решения:
# 1. Проверить firewall правила в Azure Portal
# 2. Убедиться что IP статический
# 3. Проверить SSH ключи
```

### Проблема: P2P пиры недоступны
```python
# Проверить каждого пира
for peer in manager.p2p_peers:
    result = manager.check_peer_connectivity(peer)
    print(f"{peer}: {result['status']}")

# Решения:
# 1. Проверить порты (8000, 51820)
# 2. Проверить firewall
# 3. Добавить пиры вручную
```

### Проблема: WireGuard не работает
```python
# Сгенерировать новые ключи
manager.execute("create_client", client_name="test")

# Решения:
# 1. Проверить порт 51820 (UDP) открыт
# 2. Перегенерировать ключи
# 3. Использовать WG-Easy через Docker
```

## 📈 Дальнейшее развитие

1. **Автоматическое развёртывание**: Terraform/Ansible для Azure
2. **Мониторинг**: Grafana dashboard для VPN и P2P метрик
3. **Масштабирование**: Kubernetes для P2P узлов
4. **Интеграция**: Home Assistant, IoT устройства через P2P
5. **Блокчейн**: децентрализованная идентификация через ZKP

## 📞 Поддержка

- **Файлы навыков**: `src/skills/generated/`
- **Конфигурация**: `config/vpn/`, `config/p2p/`
- **Логи**: `logs/`
- **Документация**: этот файл и `src/skills/generated/*.py`

---

**Статус:** ✅ СИСТЕМА ГОТОВА К ИСПОЛЬЗОВАНИЮ  
**Следующие шаги:** Запустить `manager.execute("check")` для проверки Azure VM

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
