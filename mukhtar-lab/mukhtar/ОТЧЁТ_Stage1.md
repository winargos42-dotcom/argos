# ОТЧЁТ Stage 1 v2 — матрица после двух фиксов (27.09.2026)

## Фиксы (по спеке Севы)
1. **Классификация контактов** (contact_pipeline): ContactSignal.kind =
   floor / obstacle / none (+ pair — имена геомов); kind_by_geom +
   name_reader (с try/except для тестовых фейков); самоконтакты (оба
   геома в geom_map) НЕ попадают в сигналы — логируются отдельно
   (last_self_pairs, self_total).
2. **R1a**: триггер только tibia.kind == "obstacle" в swing (floor и
   self не запускают); жизненный цикл: коррекция УДЕРЖИВАЕТСЯ
   hold_time=0.20 c, cooldown=0.5 c запрещает ПОВТОРНЫЙ триггер, не
   обнуляя выполняющуюся коррекцию.
3. **R3 armed**: спит, пока нога не получила валидный ground-contact
   (foot↔floor, force ≥ 0.02) И >= 2 соседних ног под нагрузкой
   (≥ 0.05). Стартовые 12 мм «в воздухе» не считаются потерей foothold.
4. R1b — НЕ ТРОНУТ (заморожен known-good).

## Тесты: 28/28 (X230 и нода) — его 4 + мои 24.

## Матрица (stage1_matrix.py, нода, MuJoCo 3.14, 20 c)

| прогон | x, м | fell | события | итог |
|---|---|---|---|---|
| FLAT_BASE | 1.260 | 0 | 0 | контроль |
| FLAT_R1B | 1.260 | 0 | 0 | ✓ ложных 0 |
| FLAT_R1A | 1.260 | 0 | 0 | ✓ ложных 0 |
| FLAT_R3 | 1.260 | 0 | 0 | ✓ ложных 0 (armed, max_int 0.13 < 0.2) |
| W12_BASE | 0.486 | 0 | 0 | контроль (застревает) |
| W12_R1B | 1.238 | 0 | R1B ×9 | ✓ проход |
| W12_FULL (+R3) | 1.157 | 0 | R1B ×7, R3 ×32 | ✗ регрессия −0.08 от R1b-only |
| STUCK14_BASE | 1.112 | 0 | 0 | контроль |
| STUCK14_R1A | 1.112 | 0 | 0 | R1A спит (см. скан) |
| GAP_BASE | 0.896 | 0 | 0 | контроль |
| GAP_R3 | 0.344 | 1 | R3 ×323 | ✗ сигнал верный, реакция валит |

## Ключевые факты
- **Flat чистый: 0/0/0/0.** Главная цель двух фиксов достигнута.
- **Скан tibia↔wire (scan_tibia.py): 0 контактов на ВСЕХ высотах
  12–28 мм.** Стена ловится только стопой (foot_wire 1154–2125). У
  текущей геометрии ног физического сценария R1a (tibia↔obstacle) НЕТ.
  «Польза» tibia-R1 в v1 (14 мм: 1.277 против 1.148) была от контакта
  тибии с ПОЛОМ при наклоне корпуса — то есть от неправильной
  классификации, которую мы только что убрали. Теперь R1a честно
  молчит: STUCK14_R1A = STUCK14_BASE = 1.112.
- **Самоконтакты: ~33–34 К за 20 c** (сегменты ног трутся на сгибах) —
  раньше они маскировались под tibia-контакты; теперь в отдельном логе
  (для будущего safety-слоя).
- **R3 в яме срабатывает ВОВРЕМЯ** (323 события, arm работает, интеграл
  до 0.46) — сигнал AMOS-II правильный. Но реакция (phase_hold +
  depress) замораживает фазы и валит робота (0.344, fell=1 против
  BASE 0.896). На ловушке R3 тоже регрессирует (1.157 против 1.238).
  R3 остаётся experimental; следующая итерация — реакция: ограниченный
  поиск (depress с лимитом времени / замедление фазы вместо вечного
  phase_hold).

## R3 v2 — измерено полезен на яме 20 мм (27.09, stage1_matrix.py)

Реакция v2 (по спеке Севы): phase НЕ заморожена → speed_scale=0.35
(замедление приращения фазы ноги); femur опускается depress_step
0.0015 рад/тик (лимит 0.15 рад); search_timeout=0.25 c; контакт →
recovery сразу nominal; timeout → retract-lift 0.10 c + cooldown 0.30 c.

| яма | BASE | R3 v2 | итог |
|---|---|---|---|
| 12 мм | 0.896, fell=0, drop 10.8 мм | 0.609, fell=1 | BASE сам проходит — R3 не нужен, мешает |
| 16 мм | 1.146, fell=0, drop 14.7 мм | — | BASE сам проходит |
| 20 мм | **0.939, fell=1, drop 152.3 мм** | **0.987, fell=0, drop 19.1 мм** | **R3 v2 спасает: падение → проход** |

