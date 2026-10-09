"""Run the exact BioLocator validation-v2 search on REAL pinned HF data.

This is ACTUAL fine-tuning against the published AvaSiG model and teacher
dataset, not the synthetic test fixture. Runs on CPU in GitHub Actions, costs
no HF dedicated GPU rental. GPU ZeroGPU deployment is a separate action.
Artifacts: metrics.json and selected.safetensors.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import sys

import numpy as np
import torch
from huggingface_hub import hf_hub_download
from safetensors.torch import save_file

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(parents=True, exist_ok=True)
DATA_SHA = "e60c8d5f06aefaa26f99b660dc570b7a7d60501b6891481993db957dbf6911a6"
MODEL_SHA = "c61ed7041ee2b47c87d98dd70e3278920401f84a2bd21e9e379f3db6b2b75da3"
REVISION = "b850d33c1acb584e9510781f082ea03bc305ecf6"
REMOTE = "AvaSiG/ARGOS-MUKHTAR-ZeroGPU"

sys.path.insert(0, str(HERE))
from validation_search import search_model, CHECKPOINT_SCHEMA

def download(name: str, expected_sha: str | None = None) -> Path:
    dest = hf_hub_download(
        repo_id=REMOTE, repo_type="space", revision=REVISION,
        filename=name, local_dir=str(OUT / "remote"),
    )
    result = Path(dest)
    if expected_sha:
        digest = hashlib.sha256(result.read_bytes()).hexdigest()
        if digest != expected_sha:
            raise RuntimeError("Hash mismatch: " + name)
        print("ORIGINAL_SHA256_PASS", name, digest[:16], flush=True)
    return result

def main() -> None:
    torch.set_num_threads(2)
    data_filename="biolocator_v3_teacher_dataset_20260928.npz"
    model_filename="biolocator_v3_student4_mlp_20260928.pt"
    source = download("train_biolocator.py")
    download("assets/" + data_filename, DATA_SHA)
    download("assets/" + model_filename, MODEL_SHA)
    sys.path.insert(0, str(source.parent))
    import train_biolocator as original
    data = original.load_teacher_data()
    print("REAL_TRAIN_DATA", data["X_train"].shape, data["Y_train"].shape, flush=True)
    print("REAL_HELDOUT_DATA", data["X_test"].shape, data["Y_test"].shape, flush=True)

    with np.load(original.ASSETS / original.DATA_FILENAME, allow_pickle=False) as archive:
        print("ORIGINAL_DATA_KEYS", [(k, str(archive[k].shape), str(archive[k].dtype)) for k in archive.files], flush=True)
        known = [
            "scenario_train", "scenarios_train", "train_scenario",
            "train_scenarios", "scenario_labels_train", "regime_train",
        ]
        present = [k for k in known if k in archive.files]
        if present:
            label_key = present[0]
            groups = np.asarray(archive[label_key])
            if len(groups) != 360:
                raise ValueError("Scenario label length mismatch")
            group_note = "source scenario labels: " + label_key
        else:
            # Honest fallback. Never pretend synthetic scenario labels exist.
            groups = np.asarray(["unlabeled"] * 360)
            group_note = "NO SOURCE SCENARIO LABELS: fixed seeded random 288/72 split"
            print("SOURCE_SCENARIOS_UNAVAILABLE", group_note, flush=True)

    model, mean, std = original.load_reference(torch)
    x_train = ((data["X_train"] - mean) / std).astype("float32")
    x_test = ((data["X_test"] - mean) / std).astype("float32")
    state = {k: v.detach().cpu().clone() for k,v in model.state_dict().items()}

    # Exactly six candidates, and no use of holdout in optimization/selection.
    metrics, winner = search_model(
        lambda: original.construct_model(torch), state,
        x_train, data["Y_train"], groups,
        x_test, data["Y_test"], device="cpu", max_seconds=35,
    )
    assert len(metrics["candidates"]) == 6 and metrics["grid_completed"]
    metrics.update({
        "data_source": REMOTE,
        "source_revision": REVISION,
        "base_sha256": MODEL_SHA,
        "dataset_sha256": DATA_SHA,
        "scenario_source": group_note,
        "real_training": True,
        "dedicated_gpu_job": False,
        "training_hardware": "GitHub Actions CPU",
        "important": "Model was previously trained on 360 samples. Holdout already inspected in earlier pilots. Fine-tuning comparison only, not new independent benchmark.",
    })
    cp = OUT / "mukhtar_validation_v2_selected.safetensors"
    save_file({k:v.contiguous() for k,v in winner.items()}, str(cp),
              metadata={"schema":CHECKPOINT_SCHEMA, "base_sha256":MODEL_SHA,
                        "dataset_sha256":DATA_SHA,
                        "validation_index_sha256":metrics["validation_index_sha256"],
                        "seed":str(metrics["best"]["seed"]),
                        "learning_rate":str(metrics["best"]["learning_rate"]),
                        "best_step":str(metrics["best"]["best_step"])})
    digest = hashlib.sha256(cp.read_bytes()).hexdigest()
    metrics["checkpoint_sha256"] = digest
    (OUT / "metrics_real_training.json").write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+"\n")
    print("REAL_DATA_TRAINING_FINISHED", json.dumps({
        "samples_train":metrics["train_count"],
        "samples_validation":metrics["validation_count"],
        "candidates":len(metrics["candidates"]),
        "base_val_mae":metrics["baseline_val_mae"],
        "selected":metrics["best"],
        "final_heldout_mae":metrics["final_heldout_mae"],
        "selected_checkpoint_sha256":digest,
        "scenario_source":group_note,
    },ensure_ascii=False), flush=True)

if __name__ == "__main__":
    main()
