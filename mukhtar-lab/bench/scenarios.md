# MUKHTAR-Bench: сценарии (геометрии и параметры)

Модель тела: `models/hexapod.xml` (генерируется `models/gen_hexapod.py`),
6 ног × 3 сустава (coxa/femur/tibia) = 18 приводов. MuJoCo 3.14.
Робот стартует с подъёмом корпуса +12 мм.

Контроллеры: freq=1.0 Гц, k_ret=0.30 (ретракция), dt=0.002 с
(управление), симуляция ~20 с, метрики после settle-окна 1.0 с.

## Сцены

### B01 — flat
Ровный пол, трения достаточно для позиционной ходьбы. Контроль ложных
срабатываний: у R1b/R3v2 ожидается 0 событий.

### B02 — footcatch12 (ловушка 12 мм)
Поперечная стена высотой 12 мм (full thickness 4 мм, half-size 0.002),
полная ширина прохода. BASE упирается стопой и застревает (~0.486 м);
R1b foot-catch детектирует устойчивый контакт стопы mid-swing
(≥8 тиков подряд, FOOT_CATCH_MIN_TIME = 8·dt = 16 мс) и делает
lift/retract → нога переносится → проход (~1.238 м).

### B03 — gap20 (яма 20 мм)
Поперечная щель глубиной 20 мм (ширина ~40 мм). BASE теряет опору:
задние ноги проваливаются, корпус проседает на ~152 мм, падение.
R3 v2 (AMOS II prediction error): ожидался touchdown + контакта нет +
ошибка держится → SEARCH_ACTIVE: фаза замедляется (speed_scale 0.35),
femur опускается (depress_step, до 0.15 рад), timeout 0.25 с,
контакт → recovery; timeout → retract-lift 0.1 с, cooldown 0.3 с.
Результат: fell 0, просадка ~19 мм.

## Воспроизведение (нода Coral, /opt/argos-roach)

```bash
cd /opt/argos-roach/fly_bridge
/root/flyenv/bin/python bench_jsonl.py   # пересоздаёт bench_out/
```

Точки врезки рефлексов: `controllers/gait_controller.py` (шаг: фазы →
`_apply_reflex` → `_post_targets` с клипом по joint_range); пакет
`mukhtar/` — reflexes/sensors/telemetry + tests (38/38 pytest).
