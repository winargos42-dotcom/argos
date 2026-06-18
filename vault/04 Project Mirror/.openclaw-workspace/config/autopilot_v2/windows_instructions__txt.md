---
argos_import: project_file
source_path: .openclaw-workspace/config/autopilot_v2/windows_instructions.txt
source_abs: F:\debug\argoss\.openclaw-workspace\config\autopilot_v2\windows_instructions.txt
source_ext: .txt
source_sha256: 4ca36c05bfe21723ac07e196289faae360a1006db3660d81364129203de9e976
text_sha256: 4ca36c05bfe21723ac07e196289faae360a1006db3660d81364129203de9e976
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:10
---

# windows_instructions.txt

- Source: `.openclaw-workspace/config/autopilot_v2/windows_instructions.txt`
- Extract: `text`
- SHA256: `4ca36c05bfe21723ac07e196289faae360a1006db3660d81364129203de9e976`

## Content

# Инструкции для настройки Windows Hub

## 1. Установка WireGuard
- Скачайте и установите WireGuard с https://www.wireguard.com/install/

## 2. Импорт конфигурации
1. Откройте WireGuard
2. Нажмите "Import tunnel(s) from file"
3. Выберите файл: config/wireguard/windows-hub.conf
4. Активируйте туннель "argos-windows-hub"

## 3. Проверка подключения
Откройте командную строку и выполните:
```
ping 10.100.0.1
ping 10.100.0.2
```

## 4. IP-адреса сети:
- azure-hub-1: 10.100.0.1 (Australia East)
- azure-hub-2: 10.100.0.2 (Japan East)
- Windows Hub: 10.100.0.3
- Termux Edge: 10.100.2.1

## 5. Автозапуск
- В WireGuard отметьте "Start on system startup" для туннеля

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
