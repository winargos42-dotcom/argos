"""tests/test_obstacle.py — 12-мм зацеп (R1b), высокие кромки (R1a),
яма (R3 AMOS II).

Поверх базы Севы. Критерии из измерений ноды (27.09): R1b должен
превращать застревание 0.486 м в проход; R3 должен включаться за десятки
мс в яме и молчать на flat.
"""

import unittest

import numpy as np

from mukhtar.reflexes import (R1FootCatchReflex, R1StumbleReflex,
                              R3SearchingReflex)
from mukhtar.reflexes.base import ReflexContext
from mukhtar.sensors.contact_pipeline import ContactSignal

DT = 0.002


def _sig(active, force=0.5, duration=0.0, kind="none"):
    s = ContactSignal()
    if active:
        s.active = True
        s.normal_force = force
        s.duration_s = duration
        s.kind = kind
        s.pair = (f"leg{kind}", "world")
    return s


def _ctx(t, leg, phi, *, foot=False, tibia=False, f_dur=0.0, expected=None,
         swing=None, kind_foot="none", kind_tibia="none",
         neighbor_loads=None):
    p = float(phi) % (2.0 * np.pi)
    if swing is None:
        swing = p < np.pi
    nl = (np.zeros(0, dtype=np.float32) if neighbor_loads is None
          else np.asarray(neighbor_loads, dtype=np.float32))
    return ReflexContext(
        dt=DT, t=t, leg=leg, phase=p, swing=swing, stance=not swing,
        contacts={"foot": _sig(foot, duration=f_dur, kind=kind_foot),
                  "tibia": _sig(tibia, duration=f_dur, kind=kind_tibia)},
        expected_contact=(0.0 if expected is None else float(expected)),
        neighbor_loads=nl,
    )


class TestR1FootCatch(unittest.TestCase):
    """R1b: устойчивый контакт стопы в mid-swing (окно 0.25π..0.75π)."""

    def setUp(self):
        self.r1b = R1FootCatchReflex(dt=DT)

    def test_silent_below_8_ticks(self):
        for i in range(1, 8):
            c = _ctx(i * DT, 0, 0.5 * np.pi, foot=True,
                     f_dur=i * DT)
            self.assertEqual(self.r1b.update(c).reasons, ())

    def test_fires_at_8_ticks(self):
        out = None
        for i in range(1, 20):
            out = self.r1b.update(_ctx(i * DT, 0, 0.5 * np.pi, foot=True,
                                       f_dur=i * DT))
            if out.reasons:
                break
        self.assertEqual(out.reasons, ("R1B_FOOT_CATCH",))
        self.assertAlmostEqual(out.phase_delta, -0.55)
        self.assertGreater(out.joint_delta[0], 0.0)  # retract
        self.assertGreater(out.joint_delta[1], 0.0)  # lift

    def test_silent_outside_window(self):
        for i in range(1, 20):
            for phi in (0.1 * np.pi, 0.9 * np.pi):
                c = _ctx(i * DT, 0, phi, foot=True, f_dur=i * DT)
                self.assertEqual(self.r1b.update(c).reasons, ())

    def test_gated_when_tibia_touches(self):
        """14-мм класс: тибия касается — R1b молчит, работает R1a."""
        for i in range(1, 20):
            c = _ctx(i * DT, 0, 0.5 * np.pi, foot=True, tibia=True,
                     f_dur=i * DT)
            self.assertEqual(self.r1b.update(c).reasons, ())

    def test_cooldown_blocks_repeat(self):
        self.r1b._last_t = -9.0
        first = None
        for i in range(1, 20):
            first = self.r1b.update(_ctx(i * DT, 0, 0.5 * np.pi,
                                         foot=True, f_dur=i * DT))
            if first.reasons:
                break
        self.assertEqual(first.reasons, ("R1B_FOOT_CATCH",))
        # свежий рефлекс, тик после срабатывания: cooldown
        r2 = R1FootCatchReflex(dt=DT)
        r2.update(_ctx(0.5, 0, 0.5 * np.pi, foot=True, f_dur=0.1))
        out = r2.update(_ctx(0.6, 0, 0.5 * np.pi, foot=True, f_dur=0.2))
        self.assertEqual(out.reasons, ())


