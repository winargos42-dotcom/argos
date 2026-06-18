---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-layout-zafiro/behaviors.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-layout-zafiro\behaviors.md
source_ext: .md
source_sha256: e6a38319e42c967be947507c34a2522f76b57e46179f9fbc12c85953b412e6bc
text_sha256: 392138c43ea796ce352a20c9ab1dd940bebcabed7a3876eb6d3c1fe3285a54b4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# behaviors.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-layout-zafiro/behaviors.md`
- Extract: `text`
- SHA256: `e6a38319e42c967be947507c34a2522f76b57e46179f9fbc12c85953b412e6bc`

## Content

# Interactions and Logic

To keep XAML clean and maintainable, minimize logic in views and avoid excessive use of converters.

## 🎭 Xaml.Interaction.Behaviors

Use `Interaction.Behaviors` to handle UI-related logic that doesn't belong in the ViewModel, such as focus management, animations, or specialized event handling.

```xml
<TextBox Text="{Binding Address}">
    <Interaction.Behaviors>
        <UntouchedClassBehavior />
    </Interaction.Behaviors>
</TextBox>
```

### Why use Behaviors?
- **Encapsulation**: UI logic is contained in a reusable behavior class.
- **Clean XAML**: Avoids code-behind and complex XAML triggers.
- **Testability**: Behaviors can be tested independently of the View.

## 🚫 Avoiding Converters

Converters often lead to "magical" logic hidden in XAML. Whenever possible, prefer:

1.  **ViewModel Properties**: Let the ViewModel provide the final data format (e.g., a `string` formatted for display).
2.  **MultiBinding**: Use for simple logic combinations (And/Or) directly in XAML.
3.  **Behaviors**: For more complex interactions that involve state or events.

### When to use Converters?
Only use them when the conversion is purely visual and highly reusable across different contexts (e.g., `BoolToOpacityConverter`).

## 🧩 Simplified Interactions

If you find yourself needing a complex converter or behavior, consider if the component can be simplified or if the data model can be adjusted to make the view binding more direct.

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
