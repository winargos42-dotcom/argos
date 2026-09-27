#!/usr/bin/env python3
"""
ARGOS-Roach variant B: sine CPG + contact feedback (step correction reflexes).

The rhythm generator is IDENTICAL to the reference sine CPG
(CPGGaitController, incl. the corrected tripod coupling and the retracted
sweep). This module only adds the ContactReflexMixin, which is shared with
the spike controller (variant C) so that B vs C isolates the rhythm-generator
contribution.

Contact reflexes (per leg, from state["foot_contact"] + body state). The
walker bounces during normal walking (several feet are regularly airborne),
so a raw per-leg contact test fires spuriously; the stance lock is therefore
gated on BODY danger:
  1. Stance lock ("do not lift a leg while the body is losing support"):
     fires only when the BODY is destabilized — |roll| > danger_rp (0.2 rad)
     or |pitch| > danger_rp or body height < danger_z (0.14 m) — AND a leg in
     stance (phi in [pi, 2*pi)) has lost contact for at least loss_trigger s
     (0.08 s). The leg's phase is then frozen (foot stays planted, sweep
     paused) until the danger clears or hold_max (0.5 s) expires. Prevents
     swinging a leg away while the body is tipping (e.g. after a push).
  2. Early-touchdown reflex ("use the ground you found"):
     leg mid-swing (phi in [swing_touch_eps, pi - snap_early)) that touches
     the ground EARLY -> phase snaps to pi (touchdown), starting its stance
     sweep immediately instead of groping in the air. Nominal touchdown
     (contact appearing within snap_early of pi) does NOT fire.
The stop policy (STOP / GO+ttl -> smooth stop to standing pose) is inherited
unchanged from CPGGaitController.
"""

import math

import numpy as np

try:  # package import (from controllers.x import ...)
    from .gait_controller import CPGGaitController, LEG_COUNT
except ImportError:  # flat import (script dir on sys.path)
    from gait_controller import CPGGaitController, LEG_COUNT


class ContactReflexMixin:
    """
    Mixin providing _apply_reflex(state, dt, prev_phases).
    Must be combined with a class that has: self.phases, self.mode,
    and calls _apply_reflex from step() (see CPGGaitController.step).
    """

    def __init__(self, hold_max=0.5, swing_touch_eps=0.90, loss_trigger=0.04,
                 snap_early=0.2, touch_trigger=0.02, danger_rp=0.2,
                 danger_z=0.14, danger_vlat=0.09, **kw):
        super().__init__(**kw)
        self.hold_max = hold_max
        self.swing_touch_eps = swing_touch_eps
        self.loss_trigger = loss_trigger   # sustained no-contact before hold
        self.snap_early = snap_early       # touchdown snap only this early
        self.touch_trigger = touch_trigger  # sustained contact before snap
        self.danger_rp = danger_rp         # |roll|/|pitch| danger threshold
        self.danger_z = danger_z           # body height danger threshold
        self.danger_vlat = danger_vlat     # lateral body-velocity danger
        self._hold_since = np.full(LEG_COUNT, np.inf)
        self._no_contact_t = np.zeros(LEG_COUNT)
        self._swing_contact_t = np.zeros(LEG_COUNT)
        self._prev_body_pos = None
        self.reflex_events = {"stance_hold": 0, "early_touchdown": 0}

    def reset(self, rng=None):
        super().reset(rng)
        self._hold_since = np.full(LEG_COUNT, np.inf)
        self._no_contact_t = np.zeros(LEG_COUNT)
        self._swing_contact_t = np.zeros(LEG_COUNT)
        self._prev_body_pos = None
        self.reflex_events = {"stance_hold": 0, "early_touchdown": 0}

    @staticmethod
    def _roll_pitch_from_quat(q):
        w, x, y, z = q[0], q[1], q[2], q[3]
        sinr = 2.0 * (w * x + y * z)
        cosr = 1.0 - 2.0 * (x * x + y * y)
        roll = math.atan2(sinr, cosr)
        sinp = 2.0 * (w * y - z * x)
        pitch = math.asin(max(-1.0, min(1.0, sinp)))
        return roll, pitch

    def _apply_reflex(self, state, dt, prev_phases):
        contacts = state.get("foot_contact")
        if contacts is None or self.mode != "go":
            return
        t = float(state.get("t", 0.0))
        # body danger: tipped or low
        danger = False
        if "body_quat" in state:
            roll, pitch = self._roll_pitch_from_quat(state["body_quat"])
            if abs(roll) > self.danger_rp or abs(pitch) > self.danger_rp:
                danger = True
        if "body_pos" in state:
            pos = np.asarray(state["body_pos"], dtype=float)
            if self._prev_body_pos is not None and dt > 0:
                vlat = abs(pos[1] - self._prev_body_pos[1]) / dt
                if vlat > self.danger_vlat:
                    danger = True
            self._prev_body_pos = pos.copy()
            if float(pos[2]) < self.danger_z:
                danger = True
        for leg in range(LEG_COUNT):
            phi = self.phases[leg] % (2.0 * math.pi)
            c = int(contacts[leg])
            if phi >= math.pi:
                # stance region: the foot must stay planted
                if c == 0:
                    self._no_contact_t[leg] += dt
                    # sustained loss of support while the body is in danger
                    # -> hold (do not lift the leg)
                    if danger and self._no_contact_t[leg] >= self.loss_trigger:
                        if math.isinf(self._hold_since[leg]):
                            self._hold_since[leg] = t
                            self.reflex_events["stance_hold"] += 1
                        if t - self._hold_since[leg] < self.hold_max:
                            self.phases[leg] = prev_phases[leg]  # stay planted
                else:
                    self._no_contact_t[leg] = 0.0
                    self._hold_since[leg] = np.inf
            elif phi >= self.swing_touch_eps:
                # mid/late swing: EARLY, SUSTAINED ground contact -> finish
                # the swing (a 1-2 step graze during the bouncy walk does not
                # count; real ground contact persists)
                if c == 1:
                    self._swing_contact_t[leg] += dt
                    if (self._swing_contact_t[leg] >= self.touch_trigger
                            and phi < math.pi - self.snap_early):
                        self.phases[leg] = math.pi
                        self._hold_since[leg] = np.inf
                        self._no_contact_t[leg] = 0.0
                        self._swing_contact_t[leg] = 0.0
                        self.reflex_events["early_touchdown"] += 1
                else:
                    self._swing_contact_t[leg] = 0.0
            # phi < swing_touch_eps: lift-off transition (contact 1 -> 0 is
            # normal here) -> no action

    def state_report(self):
        rep = super().state_report()
        rep.update(self.reflex_events)
        return rep


class SineContactController(ContactReflexMixin, CPGGaitController):
    """Variant B: sine CPG + contact reflexes. Same stop policy as A."""

    def __init__(self, hold_max=0.5, swing_touch_eps=0.90, loss_trigger=0.04,
                 snap_early=0.2, touch_trigger=0.02, danger_rp=0.2,
                 danger_z=0.14, danger_vlat=0.09, **kw):
        super().__init__(hold_max=hold_max, swing_touch_eps=swing_touch_eps,
                         loss_trigger=loss_trigger, snap_early=snap_early,
                         touch_trigger=touch_trigger, danger_rp=danger_rp,
                         danger_z=danger_z, danger_vlat=danger_vlat, **kw)
