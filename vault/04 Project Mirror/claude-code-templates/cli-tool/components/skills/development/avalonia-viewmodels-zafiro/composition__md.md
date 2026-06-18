---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-viewmodels-zafiro/composition.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-viewmodels-zafiro\composition.md
source_ext: .md
source_sha256: a6f050d07e3fd084f110a133610a7168ed0cfc62d8a6fb4a51da844f22f9846a
text_sha256: 26032108b0579d1f44229926e46276ad004766bc42a7975296d8f3b4d16cdf98
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# composition.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-viewmodels-zafiro/composition.md`
- Extract: `text`
- SHA256: `a6f050d07e3fd084f110a133610a7168ed0cfc62d8a6fb4a51da844f22f9846a`

## Content

# Composition & Mapping

Ensuring your ViewModels are correctly instantiated and mapped to their corresponding Views is crucial for a maintainable application.

## ViewModel-to-View Mapping

Zafiro uses the `DataTypeViewLocator` to automatically map ViewModels to Views based on their data type.

### Integration in App.axaml

Register the `DataTypeViewLocator` in your application's data templates:

```xml
<Application.DataTemplates>
    <DataTypeViewLocator />
    <DataTemplateInclude Source="avares://Zafiro.Avalonia/DataTemplates.axaml" />
</Application.DataTemplates>
```

### Registration

Mappings can be registered globally or locally. Common practice in Zafiro projects is to use naming conventions or explicit registrations made by source generators.

## Composition Root

Use a central `CompositionRoot` to manage dependency injection and service registration.

```csharp
public static class CompositionRoot
{
    public static IShellViewModel CreateMainViewModel(Control topLevelView)
    {
        var services = new ServiceCollection();
        
        services
            .AddViewModels()
            .AddUIServices(topLevelView);
            
        var serviceProvider = services.BuildServiceProvider();
        return serviceProvider.GetRequiredService<IShellViewModel>();
    }
}
```

### Registering ViewModels

Register ViewModels with appropriate scopes (Transient, Scoped, or Singleton).

```csharp
public static IServiceCollection AddViewModels(this IServiceCollection services)
{
    return services
        .AddTransient<IHomeSectionViewModel, HomeSectionSectionViewModel>()
        .AddSingleton<IShellViewModel, ShellViewModel>();
}
```

## View Injection

Use the `Connect` helper (if available) or manual instantiation in `OnFrameworkInitializationCompleted`:

```csharp
public override void OnFrameworkInitializationCompleted()
{
    this.Connect(
        () => new ShellView(),
        view => CompositionRoot.CreateMainViewModel(view),
        () => new MainWindow());

    base.OnFrameworkInitializationCompleted();
}
```

> [!TIP]
> Use `ActivatorUtilities.CreateInstance` when you need to manually instantiate a class while still resolving its dependencies from the `IServiceProvider`.

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
