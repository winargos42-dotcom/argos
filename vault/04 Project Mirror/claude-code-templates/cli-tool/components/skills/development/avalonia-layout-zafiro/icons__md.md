---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-layout-zafiro/icons.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-layout-zafiro\icons.md
source_ext: .md
source_sha256: 169131053afff0d4090cc9236bb77765e98705b5df49826bb59a1f02546acaa3
text_sha256: 6da1f1baa21ea256aaff6e7a17f62898cab34e0bdf10cabb5c47f6010738a18e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# icons.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-layout-zafiro/icons.md`
- Extract: `text`
- SHA256: `169131053afff0d4090cc9236bb77765e98705b5df49826bb59a1f02546acaa3`

## Content

# Icon Usage

`Zafiro.Avalonia` simplifies icon management using a specialized markup extension and styling options.

## 🛠️ IconExtension

Use the `{Icon}` markup extension to easily include icons from libraries like FontAwesome.

```xml
<!-- Positional parameter -->
<Button Content="{Icon fa-wallet}" />

<!-- Named parameter -->
<ContentControl Content="{Icon Source=fa-gear}" />
```

## 🎨 IconOptions

`IconOptions` allows you to customize icons without manually wrapping them in other controls. It's often used in styles to provide a consistent look.

```xml
<Style Selector="HeaderedContainer /template/ ContentPresenter#Header EdgePanel /template/ ContentControl#StartContent">
    <Setter Property="IconOptions.Size" Value="20" />
    <Setter Property="IconOptions.Fill" Value="{DynamicResource Accent}" />
    <Setter Property="IconOptions.Padding" Value="10" />
    <Setter Property="IconOptions.CornerRadius" Value="10" />
</Style>
```

### Common Properties:
- `IconOptions.Size`: Sets the width and height of the icon.
- `IconOptions.Fill`: The color/brush of the icon.
- `IconOptions.Background`: Background brush for the icon container.
- `IconOptions.Padding`: Padding inside the icon container.
- `IconOptions.CornerRadius`: Corner radius if a background is used.

## 📁 Shared Icon Resources

Define icons as resources for reuse across the application.

```xml
<ResourceDictionary xmlns="https://github.com/avaloniaui">
    <Icon x:Key="fa-wallet" Source="fa-wallet" />
</ResourceDictionary>
```

Then use them with `StaticResource` if they are already defined:

```xml
<Button Content="{StaticResource fa-wallet}" />
```

However, the `{Icon ...}` extension is usually preferred for its brevity and ability to create new icon instances on the fly.

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