class TestR1Stumble(unittest.TestCase):
    """R1a: устойчивый контакт голени с ПРЕПЯТСТВИЕМ в swing."""

    def test_fires_on_sustained_obstacle_contact(self):
        r = R1StumbleReflex(duration_threshold=0.03)
        out = r.update(_ctx(0.1, 0, 0.5 * np.pi, tibia=True, f_dur=0.04,
                            kind_tibia="obstacle"))
        self.assertEqual(out.reasons, ("R1A_TIBIA_STUMBLE",))
        self.assertGreater(out.joint_delta[1], 0.0)  # lift
        self.assertLess(out.joint_delta[0], 0.0)     # retract

    def test_silent_on_floor_contact(self):
        """tibia↔floor НЕ запускает R1a (нормальное чирканье)."""
        r = R1StumbleReflex(duration_threshold=0.0)
        out = r.update(_ctx(0.1, 0, 0.5 * np.pi, tibia=True, f_dur=0.04,
                            kind_tibia="floor"))
        self.assertEqual(out.reasons, ())

    def test_silent_on_short_contact(self):
        r = R1StumbleReflex(duration_threshold=0.03)
        out = r.update(_ctx(0.1, 0, 0.5 * np.pi, tibia=True, f_dur=0.01,
                            kind_tibia="obstacle"))
        self.assertEqual(out.reasons, ())

    def test_silent_in_stance(self):
        r = R1StumbleReflex(duration_threshold=0.03)
        c = _ctx(0.1, 0, 4.5, tibia=True, f_dur=0.1, swing=False,
                 kind_tibia="obstacle")
        self.assertEqual(r.update(c).reasons, ())

    def test_correction_held_after_trigger(self):
        """Коррекция держится hold_time, контакт может уже исчезнуть."""
        r = R1StumbleReflex(duration_threshold=0.03, hold_time=0.20,
                            cooldown=0.5)
        r.update(_ctx(0.10, 0, 0.5 * np.pi, tibia=True, f_dur=0.04,
                      kind_tibia="obstacle"))
        out = r.update(_ctx(0.15, 0, 0.5 * np.pi))  # контакта уже нет
        self.assertEqual(out.reasons, ("R1A_TIBIA_STUMBLE",))
        out = r.update(_ctx(0.35, 0, 0.5 * np.pi))  # hold истёк
        self.assertEqual(out.reasons, ())

    def test_cooldown_blocks_new_trigger_not_held_correction(self):
        r = R1StumbleReflex(duration_threshold=0.03, hold_time=0.20,
                            cooldown=0.5)
        # триггер в 0.10
        r.update(_ctx(0.10, 0, 0.5 * np.pi, tibia=True, f_dur=0.04,
                      kind_tibia="obstacle"))
        # 0.30: hold ещё действует — коррекция выполняется (не обнулена)
        out = r.update(_ctx(0.30, 0, 0.5 * np.pi, tibia=True, f_dur=0.04,
                            kind_tibia="obstacle"))
        self.assertEqual(out.reasons, ("R1A_TIBIA_STUMBLE",))
        # 0.35: hold истёк, новый удар — cooldown запрещает ПОВТОРНЫЙ
        out = r.update(_ctx(0.35, 0, 0.5 * np.pi, tibia=True, f_dur=0.04,
                            kind_tibia="obstacle"))
        self.assertEqual(out.reasons, ())
        # 0.70: cooldown (0.5) истёк — новый триггер разрешён
        out = r.update(_ctx(0.70, 0, 0.5 * np.pi, tibia=True, f_dur=0.04,
                            kind_tibia="obstacle"))
        self.assertEqual(out.reasons, ("R1A_TIBIA_STUMBLE",))


