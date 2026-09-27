"""reflexes/r1_foot_catch.py — R1b foot-catch (ловушка 12 мм).

Поверх базы Севы. Сигнал: устойчивый контакт СТОПЫ в середине swing
(phi-окно), gating по тибии (если тибия уже видит препятствие — работает
R1a, а не зацеп). Дискриминатор «зацеп vs чирканье» — длительность
контакта в секундах: FOOT_CATCH_MIN_TIME = 8 * control_dt (dt=0.002 ->
16 мс). Измерено 27.09: 12 мм 0.486 -> 1.189 м; на 10/14 мм деградация
~1% (чирканье отсекается порогом длительности).
"""

from __future__ import annotations

import numpy as np

from .base import ReflexContext, ReflexOutput

PHI_LO = 0.25 * np.pi
PHI_HI = 0.75 * np.pi


class R1FootCatchReflex:
    def __init__(self, *,
                 dt: float = 0.002,
                 ticks_min: int = 8,
                 phase_window: tuple[float, float] = (PHI_LO, PHI_HI),
                 pullback: float = 0.55,
                 lift: float = 0.10,
                 retract: float = 0.05,
                 tuck: float = 0.04,
                 cooldown: float = 0.5):
        self.min_time = float(ticks_min * dt)
        self.phi_lo, self.phi_hi = [float(v) for v in phase_window]
        self.pullback = float(pullback)
        self.lift = float(lift)
        self.retract = float(retract)
        self.tuck = float(tuck)
        self.cooldown = float(cooldown)
        self._pending = False
        self._last_t = -9.0

    def update(self, ctx: ReflexContext) -> ReflexOutput:
        foot = ctx.contacts.get("foot")
        tibia = ctx.contacts.get("tibia")
        tibia_active = bool(tibia is not None and tibia.active)
        phi = float(ctx.phase) % (2.0 * np.pi)
        in_window = self.phi_lo < phi < self.phi_hi
        catching = (in_window and ctx.swing
                    and foot is not None and foot.active
                    and not tibia_active)
        if catching and foot.duration_s >= self.min_time:
            if (not self._pending
                    and ctx.t - self._last_t > self.cooldown):
                self._pending = True
                self._last_t = ctx.t
                out = ReflexOutput()
                out.phase_delta = -self.pullback
                out.joint_delta[0] += self.retract
                out.joint_delta[1] += self.lift
                out.joint_delta[2] += self.tuck
                out.active = True
                out.reasons = ("R1B_FOOT_CATCH",)
                return out
            return ReflexOutput()
        if not catching:
            self._pending = False
        return ReflexOutput()

    def reset(self) -> None:
        self._pending = False
        self._last_t = -9.0
