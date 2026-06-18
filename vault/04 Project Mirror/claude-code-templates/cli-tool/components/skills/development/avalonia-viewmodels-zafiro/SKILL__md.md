---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-viewmodels-zafiro/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-viewmodels-zafiro\SKILL.md
source_ext: .md
source_sha256: eb56075c6adba282843b2864026ddf30f5fe9c940110a17868cba9076d2bedb6
text_sha256: 2042d1c3124abd66c1b13dd423b4fa54a5b79196af9b2630f77251e556ab57db
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-viewmodels-zafiro/SKILL.md`
- Extract: `text`
- SHA256: `eb56075c6adba282843b2864026ddf30f5fe9c940110a17868cba9076d2bedb6`

## Content

---
name: avalonia-viewmodels-zafiro
description: Optimal ViewModel and Wizard creation patterns for Avalonia using Zafiro and ReactiveUI.
---

# Avalonia ViewModels with Zafiro

This skill provides a set of best practices and patterns for creating ViewModels, Wizards, and managing navigation in Avalonia applications, leveraging the power of **ReactiveUI** and the **Zafiro** toolkit.

## Core Principles

1.  **Functional-Reactive Approach**: Use ReactiveUI (`ReactiveObject`, `WhenAnyValue`, etc.) to handle state and logic.
2.  **Enhanced Commands**: Utilize `IEnhancedCommand` for better command management, including progress reporting and name/text attributes.
3.  **Wizard Pattern**: Implement complex flows using `SlimWizard` and `WizardBuilder` for a declarative and maintainable approach.
4.  **Automatic Section Discovery**: Use the `[Section]` attribute to register and discover UI sections automatically.
5.  **Clean Composition**: map ViewModels to Views using `DataTypeViewLocator` and manage dependencies in the `CompositionRoot`.

## Guides

- [ViewModels & Commands](viewmodels.md): Creating robust ViewModels and handling commands.
- [Wizards & Flows](wizards.md): Building multi-step wizards with `SlimWizard`.
- [Navigation & Sections](navigation_sections.md): Managing navigation and section-based UIs.
- [Composition & Mapping](composition.md): Best practices for View-ViewModel wiring and DI.

## Example Reference

For real-world implementations, refer to the **Angor** project:
- `CreateProjectFlowV2.cs`: Excellent example of complex Wizard building.
- `HomeViewModel.cs`: Simple section ViewModel using functional-reactive commands.

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
