---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/react-best-practices/rules/js-early-exit.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\react-best-practices\rules\js-early-exit.md
source_ext: .md
source_sha256: b6b967ab80d2a5fc19851d9db9464cf8e4d0e57dccb607a474b8f7818015951d
text_sha256: 925ce5ce87f3347186ca62212f29cc6baa2b8c85a96d2720ad07c3d0abf781c0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# js-early-exit.md

- Source: `claude-code-templates/cli-tool/components/skills/development/react-best-practices/rules/js-early-exit.md`
- Extract: `text`
- SHA256: `b6b967ab80d2a5fc19851d9db9464cf8e4d0e57dccb607a474b8f7818015951d`

## Content

---
title: Early Return from Functions
impact: LOW-MEDIUM
impactDescription: avoids unnecessary computation
tags: javascript, functions, optimization, early-return
---

## Early Return from Functions

Return early when result is determined to skip unnecessary processing.

**Incorrect (processes all items even after finding answer):**

```typescript
function validateUsers(users: User[]) {
  let hasError = false
  let errorMessage = ''
  
  for (const user of users) {
    if (!user.email) {
      hasError = true
      errorMessage = 'Email required'
    }
    if (!user.name) {
      hasError = true
      errorMessage = 'Name required'
    }
    // Continues checking all users even after error found
  }
  
  return hasError ? { valid: false, error: errorMessage } : { valid: true }
}
```

**Correct (returns immediately on first error):**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) {
      return { valid: false, error: 'Email required' }
    }
    if (!user.name) {
      return { valid: false, error: 'Name required' }
    }
  }

  return { valid: true }
}
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
