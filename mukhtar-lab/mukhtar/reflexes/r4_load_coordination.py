"""reflexes/r4_load_coordination.py — R4 v2 active load sensing.

Поверх базы Севы. Отвечает не на «сколько ног касается пола», а на:
какие ноги сейчас реально держат массу корпуса, и можно ли безопасно
отпустить конкретную ногу.

Контракт (спек 27.09):

    stance-нога реально несёт нагрузку (Fz >= hold_load_min)
    в конце stance (фаза в окне liftoff 1.7π..2π)
        -> HOLD: phase_hold + inhibit_swing (задержка отрыва)

    текущая разгрузилась (Fz < release_load_max)
    И соседняя нога приняла нагрузку (>= neighbor_accept_min)
        -> RELEASE: swing разрешаем

Защита от вечности: max_hold_time снимает hold в любом случае
(урок R3 v1: вечный phase_hold = падение).

Пороги — из калибровки calib_load.py (нода, flat-трипод, 27.09):
stance Fz mean 3.1–6.4 Н, swing-шум до 18 Н → hold 2.0 / release 0.8 /
сосед 2.0 Н. Гистерезис hold>release — анти-дребезг.
"""

from __future__ import annotations

import numpy as np

from .base import ReflexContext, ReflexOutput

LIFTOFF_PHI_LO = 1.7 * np.pi
LIFTOFF_PHI_HI = 2.0 * np.pi


class R4LoadCoordinationReflex:
    def __init__(self, *,
                 hold_load_min: float = 2.0,
                 release_load_max: float = 0.8,
                 neighbor_accept_min: float = 2.0,
                 max_hold_time: float = 0.40,
                 hold_cooldown: float = 0.15,
                 liftoff_window: tuple[float, float] = (LIFTOFF_PHI_LO,
                                                        LIFTOFF_PHI_HI),
                 chatter_window: float = 0.05):
        self.hold_load_min = float(hold_load_min)
        self.release_load_max = float(release_load_max)
        self.neighbor_accept_min = float(neighbor_accept_min)
        self.max_hold_time = float(max_hold_time)
        self.hold_cooldown = float(hold_cooldown)
        self.phi_lo, self.phi_hi = [float(v) for v in liftoff_window]
        self.chatter_window = float(chatter_window)
        self._holding = False
        self._hold_start = -9.0
        self._last_release_t = -9.0
        # метрики
        self.n_holds = 0
        self.n_releases = 0
        self.hold_ms: list[float] = []
        self.n_chatter = 0

    def _load(self, ctx: ReflexContext) -> float:
        foot = ctx.contacts.get("foot")
        if foot is None or not foot.active:
            return 0.0
        return float(foot.normal_force)

    def _neighbor_took_load(self, ctx: ReflexContext) -> bool:
        loads = np.asarray(ctx.neighbor_loads, dtype=float)
        return bool(loads.size and np.any(loads >= self.neighbor_accept_min))

    def update(self, ctx: ReflexContext) -> ReflexOutput:
        load = self._load(ctx)
        phi = float(ctx.phase) % (2.0 * np.pi)
        in_liftoff = self.phi_lo < phi <= self.phi_hi
        now = float(ctx.t)

        if self._holding:
            # защита от вечности
            if now - self._hold_start >= self.max_hold_time:
                self._release(now)
                return ReflexOutput()
            if not ctx.stance:
                self._release(now)
                return ReflexOutput()
            # разгрузилась И сосед принял -> swing разрешаем
            if load < self.release_load_max and \
                    self._neighbor_took_load(ctx):
                self._release(now)
                return ReflexOutput()
            out = ReflexOutput()
            out.phase_hold = True
            out.inhibit_swing = True
            out.active = True
            out.reasons = ("R4_LOAD_HOLD",)
            return out

        # вход в hold: конец stance, нога реально несёт массу
        if (ctx.stance and in_liftoff and load >= self.hold_load_min
                and now - self._last_release_t >= self.hold_cooldown):
            self._holding = True
            self._hold_start = now
            self.n_holds += 1
            if now - self._last_release_t < self.chatter_window:
                self.n_chatter += 1
            out = ReflexOutput()
            out.phase_hold = True
            out.inhibit_swing = True
            out.active = True
            out.reasons = ("R4_LOAD_HOLD",)
            return out
        return ReflexOutput()

    def _release(self, now: float) -> None:
        self._holding = False
        self.n_releases += 1
        if self._hold_start >= 0:
            self.hold_ms.append(1000.0 * (now - self._hold_start))
        self._hold_start = -9.0
        self._last_release_t = now

    def reset(self) -> None:
        self._holding = False
        self._hold_start = -9.0
        self._last_release_t = -9.0
        self.n_holds = 0
        self.n_releases = 0
        self.hold_ms = []
        self.n_chatter = 0