class TestR3PredictionError(unittest.TestCase):
    """Яма: нога в stance (контакт ожидается), опоры нет.
    R3 должен включиться ЗА ДЕСЯТКИ мс (не через 4.3 c) — но только
    после армирования (был валидный ground-contact + опора соседей)."""

    def setUp(self):
        self.r3 = R3SearchingReflex(error_threshold=0.10)

    def _arm(self, r3):
        """Пара stance-тиков с валидным ground-контактом + 2 соседа."""
        for i in range(10):
            r3.update(_ctx(i * DT, 0, 4.5, foot=True, swing=False,
                           expected=1.0, kind_foot="floor",
                           neighbor_loads=np.array([0.5, 0.5, 0.0])))

    def _yamactx(self, t, leg=0, foot=False):
        return _ctx(t, leg, 4.5, foot=foot, swing=False, expected=1.0,
                    neighbor_loads=np.array([0.5, 0.5, 0.0]))

    def test_not_armed_silent_even_in_hole(self):
        """Без ground-contact (старт в воздухе) R3 молчит в яме."""
        for i in range(int(2.0 / DT)):
            out = self.r3.update(self._yamactx(i * DT))
            self.assertEqual(out.reasons, ())

    def test_activates_within_tens_of_ms_after_arm(self):
        self._arm(self.r3)
        steps = 0
        out = None
        while steps < 1000:
            steps += 1
            out = self.r3.update(self._yamactx(steps * DT))
            if out.reasons:
                break
        self.assertLessEqual(steps * DT, 0.25)   # десятки-сотни мс
        self.assertEqual(out.reasons, ("R3_SEARCHING",))
        # v2: фаза НЕ заморожена, но замедлена; femur опускается
        self.assertFalse(out.phase_hold)
        self.assertAlmostEqual(out.speed_scale, 0.35)
        self.assertLess(out.joint_delta[1], 0.0)

    def test_timeout_retract_without_contact(self):
        """Яма дольше timeout → поиск отменяется, краткий retract-lift."""
        self._arm(self.r3)
        seen_search = False
        seen_retract = None
        for i in range(int(1.0 / DT)):
            out = self.r3.update(self._yamactx(i * DT))
            if out.reasons == ("R3_SEARCHING",):
                seen_search = True
            if out.reasons == ("R3_SEARCH_TIMEOUT_RETRACT",):
                seen_retract = out
                break
        self.assertTrue(seen_search)
        self.assertIsNotNone(seen_retract)
        self.assertGreater(seen_retract.joint_delta[1], 0.0)  # lift
        self.assertFalse(seen_retract.phase_hold)
        # метрики
        self.assertIsNotNone(self.r3.t_first_search)
        self.assertGreaterEqual(self.r3.n_searches, 1)
        self.assertGreater(self.r3.search_total, 0.0)
        self.assertFalse(self.r3.ground_found)

    def test_recovery_on_contact_during_search(self):
        """Контакт во время поиска → recovery: nominal, ground_found."""
        self._arm(self.r3)
        # запускаем поиск
        for i in range(int(0.30 / DT)):
            out = self.r3.update(self._yamactx(i * DT))
            if out.reasons == ("R3_SEARCHING",):
                break
        self.assertEqual(out.reasons, ("R3_SEARCHING",))
        # контакт появился
        out = self.r3.update(self._yamactx(0.31, foot=True))
        self.assertEqual(out.reasons, ())
        self.assertTrue(self.r3.ground_found)
        # дальше — тишина (nominal)
        for i in range(int(0.2 / DT)):
            out = self.r3.update(self._yamactx(0.32 + i * DT, foot=True))
            self.assertEqual(out.reasons, ())

    def test_quiet_when_contact_matches(self):
        self._arm(self.r3)
        for i in range(int(0.5 / DT)):
            c = self._yamactx(i * DT, foot=True)
            self.assertEqual(self.r3.update(c).reasons, ())

    def test_quiet_during_swing_without_contact(self):
        """В swing контакт НЕ ожидается — отсутствие контакта не ошибка."""
        self._arm(self.r3)
        for i in range(int(0.5 / DT)):
            c = _ctx(i * DT, 0, 0.8, foot=False, expected=0.0,
                     neighbor_loads=np.array([0.5, 0.5, 0.0]))
            self.assertEqual(self.r3.update(c).reasons, ())

    def test_clears_after_contact_restored(self):
        self._arm(self.r3)
        for i in range(int(0.30 / DT)):
            self.r3.update(self._yamactx(i * DT))
        out = self.r3.update(self._yamactx(0.31))
        self.assertEqual(out.reasons, ("R3_SEARCHING",))
        for i in range(int(1.0 / DT)):
            out = self.r3.update(self._yamactx(0.32 + i * DT, foot=True))
        self.assertEqual(out.reasons, ())


if __name__ == "__main__":
    unittest.main(verbosity=2)