Метрики R3 v2 на яме 20 мм: time_to_first_search 10.306 c (ровно в яме),
search_duration 1074 мс, n_searches 16, ground_found=true,
net_progress 0.306. Детектор AMOS-II работает: 12-мм яма видна с 9.4 c
(11 поисков, ground_found=true) без изменения поведения (detector-only
= BASE 0.896).

Вывод: R3 v2 — условно полезный рефлекс: спасает там, где опора
реально теряется (BASE падает), мешает там, где пассивная геометрия
справляется сама. Граница на этом теле — глубина ямы ~16–20 мм.

## R4 v2 load-based — измерен DEADLOCK на походке Б (27.09)

Калибровка (calib_load.py, flat-трипод, 10 c): stance Fz mean 3.1–6.4 Н,
stance contact frac 0.62–0.86 до конца stance; swing Fz max 6.8–18 Н.
Пороги R4: hold ≥2.0 Н (окно liftoff 1.7π..2π), release <0.8 Н + сосед
≥2.0 Н, max_hold_time 0.40 c, cooldown 0.15 c.

| прогон | x, м | fell | R4 метрики | итог |
|---|---|---|---|---|
| FLAT_BASE | 1.260 | 0 | — | контроль |
| FLAT_R4 | 0.887 | 0 | holds 108, mean 195 мс, max 402 мс, chatter 0 | ✗ −30% |
| W12_R1B | 1.238 | 0 | — | known-good |
| W12_R1B_R4 | 0.974 | 0 | holds 110, max 402 мс | ✗ регрессия |
| GAP20_R3V2 | 0.987 | 0 | — | спасение |
| GAP20_R1B_R3V2_R4 | 0.813 | 1 | holds 79, max 402 мс | ✗ R4 валит combined |

Диагноз (не пороговый): CPG Б поднимает ногу АКТИВНО в начале swing;
нагрузка спадает ПОСЛЕ отрыва, а не до. R4 держит фазу в ожидании
разгрузки, которой не будет, пока нога не поднимется — deadlock,
снимаемый только страховкой max_hold_time (отсюда max 402 мс и рывки).
Hold-контракт «не уходить в swing, пока несёшь» применим к походкам с
пассивным переносом веса (compliant legs, AMOS II), а не к Б.

Варианты (решение за Севой):
(а) инверсный R4: не блокировать lift-off, а ускорять уход в swing
    уже разгруженной ноги (phase_delta+) — в норме молчит (разгрузки
    до lift-off нет), реагирует только на аномалию;
(б) отложить R4 до 6-CPG-этапа (load-mediated coordination, вариант C
    из A/B/C/D — там фаза модулируется непрерывно, не блокируется).

## Состав Stage 1 (актуальный)
- **R1b — рабочий, заморожен** (12 мм: 0.486 → 1.238, flat чистый).
- **R3 v2 — полезен на реальной потере опоры (яма 20 мм: fell 1→0,
  drop 152→19 мм)**; на мелких неровностях выключать.
- **R1a — experimental/off** (сценария tibia↔obstacle на этом теле нет,
  скан 12–28 мм: 0 контактов).
- **R4 v2 — не принят в stable** (deadlock на походке Б, см. выше);
  ждёт решения по вариантам (а)/(б).
- R6/R7/R9 — следующие этапы, не смешивать.

## Event-log (на каждый триггер)
t, leg, reason, contact_pair, contact_kind, leg_phase, armed,
cooldown_remaining — реализован в Stage1Controller (stage1_matrix.py).

## Точки врезки в контроллер Б (фрагменты для интеграции)
- `controllers/gait_controller.py` step(): prev_phases = copy →
  _update_phases(dt) → _apply_reflex(state, dt, prev_phases) (хук,
  no-op) → targets → _post_targets(state, targets) (хук, no-op).
- swing/stance: phi = phases[leg] % 2π; swing = phi < π.
- `controllers/limb_reflexes.py` _apply_reflex (~173) — фазовые правки;
  _post_targets (~405–440) — аддитивные коррекции таргетов с SIDE-
  знаками + clip по state["joint_range"].
- Каноническая врезка Stage 1 (реализована в stage1_matrix.py):
  pipeline.update(data) в run-цикле → state["leg_contacts"];
  ReflexContext(contacts=leg_contacts[leg], expected_contact=явно);
  mix_reflex_outputs → phase_hold: phases[leg]=prev_phi;
  phase_delta: phases[leg]=max(0, prev_phi+delta);
  joint_delta → q_target = q_nominal + SIDE·delta → clip.

## Следующие шаги
1. R3-реакция v2: ограниченный поиск (depress с таймаутом / замедление
   фазы вместо вечного phase_hold) → gap-тест заново.
2. Этап 2: R4 load-based (Active Load Sensing 2022) вместо аварийного
   support_count.
3. Этап 3: R6/R7 (CxHP8 limit-detector, FeCO claw/hook/club).
4. Этап 4: 6 локальных MaleCNS leg-CPG + local phase-reset.
5. Этап 5: LC16→MDN looming escape.
