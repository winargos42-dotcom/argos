---
argos_import: project_file
source_path: p2p_network_autopilot_plan.md
source_abs: F:\debug\argoss\p2p_network_autopilot_plan.md
source_ext: .md
source_sha256: 23fc38c0b6f9e7800a5ae8864dfd6e4043ec75c207fe41f039b2f2bcd9448a67
text_sha256: 23fc38c0b6f9e7800a5ae8864dfd6e4043ec75c207fe41f039b2f2bcd9448a67
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# p2p_network_autopilot_plan.md

- Source: `p2p_network_autopilot_plan.md`
- Extract: `text`
- SHA256: `23fc38c0b6f9e7800a5ae8864dfd6e4043ec75c207fe41f039b2f2bcd9448a67`

## Content

# P2P NETWORK AUTOPILOT PLAN - МАСШТАБИРОВАНИЕ ARGOS

## ТЕКУЩЕЕ СОСТОЯНИЕ
- **WireGuard full-mesh**: 5 узлов (2 Azure, Windows, Termux, будущий GCP)
- **Проблемы**: ручное управление, квадратичный рост конфигов, NAT traversal
- **Цель**: масштабирование до 20+ узлов с управляемостью

## ЭТАП 1: ГИБРИДНАЯ ТОПОЛОГИЯ (НЕДЕЛЯ 1)

### 1.1. Схема топологии
```
CORE HUBS (3 узла, полная связность):
1. azure-hub-1 (20.53.240.36) - Australia East
2. azure-hub-2 (40.81.208.101) - Japan East  
3. windows-hub (локальный) - Exit Node

REGIONAL HUBS (подключаются к Core):
- gcp-hub (будущий) - Европа/США
- termux-hub (мобильный) - NAT traversal

EDGE NODES (подключаются к ближайшему Regional Hub):
- termux-edge-1, termux-edge-2, ...
- small-vm-1, small-vm-2, ...
```

### 1.2. Центральный генератор конфигов
```python
class WireGuardConfigGenerator:
    def __init__(self):
        self.nodes = {
            "azure-hub-1": {"type": "core", "ip": "10.100.0.1", "pubkey": "...", "endpoint": "20.53.240.36:51820"},
            "azure-hub-2": {"type": "core", "ip": "10.100.0.2", "pubkey": "...", "endpoint": "40.81.208.101:51820"},
            "windows-hub": {"type": "core", "ip": "10.100.0.3", "pubkey": "...", "endpoint": "dynamic"},
            "termux-edge": {"type": "edge", "ip": "10.100.1.1", "pubkey": "...", "endpoint": "dynamic"},
        }
        self.topology = {
            "core": ["azure-hub-1", "azure-hub-2", "windows-hub"],
            "edges": {
                "termux-edge": "azure-hub-1",  # edge → core
            }
        }
    
    def generate_for_node(self, node_id):
        """Генерация конфига для конкретного узла"""
        config = []
        config.append(f"[Interface]")
        config.append(f"Address = {self.nodes[node_id]['ip']}/20")
        config.append(f"PrivateKey = {{PRIVATE_KEY}}")
        config.append(f"ListenPort = 51820")
        
        # Добавляем peers в зависимости от топологии
        if self.nodes[node_id]["type"] == "core":
            # Core видит все другие Core
            for peer_id, peer_data in self.nodes.items():
                if peer_id != node_id and peer_data["type"] == "core":
                    config.append(f"\n[Peer]")
                    config.append(f"PublicKey = {peer_data['pubkey']}")
                    config.append(f"AllowedIPs = {peer_data['ip']}/32")
                    if peer_data.get("endpoint") != "dynamic":
                        config.append(f"Endpoint = {peer_data['endpoint']}")
        else:
            # Edge видит только свой Core Hub
            core_hub = self.topology["edges"][node_id]
            core_data = self.nodes[core_hub]
            config.append(f"\n[Peer]")
            config.append(f"PublicKey = {core_data['pubkey']}")
            config.append(f"AllowedIPs = 10.100.0.0/20")  # Вся подсеть
            config.append(f"Endpoint = {core_data['endpoint']}")
            config.append(f"PersistentKeepalive = 25")
        
        return "\n".join(config)
```

### 1.3. Подсеть расширение
- **Текущая**: 10.100.0.0/24 (256 адресов)
- **Новая**: 10.100.0.0/20 (4096 адресов)
- **Распределение**:
  - 10.100.0.0/24: Core Hubs (0-255)
  - 10.100.1.0/24: Regional Hubs (256-511)
  - 10.100.2.0/24: Edge Nodes (512-767)
  - 10.100.3.0-15.0/24: Резерв

## ЭТАП 2: АВТОПИЛОТ 2.0 (НЕДЕЛЯ 2)

### 2.1. Автоматическое развёртывание
```bash
# Центральный скрипт управления
python network_autopilot.py \
  --action deploy \
  --node azure-hub-1 \
  --config configs/azure-hub-1.conf \
  --key keys/azure-hub-1.key
```

