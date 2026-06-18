---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/flutter-app/TEMPLATE.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\business-marketing\app-builder\templates\flutter-app\TEMPLATE.md
source_ext: .md
source_sha256: 0f0d55ee8629c03395355a11da0e6a28dbaf2adb0e676181fb8f5f0a9354013c
text_sha256: 2b518b263daa7bc0090e5ccc387b1c55977367527e69e672332be4cd98049c1e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# TEMPLATE.md

- Source: `claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/flutter-app/TEMPLATE.md`
- Extract: `text`
- SHA256: `0f0d55ee8629c03395355a11da0e6a28dbaf2adb0e676181fb8f5f0a9354013c`

## Content

---
name: flutter-app
description: Flutter mobile app template principles. Riverpod, Go Router, clean architecture.
---

# Flutter App Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Flutter 3.x |
| Language | Dart 3.x |
| State | Riverpod 2.0 |
| Navigation | Go Router |
| HTTP | Dio |
| Storage | Hive |

---

## Directory Structure

```
project_name/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/
│   │   ├── constants/
│   │   ├── theme/
│   │   ├── router/
│   │   └── utils/
│   ├── features/
│   │   ├── auth/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   └── home/
│   ├── shared/
│   │   ├── widgets/
│   │   └── providers/
│   └── services/
│       ├── api/
│       └── storage/
├── test/
└── pubspec.yaml
```

---

## Architecture Layers

| Layer | Contents |
|-------|----------|
| Presentation | Screens, Widgets, Providers |
| Domain | Entities, Use Cases |
| Data | Repositories, Models |

---

## Key Packages

| Package | Purpose |
|---------|---------|
| flutter_riverpod | State management |
| riverpod_annotation | Code generation |
| go_router | Navigation |
| dio | HTTP client |
| freezed | Immutable models |
| hive | Local storage |

---

## Setup Steps

1. `flutter create {{name}} --org com.{{bundle}}`
2. Update `pubspec.yaml`
3. `flutter pub get`
4. Run code generation: `dart run build_runner build`
5. `flutter run`

---

## Best Practices

- Feature-first folder structure
- Riverpod for state, React Query pattern for server state
- Freezed for immutable data classes
- Go Router for declarative navigation
- Material 3 theming

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
