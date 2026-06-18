---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-layout-zafiro/containers.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-layout-zafiro\containers.md
source_ext: .md
source_sha256: a81ea90485c16c0135edbe706acf1405b580a498df668e38662cd1d785e43364
text_sha256: 815f69e8b76593158799e0bb7c3e4e1c3c1ba314ba46f7e8e5305c90b528c849
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# containers.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-layout-zafiro/containers.md`
- Extract: `text`
- SHA256: `a81ea90485c16c0135edbe706acf1405b580a498df668e38662cd1d785e43364`

## Content

# Semantic Containers

Using the right container for the data type simplifies XAML and improves maintainability. `Zafiro.Avalonia` provides specialized controls for common layout patterns.

## 📦 HeaderedContainer

Prefer `HeaderedContainer` over a `Border` or `Grid` when a section needs a title or header.

```xml
<HeaderedContainer Header="Security Settings" Classes="WizardSection">
    <StackPanel>
        <!-- Content here -->
    </StackPanel>
</HeaderedContainer>
```

### Key Properties:
- `Header`: The content or string for the header.
- `HeaderBackground`: Brush for the header area.
- `ContentPadding`: Padding for the content area.

## ↔️ EdgePanel

Use `EdgePanel` to position elements at the edges of a container without complex `Grid` definitions.

```xml
<EdgePanel StartContent="{Icon fa-wallet}" 
           Content="Wallet Balance" 
           EndContent="$1,234.00" />
```

### Slots:
- `StartContent`: Aligned to the left (or beginning).
- `Content`: Fills the remaining space in the middle.
- `EndContent`: Aligned to the right (or end).

## 📇 Card

A simple container for grouping related information, often used inside `HeaderedContainer` or as a standalone element in a list.

```xml
<Card Header="Enter recipient address:">
    <TextBox Text="{Binding Address}" />
</Card>
```

## 📐 Best Practices

- Use `Classes` to apply themed variants (e.g., `Classes="Section"`, `Classes="Highlight"`).
- Customize internal parts of the containers using templates in your styles when necessary, rather than nesting more controls.

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
