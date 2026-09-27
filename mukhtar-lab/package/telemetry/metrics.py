"""Benchmark measurements; these observers never change controller state."""

import math
from collections import Counter

import numpy as np


class BodyMetrics:
    """Body-up tilt and height loss relative to the first observed pose.

    Call after the settling interval. Quaternion order is MuJoCo's w,x,y,z.
    ``body_drop_mm`` remains a compatibility alias for the final height loss.
    """

    def __init__(self):
        self.reference_z = None
        self.final_z = None
        self.min_z = None
        self.max_tilt = 0.0

    def observe(self, z, quaternion):
        q = np.asarray(quaternion, dtype=float)
        if q.shape != (4,) or not np.all(np.isfinite(q)):
            raise ValueError("quaternion must have four finite wxyz components")
        norm = float(np.linalg.norm(q))
        if norm == 0.0 or not math.isfinite(norm):
            raise ValueError("quaternion must have a finite nonzero norm")
        z = float(z)
        if not math.isfinite(z):
            raise ValueError("body height must be finite")
        _, x, y, _ = q / norm
        up_dot = float(np.clip(1.0 - 2.0 * (x * x + y * y), -1.0, 1.0))
        tilt = math.acos(up_dot)
        if self.reference_z is None:
            self.reference_z = z
            self.min_z = z
        self.final_z = z
        self.min_z = min(self.min_z, z)
        self.max_tilt = max(self.max_tilt, tilt)

    def summary(self):
        final = peak = tilt = None
        if self.reference_z is not None:
            final = round(1000.0 * max(0.0, self.reference_z - self.final_z), 1)
            peak = round(1000.0 * max(0.0, self.reference_z - self.min_z), 1)
            tilt = round(math.degrees(self.max_tilt), 1)
        return {"body_drop_mm": final, "final_body_drop_mm": final,
                "peak_body_drop_mm": peak, "max_tilt_deg": tilt}


class EventMetrics:
    """Count reason episodes separately from per-tick reflex output records.

    A trigger starts a reason absent in the preceding update of this leg and
    reflex. A reason transition (e.g. search -> retract) starts a new episode;
    this is distinct from domain counters such as R3's ``n_searches``.
    Observe inactive outputs too, so a later activation starts a new episode.
    """

    def __init__(self):
        self._previous = {}
        self.active_ticks = Counter()
        self.triggers = Counter()

    def observe(self, leg, reflex, reasons):
        reasons = tuple(dict.fromkeys(reasons))
        key = (leg, reflex)
        previous = self._previous.get(key, set())
        types = {}
        for reason in reasons:
            self.active_ticks[reason] += 1
            if reason not in previous:
                self.triggers[reason] += 1
                types[reason] = "trigger"
            else:
                types[reason] = "active_tick"
        self._previous[key] = set(reasons)
        return types

    def summary(self, expected_no_reflex=False):
        trigger_count = sum(self.triggers.values())
        return {
            "event_active_ticks": dict(self.active_ticks),
            "event_triggers": dict(self.triggers),
            "active_tick_count": sum(self.active_ticks.values()),
            "trigger_count": trigger_count,
            "false_events": trigger_count if expected_no_reflex else None,
            "false_events_basis": ("explicit_no_reflex_oracle" if
                                   expected_no_reflex else
                                   "unknown_without_no_reflex_oracle"),
            "false_events_scope": "stage1_reason_episode_starts",
        }
