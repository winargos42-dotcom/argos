# 2026-05-10 Agent Memory Audit

- Дата аудита: `2026-05-10`
- Цель: проверить память всех агентных контуров в Obsidian и выявить рассинхроны.

## Что проверено

- `05 SharedMemory Mirror/argos/MEMORY__shared.md`
- `05 SharedMemory Mirror/claude/MEMORY__shared.md`
- `05 SharedMemory Mirror/ollama/MEMORY__shared.md`
- `05 SharedMemory Mirror/opencode/MEMORY__shared.md`
- `05 SharedMemory Mirror/shared/SHARED__shared.md`
- `04 Project Mirror/.openclaw-workspace/MEMORY__md.md`
- `04 Project Mirror/.openclaw-workspace/AGENTS__md.md`
- `04 Project Mirror/.openclaw-workspace/HEARTBEAT__md.md`
- `00 Memory Web/Agents Hub.md`
- `00 Memory Web/SharedMemory Hub.md`

## Текущее состояние

- Память основных агентов (argos/claude/ollama/opencode/shared) доступна и читается.
- В графе есть связки через `ARGOS_MEMORY_WEB` блоки и hub-узлы.
- Mirror `05 SharedMemory Mirror` содержит актуальные зеркала из `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory`.

## Найденные рассинхроны

1. Версия ARGOS расходится по слоям:
- `argos/MEMORY__shared.md`: `v2.1.3`
- `claude/MEMORY__shared.md`: упоминание `v2.1.4`

2. MCP endpoint расходится:
- часть заметок указывает `:8000/mcp`
- legacy слой `.openclaw-workspace` указывает `:8001/mcp`

3. Бот-контекст в legacy-слое частично устарел:
- в `.openclaw-workspace/MEMORY__md.md` сохраняются старые пометки по ботам и портам.

## Вывод

Память агентов целостная по структуре, но есть 2 критичные точки рассинхронизации: версия ARGOS и MCP порт. Это не ломает чтение памяти, но может давать неверные решения при автопилоте.

## Рекомендуемая канонизация

- Канон версии: взять из текущего `AGENTS.md` в проекте и унифицировать во всех `MEMORY.md`.
- Канон MCP: зафиксировать единый активный endpoint и проставить его в `shared/SHARED.md`, `argos/MEMORY.md`, `claude/project_mcp.md`, `.openclaw-workspace/MEMORY.md`.
- Legacy слой `.openclaw-workspace` оставить как historical, но добавить явный флаг `legacy-context`.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Logs Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Logs Hub]]
