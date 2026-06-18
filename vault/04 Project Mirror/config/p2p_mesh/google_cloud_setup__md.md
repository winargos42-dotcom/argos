---
argos_import: project_file
source_path: config/p2p_mesh/google_cloud_setup.md
source_abs: F:\debug\argoss\config\p2p_mesh\google_cloud_setup.md
source_ext: .md
source_sha256: 674cb201e750c007b178ce9483b0fbcfc8e69c6cf1f313fb986dc1efc9f117d4
text_sha256: 674cb201e750c007b178ce9483b0fbcfc8e69c6cf1f313fb986dc1efc9f117d4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:59
---

# google_cloud_setup.md

- Source: `config/p2p_mesh/google_cloud_setup.md`
- Extract: `text`
- SHA256: `674cb201e750c007b178ce9483b0fbcfc8e69c6cf1f313fb986dc1efc9f117d4`

## Content

# Google Cloud Setup for ARGOS P2P Network

**Дата:** 2026-04-17 00:55  
**Статус:** ⚠️ ТРЕБУЕТСЯ НАСТРОЙКА

## 🎯 Цель

Добавить Google Cloud узел в P2P сеть ARGOS для:
1. Географической избыточности (Azure EU + GCP US/Asia)
2. Резервного копирования данных
3. Балансировки нагрузки
4. Глобального покрытия VPN

## 📋 Требования

### Минимальные спецификации:
- **VM Type**: e2-micro или e2-small (бесплатный tier)
- **OS**: Ubuntu 22.04 LTS
- **Region**: us-central1 (Iowa) или europe-west4 (Netherlands)
- **Storage**: 10GB SSD
- **Network**: Статический внешний IP

### Порты для открытия:
- **22** - SSH
- **51820** - WireGuard (UDP)
- **8000** - ARGOS API (TCP)
- **443** - HTTPS (если нужен веб-интерфейс)

## 🚀 Быстрая настройка

### 1. Создать VM в Google Cloud

```bash
# Через gcloud CLI
gcloud compute instances create argos-gcp-node \
  --project=YOUR_PROJECT_ID \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-tier=PREMIUM \
  --maintenance-policy=MIGRATE \
  --provisioning-model=STANDARD \
  --service-account=default \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --tags=http-server,https-server,wireguard \
  --image=ubuntu-2204-jammy-v20240408 \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=10GB \
  --boot-disk-type=pd-balanced \
  --boot-disk-device-name=argos-gcp-node \
  --no-shielded-secure-boot \
  --shielded-vtpm \
  --shielded-integrity-monitoring \
  --reservation-affinity=any

# Установить статический IP
gcloud compute addresses create argos-gcp-ip \
  --project=YOUR_PROJECT_ID \
  --region=us-central1

gcloud compute instances delete-access-config argos-gcp-node \
  --project=YOUR_PROJECT_ID \
  --zone=us-central1-a \
  --access-config-name="external-nat"

gcloud compute instances add-access-config argos-gcp-node \
  --project=YOUR_PROJECT_ID \
  --zone=us-central1-a \
  --address=STATIC_IP_ADDRESS
```

### 2. Настроить firewall правила

```bash
# Открыть порты
gcloud compute firewall-rules create allow-wireguard \
  --project=YOUR_PROJECT_ID \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=udp:51820 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=wireguard

gcloud compute firewall-rules create allow-argos-api \
  --project=YOUR_PROJECT_ID \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:8000 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=http-server

gcloud compute firewall-rules create allow-ssh \
  --project=YOUR_PROJECT_ID \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:22 \
  --source-ranges=0.0.0.0/0
```

### 3. Установить ARGOS на GCP

```bash
# Подключиться к VM
gcloud compute ssh argos-gcp-node --zone=us-central1-a

# На VM выполнить:
sudo apt update
sudo apt upgrade -y

# Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установить WireGuard
sudo apt install -y wireguard wireguard-tools

# Создать ключи WireGuard
wg genkey | sudo tee /etc/wireguard/private.key
sudo cat /etc/wireguard/private.key | wg pubkey | sudo tee /etc/wireguard/public.key

# Настроить WireGuard
sudo nano /etc/wireguard/wg0.conf
```

### 4. Конфигурация WireGuard для GCP

```ini
[Interface]
PrivateKey = <GCP_PRIVATE_KEY>
Address = 10.100.0.4/24
ListenPort = 51820
MTU = 1420

[Peer]
# Azure VM 1
PublicKey = <AZURE1_PUBLIC_KEY>
Endpoint = 20.53.240.36:51820
AllowedIPs = 10.100.0.2/32
PersistentKeepalive = 25

[Peer]
# Azure VM 2
PublicKey = <AZURE2_PUBLIC_KEY>
Endpoint = 40.81.208.101:51820
AllowedIPs = 10.100.0.3/32
PersistentKeepalive = 25

[Peer]
# Локальный узел (Windows)
PublicKey = <LOCAL_PUBLIC_KEY>
Endpoint = <YOUR_PUBLIC_IP>:51830
AllowedIPs = 10.100.0.1/32
PersistentKeepalive = 25
```

### 5. Запустить сервисы

```bash
# Запустить WireGuard
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0

# Проверить статус
sudo wg show

# Установить ARGOS (опционально)
git clone https://github.com/your-org/argos.git
cd argos
docker-compose up -d
```

