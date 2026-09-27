#!/usr/bin/env python3
"""
ARGOS-Roach gait controller module.

GaitController is the SWAPPABLE interface: any neuro-controller can replace the
CPG implementation without touching the simulation harness, as long as it
implements:
    step(t, state) -> np.ndarray[18]   # joint angle targets, rad
    set_command(cmd, t, ttl=None)      # 'GO' | 'STOP' | 'HOLD'
    reset(rng=None)

state dict keys: dt (s), t (s), qpos (18,), qvel (18,), body_pos (3,),
body_quat (4, wxyz), body_angvel (3,), foot_contact (6, 0/1 per leg).

Command / stop policy (fixed rule, test D):
  * 'GO'        : CPG amplitudes ramp in from 0 with smoothstep over T_RAMP s.
  * 'STOP'      : amplitudes decay exponentially (tau_amp = 0.15 s), oscillator
                  frequency decays (tau_om = 0.10 s); targets converge to the
                  standing pose q0. Below amp < 0.005 controller holds q0
                  (standing) until the next command.
  * 'GO' + ttl  : command expires at t_ttl = t + ttl -> automatic smooth stop
                  (same rule as STOP). No unbounded execution of a stale command.

Yaw fix (26.09.2026): the vestibular bias was applied with the per-leg side
sign s, which shifts BOTH sides' feet the same way (a speed trim, not steering).
A yaw moment needs DIFFERENTIAL coxa action: the bias is now added WITHOUT s
(right coxa += bias, left coxa += bias -> right foot back, left foot forward ->
clockwise moment for bias > 0). bias = k_psi*yaw + k_psid*yaw_rate gives
heading stabilization (proportional + damping).

Retracted sweep (26.09.2026): sweep(phi) = cos(phi) + k_ret*sin(2*phi).
The raw +cos profile has zero foot velocity at touchdown (phi=pi), so the
planted foot of the new tripod is dragged forward against the body's motion
(slip) and jerks the body backward. With k_ret > 0 the foot already moves
BACKWARD at touchdown (d/dphi sweep = +2*k_ret at phi=pi, and the foot
x-offset is -L*A*sweep, so x-velocity is negative) and at lift-off, matching
the body's forward speed -> no touchdown jerk, plus a push-off retraction at
the end of stance. sweep and its derivative are continuous across the
phi=0/2pi wrap.

Units: radians, seconds. Joint order per leg: [coxa, femur, tibia], legs 0..5.
"""

import math
import numpy as np

LEG_COUNT = 6
JOINTS_PER_LEG = 3
N_ACT = LEG_COUNT * JOINTS_PER_LEG

# leg numbering: 0 RF, 1 LF, 2 LM, 3 RM, 4 RR, 5 LR ; tripod A={0,2,4}, B={1,3,5}
SIDE = np.array([+1, -1, -1, +1, +1, -1], dtype=float)  # +1 right, -1 left


class GaitController:
    """Abstract interface (swappable module)."""
    def set_command(self, cmd, t, ttl=None):
        raise NotImplementedError

    def step(self, t, state):
        raise NotImplementedError

    def reset(self, rng=None):
        raise NotImplementedError


