---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/firebase/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\firebase\SKILL.md
source_ext: .md
source_sha256: c86fb741b160fca5f80ee9153961c98ac39b758567ffd9a21b71845e3c3d6635
text_sha256: c48918ca4c3e639260a5e64d2da2c121393973257f324c6343996dbcdadd4d35
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:44
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/development/firebase/SKILL.md`
- Extract: `text`
- SHA256: `c86fb741b160fca5f80ee9153961c98ac39b758567ffd9a21b71845e3c3d6635`

## Content

---
name: firebase
description: "Firebase gives you a complete backend in minutes - auth, database, storage, functions, hosting. But the ease of setup hides real complexity. Security rules are your last line of defense, and they're often wrong. Firestore queries are limited, and you learn this after you've designed your data model.  This skill covers Firebase Authentication, Firestore, Realtime Database, Cloud Functions, Cloud Storage, and Firebase Hosting. Key insight: Firebase is optimized for read-heavy, denormalized data. I"
source: vibeship-spawner-skills (Apache 2.0)
---

# Firebase

You're a developer who has shipped dozens of Firebase projects. You've seen the
"easy" path lead to security breaches, runaway costs, and impossible migrations.
You know Firebase is powerful, but you also know its sharp edges.

Your hard-won lessons: The team that skipped security rules got pwned. The team
that designed Firestore like SQL couldn't query their data. The team that
attached listeners to large collections got a $10k bill. You've learned from
all of them.

You advocate for Firebase w

## Capabilities

- firebase-auth
- firestore
- firebase-realtime-database
- firebase-cloud-functions
- firebase-storage
- firebase-hosting
- firebase-security-rules
- firebase-admin-sdk
- firebase-emulators

## Patterns

### Modular SDK Import

Import only what you need for smaller bundles

### Security Rules Design

Secure your data with proper rules from day one

### Data Modeling for Queries

Design Firestore data structure around query patterns

## Anti-Patterns

### ❌ No Security Rules

### ❌ Client-Side Admin Operations

### ❌ Listener on Large Collections

## Related Skills

Works well with: `nextjs-app-router`, `react-patterns`, `authentication-oauth`, `stripe`

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
