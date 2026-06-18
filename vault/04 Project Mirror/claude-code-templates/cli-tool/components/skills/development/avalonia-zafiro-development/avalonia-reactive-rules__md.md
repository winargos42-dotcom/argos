---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-zafiro-development/avalonia-reactive-rules.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-zafiro-development\avalonia-reactive-rules.md
source_ext: .md
source_sha256: adea0530de6483cf78c9c899efc6bc9190632a9935c4006a1ce282f2cd0e5442
text_sha256: 64aff54a560219e11dc37c5275ee20b1b469134152015f3946fff0adf0fea196
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# avalonia-reactive-rules.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-zafiro-development/avalonia-reactive-rules.md`
- Extract: `text`
- SHA256: `adea0530de6483cf78c9c899efc6bc9190632a9935c4006a1ce282f2cd0e5442`

## Content

# Avalonia, Zafiro & Reactive Rules

## Avalonia UI Rules

- **Strict Avalonia**: Never use `System.Drawing`; always use Avalonia types.
- **Pure ViewModels**: ViewModels must **never** reference Avalonia types.
- **Bindings Over Code-Behind**: Logic should be driven by bindings.
- **DataTemplates**: Prefer explicit `DataTemplate`s and typed `DataContext`s.
- **VisualStates**: Avoid using `VisualStates` unless absolutely required.

## Zafiro Guidelines

- **Prefer Abstractions**: Always look for existing Zafiro helpers, extension methods, and abstractions before re-implementing logic.
- **Validation**: Use Zafiro's `ValidationRule` and validation extensions instead of ad-hoc reactive logic.

## DynamicData & Reactive Rules

### The Mandatory Approach

- **Operator Preference**: Always prefer **DynamicData** operators (`Connect`, `Filter`, `Transform`, `Sort`, `Bind`, `DisposeMany`) over plain Rx operators when working with collections.
- **Readable Pipelines**: Build and maintain pipelines as a single, readable chain.
- **Lifecycle**: Use `DisposeWith` for lifecycle management.
- **Minimal Subscriptions**: Subscriptions should be minimal, centralized, and strictly for side-effects.

### Forbidden Anti-Patterns

- **Ad-hoc Sources**: Do NOT create new `SourceList` / `SourceCache` on the fly for local problems.
- **Logic in Subscribe**: Do NOT place business logic inside `Subscribe`.
- **Operator Mismatch**: Do NOT use `System.Reactive` operators if a DynamicData equivalent exists.

### Canonical Patterns

**Validation of Dynamic Collections:**
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

**Filtering Nulls:**
Use `WhereNotNull()` in reactive pipelines.
```csharp
this.WhenAnyValue(x => x.DurationPreset).WhereNotNull()
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
