---
argos_import: project_file
source_path: comfyui/tests/README.md
source_abs: F:\debug\argoss\comfyui\tests\README.md
source_ext: .md
source_sha256: 15d8d68748b1afde819f82c9d177a33a8e61a2eaa02ca716abf0e3b94faf26e1
text_sha256: 393cf0a0257a9930b711c379ce41c95d4321d80ab7309eb84185483c0d581fee
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:59
---

# README.md

- Source: `comfyui/tests/README.md`
- Extract: `text`
- SHA256: `15d8d68748b1afde819f82c9d177a33a8e61a2eaa02ca716abf0e3b94faf26e1`

## Content

# Automated Testing

## Running tests locally

Additional requirements for running tests:
```
pip install pytest
pip install websocket-client==1.6.1
opencv-python==4.6.0.66
scikit-image==0.21.0
```
Run inference tests:
```
pytest tests/inference
```

## Quality regression test
Compares images in 2 directories to ensure they are the same

1) Run an inference test to save a directory of "ground truth" images
```
    pytest tests/inference --output_dir tests/inference/baseline
```
2) Make code edits

3) Run inference and quality comparison tests
```
pytest
```

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
