---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-development/react-best-practices/references/rules/rendering-content-visibility.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-development\react-best-practices\references\rules\rendering-content-visibility.md
source_ext: .md
source_sha256: 0fa223eac3954b3d7e97cad36ad1bb021a077e590688101cf82a1e7f258c8c32
text_sha256: c48456cbe71373f13cbcd6e0e1c423d6388e93ddf353fccf1716bed75e58fd4f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# rendering-content-visibility.md

- Source: `claude-code-templates/cli-tool/components/skills/web-development/react-best-practices/references/rules/rendering-content-visibility.md`
- Extract: `text`
- SHA256: `0fa223eac3954b3d7e97cad36ad1bb021a077e590688101cf82a1e7f258c8c32`

## Content

---
title: CSS content-visibility for Long Lists
impact: MEDIUM
impactDescription: 10× faster initial render
tags: rendering, css, content-visibility, long-lists
---

## CSS content-visibility for Long Lists

Apply `content-visibility: auto` to defer off-screen rendering.

**CSS:**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

**Example:**

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map(msg => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  )
}
```

For 1000 messages, browser skips layout/paint for ~990 off-screen items (10× faster initial render).

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
