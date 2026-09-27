"""limb_reflexes.py — рефлекторный слой конечностей Мухтара (v0.3).

R1 Stumble/Elevator: контакт тибии/стопы в swing выше локальной плоскости
   опоры -> откат фазы переноса на 20% + подъём + отвод назад, затухание.
R2 Retraction: опорная лапа просела ниже локальной плоскости (яма/щель),
   с подтверждением latch_ms -> заморозка фазы + подъём лапы.
R3 Searching: после touchdown стопа прошла сквозь ожидаемую плоскость без
   контакта -> фаза стоит, контролируемое опускание (предел SEARCH_DOWN_MAX),
   таймаут SEARCH_TIMEOUT -> безопасный возврат (подъём) + событие search_abort.

Ожидаемая высота опоры — ЛОКАЛЬНАЯ ПЛОСКОСТЬ по 3+ опорным стопам
(z = ax+by+c, least squares); при <3 контактов — медиана опорных стоп;
иначе — последний валидный горизонт. Все латчи задаются в МИЛЛИСЕКУНДАХ
и переводятся в секунды (физика не зависит от dt).

Коррекции аддитивные (_post_targets), после чего — clip по joint_range,
если state несёт пределы суставов.
"""
import math

import numpy as np

try:
    from .gait_controller import CPGGaitController, LEG_COUNT, SIDE
    from .contact_reflex import SineContactController
except ImportError:
    from gait_controller import CPGGaitController, LEG_COUNT, SIDE
    from contact_reflex import SineContactController

TWO_PI = 2.0 * math.pi


