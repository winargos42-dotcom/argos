"""reflexes/r3_searching.py — R3 searching v2 (AMOS II prediction error).

Поверх базы Севы. Детектор без изменений (expected − actual,
интегратор); РЕАКЦИЯ переделана (фикс 27.09):

    ожидался touchdown + контакта нет + prediction_error держится
        → SEARCH_ACTIVE:
            1. фазу НЕ замораживать;
            2. фазу замедлить (speed_scale = phase_scale, 0.35 nominal);
            3. femur постепенно опускать (depress_step за тик,
               лимит max_depress);
            4. timeout 150–300 мс (search_timeout=0.25);
            5. контакт найден → recovery: сразу nominal;
            6. timeout → отменить search, краткий retract-lift
               (безопасный swing) + cooldown до нового поиска.

Принцип: R3 даёт ноге дополнительное время на поиск опоры, но не
останавливает локомоторную динамику (никакого вечного phase_hold).

Армирование: нога получила валидный ground-contact И >= 2 соседних
ног под нагрузкой — стартовые миллиметры «в воздухе» не считаются
потерей foothold.

Отклонение от decay-спеки: интегратор сбрасывается в 0 при контакте,
а не тлеет (измерено: decay копил ошибку через циклы).
"""

from __future__ import annotations

import numpy as np

from .base import ReflexContext, ReflexOutput


class R3SearchingReflex:
    def __init__(self, *,
                 error_threshold: float = 0.20,
                 phase_scale: float = 0.35,
                 depress_step: float = 0.0015,
                 max_depress: float = 0.15,
                 search_timeout: float = 0.25,
                 retract_time: float = 0.10,
                 retract_lift: float = 0.10,
                 cooldown: float = 0.30,
                 ground_force_min: float = 0.02,
                 min_neighbor_loads: int = 2,
                 neighbor_load_min: float = 0.05):
        self.thr = float(error_threshold)
        self.phase_scale = float(phase_scale)
        self.depress_step = float(depress_step)
        self.max_depress = float(max_depress)
        self.search_timeout = float(search_timeout)
        self.retract_time = float(retract_time)
        self.retract_lift = float(retract_lift)
        self.cooldown = float(cooldown)
        self.ground_force_min = float(ground_force_min)
        self.min_neighbor_loads = int(min_neighbor_loads)
        self.neighbor_load_min = float(neighbor_load_min)
        self.integral = 0.0
        self._ground_seen = False
        # жизненный цикл
        self._search_until = -9.0
        self._search_start = -9.0
        self._retract_until = -9.0
        self._last_search_end_t = -9.0
        # метрики
        self.t_first_search = None
        self.n_searches = 0
        self.search_total = 0.0
        self.ground_found = False

    @property
    def armed(self) -> bool:
        return self._ground_seen

    def _arm(self, ctx: ReflexContext) -> bool:
        foot = ctx.contacts.get("foot")
        if (not self._ground_seen and foot is not None and foot.active
                and foot.kind == "floor"
                and foot.normal_force >= self.ground_force_min):
            self._ground_seen = True
        if not self._ground_seen:
            return False
        loads = np.asarray(ctx.neighbor_loads, dtype=float)
        supporting = int(np.count_nonzero(loads >= self.neighbor_load_min))
        return supporting >= self.min_neighbor_loads

    def _actual(self, ctx: ReflexContext) -> float:
        foot = ctx.contacts.get("foot")
        return 1.0 if (foot is not None and
                       (foot.active or foot.normal_force > 0.05)) else 0.0

    def update(self, ctx: ReflexContext) -> ReflexOutput:
        now = float(ctx.t)
        if not self._arm(ctx):
            self.integral = 0.0
            return ReflexOutput()
        actual = self._actual(ctx)
        expected = float(ctx.expected_contact)
        error = expected - actual
        if error > 0:
            self.integral += error * ctx.dt
        else:
            self.integral = 0.0

        # 6. timeout-retract: короткий lift, фаза свободна
        if self._retract_until > 0 and now < self._retract_until:
            out = ReflexOutput()
            out.joint_delta[1] += self.retract_lift
            out.active = True
            out.reasons = ("R3_SEARCH_TIMEOUT_RETRACT",)
            return out
        self._retract_until = -9.0

        # SEARCH_ACTIVE
        if self._search_until > 0 and now < self._search_until:
            if actual == 1.0:
                # 5. контакт найден → recovery, сразу nominal
                self.search_total += now - self._search_start
                self.ground_found = True
                self._search_until = -9.0
                self._last_search_end_t = now
                return ReflexOutput()
            # 1–3. фаза не заморожена, замедлена; femur опускается
            self.search_total += ctx.dt
            out = ReflexOutput()
            out.joint_delta[1] -= self.depress_step
            out.speed_scale = self.phase_scale
            out.active = True
            out.reasons = ("R3_SEARCHING",)
            return out

        # 4. timeout истёк без контакта
        if self._search_until > 0 and now >= self._search_until:
            self._search_until = -9.0
            self._retract_until = now + self.retract_time
            self._last_search_end_t = now + self.retract_time
            out = ReflexOutput()
            out.joint_delta[1] += self.retract_lift
            out.active = True
            out.reasons = ("R3_SEARCH_TIMEOUT_RETRACT",)
            return out

        # начало нового поиска
        if self.integral >= self.thr and now - self._last_search_end_t \
                >= self.cooldown:
            self._search_until = now + self.search_timeout
            self._search_start = now
            if self.t_first_search is None:
                self.t_first_search = now
            self.n_searches += 1
            self.search_total += ctx.dt
            out = ReflexOutput()
            out.joint_delta[1] -= self.depress_step
            out.speed_scale = self.phase_scale
            out.active = True
            out.reasons = ("R3_SEARCHING",)
            return out
        return ReflexOutput()

    def reset(self) -> None:
        self.integral = 0.0
        self._ground_seen = False
        self._search_until = -9.0
        self._search_start = -9.0
        self._retract_until = -9.0
        self._last_search_end_t = -9.0
        self.t_first_search = None
        self.n_searches = 0
        self.search_total = 0.0
        self.ground_found = False
