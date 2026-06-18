---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-viewmodels-zafiro/navigation_sections.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-viewmodels-zafiro\navigation_sections.md
source_ext: .md
source_sha256: 6f6dc7f969d5844e4af47810331e8b260c31f5a4f2fb9f0e05e5e92759bcaec5
text_sha256: 39821612996dae2deca4fa84c59077887b482894780940482f456ca61ed6eea1
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# navigation_sections.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-viewmodels-zafiro/navigation_sections.md`
- Extract: `text`
- SHA256: `6f6dc7f969d5844e4af47810331e8b260c31f5a4f2fb9f0e05e5e92759bcaec5`

## Content

# Navigation & Sections

Zafiro provides powerful abstractions for managing application-wide navigation and modular UI sections.

## Navigation with INavigator

The `INavigator` interface is used to switch between different views or viewmodels.

```csharp
public class MyViewModel(INavigator navigator)
{
    public async Task GoToDetails()
    {
        await navigator.Navigate(() => new DetailsViewModel());
    }
}
```

## UI Sections

Sections are modular parts of the UI (like tabs or sidebar items) that can be automatically registered.

### The [Section] Attribute

ViewModels intended to be sections should be marked with the `[Section]` attribute.

```csharp
[Section("Wallet", icon: "fa-wallet")]
public class WalletSectionViewModel : IWalletSectionViewModel
{
    // ...
}
```

### Automatic Registration

In the `CompositionRoot`, sections can be automatically registered:

```csharp
services.AddAnnotatedSections(logger);
services.AddSectionsFromAttributes(logger);
```

### Switching Sections

You can switch the current active section via the `IShellViewModel`:

```csharp
shellViewModel.SetSection("Browse");
```

> [!IMPORTANT]
> The `icon` parameter in the `[Section]` attribute supports FontAwesome icons (e.g., `fa-home`) when configured with `ProjektankerIconControlProvider`.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Training Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Training Hub]]
