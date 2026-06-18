---
argos_import: project_file
source_path: A100_AGGRESSIVE_CONFIG.md
source_abs: F:\debug\argoss\A100_AGGRESSIVE_CONFIG.md
source_ext: .md
source_sha256: 357ad08e1e17523c07428a68e33041eb48f8eda4251256dd0750858cc317e686
text_sha256: 357ad08e1e17523c07428a68e33041eb48f8eda4251256dd0750858cc317e686
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-08 22:01:50
---

# A100_AGGRESSIVE_CONFIG.md

- Source: `A100_AGGRESSIVE_CONFIG.md`
- Extract: `text`
- SHA256: `357ad08e1e17523c07428a68e33041eb48f8eda4251256dd0750858cc317e686`

## Content

# ARGOS v2.2 Aggressive Config — Quick Reference

## Changes from v2.1.3
```python
per_device_train_batch_size = 4   # Was: 2
gradient_accumulation_steps = 4   # Was: 8
random_state = 3233339492         # Quantum seed (was: 3407)
```

## Expected Behavior
- **Steps:** ~606 (was 1212) — 2x fewer steps
- **Speed:** ~1.5-2x faster training
- **VRAM:** Should fit in A100 40GB with seq=2048

## ⚠️ Warnings

### 1. Loss Spikes
- **Cause:** More frequent weight updates (grad_accum=4)
- **Symptom:** Loss jumps >2x suddenly
- **Fix:** Revert to `gradient_accumulation_steps=8`
- **Monitoring:** Script includes automatic spike detection

### 2. VRAM Pressure
- **Safe:** batch=4 + seq=2048 → ~30-35GB
- **Risk:** batch=4 + seq=4096 → may OOM
- **Fix:** Reduce batch to 2 or sequence to 2048
- **Monitoring:** Script alerts if VRAM >38GB

### 3. If Training Crashes
```python
# Revert to safe config:
per_device_train_batch_size = 2
gradient_accumulation_steps = 8
# Keep: random_state=3233339492 (quantum seed)
```

## When to Use
- After v2.1.3 is deployed on V100
- When you have stable A100 access
- For faster iteration on dataset changes

## Rollback Plan
1. If loss spikes → grad_accum=8
2. If OOM → batch=2
3. If both fail → full fallback to v2.1.3 config

## Monitoring Dashboard
Watch for:
- Loss value (should decrease smoothly)
- VRAM usage (should stay <38GB)
- Iteration speed (should be ~0.12-0.15 it/s)

---
**File:** `scripts/colab_a100_aggressive_v22.py`

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
