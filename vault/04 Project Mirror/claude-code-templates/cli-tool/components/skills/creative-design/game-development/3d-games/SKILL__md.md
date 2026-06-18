---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/game-development/3d-games/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\game-development\3d-games\SKILL.md
source_ext: .md
source_sha256: dea21f28a7816ddc2cfd6d9fffc5bf5288bf0e75d2f561eb3b2024560082f273
text_sha256: 141bf1ca6af96066cffa91b2b37417b9d1cffec4fcc2a6ef1333ee976121f7dd
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/game-development/3d-games/SKILL.md`
- Extract: `text`
- SHA256: `dea21f28a7816ddc2cfd6d9fffc5bf5288bf0e75d2f561eb3b2024560082f273`

## Content

---
name: 3d-games
description: 3D game development principles. Rendering, shaders, physics, cameras.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# 3D Game Development

> Principles for 3D game systems.

---

## 1. Rendering Pipeline

### Stages

```
1. Vertex Processing → Transform geometry
2. Rasterization → Convert to pixels
3. Fragment Processing → Color pixels
4. Output → To screen
```

### Optimization Principles

| Technique | Purpose |
|-----------|---------|
| **Frustum culling** | Don't render off-screen |
| **Occlusion culling** | Don't render hidden |
| **LOD** | Less detail at distance |
| **Batching** | Combine draw calls |

---

## 2. Shader Principles

### Shader Types

| Type | Purpose |
|------|---------|
| **Vertex** | Position, normals |
| **Fragment/Pixel** | Color, lighting |
| **Compute** | General computation |

### When to Write Custom Shaders

- Special effects (water, fire, portals)
- Stylized rendering (toon, sketch)
- Performance optimization
- Unique visual identity

---

## 3. 3D Physics

### Collision Shapes

| Shape | Use Case |
|-------|----------|
| **Box** | Buildings, crates |
| **Sphere** | Balls, quick checks |
| **Capsule** | Characters |
| **Mesh** | Terrain (expensive) |

### Principles

- Simple colliders, complex visuals
- Layer-based filtering
- Raycasting for line-of-sight

---

## 4. Camera Systems

### Camera Types

| Type | Use |
|------|-----|
| **Third-person** | Action, adventure |
| **First-person** | Immersive, FPS |
| **Isometric** | Strategy, RPG |
| **Orbital** | Inspection, editors |

### Camera Feel

- Smooth following (lerp)
- Collision avoidance
- Look-ahead for movement
- FOV changes for speed

---

## 5. Lighting

### Light Types

| Type | Use |
|------|-----|
| **Directional** | Sun, moon |
| **Point** | Lamps, torches |
| **Spot** | Flashlight, stage |
| **Ambient** | Base illumination |

### Performance Consideration

- Real-time shadows are expensive
- Bake when possible
- Shadow cascades for large worlds

---

## 6. Level of Detail (LOD)

### LOD Strategy

| Distance | Model |
|----------|-------|
| Near | Full detail |
| Medium | 50% triangles |
| Far | 25% or billboard |

---

## 7. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Mesh colliders everywhere | Simple shapes |
| Real-time shadows on mobile | Baked or blob shadows |
| One LOD for all distances | Distance-based LOD |
| Unoptimized shaders | Profile and simplify |

---

> **Remember:** 3D is about illusion. Create the impression of detail, not the detail itself.

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
