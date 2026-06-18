---
argos_import: project_file
source_path: comfyui/blueprints/.glsl/README.md
source_abs: F:\debug\argoss\comfyui\blueprints\.glsl\README.md
source_ext: .md
source_sha256: b118d8e82ea0f6215debaaa0a5ea3d8395e2922cbc5778f9eef181bd04142cff
text_sha256: 31e90a92b518c44cb3e9822f32b6d095e854667cd4170bb29479d28ccfc02b62
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:58
---

# README.md

- Source: `comfyui/blueprints/.glsl/README.md`
- Extract: `text`
- SHA256: `b118d8e82ea0f6215debaaa0a5ea3d8395e2922cbc5778f9eef181bd04142cff`

## Content

# GLSL Shader Sources

This folder contains the GLSL fragment shaders extracted from blueprint JSON files for easier editing and version control.

## File Naming Convention

`{Blueprint_Name}_{node_id}.frag`

- **Blueprint_Name**: The JSON filename with spaces/special chars replaced by underscores
- **node_id**: The GLSLShader node ID within the subgraph

## Usage

```bash
# Extract shaders from blueprint JSONs to this folder
python update_blueprints.py extract

# Patch edited shaders back into blueprint JSONs
python update_blueprints.py patch
```

## Workflow

1. Run `extract` to pull current shaders from JSONs
2. Edit `.frag` files
3. Run `patch` to update the blueprint JSONs
4. Test
5. Commit both `.frag` files and updated JSONs

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
