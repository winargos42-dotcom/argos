---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/game-development/vr-ar/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\game-development\vr-ar\SKILL.md
source_ext: .md
source_sha256: 214b6b557165901acdb6e2e1fe9471fbc33d6fbb650dc53d5673a1027ddc45fe
text_sha256: 59ddbdecc4fa17e74c4747f5f02bd69edb8bffcd1cdc2866dd6a053e19bc139e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/game-development/vr-ar/SKILL.md`
- Extract: `text`
- SHA256: `214b6b557165901acdb6e2e1fe9471fbc33d6fbb650dc53d5673a1027ddc45fe`

## Content

---
name: vr-ar
description: VR/AR development principles. Comfort, interaction, performance requirements.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# VR/AR Development

> Immersive experience principles.

---

## 1. Platform Selection

### VR Platforms

| Platform | Use Case |
|----------|----------|
| **Quest** | Standalone, wireless |
| **PCVR** | High fidelity |
| **PSVR** | Console market |
| **WebXR** | Browser-based |

### AR Platforms

| Platform | Use Case |
|----------|----------|
| **ARKit** | iOS devices |
| **ARCore** | Android devices |
| **WebXR** | Browser AR |
| **HoloLens** | Enterprise |

---

## 2. Comfort Principles

### Motion Sickness Prevention

| Cause | Solution |
|-------|----------|
| **Locomotion** | Teleport, snap turn |
| **Low FPS** | Maintain 90 FPS |
| **Camera shake** | Avoid or minimize |
| **Rapid acceleration** | Gradual movement |

### Comfort Settings

- Vignette during movement
- Snap vs smooth turning
- Seated vs standing modes
- Height calibration

---

## 3. Performance Requirements

### Target Metrics

| Platform | FPS | Resolution |
|----------|-----|------------|
| Quest 2 | 72-90 | 1832x1920 |
| Quest 3 | 90-120 | 2064x2208 |
| PCVR | 90 | 2160x2160+ |
| PSVR2 | 90-120 | 2000x2040 |

### Frame Budget

- VR requires consistent frame times
- Single dropped frame = visible judder
- 90 FPS = 11.11ms budget

---

## 4. Interaction Principles

### Controller Interaction

| Type | Use |
|------|-----|
| **Point + click** | UI, distant objects |
| **Grab** | Manipulation |
| **Gesture** | Magic, special actions |
| **Physical** | Throwing, swinging |

### Hand Tracking

- More immersive but less precise
- Good for: social, casual
- Challenging for: action, precision

---

## 5. Spatial Design

### World Scale

- 1 unit = 1 meter (critical)
- Objects must feel right size
- Test with real measurements

### Depth Cues

| Cue | Importance |
|-----|------------|
| Stereo | Primary depth |
| Motion parallax | Secondary |
| Shadows | Grounding |
| Occlusion | Layering |

---

## 6. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Move camera without player | Player controls camera |
| Drop below 90 FPS | Maintain frame rate |
| Use tiny UI text | Large, readable text |
| Ignore arm length | Scale to player reach |

---

> **Remember:** Comfort is not optional. Sick players don't play.

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