### 2.2. Мониторинг
```python
class NetworkMonitor:
    def check_connectivity(self):
        """Проверка связности всех узлов"""
        results = {}
        for node_id, node_data in self.nodes.items():
            if node_data["type"] == "core":
                ping_result = self.ping_node(node_data["ip"])
                wg_result = self.check_wireguard(node_id)
                results[node_id] = {
                    "ping": ping_result,
                    "wireguard": wg_result,
                    "status": "online" if ping_result and wg_result else "offline"
                }
        return results
    
    def generate_report(self):
        """Генерация отчёта о состоянии сети"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_nodes": len(self.nodes),
            "online_nodes": 0,
            "offline_nodes": 0,
            "details": self.check_connectivity()
        }
        return report
```

### 2.3. Health-check скрипты
```bash
#!/bin/bash
# health-check.sh
wg show
ping -c 3 10.100.0.1
curl -s http://10.100.0.1:55771/status
```

## ЭТАП 3: ПОДГОТОВКА К NETMAKER (НЕДЕЛЯ 3-4)

### 3.1. Требования для Netmaker
- Выделенная VM для Netmaker server
- PostgreSQL база данных
- Docker/Docker Compose
- Public IP с портами 443, 51821-51830/UDP

### 3.2. Миграционный план
1. Установить Netmaker на отдельной VM
2. Импортировать существующие узлы
3. Постепенно мигрировать узлы с ручного WireGuard
4. Настроить ACL и политики
5. Включить NAT traversal для мобильных узлов

### 3.3. Интеграция с ARGOS
```python
class NetmakerIntegration:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
    
    def add_node(self, node_name, public_key, endpoint=None):
        """Добавление узла в Netmaker"""
        payload = {
            "name": node_name,
            "publickey": public_key,
            "endpoint": endpoint,
            "allowedips": ["10.100.0.0/20"]
        }
        response = requests.post(
            f"{self.api_url}/api/nodes",
            json=payload,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()
    
    def get_node_config(self, node_id):
        """Получение конфига для узла"""
        response = requests.get(
            f"{self.api_url}/api/nodes/{node_id}/config",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.text
```

## ЭТАП 4: РАСШИРЕННЫЕ ВОЗМОЖНОСТИ (МЕСЯЦ 2+)

### 4.1. Динамический routing
- FRR с OSPF/BGP поверх WireGuard
- Multi-cloud оптимизация трафика
- Failover между хабами

### 4.2. Service mesh
- Cilium с WireGuard backend
- Kubernetes для оркестрации
- Service discovery и load balancing

### 4.3. Полная автоматизация
- Terraform/Bicep для VM
- Ansible для конфигурации
- GitOps для управления сетью

## БЛИЖАЙШИЕ ДЕЙСТВИЯ

### СЕГОДНЯ:
1. **Создать центральный генератор конфигов**
2. **Обновить автопилот-скрипты** под новую топологию
3. **Протестировать** гибридную сеть на 3 узлах

### ЗАВТРА:
1. **Добавить NAT traversal** для Termux
2. **Создать мониторинг** `wg show`
3. **Написать health-check скрипты**

### НЕДЕЛЯ 1:
1. **Развернуть** все 5 узлов
2. **Протестировать** производительность
3. **Подготовить** документацию

## ИНТЕГРАЦИЯ С ARGOS

### SubAgencyManager:
- **NetSubAgent**: управление сетью, генерация конфигов
- **SystemSubAgent**: мониторинг, health-check
- **AISubAgent**: оптимизация топологии

### MCP сервер:
- API для управления сетью
- Автоматическое добавление узлов
- Мониторинг состояния

### Автопилот:
```python
class NetworkAutopilot:
    def scale_network(self, new_nodes):
        """Автоматическое масштабирование сети"""
        # 1. Анализ текущей топологии
        # 2. Определение оптимального размещения
        # 3. Генерация конфигов
        # 4. Развёртывание на узлах
        # 5. Проверка connectivity
        # 6. Обновление мониторинга
```

## МЕТРИКИ УСПЕХА

1. **Стабильность**: 99.9% uptime Core Hubs
2. **Масштабируемость**: добавление нового узла за <5 минут
3. **Производительность**: ping <50ms между Core Hubs
4. **Управляемость**: централизованное управление всеми узлами

## РИСКИ И МИТИГАЦИЯ

1. **Риск**: Сложность миграции на Netmaker
   **Митигация**: Постепенная миграция, тестирование на staging

2. **Риск**: Производительность при NAT traversal
   **Митигация**: Выделенные relays, оптимизация keepalive

3. **Риск**: Безопасность при масштабировании
   **Митигация**: ACL, zero-trust политики, регулярные аудиты

---

**СТАТУС**: НАЧАТО  
**СЛЕДУЮЩЕЕ ДЕЙСТВИЕ**: Создать центральный генератор конфигов

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
