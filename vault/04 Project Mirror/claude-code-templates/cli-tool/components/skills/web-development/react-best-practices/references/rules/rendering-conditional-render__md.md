---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-development/react-best-practices/references/rules/rendering-conditional-render.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-development\react-best-practices\references\rules\rendering-conditional-render.md
source_ext: .md
source_sha256: 7e185b05ef0d1dc5df8687b9c5a123df045c9551f6491799f8878345bdbd5023
text_sha256: d072261110d36ae29f289a1e7dc6bd3fc23280ae59e06f28b610da8c00bb2469
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# rendering-conditional-render.md

- Source: `claude-code-templates/cli-tool/components/skills/web-development/react-best-practices/references/rules/rendering-conditional-render.md`
- Extract: `text`
- SHA256: `7e185b05ef0d1dc5df8687b9c5a123df045c9551f6491799f8878345bdbd5023`

## Content

---
title: Use Explicit Conditional Rendering
impact: MEDIUM
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