## 🔗 Интеграция с существующей P2P сетью

### Обновить конфигурацию на других узлах:

**На Azure VM 1 (20.53.240.36):**
```bash
sudo nano /etc/wireguard/wg0.conf
# Добавить:
[Peer]
# Google Cloud
PublicKey = <GCP_PUBLIC_KEY>
Endpoint = <GCP_STATIC_IP>:51820
AllowedIPs = 10.100.0.4/32
PersistentKeepalive = 25
```

**На Azure VM 2 (40.81.208.101):**
```bash
# В WG-Easy веб-интерфейсе добавить нового клиента
# Или в Docker контейнере:
docker exec -it wg-easy wg addconf wg0 <(echo "[Peer]...")
```

**На локальном узле (Windows):**
```powershell
# В конфиге WireGuard добавить:
[Peer]
PublicKey = <GCP_PUBLIC_KEY>
Endpoint = <GCP_STATIC_IP>:51820
AllowedIPs = 10.100.0.4/32
PersistentKeepalive = 25
```

## 📊 Мониторинг GCP узла

### Cloud Monitoring:
```bash
# Установить агент мониторинга
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
sudo bash add-google-cloud-ops-agent-repo.sh --also-install

# Проверить метрики
gcloud monitoring metrics list --filter='resource.type="gce_instance"'
```

### Создать dashboard:
```bash
# Экспорт метрик в Prometheus (опционально)
sudo apt install -y prometheus-node-exporter
```

## 🔐 Безопасность

### 1. IAM роли:
```bash
# Минимальные права
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:default" \
  --role="roles/monitoring.metricWriter"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:default" \
  --role="roles/logging.logWriter"
```

### 2. SSH ключи:
```bash
# Использовать только ключи, не пароли
gcloud compute os-login ssh-keys add \
  --key-file=~/.ssh/id_rsa.pub \
  --project=YOUR_PROJECT_ID
```

### 3. Network security:
```bash
# Включить VPC flow logs
gcloud compute networks subnets update default \
  --region=us-central1 \
  --enable-flow-logs
```

## 💰 Стоимость (примерно)

| Ресурс | Спецификация | Месячная стоимость |
|--------|-------------|-------------------|
| **VM** | e2-micro (2 vCPU, 1GB RAM) | ~$6.11 |
| **IP** | Статический внешний IP | ~$1.46 |
| **Диск** | 10GB SSD | ~$0.40 |
| **Трафик** | 100GB исходящий | ~$8.00 |
| **Итого** | | **~$16.00/мес** |

**Бесплатный tier:** e2-micro в us-central1, us-west1, us-east1 до 744 часов/мес

## 🚨 Устранение неполадок

### Проблема: WireGuard не подключается
```bash
# Проверить порт
sudo netstat -tulpn | grep 51820

# Проверить firewall
sudo iptables -L -n -v | grep 51820

# Проверить маршруты
ip route show table all
```

### Проблема: Высокая задержка
```bash
# Проверить сеть
mtr 20.53.240.36
tcpping 20.53.240.36 51820

# Оптимизировать MTU
sudo ip link set wg0 mtu 1280
```

### Проблема: Нет интернета через VPN
```bash
# Включить IP forwarding
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Настроить NAT
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

## 📈 Автоматизация

### Terraform конфигурация:
```hcl
resource "google_compute_instance" "argos_gcp" {
  name         = "argos-gcp-node"
  machine_type = "e2-micro"
  zone         = "us-central1-a"
  
  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 10
    }
  }
  
  network_interface {
    network = "default"
    access_config {}
  }
  
  metadata_startup_script = file("setup_argos.sh")
}

resource "google_compute_firewall" "wireguard" {
  name    = "allow-wireguard"
  network = "default"
  
  allow {
    protocol = "udp"
    ports    = ["51820"]
  }
  
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["wireguard"]
}
```

### Ansible playbook:
```yaml
- hosts: gcp_nodes
  become: yes
  tasks:
    - name: Install WireGuard
      apt:
        name: wireguard
        state: present
    
    - name: Configure WireGuard
      template:
        src: wg0.conf.j2
        dest: /etc/wireguard/wg0.conf
    
    - name: Start WireGuard
      systemd:
        name: wg-quick@wg0
        state: started
        enabled: yes
```

## 📞 Поддержка

### Полезные команды:
```bash
# Получить внешний IP
curl -s http://checkip.amazonaws.com

# Проверить подключение к другим узлам
ping 10.100.0.2  # Azure VM 1
ping 10.100.0.3  # Azure VM 2

# Проверить WireGuard
sudo wg show
sudo journalctl -u wg-quick@wg0 -f

# Мониторинг ресурсов
htop
iftop -i wg0
```

### Логи:
- WireGuard: `/var/log/syslog` или `journalctl -u wg-quick@wg0`
- Система: `/var/log/auth.log`, `/var/log/kern.log`
- Cloud Logging: https://console.cloud.google.com/logs

---

**Статус:** ⚠️ ТРЕБУЕТСЯ РАЗВЁРТЫВАНИЕ  
**Приоритет:** Высокий (для географической избыточности)  
**Сложность:** Средняя (требуется Google Cloud аккаунт)

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
