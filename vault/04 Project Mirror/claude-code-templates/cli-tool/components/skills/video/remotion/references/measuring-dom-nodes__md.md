---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/video/remotion/references/measuring-dom-nodes.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\video\remotion\references\measuring-dom-nodes.md
source_ext: .md
source_sha256: 9836d5dc7fbedf424ddb48526e427a55e61fb80ccff64d7d94c2249c1eb54aea
text_sha256: 5270db465cb9eed1942b9970de101211f954b7802dfd92e957bdc7e3eebe6c5c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# measuring-dom-nodes.md

- Source: `claude-code-templates/cli-tool/components/skills/video/remotion/references/measuring-dom-nodes.md`
- Extract: `text`
- SHA256: `9836d5dc7fbedf424ddb48526e427a55e61fb80ccff64d7d94c2249c1eb54aea`

## Content

---
name: measuring-dom-nodes
description: Measuring DOM element dimensions in Remotion
metadata:
  tags: measure, layout, dimensions, getBoundingClientRect, scale
---

# Measuring DOM nodes in Remotion

Remotion applies a `scale()` transform to the video container, which affects values from `getBoundingClientRect()`. Use `useCurrentScale()` to get correct measurements.

## Measuring element dimensions

```tsx
import { useCurrentScale } from "remotion";
import { useRef, useEffect, useState } from "react";

export const MyComponent = () => {
  const ref = useRef<HTMLDivElement>(null);
  const scale = useCurrentScale();
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    setDimensions({
      width: rect.width / scale,
      height: rect.height / scale,
    });
  }, [scale]);

  return <div ref={ref}>Content to measure</div>;
};
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
