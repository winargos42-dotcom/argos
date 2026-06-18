---
argos_import: project_file
source_path: .openclaw-workspace/config/autopilot_v2/FINAL_INSTRUCTIONS.txt
source_abs: F:\debug\argoss\.openclaw-workspace\config\autopilot_v2\FINAL_INSTRUCTIONS.txt
source_ext: .txt
source_sha256: 5505004802b9a23975f6a840c49634da856cb7a8a3909d64805c83913dff901c
text_sha256: 19070823a100c4ff75246857c504f7356636dcff78357d897a62dde197cc5e45
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:10
---

# FINAL_INSTRUCTIONS.txt

- Source: `.openclaw-workspace/config/autopilot_v2/FINAL_INSTRUCTIONS.txt`
- Extract: `text`
- SHA256: `5505004802b9a23975f6a840c49634da856cb7a8a3909d64805c83913dff901c`

## Content

# ФИНАЛЬНЫЕ ИНСТРУКЦИИ ПО РАЗВЁРТЫВАНИЮ P2P СЕТИ ARGOS

## РАЗВЁРТАННЫЕ УЗЛЫ:
1. Australia VM: argos-vm (20.53.240.36) - WireGuard IP: 10.100.0.1
2. Japan VM: argos-vm-jp_079c3df3 (40.81.208.101) - WireGuard IP: 10.100.0.2
3. Windows Hub: требуется настройка - WireGuard IP: 10.100.0.3
4. Termux Edge: требуется настройка - WireGuard IP: 10.100.2.1

## КОМАНДЫ ДЛЯ ПРОВЕРКИ:
ping 10.100.0.1
ping 10.100.0.2

## НАСТРОЙКА WINDOWS:
1. Установить WireGuard: https://www.wireguard.com/install/
2. Импортировать config/wireguard/windows-hub.conf
3. Активировать туннель "argos-windows-hub"

## НАСТРОЙКА TERMUX:
bash config/autopilot_v2/termux_edge.sh

## АРХИТЕКТУРА СЕТИ:
- Подсеть: 10.100.0.0/20
- Порт WireGuard: 51820/UDP
- Топология: гибридная

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
