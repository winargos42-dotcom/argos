"""tests/test_flat.py — flat-пол: ноль ложных тревог + контрактные проверки.

Поверх базы Севы (ReflexContext.contacts: Mapping[str, ContactSignal]).
"""

import unittest

import numpy as np

from mukhtar.reflexes import (R1FootCatchReflex, R1StumbleReflex,
                              R3SearchingReflex, mix_reflex_outputs)
from mukhtar.reflexes.base import ReflexContext, ReflexOutput
from mukhtar.sensors.contact_pipeline import ContactSignal

DT = 0.002
N = 2500  # 5 c ходьбы


def _ctx(t, leg, phi, *, foot=False, tibia=False, expected=None):
    foot_sig = ContactSignal()
    if foot:
        foot_sig.active = True
        foot_sig.normal_force = 0.5
        foot_sig.duration_s = 0.1
        foot_sig.kind = "floor"
    tibia_sig = ContactSignal()
    if tibia:
        tibia_sig.active = True
        tibia_sig.duration_s = 0.1
        tibia_sig.kind = "floor"
    swing = float(phi) % (2.0 * np.pi) < np.pi
    return ReflexContext(
        dt=DT, t=t, leg=leg, phase=phi % (2.0 * np.pi),
        swing=swing, stance=not swing,
        contacts={"foot": foot_sig, "tibia": tibia_sig},
        expected_contact=(float(not swing) if expected is None
                          else float(expected)),
        neighbor_loads=np.array([0.5, 0.5, 0.0], dtype=np.float32),
    )


class TestFlatQuiet(unittest.TestCase):
    def setUp(self):
        self.r1a = R1StumbleReflex()
        self.r1b = R1FootCatchReflex(dt=DT)
        self.r3 = R3SearchingReflex()

    def test_no_reflex_on_flat(self):
        """Полный цикл ходьбы по ровному полу: ни одного события."""
        for i in range(N):
            t = i * DT
            phi = (i * 0.1) % (2.0 * np.pi)
            swing = phi < np.pi
            # stance: стопа на земле; swing: в воздухе; тибия всегда чиста
            c = _ctx(t, i % 6, phi, foot=(not swing))
            for out in (self.r1a.update(c), self.r1b.update(c),
                        self.r3.update(c)):
                self.assertEqual(out.reasons, (), f"ложное: {out.reasons}")


class TestContracts(unittest.TestCase):
    def test_joint_delta_arrays_independent(self):
        a = ReflexOutput()
        b = ReflexOutput()
        a.joint_delta[0] = 1.0
        self.assertEqual(b.joint_delta[0], 0.0)

    def test_joint_delta_shape_enforced(self):
        with self.assertRaises(ValueError):
            ReflexOutput(joint_delta=np.zeros(2))

    def test_context_copies_arrays(self):
        pos = np.zeros(3)
        c = ReflexContext(dt=DT, t=0, leg=0, phase=0, swing=True,
                          stance=False, contacts={},
                          foot_pos=pos, joint_pos=pos, joint_vel=pos)
        c.foot_pos[0] = 9.0
        self.assertEqual(pos[0], 0.0)

    def test_mixer_clamps_joint_delta(self):
        a = ReflexOutput(joint_delta=np.array([0.3, 0.5, 0.0]),
                         active=True, reasons=("A",))
        b = ReflexOutput(joint_delta=np.array([0.2, 0.1, 0.9]),
                         active=True, reasons=("B",))
        out = mix_reflex_outputs(
            [a, b], joint_delta_limit=np.array([0.3, 0.4, 0.4]))
        np.testing.assert_allclose(out.joint_delta, [0.3, 0.4, 0.4])

    def test_mixer_rejects_none(self):
        with self.assertRaises(TypeError):
            mix_reflex_outputs([None])

    def test_mixer_reasons_stable_order_dedup(self):
        a = ReflexOutput(active=True, reasons=("R1", "R2"))
        b = ReflexOutput(active=True, reasons=("R2", "R3"))
        out = mix_reflex_outputs([a, b])
        self.assertEqual(out.reasons, ("R1", "R2", "R3"))

    def test_mixer_speed_scale_min(self):
        a = ReflexOutput(speed_scale=0.8)
        b = ReflexOutput(speed_scale=0.6)
        self.assertEqual(mix_reflex_outputs([a, b]).speed_scale, 0.6)
        self.assertEqual(mix_reflex_outputs([a]).speed_scale, 0.8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
