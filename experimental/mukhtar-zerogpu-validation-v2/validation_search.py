"""ARGOS-MUKHTAR: deterministic stratified validation and ZeroGPU short search.

The hyperparameter search NEVER accesses X_test / Y_test. After the winning
candidate is frozen it evaluates the historic 128-state holdout ONCE, and does
not use that number to change the winner.

This is a *fine-tuning* validation, not a fresh independent evaluation of the
pretrained BioLocator: the initial distilled model already saw training data.
The 128-state holdout was also used in the October 9 pilot.
"""
from __future__ import annotations

import hashlib
import json
import math
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

SPLIT_SEED = 20261010
CHECKPOINT_SCHEMA = "argos-mukhtar-zerogpu-validation-v2"
SEEDS = (7, 21, 42)
LEARNING_RATES = (0.0001, 0.0003)
EVAL_EVERY = 10
STEPS_PER_CANDIDATE = 80
PATIENCE_EVALS = 3
MIN_DELTA = 1e-6


@dataclass(frozen=True)
class Split:
    train_indices: np.ndarray
    val_indices: np.ndarray
    val_indices_sha256: str
    groups: dict[str, dict[str, int]]
    split_seed: int


def stratified_split(labels: np.ndarray, seed: int = SPLIT_SEED,
                     fraction: float = 0.2) -> Split:
    """Reproducible disjoint indices with scenario-balanced validation."""
    values = np.asarray(labels)
    if values.ndim != 1 or len(values) < 12:
        raise ValueError("Expected at least 12 one-dimensional scenario labels")
    if not 0.05 <= fraction <= 0.4:
        raise ValueError("Validation fraction out of bounds")
    rng = np.random.default_rng(seed)
    train, val = [], []
    groups = {}
    for label in sorted(str(x) for x in np.unique(values)):
        members = np.where(values == label)[0]
        if len(members) < 5:
            raise ValueError(f"Scenario group {label!r} too small")
        perm = rng.permutation(members)
        count = max(1, min(len(members) - 1, int(round(len(members) * fraction))))
        val.extend(int(i) for i in perm[:count])
        train.extend(int(i) for i in perm[count:])
        groups[label] = {"train": int(len(members) - count), "val": int(count)}
    train_idx = np.asarray(sorted(train), dtype=np.int64)
    val_idx = np.asarray(sorted(val), dtype=np.int64)
    assert len(train_idx) + len(val_idx) == len(values)
    assert not np.intersect1d(train_idx, val_idx).size
    assert np.array_equal(np.sort(np.r_[train_idx, val_idx]), np.arange(len(values)))
    return Split(train_idx, val_idx,
                 hashlib.sha256(val_idx.astype("<i8").tobytes()).hexdigest(),
                 groups, int(seed))


def validate_grid(seeds: tuple[int, ...], rates: tuple[float, ...],
                  steps: int, max_seconds: float) -> None:
    if not seeds or not rates or len(seeds) * len(rates) > 6:
        raise ValueError("Only 1–6 candidates permitted per invocation")
    if len(set(seeds)) != len(seeds) or any(type(s) is not int or s not in SEEDS for s in seeds):
        raise ValueError("Only whitelisted, unique seeds permitted")
    if len(set(rates)) != len(rates) or any(float(v) not in LEARNING_RATES for v in rates):
        raise ValueError("Only whitelisted, unique learning rates permitted")
    if type(steps) is not int or steps not in (20, 40, 60, 80):
        raise ValueError("Step budget out of bounds")
    if not 5 <= max_seconds <= 35:
        raise ValueError("GPU time budget out of bounds")


