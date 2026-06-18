# ARGOS Status 2026-05-08 00:52

## Fine-Tuning Pipeline

### Dataset
- **Status**: Uploaded to Kaggle
- **URL**: https://www.kaggle.com/datasets/poldop/argos-training-dataset-v1
- **Size**: 5,560 examples, 18.8 MB
- **Format**: OpenAI chat format (system/user/assistant)

### Kaggle Notebook
- **Status**: Ready to push (blocked by API 403)
- **File**: `kaggle_kernel/kaggle_finetune.ipynb`
- **Config**: T4 x2 GPU, Mistral NeMo 12B, QLoRA 4-bit
- **Blocker**: Need phone verification on kaggle.com

### GCP Vertex AI
- **A100**: Denied (can re-request after 2026-05-09 22:39)
- **L4/T4**: 429 RESOURCE_EXHAUSTED in all regions
- **Auto-checker**: Running every 6 hours
- **Time remaining**: ~1 day 21 hours

## Infrastructure

### Scheduled Tasks Created
1. **ARGOS-Vault-Backup** — daily at 02:00
2. **ARGOS-GCP-Quota-Check** — every 6 hours

### GPU Cluster
- 8082: RX 580 (qwen2.5:3b) — active
- 8083: Vega 11 (tinyllama) — active  
- 8084: RX 560 (phi4-mini) — active

### MCP/API
- Port 8000: Running (Python system)
- Port 8080: Dashboard active
- Health: All systems nominal

## Blocked (Needs Manual Action)

1. **Kaggle**: Go to kaggle.com → Account → Phone Verification
2. **GCP A100**: Re-request quota on 2026-05-09 after 22:39
3. **Gmail App Password**: myaccount.google.com/apppasswords
4. **Grok API**: Get new key from x.ai
5. **SERPAPI**: Replenish balance

## Next Actions (After Unblocking)

```powershell
# 1. Push Kaggle kernel
cd F:\debug\argoss
kaggle kernels push -p kaggle_kernel

# 2. Launch fine-tuning on Kaggle
# Open: https://www.kaggle.com/code/poldop/argos-finetune-v2
# Enable GPU T4x2 → Run All

# 3. Request GCP quotas (after 2026-05-09)
# Console → IAM → Quotas → filter "nvidia_a100_gpus"
```

## Files Updated
- `.env` — GCP credentials path fixed
- `data/train.jsonl` — Regenerated from vault
- `kaggle_dataset/` — Uploaded to Kaggle
- `scripts/vault_backup.ps1` — Auto-backup script
- `scripts/check_gcp_quota.py` — Quota monitor

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