class LimbReflexMixin:
    """Накладывается на SineContactController (поверх ContactReflexMixin)."""

    def __init__(self, lift_margin=0.02, sink_margin=0.025,
                 stumble_pullback=0.2 * TWO_PI,
                 boost_lift=0.35, boost_retract=0.175, boost_tuck=0.15,
                 tau_reflex=0.30, cooldown=0.5,
                 search_window=0.5,
                 search_delay_ms=30, search_rate=0.12,
                 search_max=0.10, search_timeout_ms=400,
                 sink_confirm_ms=30,
                 r1_mode='pulse',        # 'pulse' (v0.3, контроль)
                                         # | 'integrate' (v0.4, FlyGym)
                 k_inc=4.5, k_dec=2.0, c_max=0.70,
                 r4_load_hold=False,     # v0.4: R4 support-hold
                 r4_speed_scale=0.25,
                 r4_persist_s=0.10,      # R4: низкая опора должна держаться
                 **kw):
        super().__init__(**kw)
        self.r1_mode = r1_mode
        self.k_inc = k_inc                # рад/с: нарастание при утыкании
        self.k_dec = k_dec                # рад/с: возврат при освобождении
        self.c_max = c_max                # предел накопленного подъёма, рад
        self.r4_load_hold = r4_load_hold
        self.r4_speed_scale = r4_speed_scale
        self.r4_persist_s = r4_persist_s
        self._low_support_t = 0.0
        self._c_lift = np.zeros(LEG_COUNT)     # интегратор подъёма R1
        self._r1_active = np.zeros(LEG_COUNT, dtype=bool)
        self._r4_active = False
        self.sink_confirm = sink_confirm_ms / 1000.0   # R2: подтверждение, с
        self.lift_margin = lift_margin          # R1: контакт выше опоры, м
        self.sink_margin = sink_margin          # R2: просадка ниже опоры, м
        self.stumble_pullback = stumble_pullback  # R1: откат фазы, рад
        self.boost_lift = boost_lift            # R1/R2: подъём femur, рад
        self.boost_retract = boost_retract      # R1: отвод coxa назад, рад
        self.boost_tuck = boost_tuck            # R1: подгиб tibia, рад
        self.tau_reflex = tau_reflex            # затухание коррекций, с
        self.cooldown = cooldown                # пауза после триггера, с
        self.search_window = search_window      # R3: окно после π, рад
        self.search_delay = search_delay_ms / 1000.0  # R3: латч, с
        self.search_rate = search_rate          # R3: скорость опускания, рад/с
        self.search_max = search_max            # R3: предел опускания, рад
        self.search_timeout = search_timeout_ms / 1000.0  # R3: таймаут, с
        self.r123_active = False                # станет True при наличии foot_z
        self._boost = np.zeros((LEG_COUNT, 5))  # femur_lift, coxa_retract,
        #                                          tibia_tuck, femur_lower,
        #                                          tibia_extend
        self._last_td_z = np.zeros(LEG_COUNT)   # ожидаемая опора на touchdown
        self._prev_phi = np.zeros(LEG_COUNT)
        self._last_trigger = np.full(LEG_COUNT, -np.inf)
        self._search_t = np.full(LEG_COUNT, np.inf)
        self._search_no_contact = np.zeros(LEG_COUNT)
        self._search_lower = np.zeros(LEG_COUNT)
        self._search_max_lower = np.zeros(LEG_COUNT)
        self._sink_t = np.zeros(LEG_COUNT)
        self._last_horizon_z = 0.0              # последний валидный горизонт
        self._c_lift = np.zeros(LEG_COUNT)      # интегратор подъёма R1
        self._r1_active = np.zeros(LEG_COUNT, dtype=bool)
        self._r4_active = False
        self.reflex_events.update(
            {"stumble": 0, "retraction": 0, "searching": 0,
             "search_found": 0, "search_abort": 0,
             "stumble_clear": 0, "r4_hold": 0})
        self.reflex_telemetry = []

    def reset(self, rng=None):
        super().reset(rng)
        self._boost = np.zeros((LEG_COUNT, 5))
        self._last_td_z = np.zeros(LEG_COUNT)
        self._prev_phi = np.zeros(LEG_COUNT)
        self._last_trigger = np.full(LEG_COUNT, -np.inf)
        self._search_t = np.full(LEG_COUNT, np.inf)
        self._search_no_contact = np.zeros(LEG_COUNT)
        self._search_lower = np.zeros(LEG_COUNT)
        self._search_max_lower = np.zeros(LEG_COUNT)
        self._sink_t = np.zeros(LEG_COUNT)
        self._last_horizon_z = 0.0
        self._c_lift = np.zeros(LEG_COUNT)
        self._r1_active = np.zeros(LEG_COUNT, dtype=bool)
        self._r4_active = False
        self._low_support_t = 0.0
        self.reflex_events.update(
            {"stumble": 0, "retraction": 0, "searching": 0,
             "search_found": 0, "search_abort": 0,
             "stumble_clear": 0, "r4_hold": 0})
        self.reflex_telemetry = []
        self._max_delta_preclip = 0.0
        self._max_delta_postclip = 0.0

    def _telemetry(self, t, leg, kind, detail):
        self.reflex_events[kind] += 1
        self.reflex_telemetry.append(
            {"t": round(t, 3), "leg": int(leg), "kind": kind, **detail})

    # ------------------------------------------------------------------
    def _support_plane(self, fz, contacts, fpos):
        """Локальная плоскость опоры z=ax+by+c по опорным стопам.

        Возвращает (a, b, c, ok). Требуется >=3 опорных стоп в stance.
        """
        idx = [l for l in range(LEG_COUNT) if contacts[l] == 1
               and (self.phases[l] % TWO_PI) >= math.pi]
        if len(idx) >= 3:
            X = np.array([[fpos[l][0], fpos[l][1], 1.0] for l in idx])
            z = np.array([fz[l] for l in idx])
            coef, *_ = np.linalg.lstsq(X, z, rcond=None)
            return coef[0], coef[1], coef[2], True
        return None, None, None, False

    def _expected_z(self, fz, contacts, fpos, leg):
        """Ожидаемая высота опоры в точке стопы (x, y) leg.

        3+ опорных: плоскость. 1-2 опорных: медиана их z.
        Ни одного: последний валидный горизонт.
        """
        a, b, c, ok = self._support_plane(fz, contacts, fpos)
        if ok:
            z = a * fpos[leg][0] + b * fpos[leg][1] + c
            self._last_horizon_z = float(z)
            return float(z)
        planted = [l for l in range(LEG_COUNT) if l != leg
                   and contacts[l] == 1]
        if planted:
            z = float(np.median([fz[l] for l in planted]))
            self._last_horizon_z = z
            return z
        return self._last_horizon_z

    # ------------------------------------------------------------------
    def _apply_reflex(self, state, dt, prev_phases):
        # 1) штатные рефлексы Б (stance_hold, early_touchdown)
        super()._apply_reflex(state, dt, prev_phases)

        if self.mode != "go":
            return
        fz = state.get("foot_z")
        contacts = state.get("foot_contact")
        if fz is None or contacts is None:
            return
        self.r123_active = True
        fz = np.asarray(fz, dtype=float)
        t = float(state.get("t", 0.0))
        fpos = state.get("foot_pos")
        if fpos is None:
            fpos = np.zeros((LEG_COUNT, 3))
        fpos = np.asarray(fpos, dtype=float)

        for leg in range(LEG_COUNT):
            phi = self.phases[leg] % TWO_PI
            prev_phi = prev_phases[leg] % TWO_PI
            c = int(contacts[leg])
            tc = state.get("tibia_contact")
            tibia_hit = bool(tc is not None and int(tc[leg]) == 1)
            settling = bool(state.get("settling", False))
            exp_z = self._expected_z(fz, contacts, fpos, leg)
            # --- ожидаемая опора на touchdown: пересечение π сверху вниз ---
            if prev_phi < math.pi <= phi:
                self._last_td_z[leg] = exp_z

            # --- R1: удар о препятствие во время переноса ---
            # Приоритет: контакт ТИБИИ в swing. Иначе: контакт стопы выше
            # локальной плоскости опоры (не touchdown).
            r1_hit = (tibia_hit
                      or (c == 1 and fz[leg] > exp_z + self.lift_margin))
            if self.r1_mode == 'pulse':
                if 0 < prev_phi < math.pi and r1_hit and not settling \
                        and t - self._last_trigger[leg] > self.cooldown:
                    self.phases[leg] = max(0.0, prev_phi - self.stumble_pullback)
                    self._swing_contact_t[leg] = 0.0  # отменяем snap на опору
                    self._boost[leg, 0] += self.boost_lift
                    self._boost[leg, 1] += self.boost_retract
                    self._boost[leg, 2] += self.boost_tuck
                    self._last_trigger[leg] = t
                    self._telemetry(t, leg, "stumble",
                                    {"foot_z": round(float(fz[leg]), 4),
                                     "tibia": tibia_hit,
                                     "exp_z": round(exp_z, 4),
                                     "phi": round(float(prev_phi), 3)})
            else:
                # v0.4 integrate (FlyGym): пока утыкание — лапа лезет ВЫШЕ,
                # после освобождения — плавный возврат. Snap на опору
                # отменяется, пока утыкание активно.
                if 0 < phi < math.pi and r1_hit and not settling:
                    if phi >= math.pi - 0.02 and prev_phi < math.pi:
                        # super() сделал snap — откатываем, это не touchdown
                        self.phases[leg] = prev_phi
                        self._swing_contact_t[leg] = 0.0
                    if not self._r1_active[leg]:
                        self._r1_active[leg] = True
                        self._telemetry(t, leg, "stumble",
                                        {"foot_z": round(float(fz[leg]), 4),
                                         "tibia": tibia_hit,
                                         "exp_z": round(exp_z, 4),
                                         "phi": round(float(phi), 3)})
                    self._c_lift[leg] = min(self.c_max,
                                            self._c_lift[leg]
                                            + self.k_inc * dt)
                else:
                    if self._r1_active[leg]:
                        self._r1_active[leg] = False
                        self._telemetry(t, leg, "stumble_clear",
                                        {"c_peak_rad": round(
                                            float(self._c_lift[leg]), 4)})
                    if self._c_lift[leg] > 0.0 \
                            and not (0 < phi < math.pi):
                        # затухание только ПОСЛЕ завершения переноса:
                        # найденный клиренс держим до конца свинга
                        self._c_lift[leg] = max(
                            0.0, self._c_lift[leg] - self.k_dec * dt)
                # интегратор -> boost-каналы (без эксп. затухания: значение
                # перезаписывается каждый тик текущей величиной c)
                self._boost[leg, 0] = self._c_lift[leg]
                self._boost[leg, 1] = 0.4 * self._c_lift[leg]

            # --- R2: просадка опорной лапы ниже локальной плоскости,
            #     с подтверждением latch_ms (не один тик) ---
            if math.pi <= phi < TWO_PI and c == 1 and not settling \
                    and t - self._last_trigger[leg] > self.cooldown:
                if fz[leg] < exp_z - self.sink_margin:
                    self._sink_t[leg] += dt
                    if self._sink_t[leg] >= self.sink_confirm:
                        if t - self._last_trigger[leg] < self.hold_max:
                            self.phases[leg] = prev_phases[leg]  # фаза стоит
                        self._boost[leg, 0] += 0.6 * self.boost_lift
                        self._last_trigger[leg] = t
                        self._telemetry(t, leg, "retraction",
                                        {"foot_z": round(float(fz[leg]), 4),
                                         "exp_z": round(exp_z, 4)})
                        self._sink_t[leg] = 0.0
                else:
                    self._sink_t[leg] = 0.0

            # --- R3: поиск опоры после touchdown: стопа прошла СКВОЗЬ
            #     ожидаемую плоскость, а контакта нет (яма) ---
            if (math.pi <= phi < math.pi + self.search_window and not settling
                    and fz[leg] < self._last_td_z[leg] - 0.005):
                if c == 0:
                    self._search_no_contact[leg] += dt
                else:
                    self._search_no_contact[leg] = 0.0
                    if not math.isinf(self._search_t[leg]):
                        dur = t - self._search_t[leg]
                        self._telemetry(t, leg, "search_found",
                                        {"dur_s": round(dur, 3),
                                         "max_lower_rad": round(
                                             float(self._search_max_lower[leg]), 4)})
                        self._search_t[leg] = np.inf
                        self._search_lower[leg] = 0.0
                        self._search_max_lower[leg] = 0.0
                if (self._search_no_contact[leg] >= self.search_delay
                        and math.isinf(self._search_t[leg])):
                    self._search_t[leg] = t
                    self._search_lower[leg] = 0.0
                    self._search_max_lower[leg] = 0.0
                    self._telemetry(t, leg, "searching",
                                    {"foot_z": round(float(fz[leg]), 4),
                                     "exp_z": round(
                                         float(self._last_td_z[leg]), 4)})
                if not math.isinf(self._search_t[leg]):
                    if t - self._search_t[leg] < self.search_timeout:
                        self.phases[leg] = prev_phases[leg]  # держим фазу
                        self._search_lower[leg] = min(
                            self._search_lower[leg] + self.search_rate * dt,
                            self.search_max)
                        self._search_max_lower[leg] = max(
                            self._search_max_lower[leg],
                            self._search_lower[leg])
                        self._boost[leg, 3] = self._search_lower[leg]
                        self._boost[leg, 4] = 0.5 * self._search_lower[leg]
                    else:
                        # --- безопасный выход: подъём лапы + событие ---
                        dur = t - self._search_t[leg]
                        self._telemetry(t, leg, "search_abort",
                                        {"dur_s": round(dur, 3),
                                         "reason": "timeout",
                                         "max_lower_rad": round(
                                             float(self._search_max_lower[leg]), 4)})
                        self._search_t[leg] = np.inf
                        self._boost[leg, 3] = 0.0
                        self._boost[leg, 4] = 0.0
                        self._boost[leg, 0] += 0.5 * self.boost_lift
                        self._search_lower[leg] = 0.0
                        self._search_max_lower[leg] = 0.0
            else:
                self._search_no_contact[leg] = 0.0

        # --- R4 (v0.4): пока хоть одна нога в поиске — затормозить корпус
        #     и запретить отрыв нагруженным опорным ногам (support-hold,
        #     Fukuhara active load sensing) ---
        if self.r4_load_hold:
            any_search = any(not math.isinf(self._search_t[l])
                             for l in range(LEG_COUNT))
            stable_contacts = sum(1 for l in range(LEG_COUNT)
                                  if int(contacts[l]) == 1
                                  and math.isinf(self._search_t[l]))
            settling_now = t < 0.5
            if not hasattr(self, '_low_support_t'):
                self._low_support_t = 0.0
            if any_search and not self._r4_active:
                self._r4_active = True
                self._r4_reason = 'search'
                self.reflex_events['r4_hold'] += 1
                self._telemetry(t, -1, "r4_hold",
                                {'reason': self._r4_reason,
                                 'stable': stable_contacts})
            elif stable_contacts < 3 and not settling_now:
                # низкая опора должна ДЕРЖАТЬСЯ r4_persist_s, а не
                # мигать один тик на переходе триподы
                self._low_support_t += dt
                if self._low_support_t >= self.r4_persist_s \
                        and not self._r4_active:
                    self._r4_active = True
                    self._r4_reason = 'low_support'
                    self.reflex_events['r4_hold'] += 1
                    self._telemetry(t, -1, "r4_hold",
                                    {'reason': self._r4_reason,
                                     'stable': stable_contacts})
            else:
                self._low_support_t = 0.0
            if not any_search and stable_contacts >= 3:
                self._r4_active = False
            if self._r4_active:
                for leg in range(LEG_COUNT):
                    if (not math.isinf(self._search_t[leg])
                            or int(contacts[leg]) == 0):
                        continue
                    phi_l = self.phases[leg] % TWO_PI
                    if phi_l >= math.pi:
                        self.phases[leg] = prev_phases[leg]  # держим stance

    def _update_phases(self, dt):
        # R4: при активном поиске замедляем ритм всего CPG (корпус не
        # выталкивает CoM за пределы опорного полигона)
        if self.r4_load_hold and self._r4_active:
            dt = dt * self.r4_speed_scale
        super()._update_phases(dt)

    def _post_targets(self, state, targets):
        targets = super()._post_targets(state, targets)
        dt = float(state.get("dt", 0.01))
        t = float(state.get("t", 0.0))
        # экспоненциальное затухание коррекций
        decay = math.exp(-dt / self.tau_reflex)
        self._boost *= decay
        targets = np.asarray(targets, dtype=float)
        before = targets.copy()
        for leg in range(LEG_COUNT):
            s = SIDE[leg]
            b = self._boost[leg]
            targets[3 * leg + 0] += +s * b[1]   # coxa: отвод назад (+s·b:
            #   swing_sign: A(+1): +q=назад; B(-1): -q=назад — проверено)
            targets[3 * leg + 1] += (+s * b[0]  # femur: ПОДЪЁМ (swing_sign:
                                     - s * b[3])   # A: +q↑; B: -q↑ — проверено)
            targets[3 * leg + 2] += (-s * b[2]  # tibia: подгиб (swing_sign:
                                     + s * b[4])   # A: -q↑; B: +q↑ — проверено)
            # покачивание при поиске
            if not math.isinf(self._search_t[leg]):
                targets[3 * leg + 0] += 0.03 * math.sin(TWO_PI * 2.0 * t)
        # --- защита суставов: clip по пределам модели, если state их несёт
        jr = state.get("joint_range")
        delta_preclip = float(np.max(np.abs(targets - before)))
        if jr is not None:
            jr = np.asarray(jr, dtype=float)
            if jr.shape == (18, 2):
                targets = np.clip(targets, jr[:, 0], jr[:, 1])
        delta_postclip = float(np.max(np.abs(targets - before)))
        if not hasattr(self, '_max_delta_preclip'):
            self._max_delta_preclip = 0.0
            self._max_delta_postclip = 0.0
        self._max_delta_preclip = max(self._max_delta_preclip,
                                      delta_preclip)
        self._max_delta_postclip = max(self._max_delta_postclip,
                                       delta_postclip)
        return targets

    def state_report(self):
        rep = super().state_report()
        rep.update(self.reflex_events)
        rep["r123_active"] = self.r123_active
        rep["max_delta_preclip_rad"] = round(
            getattr(self, '_max_delta_preclip', 0.0), 4)
        rep["max_delta_postclip_rad"] = round(
            getattr(self, '_max_delta_postclip', 0.0), 4)
        return rep


class ReflexController(LimbReflexMixin, SineContactController):
    """Б + рефлекторный слой R1/R2/R3 (stumble, retraction, searching)."""


class ReflexV4Controller(LimbReflexMixin, SineContactController):
    """v0.4: R1-интегратор (FlyGym) + R2/R3 + R4 support-hold (Fukuhara).

    Использовать как ReflexController(freq=..., k_ret=...,
    r1_mode='integrate', r4_load_hold=True)."""

    def __init__(self, *a, r1_mode='integrate', r4_load_hold=True, **kw):
        super().__init__(*a, r1_mode=r1_mode,
                         r4_load_hold=r4_load_hold, **kw)
