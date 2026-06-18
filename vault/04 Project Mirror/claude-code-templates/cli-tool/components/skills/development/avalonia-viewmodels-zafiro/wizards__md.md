---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-viewmodels-zafiro/wizards.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-viewmodels-zafiro\wizards.md
source_ext: .md
source_sha256: 191387094043afb1936d1b7e71af3f7e9f0120c58129cbe01f12e83a760a75b5
text_sha256: 3dd2508d4bc93b91885fbfb023c74b42d4501f7a615ba2fabac434ee46ccb566
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# wizards.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-viewmodels-zafiro/wizards.md`
- Extract: `text`
- SHA256: `191387094043afb1936d1b7e71af3f7e9f0120c58129cbe01f12e83a760a75b5`

## Content

# Wizards & Flows

Complex multi-step processes are handled using the `SlimWizard` pattern. This provides a declarative way to define steps, navigation logic, and final results.

## Defining a Wizard

Use `WizardBuilder` to define the steps. Each step corresponds to a ViewModel.

```csharp
SlimWizard<string> wizard = WizardBuilder
    .StartWith(() => new Step1ViewModel(data))
        .NextUnit()
        .WhenValid()
    .Then(prevResult => new Step2ViewModel(prevResult))
        .NextCommand(vm => vm.CustomNextCommand)
    .Then(result => new SuccessViewModel("Done!"))
        .Next((_, s) => s, "Finish")
    .WithCompletionFinalStep();
```

### Navigation Rules

- **NextUnit()**: Advances when a simple signal is emitted.
- **NextCommand()**: Advances when a specific command in the ViewModel execution successfully.
- **WhenValid()**: Wait until the current ViewModel's validation passes before allowing navigation.
- **Always()**: Navigation is always allowed.

## Navigation Integration

The wizard is navigated using an `INavigator`:

```csharp
public async Task CreateSomething()
{
    var wizard = BuildWizard();
    var result = await wizard.Navigate(navigator);
    // Handle result
}
```

## Step Configuration

- **WithCompletionFinalStep()**: Marks the wizard as finished when the last step completes.
- **WithCommitFinalStep()**: Typically used for wizards that perform a final "Save" or "Deploy" action.

> [!NOTE]
> The `SlimWizard` handles the "Back" command automatically, providing a consistent user experience across different flows.

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
