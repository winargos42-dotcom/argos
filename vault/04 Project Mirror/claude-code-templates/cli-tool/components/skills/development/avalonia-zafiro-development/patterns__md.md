---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-zafiro-development/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-zafiro-development\patterns.md
source_ext: .md
source_sha256: c72dd85a44d96fdc8af9b54c30dcc782d7efa24cd7ca696c86aa671a66578b1c
text_sha256: 8599bccde7fdc52e3c373ca13bbc46c376254bccf3a7f180695c1d28350cb2ff
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-zafiro-development/patterns.md`
- Extract: `text`
- SHA256: `c72dd85a44d96fdc8af9b54c30dcc782d7efa24cd7ca696c86aa671a66578b1c`

## Content

# Common Patterns in Angor/Zafiro

## Refreshable Collections

The `RefreshableCollection` pattern is used to manage lists that can be refreshed via a command, maintaining an internal `SourceCache`/`SourceList` and exposing a `ReadOnlyObservableCollection`.

### Implementation

```csharp
var refresher = RefreshableCollection.Create(
        () => GetDataTask(), 
        model => model.Id)
    .DisposeWith(disposable);

LoadData = refresher.Refresh;
Items = refresher.Items;
```

### Benefits
- **Automatic Loading**: Handles the command execution and results.
- **Efficient Updates**: Uses `EditDiff` internally to update items without clearing the list.
- **UI Friendly**: Exposes `Items` as a `ReadOnlyObservableCollection` suitable for binding.

## Mandatory Validation Pattern

When validating dynamic collections, always use the Zafiro validation extension:

```csharp
this.ValidationRule(
        StagesSource
            .Connect()
            .FilterOnObservable(stage => stage.IsValid)
            .IsEmpty(),
        b => !b,
        _ => "Stages are not valid")
    .DisposeWith(Disposables);
```

## Error Handling Pipeline

Instead of manual `Subscribe`, use `HandleErrorsWith` to pipe errors directly to the user:

```csharp
LoadProjects.HandleErrorsWith(uiServices.NotificationService, "Could not load projects");
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
