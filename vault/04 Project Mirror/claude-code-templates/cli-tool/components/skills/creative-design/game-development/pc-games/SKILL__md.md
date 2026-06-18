---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/game-development/pc-games/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\game-development\pc-games\SKILL.md
source_ext: .md
source_sha256: 693e7324cfdcc93fbc80ac18ade23809f2cfd314f1b923dd93058558cf9bbd31
text_sha256: 739b244b02659ec53ca719bbdf8ac2684dbeeafc5d5ddac124ffa6407f10f5df
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/game-development/pc-games/SKILL.md`
- Extract: `text`
- SHA256: `693e7324cfdcc93fbc80ac18ade23809f2cfd314f1b923dd93058558cf9bbd31`

## Content

---
name: pc-games
description: PC and console game development principles. Engine selection, platform features, optimization strategies.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# PC/Console Game Development

> Engine selection and platform-specific principles.

---

## 1. Engine Selection

### Decision Tree

```
What are you building?
│
├── 2D Game
│   ├── Open source important? → Godot
│   └── Large team/assets? → Unity
│
├── 3D Game
│   ├── AAA visual quality? → Unreal
│   ├── Cross-platform priority? → Unity
│   └── Indie/open source? → Godot 4
│
└── Specific Needs
    ├── DOTS performance? → Unity
    ├── Nanite/Lumen? → Unreal
    └── Lightweight? → Godot
```

### Comparison

| Factor | Unity 6 | Godot 4 | Unreal 5 |
|--------|---------|---------|----------|
| 2D | Good | Excellent | Limited |
| 3D | Good | Good | Excellent |
| Learning | Medium | Easy | Hard |
| Cost | Revenue share | Free | 5% after $1M |
| Team | Any | Solo-Medium | Medium-Large |

---

## 2. Platform Features

### Steam Integration

| Feature | Purpose |
|---------|---------|
| Achievements | Player goals |
| Cloud Saves | Cross-device progress |
| Leaderboards | Competition |
| Workshop | User mods |
| Rich Presence | Show in-game status |

### Console Requirements

| Platform | Certification |
|----------|--------------|
| PlayStation | TRC compliance |
| Xbox | XR compliance |
| Nintendo | Lotcheck |

---

## 3. Controller Support

### Input Abstraction

```
Map ACTIONS, not buttons:
- "confirm" → A (Xbox), Cross (PS), B (Nintendo)
- "cancel" → B (Xbox), Circle (PS), A (Nintendo)
```

### Haptic Feedback

| Intensity | Use |
|-----------|-----|
| Light | UI feedback |
| Medium | Impacts |
| Heavy | Major events |

---

## 4. Performance Optimization

### Profiling First

| Engine | Tool |
|--------|------|
| Unity | Profiler Window |
| Godot | Debugger → Profiler |
| Unreal | Unreal Insights |

### Common Bottlenecks

| Bottleneck | Solution |
|------------|----------|
| Draw calls | Batching, atlases |
| GC spikes | Object pooling |
| Physics | Simpler colliders |
| Shaders | LOD shaders |

---

## 5. Engine-Specific Principles

### Unity 6

- DOTS for performance-critical systems
- Burst compiler for hot paths
- Addressables for asset streaming

### Godot 4

- GDScript for rapid iteration
- C# for complex logic
- Signals for decoupling

### Unreal 5

- Blueprint for designers
- C++ for performance
- Nanite for high-poly environments
- Lumen for dynamic lighting

---

## 6. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Choose engine by hype | Choose by project needs |
| Ignore platform guidelines | Study certification requirements |
| Hardcode input buttons | Abstract to actions |
| Skip profiling | Profile early and often |

---

> **Remember:** Engine is a tool. Master the principles, then adapt to any engine.

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