class CPGGaitController(GaitController):
    """
    CPG: 6 coupled phase oscillators (Kuramoto), tripod gait.
    Oscillator i: dphi_i/dt = omega + K * sum_j sin(phi_j - phi_i - psi_ij)
    Coupling: same-side neighbours psi=0 (in-phase), opposite tripod pairs psi=pi.
    Joint targets (per leg, side sign s):
        coxa  = 0 + s*A_c*sweep(phi)  + bias        # fore-aft sweep (retracted)
        femur = s * (0.8 + A_f * lift(phi))         # lift
        tibia = -s * (1.45 + A_t * lift(phi))       # knee tuck
        lift(phi) = max(0, sin(phi))^2 > 0 during swing (phi in (0, pi)).
    Gait cycle: phi=0 lift-off at back (with backward retraction) -> swing
    back->front while lifted -> touchdown at front with the foot already
    moving backward (retraction, no slip jerk) -> stance sweep front->back.
    Subclass hooks: _update_phases(dt) (rhythm generator) and
    _apply_reflex(state, dt, prev_phases) (feedback; no-op in this class).
    """

    def __init__(self, freq=1.0, a_coxa=0.45, a_femur=0.40, a_tibia=0.42,
                 coupling_k=2.0, t_ramp=1.0, tau_amp=0.15, tau_om=0.10,
                 amp_floor=0.005, k_psi=0.0, k_psid=0.0, k_ret=0.30,
                 tau_yf=0.0, bias_stance=True, a_coxa_legs=None):
        self.omega0 = 2.0 * math.pi * freq
        self.a_coxa, self.a_femur, self.a_tibia = a_coxa, a_femur, a_tibia
        # per-leg coxa amplitude scale (None = 1.0 for all legs)
        self.a_coxa_legs = (np.asarray(a_coxa_legs, dtype=float)
                            if a_coxa_legs is not None else np.ones(LEG_COUNT))
        self.coupling_k = coupling_k
        self.t_ramp, self.tau_amp, self.tau_om = t_ramp, tau_amp, tau_om
        self.amp_floor = amp_floor
        # vestibular yaw stabilization: coxa bias = k_psi * yaw + k_psid * yaw_rate
        self.k_psi, self.k_psid = k_psi, k_psid
        self.k_ret = k_ret
        self.tau_yf = tau_yf          # low-pass filter time constant (0 = off)
        self.bias_stance = bias_stance  # apply yaw bias to stance feet too?
        self._yaw = 0.0
        self._yaw_rate = 0.0
        self._yaw_f = 0.0
        self._yawrate_f = 0.0
        self.F0, self.T0 = 0.8, 1.45  # standing femur / tibia magnitude (rad)
        # coupling pairs: (i, j, psi). Within-tripod pairs in-phase (psi=0),
        # cross-tripod pairs anti-phase (psi=pi). NOTE (26.09.2026 fix): the
        # original list used psi=0 for same-SIDE pairs (0,3),(3,4),(1,2),(2,5),
        # which connect legs in OPPOSITE tripods — a frustrated coupling whose
        # tripod equilibrium is unstable; the phases collapse in ~10-25 s into
        # an all-right vs all-left pattern, which is the root cause of the
        # late-run yaw drift and jerk regime.
        self.pairs = [(0, 2, 0.0), (2, 4, 0.0), (4, 0, 0.0),
                      (1, 3, 0.0), (3, 5, 0.0), (5, 1, 0.0),
                      (0, 1, math.pi), (2, 3, math.pi), (4, 5, math.pi)]
        self.reset()

    # ---------------- interface ----------------
    def reset(self, rng=None):
        self.phases = np.array([0.0, math.pi, 0.0, math.pi, 0.0, math.pi])
        self.omega_eff = self.omega0
        self.amp = 0.0
        self.mode = "hold"          # hold | go | stopping
        self._t_ref = 0.0           # reference time of last command/ramp state
        self._ttl_exp = None
        self._last_targets = np.zeros(N_ACT)
        self._yaw = 0.0
        self._yaw_rate = 0.0
        self._yaw_f = 0.0
        self._yawrate_f = 0.0

    @staticmethod
    def _yaw_from_quat(q):
        w, x, y, z = q[0], q[1], q[2], q[3]
        siny = 2.0 * (w * z + x * y)
        cosy = 1.0 - 2.0 * (y * y + z * z)
        return math.atan2(siny, cosy)

    def set_command(self, cmd, t, ttl=None):
        cmd = str(cmd).upper()
        if cmd == "GO":
            self.mode = "go"
            self._t_ref = t
            self._ttl_exp = (t + ttl) if ttl is not None else None
            self.omega_eff = self.omega0
        elif cmd == "STOP":
            self._begin_stop(t)
        elif cmd == "HOLD":
            self.mode = "hold"
            self.amp = 0.0
            self._ttl_exp = None
            self._t_ref = t
        else:
            raise ValueError(f"unknown command: {cmd}")

    def _begin_stop(self, t):
        self.mode = "stopping"
        self._t_ref = t
        self._ttl_exp = None

    # ---------------- core ----------------
    @staticmethod
    def standing_targets():
        """Standing pose q0 for all 18 joints (rad)."""
        q = np.zeros(N_ACT)
        for leg in range(LEG_COUNT):
            s = SIDE[leg]
            q[3 * leg + 0] = 0.0
            q[3 * leg + 1] = s * 0.8
            q[3 * leg + 2] = -s * 1.45
        return q

    def _update_phases(self, dt):
        """Rhythm generator. Base: Kuramoto-coupled phase oscillators."""
        dphi = np.full(LEG_COUNT, self.omega_eff * dt)
        for i, j, psi in self.pairs:
            d = self.phases[j] - self.phases[i] - psi
            dphi[i] += self.coupling_k * math.sin(d) * dt
        self.phases = (self.phases + dphi) % (2.0 * math.pi)

    def _apply_reflex(self, state, dt, prev_phases):
        """Feedback hook (no-op in the open-loop base controller)."""

    def _post_targets(self, state, targets):
        """Post-target hook for additive limb corrections (no-op in base)."""
        return targets

    def step(self, t, state):
        dt = float(state["dt"])

        # --- command expiry (ttl) -> same smooth stop as explicit STOP ---
        if self.mode == "go" and self._ttl_exp is not None and t >= self._ttl_exp:
            self._begin_stop(t)

        # --- mode state machine ---
        if self.mode == "hold":
            self._last_targets = self.standing_targets()
            return self._last_targets.copy()

        if self.mode == "go":
            # smoothstep ramp-in of amplitude
            x = max(0.0, min(1.0, (t - self._t_ref) / self.t_ramp))
            self.amp = x * x * (3.0 - 2.0 * x)
            self.omega_eff = self.omega0
        elif self.mode == "stopping":
            self.amp *= math.exp(-dt / self.tau_amp)
            self.omega_eff *= math.exp(-dt / self.tau_om)
            if self.amp < self.amp_floor:
                self.mode = "hold"
                self.amp = 0.0
                self._last_targets = self.standing_targets()
                return self._last_targets.copy()

        # --- rhythm update (overridable) + feedback reflex (overridable) ---
        prev_phases = self.phases.copy()
        self._update_phases(dt)
        self._apply_reflex(state, dt, prev_phases)

        # --- vestibular yaw feedback (steering via DIFFERENTIAL coxa bias) ---
        if "body_quat" in state:
            self._yaw = self._yaw_from_quat(state["body_quat"])
            if "body_angvel" in state:
                self._yaw_rate = float(state["body_angvel"][2])
        if self.tau_yf > 0:
            a = dt / self.tau_yf
            self._yaw_f += a * (self._yaw - self._yaw_f)
            self._yawrate_f += a * (self._yaw_rate - self._yawrate_f)
        else:
            self._yaw_f, self._yawrate_f = self._yaw, self._yaw_rate
        bias = self.k_psi * self._yaw_f + self.k_psid * self._yawrate_f

        # --- joint targets ---
        sinp = np.sin(self.phases)
        lift = np.clip(sinp, 0.0, None) ** 2
        sweep = np.cos(self.phases) + self.k_ret * np.sin(2.0 * self.phases)
        q0 = self.standing_targets()
        targets = q0.copy()
        for leg in range(LEG_COUNT):
            s = SIDE[leg]
            # bias NOT multiplied by s: right coxa += bias, left coxa += bias
            # -> differential fore-aft foot shift -> yaw moment (heading control).
            # Optional: apply the bias only while the leg is in SWING (the
            # touchdown point is steered without disturbing planted feet).
            if not self.bias_stance and (self.phases[leg] % (2.0 * math.pi)) >= math.pi:
                bias_leg = 0.0
            else:
                bias_leg = bias
            targets[3 * leg + 0] = (q0[3 * leg + 0]
                                    + s * self.a_coxa * self.a_coxa_legs[leg] * sweep[leg] * self.amp
                                    + bias_leg * self.amp)
            targets[3 * leg + 1] = s * (self.F0 + self.a_femur * lift[leg] * self.amp)
            targets[3 * leg + 2] = -s * (self.T0 + self.a_tibia * lift[leg] * self.amp)
        targets = self._post_targets(state, targets)  # hook: limb reflexes
        self._last_targets = targets
        return targets.copy()

    # ---------------- introspection (for CSV/report) ----------------
    def state_report(self):
        return {
            "mode": self.mode,
            "amp": self.amp,
            "omega_eff": self.omega_eff,
            "phases": np.round(self.phases, 3).tolist(),
        }
