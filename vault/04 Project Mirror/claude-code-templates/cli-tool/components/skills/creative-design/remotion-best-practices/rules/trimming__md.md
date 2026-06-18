---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/remotion-best-practices/rules/trimming.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\remotion-best-practices\rules\trimming.md
source_ext: .md
source_sha256: fbfa4d55404e12e962942850c1e5bbdcff0cb824a8ecf8394bd5b5398262a9b4
text_sha256: 40727aefd5939a42925f1ee1fcdfaf733f7fc098c26d7676f7fb69b418913375
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# trimming.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/remotion-best-practices/rules/trimming.md`
- Extract: `text`
- SHA256: `fbfa4d55404e12e962942850c1e5bbdcff0cb824a8ecf8394bd5b5398262a9b4`

## Content

---
name: trimming
description: Trimming patterns for Remotion - cut the beginning or end of animations
metadata:
  tags: sequence, trim, clip, cut, offset
---

Use `<Sequence>` with a negative `from` value to trim the start of an animation.

## Trim the Beginning

A negative `from` value shifts time backwards, making the animation start partway through:

```tsx
import { Sequence, useVideoConfig } from "remotion";

const fps = useVideoConfig();

<Sequence from={-0.5 * fps}>
  <MyAnimation />
</Sequence>
```

The animation appears 15 frames into its progress - the first 15 frames are trimmed off.
Inside `<MyAnimation>`, `useCurrentFrame()` starts at 15 instead of 0.

## Trim the End

Use `durationInFrames` to unmount content after a specified duration:

```tsx

<Sequence durationInFrames={1.5 * fps}>
  <MyAnimation />
</Sequence>
```

The animation plays for 45 frames, then the component unmounts.

## Trim and Delay

Nest sequences to both trim the beginning and delay when it appears:

```tsx
<Sequence from={30}>
  <Sequence from={-15}>
    <MyAnimation />
  </Sequence>
</Sequence>
```

The inner sequence trims 15 frames from the start, and the outer sequence delays the result by 30 frames.

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
