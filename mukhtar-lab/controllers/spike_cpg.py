#!/usr/bin/env python3
"""
ARGOS-Roach variant C: spike CPG + the SAME contact feedback as variant B.

Rhythm generator: 6 leaky integrate-and-fire (LIF) spiking neurons (one per
leg) wired as a half-center oscillator network:
  - 3 pairs of MUTUAL INHIBITION across tripods: (0,1), (2,3), (4,5) — each
    pair is a half-center; the reciprocal inhibition makes the two tripods
    alternate (antiphase), so the tripod gait EMERGES from the network, not
    from an imposed phase difference.
  - within-tripod mutual excitation (all-to-all, no self) synchronizes the
    3 legs of a tripod.
  - inhibition/excitation are conductance-like synaptic currents with
    exponential decay (tau_inh / tau_exc).
  - a neuron spike of leg i LOCKS the gait: phase_i := 0 (lift-off). The
    spike train therefore sets the gait timing; between spikes the kinematic
    phase advances at omega_lock = 2*pi/T_ema, where T_ema is an EMA of the
    measured inter-spike period — the phase advance rate adapts to the actual
    network period, so the sweep stays smooth (no phase jumps).
  - SELF-inhibition after each spike (adaptation, tau_self) makes each neuron
    fire ONCE per cycle instead of at its fast intrinsic rate; the partner,
    released from inhibition, fires ~half a period later — the reciprocal
    alternation then runs at the network period (~1 Hz), set jointly by
    tau_inh / tau_self / w_inh / w_self.
  - tonic drive scales with omega_eff/omega0, so STOP decays the rhythm.

Intrinsic LIF parameters (tuned: network period ~1.04 s, clean antiphase):
  tau_m=0.20 s, V_rest=-70, V_th=-50, drive=35 (mV-equivalent, intrinsic
  period ~0.17 s — faster than the network so inhibition sets the timing),
  w_inh=50, tau_inh=0.18 s, w_exc=12, tau_exc=0.03 s,
  w_self=80, tau_self=0.30 s (adaptation -> one spike per cycle).

Everything else — command/stop policy, amplitude ramp, vestibular yaw
stabilization (k_psi/k_psid), retracted sweep, contact reflexes
(ContactReflexMixin, same as variant B) — is inherited unchanged, so B vs C
isolates the contribution of the spike rhythm generator.

No packages beyond numpy. CPU cost: 6 neurons x 1 ms substeps — negligible.
"""

import math

import numpy as np

try:  # package import (from controllers.x import ...)
    from .contact_reflex import ContactReflexMixin
    from .gait_controller import CPGGaitController, LEG_COUNT
except ImportError:  # flat import (script dir on sys.path)
    from contact_reflex import ContactReflexMixin
    from gait_controller import CPGGaitController, LEG_COUNT

TRIPOD_A = (0, 2, 4)
TRIPOD_B = (1, 3, 5)
PARTNER = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}  # mutual-inhibition pairs


