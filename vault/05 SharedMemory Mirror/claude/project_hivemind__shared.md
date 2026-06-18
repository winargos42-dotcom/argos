---
argos_import: sharedmemory_mirror
source_path: claude/project_hivemind.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_hivemind.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_hivemind.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_hivemind.md`
- Category: [[Claude Hub]]

## Content

---
name: HiveMind и P2P сеть
description: Конфигурация HiveMind кластера и P2P mesh после удаления Azure VM
type: project
created: 2026-05-10
originSessionId: 07f7f1bc-6a4f-49cb-aca5-c0efa4942a8e
---
## Изменения 2026-05-10
- **Azure VM удалены** — sweden, australia, japan1, japan2, azure-gpt4
- HiveMind очищен от 5 мёртвых узлов
- P2P конфиг обновлён на домашнюю сеть

## Текущие узлы HiveMind

| Узел | Хост | Порт | Модель | Вес | Статус |
|------|------|------|--------|-----|--------|
| unified-ollama | localhost | 11434 | deepseek-v2:16b | 2.0 | active |
| laptop-ollama | 192.168.1.53 | 11434 | llama3.1:8b | 1.5 | active |
| netherlands-vm | 138.124.89.74 | 11434 | qwen2.5:7b | 0.9 | disabled |

## P2P Mesh (домашняя сеть)

| Node ID | Хост | Роль | Сервисы |
|---------|------|------|---------|
| argos-pc | 192.168.1.66 | controller | MCP:8000, Ollama:11434 |
| argos-laptop | 192.168.1.53 | brain | MCP:8000, Brain:5001, Ollama:11434, HA:8123 |
| argos-orangepi | 192.168.2.168 | iot_gateway | IoT:7777, SSH:22 |

## Удалённые Azure VM (архив)
- sweden-vm: 20.240.192.35 — УДАЛЕНА
- australia-vm: 20.53.240.36 — УДАЛЕНА
- japan1-vm: 40.81.208.101 — УДАЛЕНА
- japan2-vm: 172.207.209.134 — УДАЛЕНА
- azure-gpt4: argoss-sig-2026.openai.azure.com — УДАЛЕНА

## Netherlands VPS (Aeza)
- IP: 138.124.89.74
- Провайдер: Aeza International LTD, Amsterdam
- Был ARGOS v2.1.3 (из логов Telegram)
- НЕ настроен в P2P/HiveMind (OLLAMA_NL_ENABLED=false)
- Пинг: не отвечает (2026-05-10)

## Файлы
- `src/skills/hive_mind.py` — очищен от Azure, добавлен laptop-ollama + nl-vm (disabled)
- `config/p2p_mesh/azure_p2p_config.json` → переименован логически в home mesh
- `.env`: OLLAMA_LAPTOP_HOST, OLLAMA_NL_HOST, OLLAMA_NL_ENABLED

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_hivemind.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
