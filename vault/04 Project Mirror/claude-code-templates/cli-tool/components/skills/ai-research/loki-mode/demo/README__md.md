---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/demo/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\loki-mode\demo\README.md
source_ext: .md
source_sha256: ad820c5277fcc8f6b4a5ca443e754582baf1878736ce879b613cd8aafd5522b5
text_sha256: 94691b8ee0afd9e847689f410bb7989823ab95b58397b217d5c47ef07511a7ce
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:32
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/demo/README.md`
- Extract: `text`
- SHA256: `ad820c5277fcc8f6b4a5ca443e754582baf1878736ce879b613cd8aafd5522b5`

## Content

# Loki Mode Demo

Video demonstration of Loki Mode - Multi-agent autonomous startup system.

## Quick Start

```bash
# Full end-to-end demo with screen recording (RECOMMENDED)
./demo/record-full-demo.sh simple-todo

# Or run the simulated terminal demo
./demo/run-demo-auto.sh
```

## Full End-to-End Demo

The `record-full-demo.sh` script creates a real demo showing:
- Loki Mode running autonomously
- Dashboard with agents and tasks
- App being built in real-time
- Quality gates and code review

### Setup for Best Results

Arrange your screen like this before running:

```
+------------------+------------------+
|                  |                  |
|   TERMINAL       |   BROWSER        |
|   (run script)   |   (dashboard)    |
|                  |                  |
+------------------+------------------+
```

### Run the Demo

```bash
# Simple todo app (5-10 min)
./demo/record-full-demo.sh simple-todo

# Static landing page (3-5 min)
./demo/record-full-demo.sh static-landing

# Full-stack app (15-30 min)
./demo/record-full-demo.sh full-stack
```

The dashboard opens at: http://127.0.0.1:57374/dashboard/index.html

## Demo Contents

| File | Purpose |
|------|---------|
| `run-demo.sh` | Interactive demo script |
| `record-demo.sh` | Records demo with asciinema |
| `voice-over-script.md` | Narration script for video |
| `vhs-tape.tape` | VHS script for GIF/video generation |

## Recording Options

### Option 1: Asciinema (Terminal Recording)

```bash
# Record
./demo/record-demo.sh

# Play back
asciinema play demo/recordings/loki-demo.cast

# Upload to asciinema.org
asciinema upload demo/recordings/loki-demo.cast
```

### Option 2: VHS (GIF/Video Generation)

```bash
# Install VHS
brew install charmbracelet/tap/vhs

# Generate GIF
vhs demo/vhs-tape.tape

# Output: demo/loki-demo.gif
```

### Option 3: Screen Recording

1. Open terminal and run `./demo/run-demo.sh`
2. Use QuickTime or OBS to screen record
3. Add voice-over using `voice-over-script.md`

## Voice-Over Recording

See `voice-over-script.md` for the complete narration script with timestamps.

### Tips for Voice Recording

1. Read through the script first
2. Match your narration to the terminal actions
3. Keep energy up but professional
4. Pause at key moments for emphasis

## Demo Scenarios

### Simple Todo App (5 min)
Best for quick demos. Shows core Loki Mode workflow.

```bash
./demo/run-demo.sh simple-todo
```

### Full-Stack Demo (15-20 min)
Complete demonstration including:
- Kanban board visualization
- Parallel agent execution
- Code review process
- Quality gates

```bash
./demo/run-demo.sh full-stack
```

## Published Demos

| Demo | Duration | Link |
|------|----------|------|
| Quick Start | 5 min | [asciinema](https://asciinema.org/a/loki-quick-start) |
| Full Demo | 15 min | [YouTube](https://youtube.com/watch?v=loki-demo) |

## Creating Final Video

1. Record terminal with asciinema or screen recording
2. Record voice-over separately (cleaner audio)
3. Combine in video editor (iMovie, DaVinci Resolve)
4. Add intro/outro cards
5. Export as MP4

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
