---
argos_import: sharedmemory_mirror
source_path: Argos_Tunnel_Setup.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\Argos_Tunnel_Setup.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: Argos_Tunnel_Setup.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\Argos_Tunnel_Setup.md`
- Category: [[SharedMemory Hub]]

## Content

# Argos Tunnel Setup Log
**Дата:** 2026-05-07  
**Время:** ~13:50 UTC

## Что сделано
1. Ollama запущен и доступен локально:
   ```bash
   $ curl http://localhost:11434/api/tags
   {"models":[{"name":"llama3.1:8b", ...}]}
   ```
2. Обнаружен существующий туннель Cloudflare с ID `bf451038-e9d0-4a55-8bfd-95f6af283c59` (имя `orangepi`).
3. Конфигурация `~/.cloudflared/config.yml` уже содержит нужное правило:
   ```yaml
   tunnel: bf451038-e9d0-4a55-8bfd-95f6af283c59
   credentials-file: /home/ava/.cloudflared/bf451038-e9d0-4a55-8bfd-95f6af283c59.json

   ingress:
     - hostname: ollama-pc.agrosssss.win
       service: http://localhost:11434
     - service: http_status:404
   ```
4. Туннель запущен в фоновом режиме:
   ```bash
   nohup cloudflared tunnel --config /home/ava/.cloudflared/config.yml run > /tmp/cloudflared.log 2>&1 &
   ```
5. Попытка привязать DNS‑запись `ollama-pc.agrosssss.win` к туннелю через `cloudflared tunnel route dns orangepi ollama-pc` завершилась ошибкой, что запись уже существует (конфликт с существующей записью у другого провайдера DNS).

## Текущее состояние
- Локальный сервис Ollama работает.
- Туннель Cloudflare активен и подключается к edge‑серверам.
- DNS‑запись `ollama-pc.agrosssss.win` пока не резолвится (возможно, из-за конфликта с записью у внешнего DNS‑провайдера).
- При попытке доступа к `https://ollama-pc.agrosssss.win/api/tags` получаем ошибку разрешения имени.

## Следующие шаги
1. **Определить authoritative DNS для домена `agrosssss.win`.**  
   Если вы используете Cloudflare как DNS‑провайдер, выполните:
   ```bash
   cloudflared tunnel route dns orangepi ollama-pc
   ```
   Если DNS у другого регистратора (например, GoDaddy), зайдите в панель управления DNS и создайте/обновите CNAME‑запись:
   - **Имя:** ollama-pc
   - **Значение:** `bf451038-e9d0-4a55-8bfd-95f6af283c59.cfargotunnel.com`
   - **Тип:** CNAME

2. После обновления DNS подождать несколько секунд для распространения.

3. Проверить доступность:
   ```bash
   curl -s http://ollama-pc.agrosssss.win/api/tags
   ```
   Должен вернуться тот же JSON, что и локально.

4. При необходимости настроить автозапуск туннеля как службы (systemd или nssm) и автозапуск Ollama.

## Примечание
Все действия выполнены в среде WSL2 (Linux) на ПК с Arch Linux. Ollama слушает на `localhost:11434` внутри WSL2, что доступно из туннеля Cloudflare, запущенного в той же среде.

*Эта запись будет синхронена с вашим ПК через Obsidian синхронизацию.*

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[SharedMemory Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `Argos_Tunnel_Setup.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[SharedMemory Hub]]