def search_model(
    model_factory, initial_state: dict, x_train: np.ndarray, y_train: np.ndarray,
    scenario_train: np.ndarray, x_test: np.ndarray, y_test: np.ndarray,
    *, seeds: tuple[int, ...] = SEEDS,
    learning_rates: tuple[float, ...] = LEARNING_RATES,
    steps: int = STEPS_PER_CANDIDATE,
    device: str = "cuda", max_seconds: float = 34,
    split_seed: int = SPLIT_SEED, torch_module=None,
) -> tuple[dict[str, Any], dict]:
    """Return metrics and winning CPU tensor state (no files/network).

    No test evaluation during search. Include zero-step original as a candidate.
    A timeout refuses to declare a full-grid winner or read heldout labels.
    """
    validate_grid(seeds, learning_rates, steps, max_seconds)
    import torch as imported_torch
    torch = torch_module or imported_torch
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("ZeroGPU CUDA allocation unavailable")
    if device not in ("cpu", "cuda"):
        raise ValueError("Unsupported device")

    xtr = np.asarray(x_train, dtype="float32")
    ytr = np.asarray(y_train, dtype="float32")
    xte = np.asarray(x_test, dtype="float32")
    yte = np.asarray(y_test, dtype="float32")
    if xtr.shape != (360, 4) or ytr.shape != (360, 2):
        raise ValueError("Training data must match pinned source shape")
    if xte.shape != (128, 4) or yte.shape != (128, 2):
        raise ValueError("Heldout source must have 128 samples")
    if len(scenario_train) != 360:
        raise ValueError("Scenario count mismatch")
    if any(not np.isfinite(a).all() for a in (xtr, ytr, xte, yte)):
        raise ValueError("Non-finite input")
    split = stratified_split(np.asarray(scenario_train), seed=split_seed)
    started = time.monotonic()
    tx = torch.tensor(xtr[split.train_indices], device=device)
    ty = torch.tensor(ytr[split.train_indices], device=device)
    vx = torch.tensor(xtr[split.val_indices], device=device)
    vy = torch.tensor(ytr[split.val_indices], device=device)

    def fresh_model():
        m = model_factory().to(device)
        m.load_state_dict(initial_state, strict=True)
        return m

    def snapshot(m):
        return {k: v.detach().cpu().clone().contiguous() for k, v in m.state_dict().items()}

    def eval_mae(m, xx, yy):
        m.eval()
        with torch.inference_mode():
            return float(torch.nn.functional.l1_loss(m(xx), yy).item())

    base_model = fresh_model()
    baseline_val = eval_mae(base_model, vx, vy)
    best = {"val_mae": baseline_val, "seed": None, "learning_rate": None,
            "best_step": 0, "candidate": "unchanged-pretrained"}
    best_state = snapshot(base_model)
    candidates = []
    for seed in seeds:
        for lr in learning_rates:
            if time.monotonic() - started > max_seconds - 5:
                raise TimeoutError("GPU budget exhausted before completing the predeclared grid")
            torch.manual_seed(seed)
            rng = np.random.default_rng(seed)
            m = fresh_model()
            optim = torch.optim.Adam(m.parameters(), lr=float(lr))
            local_best, local_step, stale = baseline_val, 0, 0
            curve = [{"step": 0, "val_mae": round(baseline_val, 8)}]
            for step in range(1, steps + 1):
                if time.monotonic() - started >= max_seconds - 4:
                    raise TimeoutError("GPU budget exhausted: reject partial-grid model selection")
                indices = torch.tensor(rng.integers(0, len(tx), size=64),
                                       dtype=torch.long, device=device)
                m.train()
                optim.zero_grad(set_to_none=True)
                loss = torch.nn.functional.l1_loss(m(tx[indices]), ty[indices])
                loss.backward()
                optim.step()
                if step % EVAL_EVERY == 0:
                    score = eval_mae(m, vx, vy)
                    if not math.isfinite(score):
                        raise RuntimeError("Non-finite validation error")
                    curve.append({"step": step, "val_mae": round(score, 8)})
                    if score < local_best - MIN_DELTA:
                        local_best, local_step, stale = score, step, 0
                        if score < best["val_mae"] - MIN_DELTA:
                            best = {"val_mae": score, "seed": seed,
                                    "learning_rate": float(lr), "best_step": step,
                                    "candidate": f"seed{seed}-lr{lr}"}
                            best_state = snapshot(m)
                    else:
                        stale += 1
                    if stale >= PATIENCE_EVALS:
                        break
            candidates.append({"seed": seed, "learning_rate": float(lr),
                               "best_step": local_step, "best_val_mae": round(local_best, 8),
                               "evaluations": curve, "early_stopped": stale >= PATIENCE_EVALS})
    # All candidates locked before ever evaluating heldout labels.
    winner = fresh_model()
    winner.load_state_dict(best_state, strict=True)
    heldout_x = torch.tensor(xte, device=device)
    heldout_y = torch.tensor(yte, device=device)
    final_test_mae = eval_mae(winner, heldout_x, heldout_y)
    if device == "cuda":
        torch.cuda.synchronize()
    return ({
        "schema": CHECKPOINT_SCHEMA,
        "selection_metric": "stratified_train_validation_mae",
        "best": {**best, "val_mae": round(best["val_mae"], 8)},
        "baseline_val_mae": round(baseline_val, 8),
        "grid_completed": len(candidates) == len(seeds) * len(learning_rates),
        "candidates": candidates,
        "train_count": int(len(split.train_indices)),
        "validation_count": int(len(split.val_indices)),
        "validation_groups": split.groups,
        "validation_index_sha256": split.val_indices_sha256,
        "split_seed": split.split_seed,
        "heldout_count": 128,
        "final_heldout_mae": round(final_test_mae, 8),
        "heldout_used_in_selection": False,
        "device": device,
        "gpu_name": torch.cuda.get_device_name(0) if device == "cuda" else None,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "warning": "Base model saw the 360 training states; earlier experiments have examined the 128 holdout. This is fine-tuning validation, not a new independent scientific test.",
    }, best_state)


