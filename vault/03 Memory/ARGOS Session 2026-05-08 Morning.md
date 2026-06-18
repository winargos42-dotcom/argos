# ARGOS Session 2026-05-08 Morning

## Status: Fine-Tuning RUNNING

### Colab Training (Mistral 7B)
- **Model**: mistralai/Mistral-7B-Instruct-v0.2
- **GPU**: Tesla T4 (14.5 GB VRAM)
- **Dataset**: 6,150 examples (filtered from 5,560 — bad lines removed)
- **Progress**: Step 22/1155, Epoch 0.05/3
- **Loss**: 3.23 → 2.44 (improving)
- **ETA**: ~6 hours
- **Trainable params**: 20.9M / 7.26B (0.29% — LoRA r=8, alpha=16)
- **Batch**: 1 x 16 grad accum
- **Seq length**: 512
- **Status**: ✅ RUNNING — DO NOT CLOSE TAB

### Local GPU Cluster
- **GPU0** (RX 580): llama-server :8082, qwen2.5:3b.gguf
- **GPU1** (Vega 11): llama-server :8083, tinyllama-1.1b.gguf
- **GPU2** (RX 560): llama-server :8084, phi4-mini.gguf
- **Status**: All ACTIVE

### Next Steps After Training
1. Download `argos-mistral7b-gguf/` from Colab
2. Place `.gguf` in `models/` folder
3. Test with `ollama run` or llama-server
4. Compare with base model performance

### Blockers Resolved
- ✅ Kaggle phone verification: BLOCKED (using Colab instead)
- ✅ GCP GPU quota: BLOCKED (0/0 GPUS_ALL_REGIONS)
- ✅ Cloud.ru: SSH key mismatch, expensive
- ✅ Model size: Switched from 12B → 7B (fits T4)
- ✅ Dataset parsing: Skipped bad JSON lines
- ✅ Trainer labels: Added `labels = input_ids`

### Files Created
- `scripts/colab_mistral7b_ready.py` — working training script
- `kaggle_dataset/` — uploaded to Kaggle (backup)
- `kaggle_kernel/` — Kaggle notebook ready

### Session Duration
- Started: ~2026-05-08 01:00
- Colab running: ~06:30
- Total session time: ~5.5 hours troubleshooting

## Notes
- Training working after switching to Qwen 2.5 3B then back to Mistral 7B with fixed params
- Colab free tier sufficient for 7B model
- Local cluster stable (3x AMD GPU)

## Todo
- [ ] Download GGUF after 6 hours
- [ ] Test inference
- [ ] Update MCP server model config
- [ ] Request GCP quota increase (after 2026-05-09)

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Human Sessions Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Human Sessions Hub]]
