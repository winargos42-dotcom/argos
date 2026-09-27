from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from .base import ReflexOutput


def mix_reflex_outputs(
    outputs: Iterable[ReflexOutput],
    *,
    joint_delta_limit: np.ndarray | float | None = None,
    phase_delta_limit: float | None = None,
) -> ReflexOutput:
    """Merge independent reflex contributions deterministically.

    Policy:
    - joint_delta: additive, then symmetric clip if configured;
    - phase_delta: additive, then symmetric clip if configured;
    - phase_hold / inhibit_swing: logical OR;
    - speed_scale: minimum value, so the reflex layer can slow but not force
      an acceleration above the nominal command;
    - reasons: stable-order de-duplicated tuple.
    """

    joint_delta = np.zeros(3, dtype=np.float32)
    phase_delta = 0.0
    phase_hold = False
    inhibit_swing = False
    speed_scale = 1.0
    active = False
    reasons: list[str] = []
    seen: set[str] = set()

    for item in outputs:
        if not isinstance(item, ReflexOutput):
            raise TypeError(f"expected ReflexOutput, got {type(item)!r}")

        joint_delta += item.joint_delta
        phase_delta += float(item.phase_delta)
        phase_hold |= bool(item.phase_hold)
        inhibit_swing |= bool(item.inhibit_swing)
        speed_scale = min(speed_scale, float(item.speed_scale))
        active |= bool(item.active)

        for reason in item.reasons:
            if reason not in seen:
                seen.add(reason)
                reasons.append(reason)

    if joint_delta_limit is not None:
        limit = np.asarray(joint_delta_limit, dtype=np.float32)
        if limit.ndim == 0:
            limit = np.full(3, float(limit), dtype=np.float32)
        if limit.shape != (3,):
            raise ValueError("joint_delta_limit must be a scalar or shape (3,)")
        if np.any(limit < 0) or not np.all(np.isfinite(limit)):
            raise ValueError("joint_delta_limit must be finite and >= 0")
        joint_delta = np.clip(joint_delta, -limit, limit)

    if phase_delta_limit is not None:
        limit = float(phase_delta_limit)
        if limit < 0 or not np.isfinite(limit):
            raise ValueError("phase_delta_limit must be finite and >= 0")
        phase_delta = float(np.clip(phase_delta, -limit, limit))

    return ReflexOutput(
        joint_delta=joint_delta,
        phase_delta=phase_delta,
        phase_hold=phase_hold,
        speed_scale=speed_scale,
        inhibit_swing=inhibit_swing,
        active=active,
        reasons=tuple(reasons),
    )
