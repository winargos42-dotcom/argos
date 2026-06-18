---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-layout-zafiro/themes.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-layout-zafiro\themes.md
source_ext: .md
source_sha256: 4fa99bb255e3a05945474f4434189cbd61b68c30876faf847b831ed96946e229
text_sha256: 7c75d2f788390c607235f4d96b178f45659267db7942870a9b7e7ad49d4d2262
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# themes.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-layout-zafiro/themes.md`
- Extract: `text`
- SHA256: `4fa99bb255e3a05945474f4434189cbd61b68c30876faf847b831ed96946e229`

## Content

# Theme Organization and Shared Styles

Efficient theme organization is key to avoiding redundant XAML and ensuring visual consistency.

## 🏗️ Structure

Follow the pattern from Angor:

1.  **Colors & Brushes**: Define in a dedicated `Colors.axaml`. Use `DynamicResource` to support theme switching.
2.  **Styles**: Group styles by category (e.g., `Buttons.axaml`, `Containers.axaml`, `Typography.axaml`).
3.  **App-wide Theme**: Aggregate all styles in a main `Theme.axaml`.

## 🎨 Avoiding Redundancy

Instead of setting properties directly on elements:

```xml
<!-- ❌ BAD: Redundant properties -->
<HeaderedContainer CornerRadius="10" BorderThickness="1" BorderBrush="Blue" Background="LightBlue" />
<HeaderedContainer CornerRadius="10" BorderThickness="1" BorderBrush="Blue" Background="LightBlue" />

<!-- ✅ GOOD: Use Classes and Styles -->
<HeaderedContainer Classes="BlueSection" />
<HeaderedContainer Classes="BlueSection" />
```

Define the style in a shared `axaml` file:

```xml
<Style Selector="HeaderedContainer.BlueSection">
    <Setter Property="CornerRadius" Value="10" />
    <Setter Property="BorderThickness" Value="1" />
    <Setter Property="BorderBrush" Value="{DynamicResource Accent}" />
    <Setter Property="Background" Value="{DynamicResource SurfaceSubtle}" />
</Style>
```

## 🧩 Shared Icons and Resources

Centralize icon definitions and other shared resources in `Icons.axaml` and include them in the `MergedDictionaries` of your theme or `App.axaml`.

```xml
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <MergeResourceInclude Source="UI/Themes/Styles/Containers.axaml" />
            <MergeResourceInclude Source="UI/Shared/Resources/Icons.axaml" />
        </ResourceDictionary.MergedDictionaries>
    </ResourceDictionary>
</Application.Resources>
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
