---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/react-native-app/TEMPLATE.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\business-marketing\app-builder\templates\react-native-app\TEMPLATE.md
source_ext: .md
source_sha256: f8edc00cad28ca53ac1587fad5bae770d50c545149ff39e5b901d0f2424f850d
text_sha256: 1de9b35c7155becd8390605896b1f2fc16550ab82d1778bfdeafbec47cc48dcc
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:34
---

# TEMPLATE.md

- Source: `claude-code-templates/cli-tool/components/skills/business-marketing/app-builder/templates/react-native-app/TEMPLATE.md`
- Extract: `text`
- SHA256: `f8edc00cad28ca53ac1587fad5bae770d50c545149ff39e5b901d0f2424f850d`

## Content

---
name: react-native-app
description: React Native mobile app template principles. Expo, TypeScript, navigation.
---

# React Native App Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | React Native + Expo |
| Language | TypeScript |
| Navigation | Expo Router |
| State | Zustand + React Query |
| Styling | NativeWind |
| Testing | Jest + RNTL |

---

## Directory Structure

```
project-name/
├── app/                 # Expo Router (file-based)
│   ├── _layout.tsx      # Root layout
│   ├── index.tsx        # Home
│   ├── (tabs)/          # Tab navigation
│   └── [id].tsx         # Dynamic route
├── components/
│   ├── ui/              # Reusable
│   └── features/
├── hooks/
├── lib/
│   ├── api.ts
│   └── storage.ts
├── store/
├── constants/
└── app.json
```

---

## Navigation Patterns

| Pattern | Use |
|---------|-----|
| Stack | Page hierarchy |
| Tabs | Bottom navigation |
| Drawer | Side menu |
| Modal | Overlay screens |

---

## State Management

| Type | Tool |
|------|------|
| Local | Zustand |
| Server | React Query |
| Forms | React Hook Form |
| Storage | Expo SecureStore |

---

## Key Packages

| Package | Purpose |
|---------|---------|
| expo-router | File-based routing |
| zustand | Local state |
| @tanstack/react-query | Server state |
| nativewind | Tailwind styling |
| expo-secure-store | Secure storage |

---

## Setup Steps

1. `npx create-expo-app {{name}} -t expo-template-blank-typescript`
2. `npx expo install expo-router react-native-safe-area-context`
3. Install state: `npm install zustand @tanstack/react-query`
4. `npx expo start`

---

## Best Practices

- Expo Router for navigation
- Zustand for local, React Query for server state
- NativeWind for consistent styling
- Expo SecureStore for tokens
- Test on both iOS and Android

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
