"""Measured first-cycle phase response of the Space's isolated T1-L circuit.

This is a deterministic five-cell experiment, not locomotion or evidence of
improved robotic control. Each pulse trial uses the exact same initial state
and generator as its unperturbed control.
"""

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform

import numpy as np

import cpg_engine


TICKS = 800
WARMUP = 200
ANCHOR_AFTER = 400
MAX_PHASES = 24


def burst_onsets(raster):
    """Causal trailing three-tick E1+E2 mean, hysteresis 0.6 / 0.2."""
    e = raster[:, cpg_engine.IDX["E1"]] + raster[:, cpg_engine.IDX["E2"]]
    smoothed = np.convolve(e, np.ones(3) / 3.0, mode="full")[:len(e)]
    above = False
    onsets = []
    for tick in range(2, len(smoothed)):
        if not above and smoothed[tick] >= 0.6:
            onsets.append(tick)
            above = True
        elif smoothed[tick] < 0.2:
            above = False
    return onsets


def _protocol(drive, target, amplitude):
    edges = [[pre, post, weight]
             for (pre, post), weight in sorted(cpg_engine.BASE_EDGES.items())]
    weights = json.dumps(edges, separators=(",", ":")).encode()
    return {
        "version": 1,
        "engine": "Space BASE T1-L, five-cell LIF, float32",
        "engine_source_sha256": hashlib.sha256(
            Path(cpg_engine.__file__).read_bytes()).hexdigest(),
        "runner_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "weights_sha256": hashlib.sha256(weights).hexdigest(),
        "cell_order": list(cpg_engine.NAMES),
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "drive": drive, "target": target, "amplitude": amplitude,
        "ticks": TICKS, "warmup_ticks": WARMUP,
        "pulse_duration_ticks": 1,
        "onset_detector": "causal trailing mean(E1+E2,3), up>=0.6, reset<0.2",
        "rhythm_criterion": ">=8 intervals after warmup; interval CV<=0.25",
        "phase_quantization": "nearest tick strictly inside anchor cycle; effective phase recorded",
        "shift_convention": "positive=delay, negative=advance; radians=2*pi*shift_ticks/median_period",
        "control": "identical generator, drive, zero state and tick count; no pulse",
        "measurement": "first burst onset strictly after the common baseline anchor",
        "scope": "isolated neural module; no MuJoCo, gait, training or whole-brain inference",
    }


def run_prc(drive=0.8, target="I2", amplitude=2.0, phases=None):
    """Return JSON-safe baseline, paired perturbations and measured shifts.

    ``phases`` is an iterable of 1..24 angles in [0, 2*pi), in radians.
    The phase-zero request maps to the first tick after the anchor: changing
    the anchor itself would make a first-cycle phase comparison ambiguous.
    Actual quantized phase is returned for every trial; no wrap of shifts.
    """
    drive, amplitude = float(drive), float(amplitude)
    if not math.isfinite(drive) or not 0.0 <= drive <= 2.0:
        raise ValueError("drive must be finite and within [0,2]")
    if not math.isfinite(amplitude) or not -5.0 <= amplitude <= 5.0:
        raise ValueError("amplitude must be finite and within [-5,5]")
    if target not in cpg_engine.IDX:
        raise ValueError("target must be one of " + ", ".join(cpg_engine.NAMES))
    requested = (list(np.linspace(0.0, 2.0 * math.pi, 12, endpoint=False))
                 if phases is None else list(itertools.islice(iter(phases), MAX_PHASES + 1)))
    if not 1 <= len(requested) <= MAX_PHASES:
        raise ValueError("request 1..24 phases")
    requested = [float(p) for p in requested]
    if any(not math.isfinite(p) or not 0.0 <= p < 2.0 * math.pi for p in requested):
        raise ValueError("phases must be finite radians in [0,2*pi)")

    reference = cpg_engine.sim_cpg(drive=drive, ticks=TICKS)
    onsets = burst_onsets(reference)
    stable_onsets = [t for t in onsets if t >= WARMUP]
    intervals = np.diff(stable_onsets)
    period = float(np.median(intervals)) if len(intervals) else None
    jitter = float(np.std(intervals) / np.mean(intervals)) if len(intervals) else None
    baseline = {"period_ticks": period, "interval_cv": jitter,
                "anchor_tick": None, "next_onset_tick": None,
                "reference_cycle_ticks": None, "onsets": onsets,
                "raster": reference.astype(int).tolist()}
    result = {"status": "invalid_rhythm", "reason": None,
              "protocol": _protocol(drive, target, amplitude),
              "baseline": baseline, "trials": []}
    if len(intervals) < 8 or jitter > 0.25:
        result["reason"] = "Not enough recurrent bursts or interval CV exceeds 0.25"
        return result
    candidates = [(a, b) for a, b in zip(onsets, onsets[1:])
                  if a >= ANCHOR_AFTER and b - a >= 2]
    if not candidates:
        result["reason"] = "No complete reference cycle after the anchor boundary"
        return result
    anchor, control_onset = candidates[0]
    cycle_ticks = control_onset - anchor
    baseline.update(anchor_tick=anchor, next_onset_tick=control_onset,
                    reference_cycle_ticks=cycle_ticks)
    result.update(status="ok", reason=None)
    for phase in requested:
        offset = max(1, min(cycle_ticks - 1, round(phase * cycle_ticks / (2 * math.pi))))
        pulse_tick = anchor + offset
        perturbed = cpg_engine.sim_cpg(
            drive=drive, ticks=TICKS, pulse=(pulse_tick, target, amplitude))
        pulse_onsets = burst_onsets(perturbed)
        after = [t for t in pulse_onsets if t > anchor]
        onset = after[0] if after else None
        shift = onset - control_onset if onset is not None else None
        result["trials"].append({
            "requested_phase_rad": phase,
            "effective_phase_rad": 2 * math.pi * offset / cycle_ticks,
            "pulse_tick": pulse_tick, "control_onset_tick": control_onset,
            "pulse_onset_tick": onset, "shift_ticks": shift,
            "shift_rad": 2 * math.pi * shift / period if shift is not None else None,
            "status": "ok" if onset is not None else "no_response_burst",
            "onsets": pulse_onsets, "raster": perturbed.astype(int).tolist(),
        })
    return result


