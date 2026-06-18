---
argos_import: sharedmemory_mirror
source_path: claude/project_mcp.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_mcp.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_mcp.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_mcp.md`
- Category: [[Claude Hub]]

## Content

---
name: MCP и Claude Code конфиг
description: MCP серверы, Claude Code на ПК и ноутбуке, настройки подключений
type: project
originSessionId: 81a638d4-f034-4bbb-8b6c-d15b46bb4b71
---
## Claude Code на ноутбуке
- Конфиг: `~/.claude/settings.json`
- autoMemoryDirectory: `~/Documents/MyObsidianVault/SharedMemory/claude`
- MCP серверы:
  - `argos-pc`: `http://192.168.1.66:8000/mcp`
  - `argos-local`: `http://127.0.0.1:8000/mcp`

## Claude Code на ПК
- Установлен: да (npm install -g @anthropic-ai/claude-code — 2026-05-02)
- Конфиг: `C:\Users\AvA\.claude\settings.json`
- autoMemoryDirectory: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude`
- MCP серверы:
  - `argos-local`: `http://127.0.0.1:8000/mcp`
  - `argos-laptop`: `http://192.168.1.53:8000/mcp`

## ARGOS MCP (ПК)
- URL: `http://192.168.1.66:8000/mcp`
- Статус: работает
- Ответ: `{"name":"argos","ok":true,"transport":"http"}`
- Дополнительные порты: 8010, 8090, 8002

## .mcp.json в проекте ARGOS
- Путь: `F:\debug\argoss\.mcp.json` и `~/Projects/argoss/.mcp.json`
- Содержит: argos (localhost:8000) + huggingface MCP

**Why:** пользователь хочет единую сеть AI-агентов через MCP.
**How to apply:** при работе с ARGOS использовать MCP argos-pc для доступа к инструментам ПК.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_mcp.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
