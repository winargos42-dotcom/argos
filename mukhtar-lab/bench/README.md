# MUKHTAR-Bench v1

Воспроизводимые бенчмарки рефлекторного слоя ARGOS-MUKHTAR
(шестиногий робот, MuJoCo, 6 ног × 3 сустава).

Все прогоны детерминированы (MuJoCo без стохастики), seed=42
декларируется для воспроизводимости. Контроллеры: A (CPGGaitController,
эталонный синус-CPG), Б (SineContactController, контактная обратная
связь), рефлексы поверх Б: R1b foot-catch, R3 v2 searching (AMOS II
prediction error), R4 v2 load-coordination (experimental).

## Файлы

- `summary.json` — агрегат всех прогонов: distance_m, fell, false_events,
  body_drop_mm, min_foot_z_mm, max_tilt_deg, net_progress,
  time_to_first_search_s, search_duration_ms, ground_found, r4_holds, …
- `{bench}_{controller}_events.jsonl` — по строке на событие рефлекса:
  `t, leg, reason, contact_pair, contact_kind, leg_phase, armed,
  cooldown_remaining`.
- `scenarios.md` — геометрии сцен и параметры прогонов.

## Результаты (27.09.2026, нода Coral)

| Bench | Контроллер | distance_m | fell | события |
|---|---|---|---|---|
| B01-flat | BASE | 1.260 | 0 | 0 |
| B01-flat | R1b | 1.260 | 0 | 0 |
| B01-flat | R3v2 | 1.260 | 0 | 0 |
| B01-flat | R4 (exp) | 0.887 | 0 | 10544 (deadlock) |
| B02-footcatch12 | BASE | 0.486 | 0 | 0 (застрял) |
| B02-footcatch12 | R1b | 1.238 | 0 | 9 R1B_FOOT_CATCH |
| B03-gap20 | BASE | 0.939 | 1 | 0 (просадка 152 мм) |
| B03-gap20 | R3v2 | 0.987 | 0 | 1911 (search+retract) |
| B03-gap20 | R1b+R3v2 | 1.190 | 0 | 730 |

## Статусы MUKHTAR-Bench v1

- B01-flat — confirmed (ложных 0 у R1b/R3v2)
- B02-footcatch12 — confirmed (R1b: 0.486 → 1.238, проход)
- B03-gap20 — confirmed (R3 v2: fell 1→0, просадка 152→19 мм)
- B04-rough4_10 — planned
- B05-turn — planned (T2 steering)
- B06-stuck — planned (recovery)
- B07-cpg-ko — материалы готовы (cpg_m0: KO DNg100/E1/E2/I1/I2/I1+I2),
  полноценный bench planned
- B08-cpg-prc — planned (cpg_prc.py на ноде)
- B09-six-cpg — planned (все 6 MaleCNS-модулей)
- B10-looming — future (visual escape, LC16→MDN)

## Известные отрицательные результаты (честно)

- R4 v2 load-hold: deadlock на походке Б (активный lift-off не даёт
  разгрузки до подъёма) — flat 1.26→0.887 м. Не принят в stable.
- R1a tibia-stumble: на текущей геометрии тибия не достаёт до
  препятствий (скан 12–28 мм: 0 контактов); off по умолчанию.
- Global neural metronome + I2 phase reset: хуже baseline (локальная
  пертурбация ноги сбивала всю походку).
