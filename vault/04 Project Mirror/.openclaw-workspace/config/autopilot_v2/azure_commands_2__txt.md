---
argos_import: project_file
source_path: .openclaw-workspace/config/autopilot_v2/azure_commands_2.txt
source_abs: F:\debug\argoss\.openclaw-workspace\config\autopilot_v2\azure_commands_2.txt
source_ext: .txt
source_sha256: 5c68d62e4727743e8574ef4fe9b2867d06ac1102689ef4907e8854e3db70b08f
text_sha256: 5c68d62e4727743e8574ef4fe9b2867d06ac1102689ef4907e8854e3db70b08f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:10
---

# azure_commands_2.txt

- Source: `.openclaw-workspace/config/autopilot_v2/azure_commands_2.txt`
- Extract: `text`
- SHA256: `5c68d62e4727743e8574ef4fe9b2867d06ac1102689ef4907e8854e3db70b08f`

## Content

# Команды для azure-hub-2 (40.81.208.101)

# 1. Проверить состояние VM
az vm show -g rg-argos -n azure-hub-2 --query "{name:name, status:powerState, ip:publicIps}"

# 2. Проверить доступность
az vm run-command invoke -g rg-argos -n azure-hub-2 --command-id RunShellScript --scripts "echo 'VM работает' && whoami"

# 3. Установить WireGuard
az vm run-command invoke -g rg-argos -n azure-hub-2 --command-id RunShellScript --scripts "sudo apt update && sudo apt install -y wireguard wireguard-tools && echo 'WireGuard установлен'"

# 4. Создать конфиг
CONFIG='[Interface]
Address = 10.100.0.2/20
PrivateKey = 5M1sUk7Wm0NDtIJOLK/aXcZZd/fAiNrMgImxWDYPrtY=
ListenPort = 51820
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# azure-hub-1
PublicKey = 5M1sUk7Wm0NDtIJOLK/aXcZZd/fAiNrMgImxWDYPrtY=
Endpoint = 20.53.240.36:51820
AllowedIPs = 10.100.0.1/32

[Peer]
# windows-hub
PublicKey = 5M1sUk7Wm0NDtIJOLK/aXcZZd/fAiNrMgImxWDYPrtY=
Endpoint = dynamic
AllowedIPs = 10.100.0.3/32

[Peer]
# termux-edge-1
PublicKey = 5M1sUk7Wm0NDtIJOLK/aXcZZd/fAiNrMgImxWDYPrtY=
Endpoint = dynamic
AllowedIPs = 10.100.2.1/32'

az vm run-command invoke -g rg-argos -n azure-hub-2 --command-id RunShellScript --scripts "echo '$CONFIG' | sudo tee /etc/wireguard/wg0.conf && sudo chmod 600 /etc/wireguard/wg0.conf"

# 5. Запустить WireGuard
az vm run-command invoke -g rg-argos -n azure-hub-2 --command-id RunShellScript --scripts "echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf && sudo sysctl -p && sudo wg-quick up wg0 && sudo systemctl enable wg-quick@wg0"

# 6. Проверить состояние
az vm run-command invoke -g rg-argos -n azure-hub-2 --command-id RunShellScript --scripts "sudo wg show"

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Agents Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Agents Hub]]
