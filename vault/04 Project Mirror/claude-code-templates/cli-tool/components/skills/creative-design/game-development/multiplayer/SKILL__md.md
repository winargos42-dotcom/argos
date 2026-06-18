---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/game-development/multiplayer/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\game-development\multiplayer\SKILL.md
source_ext: .md
source_sha256: 943c5567c7d484b563d138c42cebfbd9a85530d0758bd04fce74c66b9edb145b
text_sha256: 79ee8d6f2e04a993b6cdf5eb251590051427cc4e09aa3a7f67f1ab8e61e205f5
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/game-development/multiplayer/SKILL.md`
- Extract: `text`
- SHA256: `943c5567c7d484b563d138c42cebfbd9a85530d0758bd04fce74c66b9edb145b`

## Content

---
name: multiplayer
description: Multiplayer game development principles. Architecture, networking, synchronization.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Multiplayer Game Development

> Networking architecture and synchronization principles.

---

## 1. Architecture Selection

### Decision Tree

```
What type of multiplayer?
│
├── Competitive / Real-time
│   └── Dedicated Server (authoritative)
│
├── Cooperative / Casual
│   └── Host-based (one player is server)
│
├── Turn-based
│   └── Client-server (simple)
│
└── Massive (MMO)
    └── Distributed servers
```

### Comparison

| Architecture | Latency | Cost | Security |
|--------------|---------|------|----------|
| **Dedicated** | Low | High | Strong |
| **P2P** | Variable | Low | Weak |
| **Host-based** | Medium | Low | Medium |

---

## 2. Synchronization Principles

### State vs Input

| Approach | Sync What | Best For |
|----------|-----------|----------|
| **State Sync** | Game state | Simple, few objects |
| **Input Sync** | Player inputs | Action games |
| **Hybrid** | Both | Most games |

### Lag Compensation

| Technique | Purpose |
|-----------|---------|
| **Prediction** | Client predicts server |
| **Interpolation** | Smooth remote players |
| **Reconciliation** | Fix mispredictions |
| **Lag compensation** | Rewind for hit detection |

---

## 3. Network Optimization

### Bandwidth Reduction

| Technique | Savings |
|-----------|---------|
| **Delta compression** | Send only changes |
| **Quantization** | Reduce precision |
| **Priority** | Important data first |
| **Area of interest** | Only nearby entities |

### Update Rates

| Type | Rate |
|------|------|
| Position | 20-60 Hz |
| Health | On change |
| Inventory | On change |
| Chat | On send |

---

## 4. Security Principles

### Server Authority

```
Client: "I hit the enemy"
Server: Validate → did projectile actually hit?
         → was player in valid state?
         → was timing possible?
```

### Anti-Cheat

| Cheat | Prevention |
|-------|------------|
| Speed hack | Server validates movement |
| Aimbot | Server validates sight line |
| Item dupe | Server owns inventory |
| Wall hack | Don't send hidden data |

---

## 5. Matchmaking

### Considerations

| Factor | Impact |
|--------|--------|
| **Skill** | Fair matches |
| **Latency** | Playable connection |
| **Wait time** | Player patience |
| **Party size** | Group play |

---

## 6. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Trust the client | Server is authority |
| Send everything | Send only necessary |
| Ignore latency | Design for 100-200ms |
| Sync exact positions | Interpolate/predict |

---

> **Remember:** Never trust the client. The server is the source of truth.

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
