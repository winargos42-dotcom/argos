---
title: ARGOS-MUKHTAR Lab
emoji: 🐜
colorFrom: indigo
colorTo: green
sdk: gradio
sdk_version: 6.28.0
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

- **▶ Locomotion** — MuJoCo-прогоны (исполнены заранее на ноде, здесь —
  результаты): flat / 12-mm foot-catch / 20-mm gap × BASE / R1b / R3 v2.
- **⚡ Reflex Bench** — 12-mm foot trap: BASE 0.486 м (stuck) vs R1b
  foot-catch 1.238 м (passed), timeline триггеров.
- **🧠 MaleCNS CPG** — interactive-lite: изолированный модуль T1-L
  (DgR/E1/E2/I1/I2, LIF) с knockout прямо в браузере + сохранённые
  прогоны (normal/KO×6 × drive 0.4–1.6). KO_E1 — генератор умер;
  KO_I1 — ритм остался; KO_I1I2 — E-клетки в тоническом насыщении.
- **📊 Benchmarks** — MUKHTAR-Bench v1: B01–B10 со статусами
  (confirmed/planned/future) и сырые JSONL-логи (View raw).
- **📈 Roadmap** — история версий с честными статусами
  (confirmed/experimental/failed/deprecated).
- **🎮 ARC / 👁 Vision** — второе тело и визуальный рефлекс (планируется).

## Проверенные данные схемы 2

Locomotion и Reflex Bench читают `data/schema2/`: девять 20-секундных
прогонов на исходниках `62ce2a97eb44c3a06cdd4172591eb2e724684bbc`, Python
3.11.16, NumPy 2.4.6, MuJoCo 3.14.0, seed 42. Manifest содержит SHA256
кода, точных XML-сцен и сырых JSONL. При чтении проверяется целостность файлов.

Счётчики разделяют начала эпизодов и активные тики. Ложные срабатывания
оцениваются только на ровном полу; для ловушки и ямы показано «не оценено».
Просадка разделена на пиковую и конечную, наклон считается по вертикали тела.
Для ямы 20 мм пиковая просадка BASE/R3v2 — 156.0/24.6 мм; это другая
метрика, чем прежняя конечная просадка 152/19 мм.

Все файлы доступны в dataset: [schema 2](https://huggingface.co/datasets/AvaSiG/MUKHTAR-Bench/tree/main/runs/2026-09-27-schema2).
Исторические данные и CPG-артефакты сохранены отдельно. Новые прогоны не
используют нейронный checkpoint; JSONL содержит события рефлексов, без
полной кинематической траектории и видео.

## Данные

- Model repo: [AvaSiG/ARGOS-MUKHTAR](https://huggingface.co/AvaSiG/ARGOS-MUKHTAR)
- Dataset: [AvaSiG/MUKHTAR-Bench](https://huggingface.co/datasets/AvaSiG/MUKHTAR-Bench)
- GitHub (код): [winargos42-dotcom/argos, проверенные метрики и Space](https://github.com/winargos42-dotcom/argos/tree/codex/mukhtar-bench-metrics-20260927/mukhtar-lab)

Тяжёлые MuJoCo-прогоны исполняются заранее, в Space — только
результаты и лёгкая numpy-симуляция CPG. Никакой имитации.
