---
argos_import: project_file
source_path: claude-code-templates/docu/docs/tools/sandbox.md
source_abs: F:\debug\argoss\claude-code-templates\docu\docs\tools\sandbox.md
source_ext: .md
source_sha256: 1ba4026e4ca6a6d968367c19b028f4811227304fb76c282847336423bbf6dec4
text_sha256: eda987aad19dbaef9b3002e206aa6a1d56a3163234b57dd0709aeee4874bef63
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:55
---

# sandbox.md

- Source: `claude-code-templates/docu/docs/tools/sandbox.md`
- Extract: `text`
- SHA256: `1ba4026e4ca6a6d968367c19b028f4811227304fb76c282847336423bbf6dec4`

## Content

---
sidebar_position: 6
---

# E2B Sandbox

Cloud execution environment for safe testing and experimentation.

## Setup Requirements

Add to your `.env` file:
```bash
ANTHROPIC_API_KEY=your_anthropic_key_here
E2B_API_KEY=your_e2b_key_here
```

Get keys at [console.anthropic.com](https://console.anthropic.com/) and [e2b.dev](https://e2b.dev/).

## Launch Commands

### Basic execution
```bash
npx claude-code-templates@latest --sandbox e2b --prompt "your task"
```

### With components
```bash
npx claude-code-templates@latest --sandbox e2b --agent frontend-developer --prompt "optimize React components"
```

## Features

- **Isolated environments** - Safe execution without affecting local system
- **Cloud resources** - Access to scalable computing power
- **Component integration** - Use agents, commands, and MCPs in sandbox
- **Secure execution** - Protected environment for experimental code
- **Resource scaling** - Handle intensive computational tasks
# With specific environment and timeout
```
npx claude-code-templates@latest --sandbox e2b --agent security/security-auditor --prompt "audit this codebase" --timeout 300
```

## 🔒 Isolation Features

### Complete Environment Isolation
- **Sandboxed execution** - No access to your local file system
- **Network isolation** - Controlled internet access
- **Process isolation** - Separate process space from your system
- **Resource limits** - Memory and CPU usage boundaries
- **Automatic cleanup** - Environment destroyed after execution

### Security Benefits
- **Safe code testing** - Run potentially harmful code safely
- **Malware protection** - Isolated from your main system
- **Data protection** - Local files remain untouched
- **Clean state** - Fresh environment for each execution
- **No persistent changes** - No permanent modifications to your system

---

**Complete your toolkit:** Return to [Additional Tools Overview](./overview) to explore tool combinations and advanced workflows.

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
