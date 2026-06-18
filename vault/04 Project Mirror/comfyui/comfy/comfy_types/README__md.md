---
argos_import: project_file
source_path: comfyui/comfy/comfy_types/README.md
source_abs: F:\debug\argoss\comfyui\comfy\comfy_types\README.md
source_ext: .md
source_sha256: 2524086a0776c87cff194e1a0f11ba3dcd80c68b6a0f0db4ea83c216793a4eac
text_sha256: 9f8c2a905c032baf5f4f1ad941e3a66265650ad2dbc730069e2a697c339210d1
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:58
---

# README.md

- Source: `comfyui/comfy/comfy_types/README.md`
- Extract: `text`
- SHA256: `2524086a0776c87cff194e1a0f11ba3dcd80c68b6a0f0db4ea83c216793a4eac`

## Content

# Comfy Typing
## Type hinting for ComfyUI Node development

This module provides type hinting and concrete convenience types for node developers.
If cloned to the custom_nodes directory of ComfyUI, types can be imported using:

```python
from comfy.comfy_types import IO, ComfyNodeABC, CheckLazyMixin

class ExampleNode(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(s) -> InputTypeDict:
        return {"required": {}}
```

Full example is in [examples/example_nodes.py](examples/example_nodes.py).

# Types
A few primary types are documented below.  More complete information is available via the docstrings on each type.

## `IO`

A string enum of built-in and a few custom data types.  Includes the following special types and their requisite plumbing:

- `ANY`: `"*"`
- `NUMBER`: `"FLOAT,INT"`
- `PRIMITIVE`: `"STRING,FLOAT,INT,BOOLEAN"`

## `ComfyNodeABC`

An abstract base class for nodes, offering type-hinting / autocomplete, and somewhat-alright docstrings.

### Type hinting for `INPUT_TYPES`

![INPUT_TYPES auto-completion in Visual Studio Code](examples/input_types.png)

### `INPUT_TYPES` return dict

![INPUT_TYPES return value type hinting in Visual Studio Code](examples/required_hint.png)

### Options for individual inputs

![INPUT_TYPES return value option auto-completion in Visual Studio Code](examples/input_options.png)

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
