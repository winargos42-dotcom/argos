"""Exercise the public CLI and exported evidence, including overwrite protection."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

LAB = Path(__file__).resolve().parents[2]
SCRIPT = LAB / "fly_bridge" / "bench_jsonl.py"


def test_cli_exports_portable_hashed_run_and_protects_existing_output(tmp_path):
    output = tmp_path / "run"
    command = [sys.executable, str(SCRIPT), "--out", str(output),
               "--scenario", "B01-flat", "--controller", "BASE",
               "--duration", "1.02"]
    first = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    assert first.returncode == 0, first.stderr
    summary = json.loads((output / "summary.json").read_text())
    assert summary["schema_version"] == 2
    assert len(summary["results"]) == 1
    result = summary["results"][0]
    assert result["scenario"] == "B01-flat"
    assert result["seed"] == 42
    assert result["false_events"] == 0
    assert result["reflex_events"] == 0
    assert result["max_tilt_deg"] < 10
    assert result["peak_body_drop_mm"] >= result["final_body_drop_mm"]
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["status"] == "complete"
    assert manifest["checkpoint_sha256"] is None  # These are analytic controllers.
    assert len(manifest["source_sha256"]) == 64
    assert manifest["runtime"]["mujoco"]
    for relative, expected in manifest["artifacts"].items():
        assert hashlib.sha256((output / relative).read_bytes()).hexdigest() == expected
    before = (output / "summary.json").read_bytes()
    second = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    assert second.returncode != 0
    assert (output / "summary.json").read_bytes() == before


def test_cli_rejects_settling_only_run(tmp_path):
    output = tmp_path / "invalid"
    result = subprocess.run([sys.executable, str(SCRIPT), "--out", str(output),
                             "--duration", "0.5"], capture_output=True, text=True)
    assert result.returncode != 0
    assert not output.exists()


def test_export_rejects_code_imported_from_another_checkout(tmp_path):
    other = tmp_path / "other-checkout"
    shutil.copytree(LAB / "package", other / "mukhtar")
    output = tmp_path / "mixed-run"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(output),
         "--scenario", "B01-flat", "--controller", "BASE", "--duration", "1.02"],
        env={**os.environ, "PYTHONPATH": str(other)}, cwd=tmp_path,
        capture_output=True, text=True)
    assert result.returncode != 0, "A run must not hash code other than what it imports"
    assert not output.exists()
