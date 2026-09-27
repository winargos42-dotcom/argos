from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Protocol, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from mukhtar.sensors.contact_pipeline import ContactSignal


def _vec3_zero() -> np.ndarray:
    return np.zeros(3, dtype=np.float32)


def _vec3_nan() -> np.ndarray:
    return np.full(3, np.nan, dtype=np.float32)


@dataclass(slots=True)
class ReflexOutput:
    """One reflex contribution for a single leg.

    The reflex layer returns corrections; it does not own gait generation.
    Values are merged by ``mix_reflex_outputs`` before the final safety clamp.
    """

    joint_delta: np.ndarray = field(default_factory=_vec3_zero)
    phase_delta: float = 0.0
    phase_hold: bool = False
    speed_scale: float = 1.0
    inhibit_swing: bool = False
    active: bool = False
    reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        self.joint_delta = np.asarray(self.joint_delta, dtype=np.float32).copy()
        if self.joint_delta.shape != (3,):
            raise ValueError(f"joint_delta must have shape (3,), got {self.joint_delta.shape}")
        if not np.all(np.isfinite(self.joint_delta)):
            raise ValueError("joint_delta contains non-finite values")
        if not np.isfinite(self.phase_delta):
            raise ValueError("phase_delta must be finite")
        if not np.isfinite(self.speed_scale) or self.speed_scale < 0.0:
            raise ValueError("speed_scale must be finite and >= 0")


@dataclass(slots=True)
class ReflexContext:
    """Read-only snapshot consumed by one leg reflex at one control tick."""

    dt: float
    t: float
    leg: int
    phase: float
    swing: bool
    stance: bool
    contacts: Mapping[str, "ContactSignal"]
    foot_pos: np.ndarray = field(default_factory=_vec3_nan)
    joint_pos: np.ndarray = field(default_factory=_vec3_zero)
    joint_vel: np.ndarray = field(default_factory=_vec3_zero)
    expected_contact: float = 0.0
    neighbor_loads: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=np.float32))

    def __post_init__(self) -> None:
        if self.dt <= 0.0 or not np.isfinite(self.dt):
            raise ValueError("dt must be finite and > 0")
        if self.leg < 0:
            raise ValueError("leg must be >= 0")
        self.foot_pos = np.asarray(self.foot_pos, dtype=np.float32).copy()
        self.joint_pos = np.asarray(self.joint_pos, dtype=np.float32).copy()
        self.joint_vel = np.asarray(self.joint_vel, dtype=np.float32).copy()
        self.neighbor_loads = np.asarray(self.neighbor_loads, dtype=np.float32).copy()
        if self.foot_pos.shape != (3,):
            raise ValueError("foot_pos must have shape (3,)")
        if self.joint_pos.shape != (3,) or self.joint_vel.shape != (3,):
            raise ValueError("joint_pos and joint_vel must have shape (3,)")


class Reflex(Protocol):
    def reset(self) -> None:
        """Reset internal timers/integrators between runs."""

    def update(self, ctx: ReflexContext) -> ReflexOutput:
        """Return this reflex's correction for one leg and one control tick."""
