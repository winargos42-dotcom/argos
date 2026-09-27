"""Regression checks for reported measurements, independent of gait quality."""

import math
from pathlib import Path
import sys

import numpy as np
import pytest


LAB_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LAB_ROOT))

from fly_bridge import stage1_matrix as matrix  # noqa: E402
from mukhtar.sensors.contact_pipeline import ContactSignal  # noqa: E402


class PoseOnlyController:
    def reset(self):
        pass

    def set_command(self, command, t):
        pass

    def step(self, t, state):
        return np.zeros(18)


def measured_pose(monkeypatch, *, quat=(1, 0, 0, 0), heights=None):
    model = matrix.mujoco.MjModel.from_xml_path(
        str(LAB_ROOT / "models" / "hexapod.xml"))
    tick = 0

    def prescribed_pose(model, data):
        nonlocal tick
        tick += 1
        data.qpos[2] = heights(tick) if heights else 0.25
        data.qpos[3:7] = quat
        matrix.mujoco.mj_forward(model, data)

    # Only the simulator integration step is replaced: run() still gathers,
    # transforms and aggregates all reported measurements itself.
    monkeypatch.setattr(matrix.mujoco, "mj_step", prescribed_pose)
    return matrix.run(model, PoseOnlyController, matrix.pipeline_for(model),
                      duration=1.01)


@pytest.mark.parametrize("quat, expected", [
    ((1, 0, 0, 0), 0.0),
    ((math.sqrt(0.5), 0, 0, math.sqrt(0.5)), 0.0),
    ((math.cos(math.pi / 12), math.sin(math.pi / 12), 0, 0), 30.0),
    ((0, 1, 0, 0), 180.0),
])
def test_reported_tilt_uses_body_up_not_quaternion_components(
        monkeypatch, quat, expected):
    result = measured_pose(monkeypatch, quat=quat)
    assert result["max_tilt_deg"] == pytest.approx(expected, abs=0.1)


def test_peak_drop_retains_transient_dip_after_body_recovers(monkeypatch):
    result = measured_pose(
        monkeypatch, heights=lambda tick: 0.15 if tick == 502 else 0.25)
    assert result.get("peak_body_drop_mm") == pytest.approx(100.0)
    assert result.get("final_body_drop_mm") == 0.0
    assert result["body_drop_mm"] == result["final_body_drop_mm"]


def test_unknown_false_positive_oracle_is_not_reported_as_zero(monkeypatch):
    result = measured_pose(monkeypatch)
    assert result["false_events"] is None
    assert result.get("false_events_basis")


def test_continuous_load_hold_is_one_trigger_not_ten():
    ctrl = matrix.Stage1Controller(enabled=("r4",), apply_response=False)
    ctrl.set_command("GO", 0.0)
    contacts = {
        leg: {"foot": ContactSignal(active=True, normal_force=3.0,
                                    kind="floor"),
              "tibia": ContactSignal()}
        for leg in range(6)
    }
    phases = np.full(6, 1.8 * math.pi)
    for tick in range(10):
        ctrl._apply_reflex({"t": 1.0 + tick * 0.002,
                            "leg_contacts": contacts,
                            "foot_load": [3.0] * 6}, 0.002, phases)
    assert len(ctrl.event_log) == 60
    assert sum(e.get("event_type") == "trigger"
               for e in ctrl.event_log) == 6
    assert sum(e.get("event_type") == "active_tick"
               for e in ctrl.event_log) == 54
