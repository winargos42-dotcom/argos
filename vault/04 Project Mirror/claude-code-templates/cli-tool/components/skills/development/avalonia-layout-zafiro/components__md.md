---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-layout-zafiro/components.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-layout-zafiro\components.md
source_ext: .md
source_sha256: bd1c64ab5f0426ada1b62e96446c84394cb0574806459ec102a296528f94d267
text_sha256: bc37e1f6445d1e64b47560b14f7435890dd29ece101fb1f5ec2a3d5a18d708e3
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# components.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-layout-zafiro/components.md`
- Extract: `text`
- SHA256: `bd1c64ab5f0426ada1b62e96446c84394cb0574806459ec102a296528f94d267`

## Content

# Building Generic Components

Reducing nesting and complexity is achieved by breaking down views into generic, reusable components.

## 🧊 Generic Components

Instead of building large, complex views, extract recurring patterns into small `UserControl`s.

### Example: A generic "Summary Item"
Instead of repeating a `Grid` with labels and values:

```xml
<!-- ❌ BAD: Repeated Grid -->
<Grid ColumnDefinitions="*,Auto">
   <TextBlock Text="Total:" />
   <TextBlock Grid.Column="1" Text="{Binding Total}" />
</Grid>
```

Create a generic component (or use `EdgePanel` with a Style):

```xml
<!-- ✅ GOOD: Use a specialized control or style -->
<EdgePanel StartContent="Total:" EndContent="{Binding Total}" Classes="SummaryItem" />
```

## 📉 Flattening Layouts

Avoid deep nesting. Deeply nested XAML is hard to read and can impact performance.

- **StackPanel vs Grid**: Use `StackPanel` (with `Spacing`) for simple linear layouts.
- **EdgePanel**: Great for "Label - Value" or "Icon - Text - Action" rows.
- **UniformGrid**: Use for grids where all cells are the same size.

## 🔧 Component Granularity

- **Atomical**: Small controls like custom buttons or icons.
- **Molecular**: Groups of atoms like a `HeaderedContainer` with specific content.
- **Organisms**: Higher-level sections of a page.

Aim for components that are generic enough to be reused but specific enough to simplify the parent view significantly.

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
