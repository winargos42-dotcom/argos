"""reflexes/r1_stumble.py — R1a tibia-stumble (высокие кромки).

Поверх базы Севы. Сигнал: устойчивый контакт ГОЛЕНИ с ПРЕПЯТСТВИЕМ
(kind == "obstacle") в swing. Контакты tibia↔floor и самоконтакты
триггер не запускают — пайплайн классифицирует их отдельно (floor /
self-лог).

Жизненный цикл (фикс 27.09):
- trigger: tibia.kind=="obstacle" and swing and duration >= thr;
- коррекция УДЕРЖИВАЕТСЯ hold_time секунд после триггера (не обнуляется
  посередине выполнения);
- cooldown запрещает ПОВТОРНЫЙ триггер, но не трогает уже выполняющуюся
  коррекцию.
"""

from __future__ import annotations

from .base import ReflexContext, ReflexOutput


class R1StumbleReflex:
    def __init__(self, *,
                 duration_threshold: float = 0.03,
                 max_lift: float = 0.30,
                 max_retract: float = 0.20,
                 hold_time: float = 0.20,
                 cooldown: float = 0.5):
        self.thr = float(duration_threshold)
        self.max_lift = float(max_lift)
        self.max_retract = float(max_retract)
        self.hold_time = float(hold_time)
        self.cooldown = float(cooldown)
        self._held_until = -9.0
        self._last_trigger_t = -9.0

    def cooldown_remaining(self, t: float) -> float:
        return max(0.0, self._last_trigger_t + self.cooldown - t)

    def update(self, ctx: ReflexContext) -> ReflexOutput:
        tibia = ctx.contacts.get("tibia")
        # trigger: голень бьёт ПРЕПЯТСТВИЕ в swing, устойчивый контакт
        hit = bool(ctx.swing and tibia is not None and tibia.active
                   and tibia.kind == "obstacle"
                   and tibia.duration_s >= self.thr)
        if hit and ctx.t - self._last_trigger_t > self.cooldown:
            self._last_trigger_t = ctx.t
            self._held_until = ctx.t + self.hold_time
        if ctx.t <= self._held_until:
            out = ReflexOutput()
            out.joint_delta[1] = self.max_lift
            out.joint_delta[0] = -self.max_retract
            out.active = True
            out.reasons = ("R1A_TIBIA_STUMBLE",)
            return out
        return ReflexOutput()

    def reset(self) -> None:
        self._held_until = -9.0
        self._last_trigger_t = -9.0
