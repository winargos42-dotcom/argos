---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/avalonia-zafiro-development/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\avalonia-zafiro-development\SKILL.md
source_ext: .md
source_sha256: c6bb95206522887284f0e44112441c5b45a8e294068f088956cbee1a36ce87c0
text_sha256: f2798ef3ef18c5cf124a7f9289c5f6d7c128129a4d23ef58bfbe038a0f05938b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/development/avalonia-zafiro-development/SKILL.md`
- Extract: `text`
- SHA256: `c6bb95206522887284f0e44112441c5b45a8e294068f088956cbee1a36ce87c0`

## Content

---
name: avalonia-zafiro-development
description: Mandatory skills, conventions, and behavioral rules for Avalonia UI development using the Zafiro toolkit.
---

# Avalonia Zafiro Development

This skill defines the mandatory conventions and behavioral rules for developing cross-platform applications with Avalonia UI and the Zafiro toolkit. These rules prioritize maintainability, correctness, and a functional-reactive approach.

## Core Pillars

1.  **Functional-Reactive MVVM**: Pure MVVM logic using DynamicData and ReactiveUI.
2.  **Safety & Predictability**: Explicit error handling with `Result` types and avoidance of exceptions for flow control.
3.  **Cross-Platform Excellence**: Strictly Avalonia-independent ViewModels and composition-over-inheritance.
4.  **Zafiro First**: Leverage existing Zafiro abstractions and helpers to avoid redundancy.

## Guides

- [Core Technical Skills & Architecture](core-technical-skills.md): Fundamental skills and architectural principles.
- [Naming & Coding Standards](naming-standards.md): Rules for naming, fields, and error handling.
- [Avalonia, Zafiro & Reactive Rules](avalonia-reactive-rules.md): Specific guidelines for UI, Zafiro integration, and DynamicData pipelines.
- [Zafiro Shortcuts](zafiro-shortcuts.md): Concise mappings for common Rx/Zafiro operations.
- [Common Patterns](patterns.md): Advanced patterns like `RefreshableCollection` and Validation.

## Procedure Before Writing Code

1.  **Search First**: Search the codebase for similar implementations or existing Zafiro helpers.
2.  **Reusable Extensions**: If a helper is missing, propose a new reusable extension method instead of inlining complex logic.
3.  **Reactive Pipelines**: Ensure DynamicData operators are used instead of plain Rx where applicable.

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
