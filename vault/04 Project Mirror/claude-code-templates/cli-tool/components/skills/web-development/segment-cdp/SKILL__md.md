---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-development/segment-cdp/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-development\segment-cdp\SKILL.md
source_ext: .md
source_sha256: a78f4bac42da6db3d75f12b300ed2aace76a01d1126960c41a43db1829248784
text_sha256: 39eb6ef8d81adaa58587929d4875d94bd6ecd9c2ab0168d7f724d3820023521f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/web-development/segment-cdp/SKILL.md`
- Extract: `text`
- SHA256: `a78f4bac42da6db3d75f12b300ed2aace76a01d1126960c41a43db1829248784`

## Content

---
name: segment-cdp
description: "Expert patterns for Segment Customer Data Platform including Analytics.js, server-side tracking, tracking plans with Protocols, identity resolution, destinations configuration, and data governance best practices. Use when: segment, analytics.js, customer data platform, cdp, tracking plan."
source: vibeship-spawner-skills (Apache 2.0)
---

# Segment CDP

## Patterns

### Analytics.js Browser Integration

Client-side tracking with Analytics.js. Include track, identify, page,
and group calls. Anonymous ID persists until identify merges with user.


### Server-Side Tracking with Node.js

High-performance server-side tracking using @segment/analytics-node.
Non-blocking with internal batching. Essential for backend events,
webhooks, and sensitive data.


### Tracking Plan Design

Design event schemas using Object + Action naming convention.
Define required properties, types, and validation rules.
Connect to Protocols for enforcement.


## Anti-Patterns

### ❌ Dynamic Event Names

### ❌ Tracking Properties as Events

### ❌ Missing Identify Before Track

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | medium | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |
| Issue | high | See docs |
| Issue | low | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | high | See docs |

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
