---
title: ARGOS-MUKHTAR Lab
emoji: 🐜
colorFrom: indigo
colorTo: green
sdk: gradio
sdk_version: 6.28.0
python_version: '3.12'
app_file: app.py
pinned: false
license: apache-2.0
short_description: Insect neural circuits on a six-legged body
---

# ARGOS-MUKHTAR Lab

Мухтар — стенд, где конкретные нервные цепи насекомого можно включить,
отключить, нарушить и проверить, что они реально меняют в поведении
шестиногого тела.

ARGOS-MUKHTAR is an embodied connectome testbed that connects anatomically
identified insect neural circuits to a simulated six-legged body and measures
their causal contribution to behavior.

## Что внутри

- **▶ Locomotion** — настоящий MuJoCo-прогон на сервере Space длительностью
  2–20 секунд: flat / 12-mm foot-catch / 20-mm gap / rough 4–10 mm × BASE / R1b / R3 v2 /
  combined / R4. Метрики и графики строятся из нового расчёта; ZIP содержит
  XML сцены, sampled qpos/qvel/позиции стоп, события, summary и manifest SHA256.
  Сохранённая матрица schema 2 доступна отдельно.
- **⚡ Reflex Bench** — 12-mm foot trap: BASE 0.486 м (stuck) vs R1b
  foot-catch 1.238 м (passed), timeline триггеров.
- **🧠 MaleCNS CPG** — interactive-lite: изолированный модуль T1-L
  (DgR/E1/E2/I1/I2, LIF) с knockout на сервере Space + сохранённые
  прогоны (normal/KO×6 × drive 0.4–1.6). KO_E1 — генератор умер;
  KO_I1 — ритм остался; KO_I1I2 — E-клетки в тоническом насыщении.
- **🧠 PRC** — контрольный прогон и 12 однотиковых импульсов в выбранную
  клетку. Измеряется сдвиг первого следующего burst, положительный знак —
  задержка. JSON содержит все растры, pulse ticks, контрольные onset и протокол.
  При отсутствии устойчивого ритма возвращается `invalid_rhythm`.
- **📊 Benchmarks** — результаты измерений и сырые JSONL-логи (View raw).
- **📈 Roadmap** — история версий с честными статусами
  (confirmed/experimental/failed/deprecated).
- **🎮 ARC** — настоящий офлайн-движок ARC-AGI-3 и пять локальных игр.
  Search-агент и отдельно replay известного LS20-маршрута, реальные кадры,
  действия, уровни и финальное состояние, ZIP с данными и SHA256. Replay
  не считается самостоятельным решением или нейронным результатом.
- **👁 Vision** — работающий анализ трёх записанных optic-lobe экспериментов,
  графики fly/twin/baselines и исходные файлы. Это измерения untrained conversion,
  не включённая в походку камера и не повторный запуск checkpoint.
- **🧪 Neural records** — проверенные по SHA256 записи B09 shadow, T2 steering,
  olfaction и Central Complex; графики, структуры результатов и скачивание.

## Проверенные данные схемы 2

Сохранённая таблица Locomotion и Reflex Bench читают `data/schema2/`: девять 20-секундных
прогонов на исходниках `62ce2a97eb44c3a06cdd4172591eb2e724684bbc`, Python
3.11.16, NumPy 2.4.6, MuJoCo 3.14.0, seed 42. Manifest содержит SHA256
кода, точных XML-сцен и сырых JSONL. При чтении проверяется целостность файлов.

Счётчики разделяют начала эпизодов и активные тики. Ложные срабатывания
оцениваются только на ровном полу; для ловушки и ямы показано «не оценено».
Просадка разделена на пиковую и конечную, наклон считается по вертикали тела.
Для ямы 20 мм пиковая просадка BASE/R3v2 — 156.0/24.6 мм; это другая
метрика, чем прежняя конечная просадка 152/19 мм.

Все файлы доступны в dataset: [schema 2](https://huggingface.co/datasets/AvaSiG/MUKHTAR-Bench/tree/main/runs/2026-09-27-schema2).
Исторические данные и CPG-артефакты сохранены отдельно. Эти прогоны не
используют нейронный checkpoint; исторический JSONL содержит только события
рефлексов. Живой запуск дополнительно записывает кинематику с шагом 50 мс.

## Данные

- Model repo: [AvaSiG/ARGOS-MUKHTAR](https://huggingface.co/AvaSiG/ARGOS-MUKHTAR)
- Dataset: [AvaSiG/MUKHTAR-Bench](https://huggingface.co/datasets/AvaSiG/MUKHTAR-Bench)
- GitHub (код): [winargos42-dotcom/argos, проверенные метрики и Space](https://github.com/winargos42-dotcom/argos/tree/codex/mukhtar-bench-metrics-20260927/mukhtar-lab)

## Локальный запуск и сборка

Нужен Python 3.12+ (требование ARC SDK). Из `mukhtar-lab/`: установите `space/requirements.txt`, затем запустите
`python space/app.py`. Полная автономная сборка для HF:
`python space/stage_space.py --out /new/space-directory`.
Она переносит точные runtime-исходники и XML из этого checkout; старые
абсолютные пути `/opt/argos-roach` для live-прогона не используются.

Одновременно выполняется один MuJoCo/PRC/ARC запрос, очередь ограничена восемью.
ARC запускается в отдельном процессе: OFFLINE SDK, сетевые обращения запрещены,
не больше 400 действий и 75 секунд на запрос. Игры включены с MIT notice.
Временные рабочие файлы удаляются после расчёта; скачиваемые файлы и графики
хранятся в кеше Gradio с очисткой каждый час для файлов старше часа.
Живой MuJoCo использует аналитические контроллеры. PRC — изолированные пять
клеток T1-L с BASE-весами; это не полный MaleCNS и не нейронное управление телом.
