---
argos_import: project_file
source_path: P2P_MESH_SETUP.md
source_abs: F:\debug\argoss\P2P_MESH_SETUP.md
source_ext: .md
source_sha256: 53a507add9397c68033ad3100d91c4cccdacf44faa351c3bbdefb2ea3d022c8e
text_sha256: 53a507add9397c68033ad3100d91c4cccdacf44faa351c3bbdefb2ea3d022c8e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# P2P_MESH_SETUP.md

- Source: `P2P_MESH_SETUP.md`
- Extract: `text`
- SHA256: `53a507add9397c68033ad3100d91c4cccdacf44faa351c3bbdefb2ea3d022c8e`

## Content

# ARGOS P2P Mesh — план подключения всех VM к Brain

Дата: 2026-04-18
Автор: Сева

## 1. Текущая инвентаризация

| Role          | Host                   | Region           | IP (public)     | Port  | Status |
|---------------|------------------------|------------------|-----------------|-------|--------|
| **Brain hub** | windows-pc             | LAN 192.168.1.x  | 192.168.1.66    | 5001  | ✅     |
| P2P local     | localhost (pc)         | LAN              | 127.0.0.1       | 8000  | ✅     |
| argos-vm      | Australia East         | rg-argos         | 20.53.240.36    | 8000  | ✅     |
| argos-vm-jp_079c3df3 | Japan East      | rg-argos         | 172.207.209.134 | 8000  | ✅     |
| argos-vm-jp_27e38b15 | Japan East      | rg-argos         | 40.81.208.101   | 8000  | ✅     |
| ollama        | Sweden Central         | rg-argos         | 20.240.192.35   | 11434 | ✅     |

**Проблема:** Brain висит на LAN-адресе `192.168.1.66`. Из Azure VM он недоступен.
Решение — сделать Brain публичным. Два варианта ниже.

---

## 2. Вариант A — Cloudflared Tunnel (быстро, 10 минут, бесплатно)

Выставляет локальный `http://192.168.1.66:5001` как `https://brain-<random>.trycloudflare.com`
без роутер-форвардинга и без статического IP.

### Шаги на PC (Windows PowerShell, Admin)

```powershell
# 1. Установить cloudflared
winget install --id Cloudflare.cloudflared
# проверить
cloudflared --version

# 2. Запустить quick-tunnel (автогенерит публичный URL)
cloudflared tunnel --url http://192.168.1.66:5001
```

В консоли появится строка вида:
```
https://fuzzy-owl-dance-plum.trycloudflare.com
```

Это твой **BRAIN_URL**. Теперь на каждой VM:
```bash
export ARGOS_BRAIN_URL=https://fuzzy-owl-dance-plum.trycloudflare.com
```

### Минусы
- URL меняется при каждом запуске (лечится платным named tunnel).
- Tunnel живёт пока запущен `cloudflared` — вырубил терминал → brain недоступен.

### Как сделать постоянным (named tunnel, всё равно бесплатно)

```powershell
cloudflared tunnel login                         # открывает браузер, привязка к Cloudflare account
cloudflared tunnel create argos-brain            # создаёт UUID-туннель
cloudflared tunnel route dns argos-brain brain.argos.dev   # твой реальный домен
# config.yml
#   tunnel: <UUID>
#   credentials-file: C:\Users\<you>\.cloudflared\<UUID>.json
#   ingress:
#     - hostname: brain.argos.dev
#       service: http://192.168.1.66:5001
#     - service: http_status:404
cloudflared service install                      # ставит как Windows service
```

---

## 3. Вариант B — Tailscale mesh (правильно, переносим P2P в VPN-сеть)

Tailscale создаёт WireGuard-mesh: каждый узел получает `100.x.x.x` IP и видит все остальные.
Brain остаётся на LAN, но теперь доступен соседям по tailscale-IP.

### 3.1 На PC

```powershell
winget install Tailscale.Tailscale
tailscale up                                    # откроет браузер, логинься Google-аккаунтом
tailscale ip -4                                 # запомни, напр. 100.88.42.1  <-- BRAIN_TS_IP
```

### 3.2 На каждой Linux VM (через az ssh vm)

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --authkey=tskey-auth-xxxxx    # создать ключ в Tailscale admin console
tailscale ip -4
```

### 3.3 На VM'ках экспортируем brain URL

```bash
export ARGOS_BRAIN_URL=http://100.88.42.1:5001  # Tailscale IP твоего PC
```

### Плюсы / минусы
+ End-to-end encrypted, никакой публичной экспозиции.
+ Работает через NAT без роутер-настроек.
+ Free tier: 100 устройств, 3 пользователя — нам хватит.
- Надо поставить клиент на каждую машину (~5 минут на VM).

---

## 4. Раскатка P2P-агента на 4 VM (после решения варианта A или B)

### 4.1 argos-vm (Australia East, 20.53.240.36)

```bash
az ssh vm --resource-group rg-argos --name argos-vm
# ИЛИ: ssh azureuser@20.53.240.36

