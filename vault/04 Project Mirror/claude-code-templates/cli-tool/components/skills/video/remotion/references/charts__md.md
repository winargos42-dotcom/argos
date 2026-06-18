---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/video/remotion/references/charts.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\video\remotion\references\charts.md
source_ext: .md
source_sha256: 39c8638f05a5453a7ae07d586869a8a6432bf2de331b518e012d4c6de5add275
text_sha256: 2430705a627c468e0922e2f78ca1a2379537d378b5fe76292b69f44659a5d66e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# charts.md

- Source: `claude-code-templates/cli-tool/components/skills/video/remotion/references/charts.md`
- Extract: `text`
- SHA256: `39c8638f05a5453a7ae07d586869a8a6432bf2de331b518e012d4c6de5add275`

## Content

---
name: charts
description: Chart and data visualization patterns for Remotion. Use when creating bar charts, pie charts, histograms, progress bars, or any data-driven animations.
metadata:
  tags: charts, data, visualization, bar-chart, pie-chart, graphs
---

# Charts in Remotion

You can create bar charts in Remotion by using regular React code - HTML and SVG is allowed, as well as D3.js.

## No animations not powered by `useCurrentFrame()`

Disable all animations by third party libraries.  
They will cause flickering during rendering.  
Instead, drive all animations from `useCurrentFrame()`.

## Bar Chart Animations

See [Bar Chart Example](assets/charts/bar-chart.tsx) for a basic example implmentation.

### Staggered Bars

You can animate the height of the bars and stagger them like this:

```tsx
const STAGGER_DELAY = 5;
const frame = useCurrentFrame();
const {fps} = useVideoConfig();

const bars = data.map((item, i) => {
  const delay = i * STAGGER_DELAY;
  const height = spring({
    frame,
    fps,
    delay,
    config: {damping: 200},
  });
  return <div style={{height: height * item.value}} />;
});
```

## Pie Chart Animation

Animate segments using stroke-dashoffset, starting from 12 o'clock.

```tsx
const frame = useCurrentFrame();
const {fps} = useVideoConfig();

const progress = interpolate(frame, [0, 100], [0, 1]);

const circumference = 2 * Math.PI * radius;
const segmentLength = (value / total) * circumference;
const offset = interpolate(progress, [0, 1], [segmentLength, 0]);

<circle r={radius} cx={center} cy={center} fill="none" stroke={color} strokeWidth={strokeWidth} strokeDasharray={`${segmentLength} ${circumference}`} strokeDashoffset={offset} transform={`rotate(-90 ${center} ${center})`} />;
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
