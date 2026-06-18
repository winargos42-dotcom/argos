---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/react-best-practices/rules/rendering-conditional-render.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\react-best-practices\rules\rendering-conditional-render.md
source_ext: .md
source_sha256: 6db58f36c8b080c35e91f6504281f85ea2dbd133030610c860e60181d6d9556a
text_sha256: 2ec2fa23c4148285144687050c52369adba3da2fbe3d486f8d3e0aad8f06f2bc
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# rendering-conditional-render.md

- Source: `claude-code-templates/cli-tool/components/skills/development/react-best-practices/rules/rendering-conditional-render.md`
- Extract: `text`
- SHA256: `6db58f36c8b080c35e91f6504281f85ea2dbd133030610c860e60181d6d9556a`

## Content

---
title: Use Explicit Conditional Rendering
impact: LOW
impactDescription: prevents rendering 0 or NaN
tags: rendering, conditional, jsx, falsy-values
---

## Use Explicit Conditional Rendering

Use explicit ternary operators (`? :`) instead of `&&` for conditional rendering when the condition can be `0`, `NaN`, or other falsy values that render.

**Incorrect (renders "0" when count is 0):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count && <span className="badge">{count}</span>}
    </div>
  )
}

// When count = 0, renders: <div>0</div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```

**Correct (renders nothing when count is 0):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count > 0 ? <span className="badge">{count}</span> : null}
    </div>
  )
}

// When count = 0, renders: <div></div>
// When count = 5, renders: <div><span class="badge">5</span></div>
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
