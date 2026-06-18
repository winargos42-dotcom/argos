---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/video/motion-canvas/references/signals.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\video\motion-canvas\references\signals.md
source_ext: .md
source_sha256: 4b265e386c9634bf4a8eccfe8900d56964cd11424d03f3f49a4ade47bd42e9cf
text_sha256: 38cf5b762c2797f8ad1be4cd0c777409c680d92d734f0c12b7540155c35bb4c4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# signals.md

- Source: `claude-code-templates/cli-tool/components/skills/video/motion-canvas/references/signals.md`
- Extract: `text`
- SHA256: `4b265e386c9634bf4a8eccfe8900d56964cd11424d03f3f49a4ade47bd42e9cf`

## Content

# Signals in Motion Canvas

Signals represent values that may change over time. They create reactive dependencies between properties, automatically updating dependent values when source values change.

## Creating Signals

```typescript
import {createSignal} from '@motioncanvas/core/lib/signals';

// Create a simple signal
const radius = createSignal(10);

// Get the current value
console.log(radius()); // 10

// Set a new value
radius(20);
console.log(radius()); // 20
```

## Computed Signals

Create signals that depend on other signals:

```typescript
import {createSignal, createComputed} from '@motioncanvas/core/lib/signals';

const radius = createSignal(10);

// Area automatically updates when radius changes
const area = createComputed(() => Math.PI * radius() ** 2);

console.log(area()); // ~314.159

radius(20);
console.log(area()); // ~1256.637
```

## Signals in Components

Components use signals for reactive properties:

```typescript
import {makeScene2D} from '@motioncanvas/2d/lib/scenes';
import {Circle} from '@motioncanvas/2d/lib/components';
import {createRef, createSignal} from '@motioncanvas/core/lib/utils';

export default makeScene2D(function* (view) {
  const circleRef = createRef<Circle>();
  const radiusSignal = createSignal(50);

  view.add(
    <Circle
      ref={circleRef}
      size={() => radiusSignal() * 2} // Reactive binding
      fill="#e13238"
    />
  );

  // Animate the signal
  yield* radiusSignal(100, 2);
});
```

## Binding Signals

Link signals together for synchronized updates:

```typescript
export default makeScene2D(function* (view) {
  const circle1 = createRef<Circle>();
  const circle2 = createRef<Circle>();

  view.add(
    <>
      <Circle ref={circle1} x={-200} size={100} fill="#e13238" />
      <Circle ref={circle2} x={200} size={100} fill="#e6a700" />
    </>
  );

  // Bind circle2's size to circle1's size
  circle2().size(circle1().size);

  // Now both circles resize together
  yield* circle1().size(200, 1);
});
```

## Animating Signals

Signals can be tweened over time:

```typescript
import {createSignal} from '@motioncanvas/core/lib/signals';
import {tween} from '@motioncanvas/core/lib/tweening';
import {easeInOutCubic} from '@motioncanvas/core/lib/tweening';

export default makeScene2D(function* (view) {
  const mySignal = createSignal(0);

  // Tween from 0 to 100 over 2 seconds
  yield* tween(2, value => {
    mySignal(easeInOutCubic(value, 0, 100));
  });
});
```

## Resources

- [Motion Canvas Signals Documentation](https://motioncanvas.io/docs/signals/)
- [Reactive Programming Concepts](https://motioncanvas.io/docs/signals/)

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
