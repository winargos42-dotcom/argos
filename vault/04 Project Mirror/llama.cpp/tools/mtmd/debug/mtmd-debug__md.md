---
argos_import: project_file
source_path: llama.cpp/tools/mtmd/debug/mtmd-debug.md
source_abs: F:\debug\argoss\llama.cpp\tools\mtmd\debug\mtmd-debug.md
source_ext: .md
source_sha256: d47efe5d8bf36c9b34c78fb18a5f1624610aa4bbdf7f5c7b73d47b1dbdbfb342
text_sha256: cb952bffd8655e078116b2e945fc5a6d491bd2be7550512af5038fd397ff2491
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# mtmd-debug.md

- Source: `llama.cpp/tools/mtmd/debug/mtmd-debug.md`
- Extract: `text`
- SHA256: `d47efe5d8bf36c9b34c78fb18a5f1624610aa4bbdf7f5c7b73d47b1dbdbfb342`

## Content

# mtmd-debug

## Debugging encode pass

Example of debugging an input gray image (raw, not preprocessed):

```py
from transformers import AutoModel

model = AutoModel.from_pretrained(...)

def test_vision():
  img_size = 896 # number of patches per side
  pixel_values = torch.zeros(1, 3, img_size, img_size) + 0.5 # gray image
  with torch.no_grad():
    outputs = model.model.get_image_features(pixel_values=pixel_values)
  print("last_hidden_state shape:", outputs.last_hidden_state.shape)
  print("last_hidden_state:", outputs.last_hidden_state)

test_vision()
```

## Debugging preprocess pass

(TODO)

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
