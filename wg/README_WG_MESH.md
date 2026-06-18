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
