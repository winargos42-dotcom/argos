---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/game-development/unity-project-setup.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\game-development\unity-project-setup.md
source_ext: .md
source_sha256: 78eec5c5e1e2ccbc8a200c0b7922c0d09f4f7a40638489f44c2d6e69c515f7bc
text_sha256: 084bc1b365c0512368f1d22bcbf7e5170c173203738e76db4a4864d69d7bdc27
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# unity-project-setup.md

- Source: `claude-code-templates/cli-tool/components/commands/game-development/unity-project-setup.md`
- Extract: `text`
- SHA256: `78eec5c5e1e2ccbc8a200c0b7922c0d09f4f7a40638489f44c2d6e69c515f7bc`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [project-name] | --2d | --3d | --mobile | --vr | --console
description: Use PROACTIVELY to set up professional Unity game development projects with industry-standard structure, essential packages, and platform-optimized configurations
---

# Unity Project Setup & Development Environment

Initialize professional Unity game development project: $ARGUMENTS

## Current Unity Environment

- Unity version: !`unity-editor --version 2>/dev/null || echo "Unity Editor not found"`
- Current directory: !`pwd`
- Available templates: !`find . -name "*.unitypackage" 2>/dev/null | wc -l` Unity packages
- Git status: !`git status --porcelain 2>/dev/null | wc -l` uncommitted changes
- System info: !`system_profiler SPSoftwareDataType | grep "System Version" 2>/dev/null || uname -a`

## Task

Set up a complete Unity project with professional development environment and platform-specific optimizations.

## What it creates:

### Project Structure
```
Assets/
├── _Project/
│   ├── Scripts/
│   │   ├── Managers/
│   │   ├── Player/
│   │   ├── UI/
│   │   ├── Gameplay/
│   │   └── Utilities/
│   ├── Art/
│   │   ├── Textures/
│   │   ├── Materials/
│   │   ├── Models/
│   │   └── Animations/
│   ├── Audio/
│   │   ├── Music/
│   │   ├── SFX/
│   │   └── Voice/
│   ├── Prefabs/
│   │   ├── Characters/
│   │   ├── Environment/
│   │   ├── UI/
│   │   └── Effects/
│   ├── Scenes/
│   │   ├── Development/
│   │   ├── Production/
│   │   └── Testing/
│   ├── Settings/
│   │   ├── Input/
│   │   ├── Rendering/
│   │   └── Audio/
│   └── Resources/
├── Plugins/
├── StreamingAssets/
└── Editor/
    ├── Scripts/
    └── Resources/
```

### Essential Packages
- Universal Render Pipeline (URP)
- Input System
- Cinemachine
- ProBuilder
- Timeline
- Addressables
- Unity Analytics
- Version Control (if available)

### Project Settings
- Optimized quality settings for target platforms
- Input system configuration
- Physics settings
- Time and rendering configurations
- Build settings for multiple platforms

### Development Tools
- Code formatting rules (.editorconfig)
- Git configuration with Unity-optimized .gitignore
- Assembly definition files for better compilation
- Custom editor scripts for workflow improvement

### Version Control Setup
- Git repository initialization
- Unity-specific .gitignore
- LFS configuration for large assets
- Branching strategy documentation

## Usage:

```bash
npx claude-code-templates@latest --command unity-project-setup
```

## Interactive Options:

1. **Project Type Selection**
   - 2D Game
   - 3D Game
   - Mobile Game
   - VR/AR Game
   - Hybrid (2D/3D)

2. **Target Platforms**
   - PC (Windows/Mac/Linux)
   - Mobile (iOS/Android)
   - Console (PlayStation/Xbox/Nintendo)
   - WebGL
   - VR (Oculus/SteamVR)

3. **Version Control**
   - Git
   - Plastic SCM
   - Perforce
   - None

4. **Additional Packages**
   - TextMeshPro
   - Post Processing
   - Unity Ads
   - Unity Analytics
   - Unity Cloud Build
   - Custom package selection

## Generated Files:

### Core Scripts
- `GameManager.cs` - Main game controller
- `SceneLoader.cs` - Scene management system
- `AudioManager.cs` - Audio system controller
- `InputManager.cs` - Input handling system
- `UIManager.cs` - UI system manager
- `SaveSystem.cs` - Save/load functionality

### Editor Tools
- `ProjectSetupWindow.cs` - Custom editor window
- `SceneQuickStart.cs` - Scene setup automation
- `AssetValidator.cs` - Asset validation tools
- `BuildAutomation.cs` - Build pipeline helpers

### Configuration Files
- `ProjectSettings.asset` - Optimized project settings
- `QualitySettings.asset` - Multi-platform quality tiers
- `InputActions.inputactions` - Input system configuration
- `AssemblyDefinitions` - Modular compilation setup

### Documentation
- `README.md` - Project overview and setup instructions
- `CONTRIBUTING.md` - Development guidelines
- `CHANGELOG.md` - Version history template
- `API_REFERENCE.md` - Code documentation template

## Post-Setup Checklist:

- [ ] Review and adjust quality settings for target platforms
- [ ] Configure input actions for your game controls
- [ ] Set up build configurations for all target platforms
- [ ] Review folder structure and rename as needed
- [ ] Configure version control and make initial commit
- [ ] Set up continuous integration if required
- [ ] Configure analytics and crash reporting
- [ ] Review and customize coding standards

## Platform-Specific Configurations:

### Mobile
- Touch input configuration
- Performance optimization settings
- Battery usage optimization
- App store submission setup

### PC
- Multi-resolution support
- Keyboard/mouse input setup
- Graphics options menu template
- Windows/Mac/Linux build configs

### Console
- Platform-specific input mapping
- Achievement/trophy integration setup
- Online services configuration
- Certification requirement templates

This command creates a production-ready Unity project structure that scales from prototype to shipped game, following industry best practices and Unity's recommended patterns.

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
