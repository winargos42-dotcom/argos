import hashlib
import importlib
import importlib.util
import inspect
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def engine():
    return importlib.import_module("cpg_engine")


def lab():
    assert importlib.util.find_spec("prc_lab") is not None, "PRC runner is absent"
    return importlib.import_module("prc_lab")


def test_original_rasters_remain_bitwise_identical():
    e = engine()
    hashes = json.loads(Path(__file__).with_name("raster_reference.json").read_text())
    for experiment in e.EXPERIMENTS:
        for drive in e.DRIVES:
            raster = e.sim_cpg(drive=drive, ko=e.KO_MAP[experiment])
            assert hashlib.sha256(raster.tobytes()).hexdigest() == hashes[f"{experiment}/{drive}"]


def test_zero_pulse_leaves_the_whole_raster_unchanged():
    e = engine()
    assert "pulse" in inspect.signature(e.sim_cpg).parameters, "No pulse injection API"
    np.testing.assert_array_equal(e.sim_cpg(), e.sim_cpg(pulse=(123, "I2", 0.0)))


def test_pulse_is_single_tick_and_does_not_change_its_past():
    e = engine()
    assert "pulse" in inspect.signature(e.sim_cpg).parameters, "No pulse injection API"
    baseline = e.sim_cpg()
    changed = e.sim_cpg(pulse=(123, "I2", 2.0))
    np.testing.assert_array_equal(changed[:123], baseline[:123])
    assert np.any(changed[123:] != baseline[123:])
    isolated = e.sim_cpg(drive=0.0, ticks=20, pulse=(5, "I2", 1.0))
    assert np.flatnonzero(isolated[:, e.IDX["I2"]]).tolist() == [5]


def test_zero_pulse_has_zero_matched_control_shift_at_all_phases():
    result = lab().run_prc(amplitude=0.0)
    assert result["status"] == "ok"
    assert len(result["trials"]) == 12
    for trial in result["trials"]:
        assert trial["status"] == "ok"
        assert trial["shift_ticks"] == trial["shift_rad"] == 0.0
        assert trial["pulse_onset_tick"] == trial["control_onset_tick"]
        assert trial["raster"] == result["baseline"]["raster"]


def test_nonzero_pulse_produces_measured_phase_effect():
    result = lab().run_prc(target="I2", amplitude=2.0)
    assert result["status"] == "ok"
    shifts = [t["shift_rad"] for t in result["trials"] if t["status"] == "ok"]
    assert shifts and all(math.isfinite(s) for s in shifts)
    assert any(abs(s) > 0.01 for s in shifts)
    for trial in result["trials"]:
        assert trial["control_onset_tick"] == result["baseline"]["next_onset_tick"]
        if trial["status"] == "ok":
            assert trial["shift_ticks"] == (trial["pulse_onset_tick"] - trial["control_onset_tick"])


def test_silent_baseline_reports_invalid_rhythm_without_fabricated_points():
    result = lab().run_prc(drive=0.0)
    assert result["status"] == "invalid_rhythm"
    assert result["reason"]
    assert result["trials"] == []
    assert result["baseline"]["period_ticks"] is None


def test_protocol_json_and_plot_are_real_outputs():
    p = lab()
    result = p.run_prc(phases=[0.0, math.pi])
    encoded = p.prc_json(result)
    restored = json.loads(encoded)
    assert restored == result
    assert restored["protocol"]["engine_source_sha256"]
    assert restored["protocol"]["weights_sha256"]
    figure = p.plot_prc(result)
    assert len(figure.axes) >= 2
    assert figure.axes[0].lines


@pytest.mark.parametrize("kwargs", [
    {"drive": float("nan")}, {"amplitude": 10000}, {"target": "missing"},
    {"phases": [float("inf")]}, {"phases": [0.0] * 1000},
])
def test_rejects_invalid_or_unbounded_requests(kwargs):
    with pytest.raises(ValueError):
        lab().run_prc(**kwargs)
