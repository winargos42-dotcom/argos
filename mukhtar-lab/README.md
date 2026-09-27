# ARGOS-MUKHTAR — embodied connectome testbed (ветка `mukhtar`)

Мухтар — стенд, где конкретные нервные цепи насекомого можно включить,
отключить, нарушить и проверить, что они реально меняют в поведении
шестиногого тела (MuJoCo-симуляция, Python 3.11, нода Coral/нода X230).

ARGOS-MUKHTAR is an embodied connectome testbed that connects anatomically
identified insect neural circuits to a simulated six-legged body and measures
their causal contribution to behavior.

## Структура

| Каталог | Что |
|---|---|
| `mukhtar/` | Модульный рефлекторный пакет Stage 1: `reflexes/` (R1a stumble, R1b foot-catch, R3 v2 searching, R4 load-coordination, mixer, база ReflexContext/ReflexOutput), `sensors/` (ContactPipeline с kind floor/obstacle/self), `telemetry/`, `tests/` (38/38 pytest), `ОТЧЁТ_Stage1.md` |
| `controllers/` | Контроллеры: A = CPGGaitController (эталонный синус-CPG), Б = SineContactController (+contact feedback), В = SpikeCPGController (6-нейронный LIF half-center); `limb_reflexes_FROZEN_v03_filters.py` — замороженный боевой контроллер (sha256 `a8db07c0…6dcde`) |
| `models/` | `hexapod.xml` (6 ног × 3 сустава, 18 приводов) + генератор `gen_hexapod.py` |
| `cpg_m0/` | Изолированный MaleCNS-модуль T1-L: `config.json` (клетки DgR/E1/E2/I1/I2 + рёбра, BASE-веса), raster `*.npz` и метрики `*.json` для normal / KO DNg100 / KO E1 / KO E2 / KO I1 / KO I2 / KO I1+I2 при drive 0.4–1.6. Base checkpoint `male_cns_spikewhale.pt` sha256 `b381422e…f6fb` |
| `fly_bridge/` | Сценарии и бенчи: `stage1_matrix.py` (матрица flat/12мм/gap + event-log), `stage1_regression.py`, `calib_load.py`, `scan_tibia.py`, CPG: `cpg_module_test.py`, `cpg_m5.py`, `cpg_base_vs_trained.py`, `cpg_prc.py`, `base_provenance.py`, история: `foot_catch.py`, `support_loss.py`, `neural_metronome.py` |
| `docs/` | `PROJECT_STATUS.md` (статус ноды 26.09), протоколы диагностики |
| `logs/` | Сырые логи прогонов матрицы/regression (если доступны) |

## Статусы рефлексов (измерено 27.09.2026)

- **R1b foot-catch — confirmed**: 12-мм ловушка BASE 0.486 м (застрял) →
  R1b 1.238 м (прошёл), flat 0 ложных.
- **R3 v2 searching — confirmed**: яма 20 мм BASE fell=1 (просадка 152 мм) →
  R3 v2 fell=0 (просадка 19 мм, 0.987 м). На мелких неровностях выключать.
- **R1a tibia-stumble — experimental/off**: на текущей геометрии тибия не
  достаёт до препятствий (скан 12–28 мм: 0 контактов); польза v1 была
  артефактом tibia↔floor.
- **R4 load-coordination — failed (v2)**: deadlock «hold фазы vs активный
  lift-off» походки Б (flat 1.26→0.887 м); ждёт инверсной схемы или
  6-CPG-этапа.
- **Global neural metronome + I2 phase reset — failed**: локальная
  пертурбация ноги сбивала всю походку (global metronome хуже локальных
  CPG).

## Воспроизведение

Нода: `cd /opt/argos-roach && ./venv/bin/python fly_bridge/stage1_matrix.py`
(X230: тот же пакет в `/home/argos-data/improve/mukhtar/`).
Тесты пакета: `python -m pytest mukhtar/tests/ -q` → 38 passed.

Публикации: HF Space `ARGOS-MUKHTAR-Lab`, dataset `MUKHTAR-Bench`,
model repo `ARGOS-MUKHTAR` (аккаунт AvaSiG).