def prc_json(result):
    return json.dumps(result, ensure_ascii=False, allow_nan=False, indent=2)


def plot_prc(result):
    """Plot measured PRC and the largest-effect trial's control/response trace."""
    from matplotlib.figure import Figure

    fig = Figure(figsize=(9, 6), constrained_layout=True)
    curve, trace = fig.subplots(2, 1)
    valid = [t for t in result["trials"] if t["status"] == "ok"]
    curve.axhline(0.0, color="gray", linewidth=0.8)
    curve.set(xlabel="Effective pulse phase (rad)", ylabel="Response shift (rad)",
              title="First-cycle PRC: positive delay / negative advance")
    if not valid:
        curve.text(0.5, 0.5, result["reason"] or "No response bursts",
                   transform=curve.transAxes, ha="center", wrap=True)
        trace.set_axis_off()
        return fig
    ordered = sorted(valid, key=lambda row: row["effective_phase_rad"])
    curve.plot([r["effective_phase_rad"] for r in ordered],
               [r["shift_rad"] for r in ordered], "o-")
    selected = max(valid, key=lambda row: abs(row["shift_rad"]))
    control = np.asarray(result["baseline"]["raster"])
    response = np.asarray(selected["raster"])
    trace.step(np.arange(TICKS), control[:, 1:3].sum(axis=1),
               where="post", label="Unperturbed E1+E2", alpha=0.7)
    trace.step(np.arange(TICKS), response[:, 1:3].sum(axis=1),
               where="post", label="Pulse trial E1+E2", alpha=0.7)
    trace.axvline(selected["pulse_tick"], color="red", linestyle=":", label="One-tick pulse")
    trace.axvline(selected["control_onset_tick"], color="gray", linestyle="--", label="Control onset")
    trace.axvline(selected["pulse_onset_tick"], color="green", linestyle="--", label="Response onset")
    anchor = result["baseline"]["anchor_tick"]
    period = result["baseline"]["period_ticks"]
    trace.set(xlim=(anchor - period, max(selected["pulse_onset_tick"], anchor) + 2 * period),
              xlabel="Neural tick", ylabel="E1+E2 spikes", title="Largest measured effect: matched traces")
    trace.legend(fontsize="small", loc="upper right")
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--drive", type=float, default=0.8)
    parser.add_argument("--target", choices=cpg_engine.NAMES, default="I2")
    parser.add_argument("--amplitude", type=float, default=2.0)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    result = run_prc(args.drive, args.target, args.amplitude)
    (args.out / "prc.json").write_text(prc_json(result) + "\n", encoding="utf-8")
    plot_prc(result).savefig(args.out / "prc.png", dpi=150)
    print(json.dumps({"status": result["status"], "out": str(args.out),
                      "period_ticks": result["baseline"]["period_ticks"],
                      "shifts": [t["shift_rad"] for t in result["trials"]]}))


if __name__ == "__main__":
    main()
