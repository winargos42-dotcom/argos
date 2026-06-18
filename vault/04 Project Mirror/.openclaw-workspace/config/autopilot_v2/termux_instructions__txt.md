---
argos_import: project_file
source_path: .openclaw-workspace/config/autopilot_v2/termux_instructions.txt
source_abs: F:\debug\argoss\.openclaw-workspace\config\autopilot_v2\termux_instructions.txt
source_ext: .txt
source_sha256: 02c4bdd467d32d08db2a7ab4a6d5aafb1e4f0471128724d3efd35b0dd12802b5
text_sha256: 02c4bdd467d32d08db2a7ab4a6d5aafb1e4f0471128724d3efd35b0dd12802b5
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:10
---

# termux_instructions.txt

- Source: `.openclaw-workspace/config/autopilot_v2/termux_instructions.txt`
- Extract: `text`
- SHA256: `02c4bdd467d32d08db2a7ab4a6d5aafb1e4f0471128724d3efd35b0dd12802b5`

## Content

ИНСТРУКЦИЯ ДЛЯ TERMUX:
        
        1. Установите WireGuard в Termux:
           pkg update
           pkg install -y wireguard-tools
        
        2. Скопируйте конфигурацию:
           cp config\wireguard\termux-edge-1.conf ~/.wireguard/wg0.conf
           chmod 600 ~/.wireguard/wg0.conf
        
        3. Запустите WireGuard:
           wg-quick up ~/.wireguard/wg0.conf
        
        4. Добавьте в автозагрузку:
           echo 'wg-quick up ~/.wireguard/wg0.conf' >> ~/.bashrc
        
        5. Проверьте подключение:
           ping -c 3 10.100.0.1
        
        Или запустите готовый скрипт:
           bash config\autopilot_v2\termux_edge.sh
        
        Конфиг сохранен: config\wireguard\termux-edge-1.conf
        Скрипт: config\autopilot_v2\termux_edge.sh

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
