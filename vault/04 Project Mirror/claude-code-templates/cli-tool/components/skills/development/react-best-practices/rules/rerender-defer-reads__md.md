---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/react-best-practices/rules/rerender-defer-reads.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\react-best-practices\rules\rerender-defer-reads.md
source_ext: .md
source_sha256: bb98d9b7c7622641887df6407406a8c4f61510af9cc1bd275574ebee71bac8c8
text_sha256: 234050a77faf50cb306be10a9e15bd4421134ab5907e75f13e6d78e2bd262dc9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# rerender-defer-reads.md

- Source: `claude-code-templates/cli-tool/components/skills/development/react-best-practices/rules/rerender-defer-reads.md`
- Extract: `text`
- SHA256: `bb98d9b7c7622641887df6407406a8c4f61510af9cc1bd275574ebee71bac8c8`

## Content

---
title: Defer State Reads to Usage Point
impact: MEDIUM
impactDescription: avoids unnecessary subscriptions
tags: rerender, searchParams, localStorage, optimization
---

## Defer State Reads to Usage Point

Don't subscribe to dynamic state (searchParams, localStorage) if you only read it inside callbacks.

**Incorrect (subscribes to all searchParams changes):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const searchParams = useSearchParams()

  const handleShare = () => {
    const ref = searchParams.get('ref')
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>Share</button>
}
```

**Correct (reads on demand, no subscription):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const handleShare = () => {
    const params = new URLSearchParams(window.location.search)
    const ref = params.get('ref')
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>Share</button>
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
