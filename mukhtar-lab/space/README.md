---
title: ARGOS-MUKHTAR Lab
emoji: 🐜
colorFrom: indigo
colorTo: green
sdk: gradio
sdk_version: 5.49.2
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

## Данные

- Model repo: [AvaSiG/ARGOS-MUKHTAR](https://huggingface.co/AvaSiG/ARGOS-MUKHTAR)
- Dataset: [AvaSiG/MUKHTAR-Bench](https://huggingface.co/datasets/AvaSiG/MUKHTAR-Bench)
- GitHub (код): [winargos42-dotcom/argos, ветка mukhtar](https://github.com/winargos42-dotcom/argos/tree/mukhtar/mukhtar-lab)

Тяжёлые MuJoCo-прогоны исполняются на ноде (Coral), в Space — только
результаты и лёгкая numpy-симуляция CPG. Никакой имитации.
