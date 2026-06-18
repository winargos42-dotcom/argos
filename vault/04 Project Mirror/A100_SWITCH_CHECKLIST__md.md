---
argos_import: project_file
source_path: A100_SWITCH_CHECKLIST.md
source_abs: F:\debug\argoss\A100_SWITCH_CHECKLIST.md
source_ext: .md
source_sha256: 43521cf9542d885532481bd7a9ad9cbf0739f53e8c45b625799467c0063caa83
text_sha256: 43521cf9542d885532481bd7a9ad9cbf0739f53e8c45b625799467c0063caa83
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-08 16:33:13
---

# A100_SWITCH_CHECKLIST.md

- Source: `A100_SWITCH_CHECKLIST.md`
- Extract: `text`
- SHA256: `43521cf9542d885532481bd7a9ad9cbf0739f53e8c45b625799467c0063caa83`

## Content

# ARGOS A100 Switch Checklist

## When T4 training finishes (or if it crashes)

### 1. Download T4 results (if finished)
- In Colab: download `argos-mistral7b-gguf/` folder
- Or copy to Drive if backed up

### 2. Switch Colab runtime to A100
- Runtime -> Change runtime type -> GPU -> A100
- Re-connect (takes ~1 min)

### 3. Upload new dataset
```python
from google.colab import files
files.upload()  # Select train_for_colab.zip
!unzip -q train_for_colab.zip
!mv train_clean.jsonl train.jsonl
```

Or mount Drive:
```python
from google.colab import drive
drive.mount('/content/drive')
!cp /content/drive/MyDrive/ARGOS/train_clean.jsonl /content/train.jsonl
```

### 4. Install dependencies
```bash
!pip install unsloth transformers datasets torch --quiet
```

### 5. Run A100 training
Upload `scripts/colab_a100_nemo12b.py` and run:
```bash
!python colab_a100_nemo12b.py
```

### 6. Parameters
- Model: Mistral NeMo 12B Instruct
- Seq length: 2048
- LoRA: r=16, alpha=32
- Batch: 2 x 8 grad accum = 16
- Precision: bf16
- ETA: 4-5 hours

### 7. After training
- Download `argos-nemo12b-gguf/` (~8-10 GB)
- Or find in Google Drive under `/ARGOS/`

### 8. Local test
```bash
# Place GGUF in models/
# Update docker-compose or llama-server command
```

---

## Dataset info
- Source: `data/train_clean.jsonl`
- Size: 6461 examples, 20.92 MB
- Vault: ~5560 examples
- Telegram: ~901 examples (after filtering)
- Filtered: 41 removed (21 too long, 10 gibberish, 9 short, 1 total too long)

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
