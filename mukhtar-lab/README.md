# ARGOS-MUKHTAR — embodied connectome testbed

Мухтар — стенд, где конкретные нервные цепи насекомого можно включить,
отключить, нарушить и проверить, что они реально меняют в поведении
шестиногого тела (MuJoCo-симуляция, Python 3.11, нода Coral/нода X230).

ARGOS-MUKHTAR is an embodied connectome testbed that connects anatomically
identified insect neural circuits to a simulated six-legged body and measures
their causal contribution to behavior.

## Живая лаборатория

[Space](https://huggingface.co/spaces/AvaSiG/ARGOS-MUKHTAR-Lab) выполняет новые
MuJoCo-прогоны четырёх сценариев, включая rough 4–10 мм, и сохраняет кинематику,
события и происхождение кода в скачиваемый ZIP. PRC запускает контроль и
12 импульсных экспериментов изолированного T1-L. ARC использует настоящий
офлайн-движок пяти игр: поиск и отдельно воспроизведение известного LS20-маршрута.
Нейронный ranker к этим режимам не подключён.

Vision и Neural records показывают исходные записанные эксперименты с проверкой
SHA256; их просмотр не выдаётся за новый запуск нейросети. Подробности,
ограничения и автономная сборка — в [space/README.md](space/README.md).
Для полной Space-сборки нужен Python 3.12; исторические бенчмарки ниже
сохраняют исходное окружение Python 3.11.

Расширенная проверка: [20 прогонов движения, 12 PRC и пять ARC-игр](benchmarks/2026-09-27-full-lab/README.md).
Отдельный [ARC state-action head v2](experiments/arc-head-v2/README.md) исправляет
независимость ranking от состояния. Код, реальные тренировочные данные, веса
и A/B-прогоны сохранены; улучшение прохождения игр пока не показано, поэтому
эта политика остаётся отдельным экспериментом.

[SNN worker v2](experiments/snn-worker-v2/README.md) исправляет направление
рекуррентных импульсов, обход downstream-связей и дубли нейронов. Проверен
на настоящем MaleCNS checkpoint и установлен на Coral отдельно от старого
worker. В пакете сохранены исходники, 16 тестов и сырые сравнения. Это
исправление нейронного расчёта; повышение качества ARC не заявляется.
Пакет опубликован в [HF Model repo](https://huggingface.co/AvaSiG/ARGOS-MUKHTAR/tree/99f90b7c9d6c9b4c2d0c7cc6cdd7764fb1957b74/experimental/snn-worker-v2);
все 15 файлов сверены после загрузки. README внутри пакета сохраняет состояние
на момент эксперимента, до публикации; исходный worker и launcher не заменены.

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
| `bench/`, `space/` | Опубликованный Hermes бенчмарк v1 и Gradio Space; их исторические данные сохранены |
| `benchmarks/2026-09-27-schema2/` | Девять проверенных прогонов с исправленными метриками, raw JSONL, точными XML и manifest SHA256 |

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

Запуск из чистого checkout, без `/opt/argos-roach` и рабочего дерева X230:

```bash
cd mukhtar-lab
python3.11 -m venv /tmp/mukhtar-venv
/tmp/mukhtar-venv/bin/python -m pip install -c bench-constraints.txt -e '.[bench,test]'
/tmp/mukhtar-venv/bin/python -m pytest
/tmp/mukhtar-venv/bin/python fly_bridge/bench_jsonl.py --out /tmp/mukhtar-bench-v1
```

Каталог `--out` должен быть новым: существующие результаты не перезаписываются.
Экспортёр выполняет девять 20-секундных прогонов B01-flat/B02-footcatch12/B03-gap20.
Для короткой проверки: `--scenario B01-flat --controller BASE --duration 1.02`.
Короткая проверка подтверждает запуск, но не является locomotion benchmark.

В `summary.json` находятся агрегаты; `*_events.jsonl` содержит сырые события
рефлексов (не полную кинематическую траекторию). Для каждого сценария сохраняется
точный XML модели. `manifest.json` содержит git revision, dirty-флаг, SHA256
исходников и артефактов, версии Python/NumPy/MuJoCo, seed и длительность.
Состояние `complete` записывается только после завершения всех выбранных прогонов.
Эти контроллеры аналитические: neural checkpoint отсутствует и обозначен `null`.
Seed фиксирует настройку запуска; стохастических входов у текущих сценариев нет.

### Метрики схемы 2

- `reflex_events`/`trigger_count`: число начал эпизодов по рефлексу/ноге/reason.
  `event_active_ticks`/`active_tick_count`: число активных записей, включая
  продолжающийся R4 hold. Это разные величины; `n_searches` остаётся отдельным
  доменным счётчиком R3.
- `false_events`: число начал эпизодов только в flat-проверке с явным условием
  «рефлексы не ожидаются». На препятствиях и ямах значение `null`: сырые события
  сами по себе не устанавливают ложность или полезность.
- `max_tilt_deg`: угол между вертикалью тела и мировой вертикалью; yaw не
  считается наклоном.
- `peak_body_drop_mm`: максимальная просадка после первой секунды стабилизации.
  `final_body_drop_mm`: просадка в конце. Старое `body_drop_mm` сохранено как
  псевдоним конечной просадки.

Исторические цифры выше получены старым кодом. Его `false_events` вне flat
считал все активные записи, а `max_tilt_deg` не был углом. Исторические артефакты
не исправляются задним числом; для сравнений используйте новые прогоны схемы 2
с совпадающими версиями, длительностью и параметрами среды.

Проверенная матрица схемы 2: [результаты и протокол](benchmarks/2026-09-27-schema2/README.md).
Она записана на коммите `62ce2a9`, до объединения с переименованием `package/`
в `mukhtar/`. Этот коммит сохранён в истории ветки для точного воспроизведения.
Locomotion, Reflex Bench и таблица Space читают `space/data/schema2/`, проверяя
SHA256 по manifest. Исторический `space/data/summary.json` сохранён отдельно;
CPG продолжает использовать свои исходные артефакты `space/data/cpg_m0/`.
Просмотр сырых данных ограничен файлами проверенного прогона.

Публикации: HF Space `ARGOS-MUKHTAR-Lab`, dataset `MUKHTAR-Bench`,
model repo `ARGOS-MUKHTAR` (аккаунт AvaSiG).
## Реальная проверка системы — 27.09.2026

Статусы ниже означают именно проверку на текущих файлах X230/Coral-ноды, а не
ожидаемое поведение по статье. Обозначения: **CONFIRMED** — измерено,
**PARTIAL** — работает только часть контура, **FAILED** — проверено и отвергнуто,
**NOT CONNECTED** — артефакт/нейросеть существует, но к телу Мухтара не подключена.

| Контур | Статус | Фактический результат |
|---|---|---|
| Stage1 package | CONFIRMED | свежий прогон на Coral: `38 passed in 0.61s` |
| R1b foot-catch | CONFIRMED | B02 12 мм: BASE 0.486 м → R1b 1.238 м, fell=0 |
| R3 v2 searching | CONFIRMED | B03 gap20: BASE fell=1/drop 152.3 мм → R3v2 fell=0/drop 19.1 мм |
| R4 load-hold | FAILED | flat 1.260→0.887 м; deadlock load↔phase, max hold 402 мс |
| global neural metronome | FAILED | локальный phase reset сбивал ритм всех ног |
| T2 steering | PARTIAL | свежий held-out: mean final dist 0.657 м против fixed 0.765; goal=0/4 |
| Central Complex EPG→PFL | FAILED/INACTIVE | EPG/Delta7/FC2/PFL3/PFL2 = 0 spikes и на синтетике, и на 6400 реальных кадрах |
| Vision optic-lobe | NOT CONNECTED | vision checkpoints/логи есть; locomotion camera→body отсутствует |
| Olfaction MB | NOT CONNECTED | KC/MBON/DAN эксперимент существует; газовый сенсор→робот отсутствует |
| Wings / halteres | NOT IMPLEMENTED | `hexapod.xml` содержит только 18 leg position actuators |

### B09-SHADOW-6CPG — подтверждённый рубеж

Свежий повтор `fly_bridge/b09_shadow.py` на Coral: **PASS**. Controller Б
продолжал вести тело, шесть MaleCNS CPG работали параллельно и не имели доступа
к актуаторам. Все три повтора дали одинаковые периоды и 0 dropout.
| Модуль | период, тики | период при 20 мс/tick | jitter | dropouts |
|---|---:|---:|---:|---:|
| T1-L | 17 | 0.34 с | 0.059 | 0 |
| T2-L | 17 | 0.34 с | 0.059 | 0 |
| T3-L | 18 | 0.36 с | 0.094 | 0 |
| T1-R | 17 | 0.34 с | 0.059 | 0 |
| T2-R | 17 | 0.34 с | 0.059 | 0 |
| T3-R | 20 | 0.40 с | 0.000 | 0 |

Последний burst каждого модуля был на тиках 983–998 из 1000. Межповторный
std периода = 0.0 для всех шести. Свежий CPU замер: 0.275–0.280 мс на тик
для всех 6 модулей; более ранний запуск давал ~0.50 мс/tick, поэтому CPU
считаем диапазоном, а не константой. Body x = 1.266 м во всех трёх повторах.

**Практический вывод:** T3-R примерно на 18% медленнее 0.34-с модулей.
Перед передачей фаз на ноги требуется либо per-leg drive calibration, либо
мягкая межлапная синхронизация. Жёсткий общий метроном запрещён результатом M6.

### M5 BASE/TRAINED — свежая проверка drive=0.8

Все 6 подграфов осциллируют и на BASE, и на TRAINED. I2 — доминирующий
тормозной пул во всех 6 модулях в этой конкретной реализации. TRAINED не
делает модули изохронными: например T1-L 12.00 ticks, T1-R 10.89,
T2-L 21.94, T3-R 22.18. Поэтому «одинаковый DNg drive = одинаковая
скорость всех ног» неверно.

Исправленный burst-based PRC остаётся каноническим: baseline ~18 ticks;
I2 pulse даёт сильный фазозависимый сдвиг, E1 pulse слабее на большинстве
фаз. Старый PRC по отдельным E1-spike ISI с P≈8.9 ticks не использовать
как фазу CPG — это другой детектор события.
## Что из «биологических ядер» реально работает сейчас

### Central Complex / steering

Популяции EPG, Delta7, FC2, PFL3 и PFL2 найдены и сопоставлены с индексами,
но функционально текущий тракт не активирован. На сетке Δθ от -180° до +180°
все пять популяций дали ровно 0 spikes. Контрольная сеть при этом не полностью
молчит: global fraction spiking ≈0.0003. На 6400 реальных teacher-кадрах
EPG/Delta7/FC2/PFL3/PFL2 также дали 0 spikes при global mean ≈0.00206.

Следствие: PFL3/PFL2 сейчас нельзя ставить в реальный steering loop.
Следующий научный тест CX — прямое контролируемое возбуждение ER/EPG,
проверка появления локального bump, затем perturb/KO и только после этого PFL.

T2 micro-MLP остаётся инженерным steering fallback. Свежий closed-loop
held-out прогон: teacher mean final distance 0.518 м, fixed 0.765 м,
T2 0.657 м; falls=0 у всех, goal rate=0/4. T2 уменьшает ошибку относительно
нулевого steering, но пока не решает навигацию и не считается заменой CX.

### Vision

На ноде есть `vision_v4_step14580_frozen_day30.pt` и полный trained export,
но камера ещё не замыкает контур на тело Мухтара. Старые изолированные
optic-lobe проверки честно смешанные: MNIST fly=0.874 против raw pixels=0.882,
random projection=0.899, twin=0.905; looming fly=0.290 против pixels=0.840
и twin=0.536; parallax fly=0.4175 выше pixels=0.3263/random=0.3463, но
ниже twin=0.600. Поэтому «готовое зрение Мухтара» пока не заявляется.

### Olfaction

На MaleCNS есть проверенный mushroom-body стенд: 4064 Kenyon cells, 97 MBON,
340 DAN и 61,210 KC→MBON synapses, пять seed-прогонов odour-conditioning.
Это доказательство доступного обучаемого MB-контура, но не работающий нюх
робота: BME688/MQ/виртуальный plume ещё не подключён к ORN/PN/LH→steering.

### Wings / flight

В текущем `models/hexapod.xml` нет wing/haltere/rotor/flight actuator:
только 18 position actuators ног. Следовательно Tarsal Inhibition, wing CPG,
GF takeoff и haltere/IMU stabilization — пока архитектурные кандидаты,
а не реализованные функции Мухтара.
## Архитектурные правила после проверок

1. **Никакого глобального neural metronome.** Каждая нога получает свой
   CPG state; межлапная координация допускается только как слабая модуляция.
2. **Никакого hard load→phase_hold на Controller Б.** R4 v2 доказал deadlock.
   Нагрузка может непрерывно менять dφ/dt или входной ток локального CPG,
   но не ждать разгрузки, одновременно запрещая lift-off.
3. **I2-доминантность — факт нашего MaleCNS, не универсальный закон.**
   Connectome-simulation MANC выделяет E1/E2/I1, FANC — E1/E2/I2+E3.
4. **MDN/GF не равны «поворот фазы на π».** Биология подтверждает backward
   walking / escape, а конкретное воздействие на наши 6 CPG надо измерять.
5. **Connectome topology — inductive bias, не готовая динамика.** FlyGM
   показывает пользу directed message-passing graph для embodied learning,
   но это инженерная модель, а не доказательство того, что биологический
   MaleCNS работает как обычный GNN.
6. Каждый новый biological module обязан пройти:
   anatomy → isolated activity → stimulus-response → KO/ablation →
   recovery/rescue → body A/B → combined regression.

## Следующий порядок бенчей

- **B09-A SHADOW-6CPG — DONE/PASS.**
- **B09-B CALIBRATE-6CPG:** подобрать DNg drive_i, чтобы периоды шести модулей
  совпали в заданном диапазоне без изменения весов.
- **B09-C NEURAL-PHASE-BODY:** заменить только источник фазы Controller Б:
  neural φ_i → прежняя проверенная q_nominal(φ_i); reflexes OFF.
  Сравнение с BASE на flat, seeds/initial phases фиксированы.
- **B09-D LOCAL-PRC:** только после стабильного B09-C: локальный E1-vs-I2
  pulse на одной ноге, остальные пять не должны получать reset.
- **B09-E LOAD-MOD:** непрерывная load→drive/phase-rate modulation; hard hold
  запрещён. Сначала flat, потом gap20.
- **B05-T2:** оставить контрольным steering baseline.
- **B11-CX-BUMP:** ER/EPG direct drive → bump → perturb → recovery.
- **B10-LOOMING:** сначала engineering looming→MDN-like reverse; затем
  LC16/LPLC2/GF anatomical substitution.
- **B12-ODOR:** bilateral virtual plume / BME688 → odor motion+gradient cues →
  casting/upwind steering; только потом MB/LH biological substitution.
- **B13-FLIGHT:** начинать только после добавления физики крыльев/винтов и
  отдельного flight safety bench; не привязывать к «все 6 стоп потеряли контакт»
  без отдельного fall/takeoff classifier.
## Научная карта — источники, которые напрямую меняют дизайн

Ниже приоритетный набор работ, который уже используется как инженерные
ограничения. Peer-reviewed и preprint помечены отдельно.

### Connectome / whole-system architecture

- **Berg et al., Cell 2026 — complete MaleCNS** (peer-reviewed):
  https://doi.org/10.1016/j.cell.2026.08.015
  Полный male brain+VNC, sensory→motor flow. Это основной анатомический
  источник для bodyId/type/flow Мухтара.
- **Dorkenwald et al. / FlyWire, Nature 2024 — whole adult brain**:
  https://www.nature.com/articles/s41586-024-07686-5
  Типизация и сравнение cell types; полезно для CX/vision/MB.
- **Takemura/FANC, Nature 2024 — female VNC connectome**:
  https://doi.org/10.1038/s41586-024-07389-x
  Motor-neuron atlas, leg/wing/takeoff circuits.
- **Cheong et al., eLife 2026 — DN→motor organization**:
  https://doi.org/10.7554/eLife.96084
  Walking, flight steering, power generation, coordinated wings+legs.
- **Bates et al., Nature 2026 — distributed brain-and-cord control**:
  https://www.nature.com/articles/s41586-026-10735-w
  Полезно для supervisory loops CX↔DN↔AN и multimodal control.
- **FlyGM, arXiv 2026** (engineering preprint):
  https://arxiv.org/abs/2602.17997
  Connectome как directed message-passing graph; использовать как A/B
  архитектурный baseline против rewired/random graph, не как биологический факт.

### Walking CPG / steering

- **Connectome simulations identify a CPG for fly walking** (bioRxiv 2025,
  preprint): https://doi.org/10.1101/2025.09.12.675944
  E1=IN17A001, E2=INXXX466; MANC core uses I1=IN16B036, FANC variant I2=
  IN19A007 + E3. Поддерживает наш six-module/KO протокол и запрещает
  универсализировать I2.
- **Pires et al., Nature 2024 — head direction→goal steering**:
  https://www.nature.com/articles/s41586-024-07039-2
  PFL3 задаёт sign steering, PFL2 увеличивает gain около anti-goal;
  DNa03/DNa02 — естественный descending bridge.
- **Feng et al., bioRxiv 2024 — central steering circuit** (preprint):
  https://doi.org/10.1101/2024.06.27.601106
  DNa03↔LAL013 top layer, DNa11 intermediate; использовать для разделения
  slow correction и saccadic turn, но помечать как preprint.
### Proprioception / reflexes

- **Lee et al., Nature Communications 2025 — FeCO circuits**:
  https://www.nature.com/articles/s41467-025-59302-3
  claw=position, hook=movement, club=vibration/exteroception; основа R7.
- **Pratt et al., Nature Communications 2026 — CxHP8 limit detectors**:
  https://www.nature.com/articles/s41467-026-69333-z
  CxHP8 возбуждает движение от anterior coxa limit и тормозит движение к
  пределу; прямой шаблон для R6.
- **Fukuhara et al., Frontiers Neurorobotics 2022 — active load sensing**:
  https://doi.org/10.3389/fnbot.2022.645683
  Важен как идея decentralized support, но наш R4 доказал, что бинарный
  stance hold нельзя переносить буквально на активный lift-off Controller Б.

### Vision / navigation / escape

- **Wolff et al., Nature 2024 — visual features for navigation**:
  https://www.nature.com/articles/s41586-024-07967-z
  ER→EPG visual heading pathway; шаблон для B11-CX-BUMP после оживления EPG.
- **LC16→MDN, Current Biology 2017**:
  https://pubmed.ncbi.nlm.nih.gov/28238656/
  LC16/MDN необходимы для visually evoked retreat; основа B10 reverse.
- **LPLC2+LC4→Giant Fiber, Current Biology 2019**:
  https://doi.org/10.1016/j.cub.2019.01.079
  LPLC2 кодирует looming size, LC4 speed; отдельный fast escape channel.
- **NeuroMechFly v2, Nature Methods 2024/2025**:
  https://www.nature.com/articles/s41592-024-02497-y
  Готовые embodied patterns: vision-following, odor-taxis, hybrid locomotion;
  использовать как reference environment и regression inspiration.

### Olfaction

- **Sensorimotor transformation underlying odor-modulated locomotion,
  Nature Communications 2023**:
  https://www.nature.com/articles/s41467-023-42613-8
  ORN/PN/LH signals modulate several motor parameters; не сводить нюх к одному dC/dt.
- **Odour motion sensing enhances navigation, Nature 2022**:
  https://www.nature.com/articles/s41586-022-05423-4
  bilateral temporal correlations между антеннами дают direction cue.
- **Fly navigational responses exploit plume-specific gradient/motion cues,
  2026**: https://pubmed.ncbi.nlm.nih.gov/42446985/
  В smooth plume важнее gradient, в complex plume — odor motion. Поэтому B12
  должен иметь минимум два plume режима, а не один universal casting rule.

### Flight / wings / halteres

- **Verbe et al., Current Biology 2024 — multifunctional haltere**:
  https://doi.org/10.1016/j.cub.2024.06.066
  Haltere feedback активно регулируется и участвует в saccades; IMU-loop
  должен быть feedback controller, а не просто «гироскоп → мотор».
- **Dhawan et al., Current Biology 2026 — flight-control connectivity atlas**:
  https://doi.org/10.1016/j.cub.2025.12.024
  Карта haltere campaniform afferents→wing motor circuits; основа будущего B13.
- **Lesser et al./FANC, Nature 2024 — leg/wing premotor architecture**:
  https://doi.org/10.1038/s41586-024-07600-z
  Leg premotor networks модульны; wing steering architecture отличается и
  не должна моделироваться копией leg CPG.
## Артефакты независимой проверки

- `verification/b09_shadow_results.json` — свежие 3 повторения six-CPG shadow.
- `verification/t2_closed_fresh.txt` — свежий T2 held-out closed loop.
- `verification/cc_activity.json` — synthetic Δθ scan EPG/Delta7/FC2/PFL3/PFL2.
- `verification/cc_real_control.json` — те же CX-популяции на 6400 real frames.
- `verification/vision_phase0_rec20.json` — untrained optic-lobe encoder benchmark.
- `verification/vision_depth_looming.json` — looming benchmark.
- `verification/vision_depth_parallax.json` — parallax benchmark.
- `fly_bridge/b09_shadow.py` — воспроизводимый shadow harness.

Правило публикации: README не повышает статус результата. `CONFIRMED` появляется
только после сохранённого A/B или causal probe. Отрицательные результаты
(R4 deadlock, global metronome, silent CX) сохраняются наравне с удачными.
### B09-B calibration hypothesis (ещё не PASS)

Грубая линейная интерполяция BASE M5 drive-sweep к общей цели 17.5 neural
ticks даёт стартовые DNg drive-кандидаты:
`T1L≈0.891, T2L≈0.666, T3L≈0.787, T1R=0.400, T2R≈0.886, T3R=1.200`.
Это только initial guess: период нелинеен и местами насыщается. Следующий
изолированный probe обязан прогнать эти значения минимум 3 раза и измерить
period/jitter/dropout до подключения фаз к телу.
Olfaction MB, 5-seed проверка step2948: mean test accuracy =
`frozen 0.4699`, `backprop 0.7070`, `DAN-per-MBON 0.6902`,
`real DAN wiring 0.6691`, `global reward 0.6395`. Эти числа относятся к
синтетическому odour-conditioning тесту, а не к поиску источника газа телом.
Raw seed-файлы сохранены в `verification/olfaction_mb_seed0..4.json`.
