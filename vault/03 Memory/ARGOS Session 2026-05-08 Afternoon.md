# ARGOS Session 2026-05-08 Afternoon

## Status: A100 Training IN PROGRESS

### What happened:
1. **T4 training completed** - Mistral 7B finished, backed up to Drive
2. **Switched to A100** - Runtime changed to A100-SXM4-40GB
3. **A100 training started** - Mistral NeMo 12B Instruct
4. **Dataset merged** - Vault (5560) + Telegram (942) = 6502 examples
5. **Dataset cleaned** - Removed 41 bad examples, 6461 remain

### Current Progress:
- Model: Mistral NeMo 12B Instruct
- GPU: NVIDIA A100-SXM4-40GB (40GB VRAM)
- Dataset: 6461 examples, 20.92 MB
- Seq length: 2048
- LoRA: r=16, alpha=32
- Batch: 2 x 8 grad accum = 16
- ETA: ~4-5 hours

### V100 Preparation:
- Creating V100 deployment scripts
- GGUF + Merged model for V100 inference
- Docker compose ready
- API client ready
- V100 uses FP16 (not BF16)

### Files Created:
- `A100_COLAB_NOTEBOOK.ipynb` - Main training notebook
- `scripts/v100_inference.py` - V100 inference script
- `scripts/merge_lora.py` - Merge LoRA + base model
- `scripts/argos_client.py` - API client
- `docker-compose.v100.yml` - Docker deployment
- `V100_DEPLOYMENT_GUIDE.md` - Full deployment guide
- `data/train_clean.jsonl` - Cleaned dataset (6461 examples)
- `data/train_for_colab.zip` - Zipped dataset for upload

### Next Steps:
1. Wait for A100 training to complete
2. Export GGUF + merged model
3. Test inference in Colab
4. Save everything to Google Drive
5. Deploy on V100 server

### Blockers:
- None currently

### Notes:
- V100 will be used for production inference
- A100 only for training
- GGUF Q4_K_M recommended for V100 (6-8GB VRAM)
- Merged model + 4-bit also works on V100

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
