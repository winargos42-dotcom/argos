---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-zafiro-development/zafiro-shortcuts.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-zafiro-development\zafiro-shortcuts.md
source_ext: .md
source_sha256: e4c4f04d1cd2ba32a86d3502ec93b47f148633a435b3e9cd784528eef12b9bf6
text_sha256: d1b74b49339dfd4b6e55ecdc15fa29c63c461389804e4cf9a605c868d3cb7cb0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# zafiro-shortcuts.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-zafiro-development/zafiro-shortcuts.md`
- Extract: `text`
- SHA256: `e4c4f04d1cd2ba32a86d3502ec93b47f148633a435b3e9cd784528eef12b9bf6`

## Content

# Zafiro Reactive Shortcuts

Use these Zafiro extension methods to replace standard, more verbose Reactive and DynamicData patterns.

## General Observable Helpers

| Standard Pattern | Zafiro Shortcut |
| :--- | :--- |
| `Replay(1).RefCount()` | `ReplayLastActive()` |
| `Select(_ => Unit.Default)` | `ToSignal()` |
| `Select(b => !b)` | `Not()` |
| `Where(b => b).ToSignal()` | `Trues()` |
| `Where(b => !b).ToSignal()` | `Falses()` |
| `Select(x => x is null)` | `Null()` |
| `Select(x => x is not null)` | `NotNull()` |
| `Select(string.IsNullOrWhiteSpace)` | `NullOrWhitespace()` |
| `Select(s => !string.IsNullOrWhiteSpace(s))` | `NotNullOrEmpty()` |

## Result & Maybe Extensions

| Standard Pattern | Zafiro Shortcut |
| :--- | :--- |
| `Where(r => r.IsSuccess).Select(r => r.Value)` | `Successes()` |
| `Where(r => r.IsFailure).Select(r => r.Error)` | `Failures()` |
| `Where(m => m.HasValue).Select(m => m.Value)` | `Values()` |
| `Where(m => !m.HasValue).ToSignal()` | `Empties()` |

## Lifecycle Management

| Description | Method |
| :--- | :--- |
| Dispose previous item before emitting new one | `DisposePrevious()` |
| Manage lifecycle within a disposable | `DisposeWith(disposables)` |

## Command & Interaction

| Description | Method |
| :--- | :--- |
| Add metadata/text to a ReactiveCommand | `Enhance(text, name)` |
| Automatically show errors in UI | `HandleErrorsWith(notificationService)` |

> [!TIP]
> Always check `Zafiro.Reactive.ObservableMixin` and `Zafiro.CSharpFunctionalExtensions.ObservableExtensions` before writing custom Rx logic.

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
