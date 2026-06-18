# Сессия ARGOS 2026-05-08 18:00–23:00 (OpenCode / K2P6)

## Агент
- **Model**: K2P6 (kimi-for-coding/k2p6)
- **Platform**: OpenCode CLI
- **Working dir**: `C:\Users\AvA\.local\share\opencode\worktree\7169db9cd808b22bc8beae97cefd72ab4fc365fa\glowing-pixel`
- **Context source**: `CLAUDE.md` (профиль пользователя)

## Пользователь
- **Name**: Всеволод (Seva / AvA / SiG)
- **Profession**: Ассенизатор
- **Coding experience**: 2 месяца
- **Project**: ARGOS v2.1.3

---

## Phase 1: Status Check (18:00–18:10)

### User request
> "What did we do so far?"

### Actions taken
1. Read `CLAUDE.md` to load user context.
2. Browsed `F:\debug\argoss` directory structure.
3. Checked git repo status (`git status`, `git log`).
4. Verified `data/train.jsonl` existence and size (5,560 lines).
5. Attempted to check `telegram_only.jsonl` — file not found.

### Key finding
Telegram export was **NOT merged** into `train.jsonl` despite previous session claiming it was.

---

## Phase 2: Telegram Dataset Merge (18:10–18:25)

### Problem
`data/telegram_only.jsonl` missing. Converter script `scripts/convert_telegram_to_train.py` had Unicode emoji (`→`) causing `UnicodeEncodeError` on Windows cp1251.

### Actions
1. Read converter script.
2. Fixed Unicode arrow → ASCII `-`>` and emoji → `[OK]` markers.
3. Re-ran converter.

### Results
- **Total messages in export**: 5,231
- **Valid text messages**: 4,218
- **Generated training examples**: 942
- **Existing examples**: 5,560
- **Merged dataset**: 6,502 examples (22.18 MB)
- **Output**: `data/train.jsonl`, `data/telegram_only.jsonl`

### Data quality issue
- Max user message length: 88,632 chars (code dump)
- 97 examples with user > 2048 chars
- Gibberish tokens detected (`OGMwNGJiODYt...`)

---

## Phase 3: Dataset Filtering (18:25–18:40)

### Actions
1. Created `scripts/filter_dataset.py` (soft filter).
2. Ran filter: MAX_USER_LEN=15000, MAX_ASSIST_LEN=12000, MIN_ASSIST_LEN=15.

### Results
- **Clean dataset**: 6,461 / 6,502 examples
- **Removed**: 41 (21 long user, 10 gibberish, 9 short assist, 1 long total)
- **Output**: `data/train_clean.jsonl` (20.92 MB)

### Validation
```
All checks passed! 5/5 examples valid format.
```

---

## Phase 4: A100 Preparation (18:40–19:00)

### Actions
1. Zipped dataset: `data/train_for_colab.zip` (6.2 MB).
2. Updated `scripts/colab_a100_nemo12b.py`:
   - Removed Unicode emojis (Windows compatibility)
   - Added Google Drive backup
   - Added Drive mount check
3. Created `A100_SWITCH_CHECKLIST.md`.

### A100 Script parameters
- Model: Mistral NeMo 12B Instruct
- Seq length: 2048
- LoRA: r=16, alpha=32
- Batch: 2 x 8 grad accum = 16
- Precision: bf16
- ETA: 4-5 hours

---

## Phase 5: Colab Training (19:00–22:30) — USER SIDE

### User progress log (provided in chat)

**T4 Phase (earlier session)**
- Step 6/1155, Epoch 0.01/3, Loss dropping
- ETA: ~6 hours

**A100 Phase (this session)**
- **19:00**: A100 runtime selected, dataset uploaded
- **19:05**: Model loading started (24GB download)
- **19:10**: Training started
  - Step 6/1212, Epoch 0.03/3
  - Loss: 27.94
- **20:00**: Step 386/1212, Epoch 0.95/3, Loss ~13.0
- **21:00**: Step 651/1212, Epoch 1.61/3
- **22:00**: Step 1141/1212, Epoch 2.82/3
- **22:30**: Training COMPLETE (all 3 epochs)

---

## Phase 6: Post-Training Pipeline (22:30–23:00)

### Crisis: Disk full + time limits
Colab session about to expire. User cannot download 24GB GGUF due to bad internet.

### Emergency actions
1. Created `v100_post_training.py` — one-cell pipeline.
2. Attempted Google Drive backup to second account — **hung**.
3. Attempted HF Hub upload with token from `.env`.
4. Created `COLAB_4_CELLS.py` for manual execution.

### HF Upload results
- **Repo**: `AvaSiG/argos-mistral-nemo-12b-v100`
- **LoRA**: 245MB uploaded ✅
- **GGUF**: 24.5GB uploaded ✅ (Q4_K_M, 5 files)
- **URL**: https://huggingface.co/AvaSiG/argos-mistral-nemo-12b-v100

### Inference test (last minute)
```
User: Привет!
Assistant: Привет! Я готов помочь. Что тебя интересует? 👁️ *ARGOS*
```
✅ Russian language ✅ ARGOS awareness ✅ Markdown formatting

---

## Files Created (15+)

| File | Size | Purpose |
|------|------|---------|
| `scripts/convert_telegram_to_train.py` | 159 lines | Fixed Unicode, merged dataset |
| `scripts/filter_dataset.py` | 50 lines | Clean dataset filter |
| `scripts/colab_a100_nemo12b.py` | 138 lines | A100 training (no emojis) |
| `scripts/colab_a100_aggressive_v22.py` | 150 lines | Aggressive config (batch=4) |
| `scripts/merge_lora.py` | 60 lines | Merge for V100 |
| `scripts/v100_inference.py` | 80 lines | V100 inference script |
| `scripts/v100_post_training.py` | 200 lines | Post-training pipeline |
| `scripts/quantum_seed.py` | 50 lines | Genesis seed extractor |
| `scripts/deploy_v100.py` | 120 lines | V100 deployment |
| `scripts/argos_client.py` | 40 lines | API client |
| `A100_COLAB_NOTEBOOK.ipynb` | — | Notebook for A100 |
| `COLAB_A100_V100_READY.ipynb` | — | Full pipeline notebook |
| `A100_SWITCH_CHECKLIST.md` | — | Switch checklist |
| `V100_DEPLOYMENT_GUIDE.md` | — | Deployment guide |
| `docker-compose.v100.yml` | — | Docker config |
| `start_v100.sh` / `.ps1` | — | Startup scripts |

---

## Quantum Genesis Archive

- **Source**: IBM Quantum `ibm_fez`, 2026-03-04
- **Jobs**: 3 (archived to `archive/genesis/`)
- **Seed extracted**: `3233339492` (reserved for ARGOS v2.2)

---

## Mistakes Made

1. **Did NOT log to Obsidian in real-time** — violated vault rules (`02 Logs/` and `03 Memory/`).
2. Assumed `train.jsonl` had Telegram data — had to verify and merge manually.
3. Unicode emojis in scripts broke on Windows cp1251.
4. Multiple failed attempts at Google Drive backup before switching to HF Hub.

---

## Next Steps (for user)

1. ⏳ Get V100 server
2. ⏳ Download from HF: `huggingface-cli download AvaSiG/argos-mistral-nemo-12b-v100`
3. ⏳ Run: `python scripts/deploy_v100.py`
4. ⏳ Test inference

---

*Logged retroactively: 2026-05-08 23:15*
*Should have been logged in real-time to `02 Logs/`*

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Logs Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Logs Hub]]