# Копируем агент (если репо уже клонирован)
cd ~/argoss && git pull

# Или качаем одним шотом:
curl -fsSL https://raw.githubusercontent.com/thoresensandmann432-source/argoss/main/p2p_agent.py -o p2p_agent.py
curl -fsSL https://raw.githubusercontent.com/thoresensandmann432-source/argoss/main/deploy_p2p_agent.sh -o deploy.sh

sudo ARGOS_BRAIN_URL="<твой_BRAIN_URL>" \
     ARGOS_NODE_NAME="argos-vm-au" \
     ARGOS_NODE_ROLE="compute" \
     ARGOS_NODE_CAPABILITIES="p2p,compute,argos-mcp" \
     bash deploy.sh
```

### 4.2 argos-vm-jp_079c3df3 (Japan East, 172.207.209.134)

```bash
ssh azureuser@172.207.209.134
sudo ARGOS_BRAIN_URL="<BRAIN_URL>" \
     ARGOS_NODE_NAME="argos-vm-jp-1" \
     ARGOS_NODE_ROLE="compute" \
     ARGOS_NODE_CAPABILITIES="p2p,compute" \
     bash deploy.sh
```

### 4.3 argos-vm-jp_27e38b15 (Japan East, 40.81.208.101)

```bash
ssh azureuser@40.81.208.101
sudo ARGOS_BRAIN_URL="<BRAIN_URL>" \
     ARGOS_NODE_NAME="argos-vm-jp-2" \
     ARGOS_NODE_ROLE="compute" \
     ARGOS_NODE_CAPABILITIES="p2p,compute" \
     bash deploy.sh
```

### 4.4 ollama (Sweden Central, 20.240.192.35)

```bash
ssh azureuser@20.240.192.35
sudo ARGOS_BRAIN_URL="<BRAIN_URL>" \
     ARGOS_NODE_NAME="ollama-se" \
     ARGOS_NODE_ROLE="ollama" \
     ARGOS_NODE_CAPABILITIES="p2p,ollama,llm" \
     OLLAMA_HOST="http://localhost:11434" \
     bash deploy.sh
```

### 4.5 PC (hub)

```powershell
# В argoss/ в PowerShell Admin
$env:ARGOS_BRAIN_URL="http://192.168.1.66:5001"
$env:ARGOS_NODE_NAME="windows-pc"
$env:ARGOS_NODE_ROLE="hub"
./deploy_p2p_agent.ps1
```

---

## 5. Проверка

### 5.1 Со стороны Brain

```powershell
curl http://192.168.1.66:5001/brain/nodes
```

должно вернуть JSON с 5 узлами (pc + 4 VM).

### 5.2 Дашборд

Открыть в браузере:
```
http://192.168.1.66:5001/dashboard
```

Обновление раз в 5 секунд. Узлы без heartbeat > 90s становятся серыми.

### 5.3 Логи на VM

```bash
journalctl -u argos-p2p.service -f
```

---

## 6. После раскатки — что доступно

Когда все узлы в реестре, Brain может:
- **/brain/nodes?role=ollama** — найти LLM-ноду и проксировать запрос
- распределять `/think`, `/analyze`, `/compute` задачи по живым узлам
- корректно реагировать на падение узла (circuit breaker)

Это основа для того, что ты описываешь как "AWA-Core координатор" — но на одну сеть выше.

---

## 7. Что делать **сейчас** (пошагово)

1. [ ] Выбрать вариант: **A (cloudflared quick)** или **B (tailscale mesh)**
2. [ ] Получить публичный `BRAIN_URL`
3. [ ] Запушить обновлённые `p2p_agent.py`, `deploy_p2p_agent.sh`, `argos_brain_api.py`, `argos_brain_dashboard.html` в GitHub
4. [ ] Перезапустить Brain на PC: `python argos_brain_api.py` (подхватит новые endpoints)
5. [ ] Раскатать агента на 4 VM по разделу 4
6. [ ] Открыть `/dashboard` → все 5 узлов зелёные

Если возникнут затыки с конкретной VM — скинь `journalctl -u argos-p2p.service -n 50` и разберём.

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
