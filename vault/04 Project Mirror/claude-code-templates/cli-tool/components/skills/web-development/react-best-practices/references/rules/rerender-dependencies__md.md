---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-development/react-best-practices/references/rules/rerender-dependencies.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-development\react-best-practices\references\rules\rerender-dependencies.md
source_ext: .md
source_sha256: a389de1658fd51b077aeb208a59d199b75097a9d94e23cab059b45edddf3feca
text_sha256: 379ac335c8042df57646326de95deabef38e20ce2b8d8a21fbd579f8c74d312f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# rerender-dependencies.md

- Source: `claude-code-templates/cli-tool/components/skills/web-development/react-best-practices/references/rules/rerender-dependencies.md`
- Extract: `text`
- SHA256: `a389de1658fd51b077aeb208a59d199b75097a9d94e23cab059b45edddf3feca`

## Content

---
title: Narrow Effect Dependencies
impact: MEDIUM
impactDescription: minimizes effect re-runs
tags: rerender, useEffect, dependencies, optimization
---

## Narrow Effect Dependencies

Specify primitive dependencies instead of objects to minimize effect re-runs.

**Incorrect (re-runs on any user field change):**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user])
```

**Correct (re-runs only when id changes):**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

**For derived state, compute outside effect:**

```tsx
// Incorrect: runs on width=767, 766, 765...
useEffect(() => {
  if (width < 768) {
    enableMobileMode()
  }
}, [width])

// Correct: runs only on boolean transition
const isMobile = width < 768
useEffect(() => {
  if (isMobile) {
    enableMobileMode()
  }
}, [isMobile])
```

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