def run_from_pinned_assets(*, require_cuda=True, output_dir=None):
    """ZeroGPU callable; imports the deployed v1 loader to preserve SHA checks."""
    import torch
    import train_biolocator as original
    original.verify_assets()
    with np.load(original.ASSETS / original.DATA_FILENAME, allow_pickle=False) as archive:
        labels = archive["scenario_train"].copy()
    data = original.load_teacher_data()
    source_model, mean, std = original.load_reference(torch)
    initial_state = {k: v.detach().cpu().clone() for k, v in source_model.state_dict().items()}
    x_train = (data["X_train"] - mean) / std
    x_test = (data["X_test"] - mean) / std
    metrics, winning_state = search_model(
        lambda: original.construct_model(torch), initial_state, x_train,
        data["Y_train"], labels, x_test, data["Y_test"],
        device="cuda" if require_cuda else "cpu",
    )
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="mukhtar_val_v2_")
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    from safetensors.torch import save_file
    checkpoint = target / "mukhtar_biolocator_selected_validation_v2.safetensors"
    metadata = {
        "schema": CHECKPOINT_SCHEMA,
        "base_sha256": original.BASE_SHA,
        "dataset_sha256": original.DATA_SHA,
        "architecture": "4-64-32-2",
        "validation_index_sha256": metrics["validation_index_sha256"],
        "selected_seed": str(metrics["best"]["seed"]),
        "selected_lr": str(metrics["best"]["learning_rate"]),
        "selected_steps": str(metrics["best"]["best_step"]),
        "warning": "Never use heldout results to select the checkpoint",
    }
    save_file(winning_state, str(checkpoint), metadata=metadata)
    if checkpoint.stat().st_size > 100_000:
        checkpoint.unlink()
        raise RuntimeError("Checkpoint exceeds safety size")
    metrics["base_sha256"] = original.BASE_SHA
    metrics["dataset_sha256"] = original.DATA_SHA
    metrics["checkpoint_sha256"] = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    metrics["checkpoint_file"] = checkpoint.name
    report = target / "validation_search_v2_metrics.json"
    report.write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n")
    return metrics, str(checkpoint), str(report)
