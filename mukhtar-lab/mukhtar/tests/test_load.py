"""tests/test_load.py — R4 load-based: юнит-контракт + flat-цикл без дребезга.
"""

import unittest

import numpy as np

from mukhtar.reflexes import R4LoadCoordinationReflex
from mukhtar.reflexes.base import ReflexContext
from mukhtar.sensors.contact_pipeline import ContactSignal

DT = 0.002


def _sig(active, force=0.0):
    s = ContactSignal()
    if active:
        s.active = True
        s.normal_force = force
    return s


def _ctx(t, phi, load, neighbors=(), stance=None):
    p = float(phi) % (2.0 * np.pi)
    if stance is None:
        stance = p >= np.pi
    active = load > 0.0
    return ReflexContext(
        dt=DT, t=t, leg=0, phase=p, swing=not stance, stance=stance,
        contacts={"foot": _sig(active, force=load),
                  "tibia": _sig(False)},
        expected_contact=0.0,
        neighbor_loads=np.asarray(neighbors, dtype=np.float32),
    )


class TestR4Contract(unittest.TestCase):
    def setUp(self):
        self.r4 = R4LoadCoordinationReflex()

    def test_hold_in_liftoff_window_under_load(self):
        # конец stance: phi=6.0 рад (343°), нагрузка 4 Н
        out = self.r4.update(_ctx(0.10, 6.0, 4.0))
        self.assertEqual(out.reasons, ("R4_LOAD_HOLD",))
        self.assertTrue(out.phase_hold)
        self.assertTrue(out.inhibit_swing)

    def test_no_hold_mid_stance(self):
        # середина stance: phi=4.5 рад (258°) — окно liftoff позже
        out = self.r4.update(_ctx(0.10, 4.5, 4.0))
        self.assertEqual(out.reasons, ())

    def test_no_hold_in_swing(self):
        out = self.r4.update(_ctx(0.10, 1.0, 4.0, stance=False))
        self.assertEqual(out.reasons, ())

    def test_no_hold_light_load(self):
        out = self.r4.update(_ctx(0.10, 6.0, 0.5))
        self.assertEqual(out.reasons, ())

    def test_release_when_neighbor_took_load(self):
        r4 = self.r4
        r4.update(_ctx(0.10, 6.0, 4.0))
        # разгрузилась + сосед принял -> отпускаем
        out = r4.update(_ctx(0.12, 6.0, 0.3, neighbors=(3.0, 0.0)))
        self.assertEqual(out.reasons, ())
        self.assertEqual(r4.n_releases, 1)

    def test_keep_hold_when_unloaded_but_no_neighbor(self):
        r4 = self.r4
        r4.update(_ctx(0.10, 6.0, 4.0))
        # разгрузилась, но сосед не принял -> держим
        out = r4.update(_ctx(0.12, 6.0, 0.3, neighbors=(0.2, 0.0)))
        self.assertEqual(out.reasons, ("R4_LOAD_HOLD",))

    def test_max_hold_time_releases_forever_hold(self):
        r4 = self.r4
        r4.update(_ctx(0.10, 6.0, 4.0))
        for i in range(int(0.5 / DT)):  # дольше max_hold 0.4 c
            out = r4.update(_ctx(0.12 + i * DT, 6.0, 4.0))
        self.assertEqual(out.reasons, ())
        self.assertEqual(r4.n_releases, 1)


class TestR4FlatCycle(unittest.TestCase):
    def test_no_chatter_in_normal_tripod(self):
        """Нормальная передача нагрузки не должна дребезжать hold/release.

        Модель трипода: в liftoff-окне нагрузка спадает от 4 Н к 0.2 Н
        за 40 мс, сосед в это время принимает (3 Н). Ожидаем: один hold,
        один release, ноль chatter, короткий hold (~40 мс).
        """
        r4 = R4LoadCoordinationReflex()
        t = 0.0
        for i in range(int(0.10 / DT)):  # 100 мс liftoff
            frac = i * DT / 0.10
            load = 4.0 * (1.0 - frac) if frac < 1.0 else 0.2
            neighbors = (3.0 if frac > 0.3 else 0.0, 0.0)
            r4.update(_ctx(t, 6.0, load, neighbors=neighbors))
            t += DT
        self.assertEqual(r4.n_holds, 1)
        self.assertEqual(r4.n_releases, 1)
        self.assertEqual(r4.n_chatter, 0)
        self.assertGreater(len(r4.hold_ms), 0)
        self.assertLess(r4.hold_ms[0], 150.0)  # краткий liftoff-hold


if __name__ == "__main__":
    unittest.main(verbosity=2)
