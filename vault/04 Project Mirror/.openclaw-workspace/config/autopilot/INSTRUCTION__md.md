---
argos_import: project_file
source_path: .openclaw-workspace/config/autopilot/INSTRUCTION.md
source_abs: F:\debug\argoss\.openclaw-workspace\config\autopilot\INSTRUCTION.md
source_ext: .md
source_sha256: 16a6c7bcb990d7bf922620d78d0044ff3da632ee93ae17d40bcb1f2d5ae0e7bf
text_sha256: 2942480f6c9e9e4d827e15e997294a1c4e71c94943406ee610c8676f2aa407c6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:10
---

# INSTRUCTION.md

- Source: `.openclaw-workspace/config/autopilot/INSTRUCTION.md`
- Extract: `text`
- SHA256: `16a6c7bcb990d7bf922620d78d0044ff3da632ee93ae17d40bcb1f2d5ae0e7bf`

## Content

# ИНСТРУКЦИЯ ПО НАСТРОЙКЕ P2P СЕТИ ARGOS
# Создано: 2026-04-17 01:49:10

## Шаг 1: Настроить Azure VM 1

scp config/autopilot/azure_vm1_setup.sh azureuser@20.53.240.36:~/
ssh azureuser@20.53.240.36
chmod +x azure_vm1_setup.sh
sudo ./azure_vm1_setup.sh

# Записать публичный ключ:
sudo cat /etc/wireguard/public.key

## Шаг 2: Настроить Azure VM 2

scp config/autopilot/azure_vm2_setup.sh azureuser@40.81.208.101:~/
ssh azureuser@40.81.208.101
chmod +x azure_vm2_setup.sh
sudo ./azure_vm2_setup.sh

# Записать публичный ключ:
sudo cat /etc/wireguard/public.key

## Шаг 3: Настроить Windows

1. Запустить PowerShell от имени администратора
2. Выполнить:
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\config\autopilot\windows_p2p_setup.ps1
3. Установить WireGuard
4. Импортировать конфиг с рабочего стола
5. Сгенерировать ключи
6. Записать публичный ключ

## Шаг 4: Обновить конфиги

Заменить в конфигах:
- <AZURE1_PUBLIC_KEY> - ключ Azure VM 1
- <AZURE2_PUBLIC_KEY> - ключ Azure VM 2
- <LOCAL_PUBLIC_KEY> - ключ Windows

## Шаг 5: Запустить WireGuard

Azure VM 1: sudo systemctl restart wg-quick@wg0
Azure VM 2: sudo systemctl restart wg-quick@wg0
Windows: активировать туннель

## Шаг 6: Проверить сеть

ping 10.100.0.1  # Windows
ping 10.100.0.2  # Azure VM 1
ping 10.100.0.3  # Azure VM 2

sudo wg show

---
Готово к развёртыванию!

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
