# ARGOS Russian LLM Training Dataset

**Location:** `/home/ava/Projects/argoss/data/datasets/`  
**Target Model:** `Qwen/Qwen2.5-7B-Instruct` (Tesla V100-SXM2-16GB)  
**Tokenizer:** Qwen2.5 (`<|im_start|>`, `<|im_end|>`)  
**Last Updated:** 2026-06-08

## Sources

The merged dataset combines the following HuggingFace datasets (with fallbacks to public versions where private access is unavailable):

| Dataset | Fallback | Split | Weight | Description |
|---------|----------|-------|--------|-------------|
| `AvaSiG/ru-big-russian-dataset-bucket` | `ZeroAgency/ru-big-russian-dataset` | `train` | 1.0 | General Russian text, instructions, completions |
| `AvaSiG/ru-thinking-reasoning-r1-deduped-bucket` | `ZeroAgency/ru-thinking-reasoning-r1-deduped` | `train` | 1.0 | Reasoning / chain-of-thought Russian data |
| `AvaSiG/ru-instruct-conversation-v3.1-small-bucket` | `ZeroAgency/ru-instruct-conversation-v3.1-small` | `train` | 1.0 | Instruction-following conversations |
| `AvaSiG/ru-tasks-conversation-deduped-bucket` | `ZeroAgency/ru-tasks-conversation-deduped` | `train` | 1.0 | Task-oriented Russian dialogues |

> **Note:** The `AvaSiG/*-bucket` datasets are private or require a valid HF token. The pipeline automatically falls back to the equivalent `ZeroAgency` public datasets. The provided HF token (`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`) currently returns **401 Unauthorized** — the token may be expired or revoked. Update `HF_TOKEN` in the environment before running the full pipeline.

## Processing Pipeline

**Script:** `scripts/data_pipeline_hf.py`

### Steps

1. **Download** — Datasets are loaded from HuggingFace Hub via `datasets.load_dataset()` with automatic fallback logic. Streaming mode is available for large datasets.
2. **Normalize** — All records are normalized to a unified chat format `{"messages": [{"role": "...", "content": "..."}]}`.
3. **Exact Deduplication** — MD5 hash dedup on the serialized `messages` array.
4. **Near-Deduplication** — MinHash LSH with 128 permutations, 16 bands, 5-gram shingles, Jaccard threshold ≥ 0.85.
5. **Quality Filtering** —
   - Minimum text length: 30 chars
   - Must contain at least one `assistant` message
   - Cyrillic ratio ≥ 30% (to ensure Russian language dominance)
   - Token count bounds: 20 ≤ tokens ≤ 2048 (via Qwen2.5 tokenizer)
6. **Tokenization Check** — Verified against `Qwen/Qwen2.5-7B-Instruct` tokenizer.
7. **Format for Training** — Converted to Qwen2.5 chat template:
   ```
   <|im_start|>user
   ...<|im_end|>
   <|im_start|>assistant
   ...<|im_end|>
   ```
8. **Vertex AI Augmentation** *(optional)* — If `GOOGLE_APPLICATION_CREDENTIALS` is set (see `~/.config/gcloud/`), the pipeline can be extended to augment data via Vertex AI. Currently a placeholder — requires manual setup of augmentation rules.

## Output Files

| File | Description |
|------|-------------|
| `merged_ru_dataset.jsonl` | Final merged, deduped, filtered dataset ready for training |
| `processing_report.json` | Per-dataset statistics, durations, token counts |
| `statistics.json` | Alias to `processing_report.json` |
| `cache/` | HuggingFace `datasets` cache directory |

## Usage

### Quick test (100 rows, 1 dataset)
```bash
cd /home/ava/Projects/argoss
.venv/bin/python scripts/data_pipeline_hf.py --test --max-rows=100
```

### Full pipeline
```bash
cd /home/ava/Projects/argoss
export HF_TOKEN="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"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/application_default_credentials.json"
.venv/bin/python scripts/data_pipeline_hf.py
```

## Training

The processed `merged_ru_dataset.jsonl` is consumed by:
- `scripts/train_v100.py` — QLoRA fine-tuning on Tesla V100 (Windows / PC Orion)
- `scripts/train_argos_dal.py` — Unsloth-based training (requires `unsloth` package)

## Environment

- **Host:** X230 (Linux)
- **Venv:** `/home/ava/Projects/argoss/.venv` (Python 3.14.5)
- **GPU Training:** PC Orion (Windows, Tesla V100-SXM2-16GB)
- **Key Packages:** `datasets`, `transformers`, `huggingface-hub`, `sentencepiece`, `protobuf`, `pyarrow`, `google-cloud-aiplatform`, `gcloud-aio-storage`

## Known Issues

1. **HF Token Invalid** — The provided token is returning 401 Unauthorized. Either regenerate the token on [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) or use the public fallbacks.
2. **Unsloth Not Installed** — `unsloth` compilation failed on Python 3.14 (no pre-built wheel). It is only needed for `train_argos_dal.py` (training), not for data processing.
3. **Large Datasets** — Full download of all 4 datasets may take 30+ minutes and require ~2-5 GB disk space depending on split sizes.
