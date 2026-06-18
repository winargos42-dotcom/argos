---
argos_import: project_file
source_path: wg/README_WG_MESH.md
source_abs: F:\debug\argoss\wg\README_WG_MESH.md
source_ext: .md
source_sha256: 8b46b24a28f8758fd004feb0447c33af1d6cec98077cb5af1d17cca3ffe8b38e
text_sha256: 06c2d27cc9e2517a9d7cd2250448d23ca98705c3b967a1b5de0ee6a564f454d8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:48
---

# README_WG_MESH.md

- Source: `wg/README_WG_MESH.md`
- Extract: `text`
- SHA256: `8b46b24a28f8758fd004feb0447c33af1d6cec98077cb5af1d17cca3ffe8b38e`

## Content

# ARGOS WireGuard Mesh Network
# Generated: 2026-04-23 04:02:45
# Network: 10.200.0.0/24

## NODES

| Node | WG IP | Public Endpoint | Public Key |
|------|-------|-----------------|------------|
| AU   | 10.200.0.1 | 20.53.240.36:51820 | 0XlzOCK3hX7KigbcvHtre5KZdY5NPtPW8w43OEqi3HU= |
| JP1  | 10.200.0.2 | 40.81.208.101:51821 | i3nHuoWUAYqjBFnclp8ZqcEaEtXf8aI93xPPFw7rbXg= |
| JP2  | 10.200.0.3 | 172.207.209.134:51820 | y4X9oNGUk18MWjmvaK4Z0JhCY2+yDpIM9TMVz/Ontyo= |
| SE   | 10.200.0.4 | 20.240.192.35:51822 | SMRYCnRWAelW2/reWp/Hod5KWNPHhq2ummvQW3YEh30= |
| EXT  | 10.200.0.5 | 47.237.24.124:51820 | N4zPt3hXeJgrFAP7ZFb2/LnttT6ea2psf57brz2GqVQ= |
| PC   | 10.200.0.6 | - | [PC_PUBLIC_KEY] |

## CONFIG FILES

- wg0_au.conf - AU Node
- wg0_jp1.conf - JP1 Node
- wg0_jp2.conf - JP2 Node
- wg0_se.conf - SE Node
- wg0_ext.conf - EXT Node
- rgos-pc.conf - PC Master Node

## SETUP

### VM (Linux):
`ash
sudo cp wg0_[node].conf /etc/wireguard/wg0.conf
sudo chmod 600 /etc/wireguard/wg0.conf
sudo systemctl enable wg-quick@wg0
sudo wg-quick up wg0
`

### PC (Windows):
1. Open WireGuard
2. Add Tunnel → Import from file
3. Select rgos-pc.conf
4. Click Activate

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