class SpikeCPGController(ContactReflexMixin, CPGGaitController):
    def __init__(self, freq=1.0, a_coxa=0.45, a_femur=0.40, a_tibia=0.42,
                 t_ramp=1.0, tau_amp=0.15, tau_om=0.10, amp_floor=0.005,
                 k_psi=0.0, k_psid=0.0, k_ret=0.30, hold_max=0.5,
                 swing_touch_eps=0.90, loss_trigger=0.04, snap_early=0.2,
                 touch_trigger=0.02, danger_rp=0.2, danger_z=0.14,
                 danger_vlat=0.09,
                 tau_m=0.20, v_rest=-70.0, v_thr=-50.0, i_tonic=35.0,
                 w_inh=50.0, tau_inh=0.18, w_exc=12.0, tau_exc=0.03,
                 w_self=80.0, tau_self=0.30,
                 **kw):
        # LIF parameters
        self.tau_m = tau_m
        self.v_rest, self.v_thr = v_rest, v_thr
        self.i_tonic = i_tonic
        self.w_inh, self.tau_inh = w_inh, tau_inh
        self.w_exc, self.tau_exc = w_exc, tau_exc
        self.w_self, self.tau_self = w_self, tau_self
        super().__init__(freq=freq, a_coxa=a_coxa, a_femur=a_femur,
                         a_tibia=a_tibia, t_ramp=t_ramp, tau_amp=tau_amp,
                         tau_om=tau_om, amp_floor=amp_floor, k_psi=k_psi,
                         k_psid=k_psid, k_ret=k_ret, hold_max=hold_max,
                         swing_touch_eps=swing_touch_eps,
                         loss_trigger=loss_trigger, snap_early=snap_early,
                         touch_trigger=touch_trigger, danger_rp=danger_rp,
                         danger_z=danger_z, danger_vlat=danger_vlat)
        self.coupling_k = None  # not used by the spike rhythm (introspection only)

    # ---------------- interface ----------------
    def reset(self, rng=None):
        super().reset(rng)
        self.v = np.full(LEG_COUNT, self.v_rest)
        self.s_inh = np.zeros(LEG_COUNT)
        self.s_exc = np.zeros(LEG_COUNT)
        self.s_self = np.zeros(LEG_COUNT)
        # symmetry break: hyperpolarize tripod B so tripod A fires first
        self.v[list(TRIPOD_B)] -= 30.0
        self.spike_count = np.zeros(LEG_COUNT, dtype=int)
        self._t_clock = 0.0
        self._t_ema = 1.0 / max(self.omega0 / (2.0 * math.pi), 1e-9)
        self._last_spike = np.full(LEG_COUNT, np.nan)

    def _tripod_of(self, i):
        return TRIPOD_A if i in TRIPOD_A else TRIPOD_B

    def _update_phases(self, dt):
        self._t_clock += dt
        t = self._t_clock

        # phase advance rate adapts to the measured network period
        omega_lock = 2.0 * math.pi / max(self._t_ema, 1e-9)
        if self.mode == "stopping":
            omega_lock *= self.omega_eff / self.omega0
        self.phases = (self.phases + omega_lock * dt) % (2.0 * math.pi)

        # integrate the LIF network at 1 ms substeps
        drive_scale = self.omega_eff / self.omega0
        nsub = max(1, int(round(dt / 0.001)))
        h = dt / nsub
        for _ in range(nsub):
            self.s_inh *= math.exp(-h / self.tau_inh)
            self.s_exc *= math.exp(-h / self.tau_exc)
            self.s_self *= math.exp(-h / self.tau_self)
            dv = (-(self.v - self.v_rest) + self.i_tonic * drive_scale
                  - self.s_inh + self.s_exc - self.s_self) / self.tau_m
            self.v += dv * h
            fired = np.where(self.v >= self.v_thr)[0]
            for i in fired:
                self.v[i] = self.v_rest
                self.spike_count[i] += 1
                # spike -> lift-off (phase lock) + synaptic events
                self.phases[i] = 0.0
                self.s_inh[PARTNER[i]] += self.w_inh
                self.s_self[i] += self.w_self
                for j in self._tripod_of(i):
                    if j != i:
                        self.s_exc[j] += self.w_exc
                # update the period estimate (reject doublets/transients)
                if not math.isnan(self._last_spike[i]):
                    sample = t - self._last_spike[i]
                    if 0.5 * self._t_ema < sample < 2.0 * self._t_ema:
                        self._t_ema = 0.8 * self._t_ema + 0.2 * sample
                self._last_spike[i] = t

    # ---------------- introspection ----------------
    def state_report(self):
        rep = super().state_report()
        rep.update({
            "v_mean": round(float(np.mean(self.v)), 2),
            "spikes": int(np.sum(self.spike_count)),
            "t_ema": round(self._t_ema, 3),
        })
        return rep
