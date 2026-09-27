"""Export reproducible B01/B02/B03 MuJoCo runs from this checkout.

Raw JSONL contains reflex events, not a full kinematic trajectory. No neural
checkpoint is used by these analytic controllers. Existing output is preserved.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import subprocess
import sys

LAB = Path(__file__).resolve().parents[1]
PLAN = [
    ("B01-flat", "BASE", ()),
    ("B01-flat", "R1b", ("r1b",)),
    ("B01-flat", "R3v2", ("r3",)),
    ("B01-flat", "R4", ("r4",)),
    ("B02-footcatch12", "BASE", ()),
    ("B02-footcatch12", "R1b", ("r1b",)),
    ("B03-gap20", "BASE", ()),
    ("B03-gap20", "R3v2", ("r3",)),
    ("B03-gap20", "R1b+R3v2", ("r1b", "r3")),
]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_provenance():
    """Hash actual checkout inputs; a git revision alone misses uncommitted fixes."""
    paths = [LAB / "pyproject.toml"]
    for directory in ("controllers", "fly_bridge", "package", "models"):
        paths.extend(p for p in (LAB / directory).rglob("*")
                     if p.is_file() and p.suffix in (".py", ".xml")
                     and "tests" not in p.parts and "__pycache__" not in p.parts)
    files = {str(p.relative_to(LAB)): sha256(p) for p in sorted(paths)}
    digest = hashlib.sha256(json.dumps(files, sort_keys=True,
                                      separators=(",", ":")).encode()).hexdigest()
    revision = None
    dirty = None
    try:
        revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=LAB, text=True,
            stderr=subprocess.DEVNULL, timeout=5).strip()
        dirty = bool(subprocess.check_output(
            ["git", "status", "--porcelain", "--", "."], cwd=LAB,
            text=True, stderr=subprocess.DEVNULL, timeout=5).strip())
    except (OSError, subprocess.SubprocessError):
        pass
    return {"git_revision": revision, "git_dirty": dirty,
            "source_sha256": digest, "source_files": files}


def dump_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2,
                               allow_nan=False) + "\n", encoding="utf-8")


def verify_import_origins():
    """Ensure the manifest describes the code actually executing this trial."""
    for name, module in tuple(sys.modules.items()):
        if name == "stage1_matrix":
            expected = LAB / "fly_bridge" / "stage1_matrix.py"
        elif name == "mukhtar" or name.startswith("mukhtar."):
            expected = LAB / "package"
            if name != "mukhtar":
                expected = expected.joinpath(*name.split(".")[1:])
            expected = (expected / "__init__.py" if hasattr(module, "__path__")
                        else expected.with_suffix(".py"))
        elif name.startswith("controllers."):
            expected = LAB.joinpath(*name.split(".")).with_suffix(".py")
        else:
            continue
        origin = getattr(module, "__file__", None)
        if origin is None or Path(origin).resolve() != expected.resolve():
            raise RuntimeError(f"{name} was imported outside this checkout. "
                               "Install this mukhtar-lab with pip install -e '.[bench]'.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True,
                        help="New output directory (existing paths are never overwritten)")
    parser.add_argument("--scenario", choices=sorted({p[0] for p in PLAN}))
    parser.add_argument("--controller", choices=sorted({p[1] for p in PLAN}))
    parser.add_argument("--duration", type=float, default=20.0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)
    if not math.isfinite(args.duration) or args.duration <= 1.002:
        parser.error("duration must exceed the 1-second settling period (>1.002 s)")
    if not 0 <= args.seed < 2**32:
        parser.error("seed must be in [0, 2**32)")
    selected = [p for p in PLAN if (not args.scenario or p[0] == args.scenario)
                and (not args.controller or p[1] == args.controller)]
    if not selected:
        parser.error("no configured scenario/controller combination matches")
    if args.out.exists():
        parser.error(f"output already exists: {args.out}")

    import mujoco
    import numpy as np
    from stage1_matrix import (Stage1Controller, build_gap, build_wall,
                               pipeline_for, run)
    from controllers.contact_reflex import SineContactController

    verify_import_origins()
    provenance = source_provenance()
    runtime = {name: importlib.metadata.version(name) for name in ("numpy", "mujoco")}
    runtime.update(python=platform.python_version(), platform=platform.system(),
                   architecture=platform.machine())
    args.out.mkdir(parents=True, exist_ok=False)
    xml = LAB / "models" / "hexapod.xml"
    results = []
    artifacts = {}
    for scenario, label, enabled in selected:
        np.random.seed(args.seed)
        if scenario == "B02-footcatch12":
            model = build_wall(str(xml), 0.012)
        elif scenario == "B03-gap20":
            model = build_gap(str(xml), depth=0.020)
        else:
            model = mujoco.MjModel.from_xml_path(str(xml))
        run_id = f"{scenario}_{label}"
        model_name = f"{run_id}_model.xml"
        mujoco.mj_saveLastXML(str(args.out / model_name), model)
        artifacts[model_name] = sha256(args.out / model_name)
        ctrl = (Stage1Controller(freq=1.0, k_ret=0.30, enabled=enabled,
                                 apply_response=True) if enabled else
                SineContactController(freq=1.0, k_ret=0.30))
        result = run(model, lambda: ctrl, pipeline_for(model),
                     duration=args.duration, label=run_id,
                     expected_no_reflex=scenario == "B01-flat")
        events_name = f"{run_id}_events.jsonl"
        events = getattr(ctrl, "event_log", [])
        with (args.out / events_name).open("w", encoding="utf-8") as stream:
            for event in events:
                stream.write(json.dumps(event, ensure_ascii=False,
                                         allow_nan=False) + "\n")
        artifacts[events_name] = sha256(args.out / events_name)
        result.update(scenario=scenario, bench_id=scenario, controller=label,
                      seed=args.seed, duration_s=args.duration,
                      distance_m=result["x"], fell=bool(result["fell"]),
                      reflex_events=result["trigger_count"],
                      events_file=events_name, model_file=model_name,
                      model_sha256=artifacts[model_name])
        results.append(result)
        print(f'{run_id}: distance={result["distance_m"]} m '
              f'fell={result["fell"]} triggers={result["reflex_events"]}', flush=True)
    dump_json(args.out / "summary.json", {"schema_version": 2, "results": results})
    artifacts["summary.json"] = sha256(args.out / "summary.json")
    # A manifest marked complete is written only after every run and artifact succeeds.
    dump_json(args.out / "manifest.json", {
        "schema_version": 2, "status": "complete",
        "created_at": datetime.now(timezone.utc).isoformat(),
        **provenance, "runtime": runtime, "seed": args.seed,
        "seed_policy": "NumPy seeded; these controllers and scenarios use no stochastic inputs",
        "duration_s": args.duration, "settling_s": 1.0,
        "checkpoint_sha256": None,
        "checkpoint_reason": "Analytic SineContact/Stage1 controllers; no neural checkpoint loaded",
        "telemetry_kind": "reflex_events_only",
        "metric_notes": {
            "distance_m": "Final forward x displacement from spawn x=0, metres",
            "reflex_events": "Reason-episode starts per leg/reflex; not active ticks",
            "false_events": "Flat no-reflex oracle only; null for unlabelled obstacle/gap runs",
            "body_drop_mm": "Legacy alias of final_body_drop_mm; peak_body_drop_mm is separate",
            "max_tilt_deg": "Body up-axis angle to world up; yaw is not tilt",
        },
        "artifacts": artifacts,
    })
    print(f"BENCH_DONE {args.out}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
