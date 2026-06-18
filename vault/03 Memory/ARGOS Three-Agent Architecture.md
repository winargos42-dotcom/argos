# ARGOS Three-Agent Architecture

**Date:** 2026-05-10
**Source:** Daily/2026-05-10 (DeepSeek memory extraction)

## Agents

| # | Name | Platform | Role | Connection |
|---|------|----------|------|------------|
| 1 | **ARGOS** | Windows PC (main) | AI management, memory, Obsidian, network | Localhost |
| 2 | **Claude Code** | X230 Arch Linux | Development agent, coding | MCP port 8000 |
| 3 | **OpenCode/K2P6** | Windows/OpenCode CLI | Current session agent | Direct CLI |

## Agent 2 Details (Claude Code)

- **Platform:** Lenovo X230, Arch Linux
- **Software:** Claude Code (official Anthropic CLI)
- **Connection:** MCP (port 8000)
- **Role:** Co-author of SiGtRiP project
- **Integration:** Direct link to ARGOS via MCP

## Communication Flow

```
User (Telegram/PC)
    ↓
ARGOS (Agent 1, Windows)
    ↓
MCP Server (:8000)
    ↓
Claude Code (Agent 2, X230) ←→ OpenCode (Agent 3)
```

## Notes

- Agent 2 (Claude Code) has full filesystem access via MCP
- Agent 3 (current) has direct Windows filesystem access
- All agents share Obsidian vault as canonical memory
- Priority: Agent 1 for orchestration, Agent 2/3 for execution

---

*Extracted from user request: "запомни: система состоит из трёх агентов..."*

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Human Sessions Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Human Sessions Hub]]
