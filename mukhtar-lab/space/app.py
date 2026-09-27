"""ARGOS-MUKHTAR-Lab — embodied connectome testbed (Gradio Space).

Честность исполнения: тяжёлые MuJoCo-прогоны НЕ запускаются в браузере —
показываются результаты, заранее полученные на ноде (npy/json/jsonl).
Прямо в Space исполняется только interactive-lite: изолированный
MaleCNS CPG-модуль (5 клеток, numpy) с knockout.
"""

import json
import math
import os
from pathlib import Path

from benchmark_data import BenchmarkData

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import gradio as gr  # noqa: E402

DATA = os.path.join(os.path.dirname(__file__), "data")
CPG = os.path.join(DATA, "cpg_m0")
try:
    BENCH = BenchmarkData(Path(DATA) / "schema2")
    BENCH_ERROR = None
except (OSError, ValueError, KeyError, TypeError) as exc:
    BENCH = None
    BENCH_ERROR = str(exc)

# ─────────────────────────── константы CPG M0 ───────────────────────────
NAMES = ["DgR", "E1", "E2", "I1", "I2"]
IDX = {nm: i for i, nm in enumerate(NAMES)}
BASE_EDGES = {
    ("DgR", "E1"): 1.55, ("DgR", "E2"): 0.01, ("DgR", "I2"): 0.07,
    ("E1", "E2"): 4.65, ("E2", "E1"): 0.11, ("E1", "DgR"): 0.01,
    ("E2", "I1"): 0.38, ("E1", "I1"): 0.06,
    ("E1", "I2"): 0.84, ("E2", "I2"): 2.15,
    ("I1", "E1"): -5.26, ("I1", "E2"): -1.21, ("I1", "I2"): -0.02,
    ("I2", "E1"): -3.28, ("I2", "E2"): -0.56,
}
BETA = 0.9
THR = 1.0
_ERF_K = math.sqrt(math.pi) / 2.0
_erf = np.vectorize(math.erf)

EXPERIMENTS = ["normal", "KO_DNg100", "KO_E1", "KO_E2", "KO_I1",
               "KO_I2", "KO_I1I2"]
DRIVES = [0.4, 0.8, 1.2, 1.6]
KO_MAP = {"normal": (), "KO_DNg100": ("DgR",), "KO_E1": ("E1",),
          "KO_E2": ("E2",), "KO_I1": ("I1",), "KO_I2": ("I2",),
          "KO_I1I2": ("I1", "I2")}


# ─────────────────────────── CPG live (numpy) ───────────────────────────
def sim_cpg(drive=0.8, ko=(), ticks=500, beta=BETA, thr=THR):
    W = np.zeros((5, 5), dtype=np.float32)
    for (pre, post), w in BASE_EDGES.items():
        W[IDX[post], IDX[pre]] = w
    for nm in ko:
        W[IDX[nm], :] = 0.0
        W[:, IDX[nm]] = 0.0
    mem = np.zeros(5, dtype=np.float32)
    spk = np.zeros(5, dtype=np.float32)
    cur = np.zeros(5, dtype=np.float32)
    cur[IDX["DgR"]] = drive
    rast = np.zeros((ticks, 5), dtype=np.float32)
    for t in range(ticks):
        rec = W @ spk
        pre = beta * mem + cur + rec
        s = (pre >= thr).astype(np.float32)
        for nm in ko:
            s[IDX[nm]] = 0.0
        # soft_clamp(pre - s*thr, 30.0): 30*erf(x*(sqrt(pi)/2)/30)
        mem = (30.0 * _erf((pre - s * thr) * (_ERF_K / 30.0))
               ).astype(np.float32)
        spk = s
        rast[t] = s
    return rast


def cpg_metrics(rast):
    rates = {nm: rast[:, IDX[nm]] for nm in NAMES[1:]}
    out = {}
    for nm, r in rates.items():
        out[f"{nm}_rate_mean"] = round(float(r.mean()), 3)
    e_all = rates["E1"] + rates["E2"]
    i_all = rates["I1"] + rates["I2"]
    total = e_all + i_all
    spec = np.abs(np.fft.rfft(total - total.mean()))
    freqs = np.fft.rfftfreq(len(total), d=1.0)
    band = (freqs > 0.005) & (freqs < 0.15)
    if band.any() and spec[band].sum() > 1e-9:
        k = int(np.argmax(spec[band]))
        out["osc_period_ticks"] = round(float(1.0 / freqs[band][k]), 1)
        out["osc_power"] = round(
            float(spec[band][k] / max(1e-9, spec[band].mean())), 1)
    else:
        out["osc_period_ticks"] = None
        out["osc_power"] = 0.0
    e = e_all - e_all.mean()
    i = i_all - i_all.mean()
    best_corr = None
    for lag in range(2, min(60, len(e) // 2)):
        ea, ib = e[:-lag], i[lag:]
        if ea.std() < 1e-9 or ib.std() < 1e-9:
            continue
        c = float(np.corrcoef(ea, ib)[0, 1])
        if np.isfinite(c) and (best_corr is None or abs(c) > abs(best_corr)):
            best_corr = c
    out["alt_corr_max"] = (round(best_corr, 3)
                              if best_corr is not None else None)

    for nm, r in rates.items():
        r = r - r.mean()
        ac = []
        for lag in range(3, 61):
            a, b = r[:-lag], r[lag:]
            if a.std() < 1e-9 or b.std() < 1e-9:
                continue
            c = float(np.corrcoef(a, b)[0, 1])
            if np.isfinite(c):
                ac.append(c)
        out[f"{nm}_autocorr_p1"] = (round(max(ac, key=abs), 3)
                                         if ac else None)

    for a, b in [("E1", "E2"), ("E1", "I1"), ("E2", "I1"),
                 ("E1", "I2"), ("E2", "I2")]:
        ra = rates[a] - rates[a].mean()
        rb = rates[b] - rates[b].mean()
        if ra.std() < 1e-9 or rb.std() < 1e-9:
            out[f"lag_{a}_{b}"] = None
            continue
        best_lag = None
        best_corr = None
        for lag in range(-60, 61):
            if lag >= 0:
                aa, bb = ra[lag:], rb[:len(ra) - lag]
            else:
                aa, bb = ra[:len(ra) + lag], rb[-lag:]
            if len(aa) < 2 or aa.std() < 1e-9 or bb.std() < 1e-9:
                continue
            c = float(np.corrcoef(aa, bb)[0, 1])
            if np.isfinite(c) and (best_corr is None or abs(c) > abs(best_corr)):
                best_corr = c
                best_lag = lag
        out[f"lag_{a}_{b}"] = best_lag
    return out


# ─────────────────────────── данные бенчей ──────────────────────────────
def load_summary():
    if BENCH is None:
        raise ValueError(BENCH_ERROR)
    return BENCH.summary


def load_events(bid, ctrl):
    return BENCH.events(bid, ctrl) if BENCH is not None else []


SCENARIOS = {
    "B01-flat": "Ровный пол: контроль ложных срабатываний (должно быть 0).",
    "B02-footcatch12": "Поперечная ловушка 12 мм: BASE застревает "
                       "(0.486 м), R1b foot-catch проходит (1.238 м).",
    "B03-gap20": "Яма 20 мм: сравнение BASE и поиска опоры R3 v2. "
                 "Пиковая и конечная просадка измерены отдельно.",
}
MODES = ["BASE", "R1b", "R3v2", "R1b+R3v2", "R4"]


def loco_metrics(scenario, mode):
    if BENCH is None:
        return f"Данные schema 2 недоступны: {BENCH_ERROR}"
    r = BENCH.result(scenario, mode)
    if r is None:
        return "Нет данных: этот режим в этом сценарии не прогонялся " \
               "(или не применим)."
    false_events = r["false_events"]
    false_label = "не оценено" if false_events is None else str(false_events)
    lines = [
        f"## {scenario} / {mode}",
        "",
        SCENARIOS.get(scenario, ""),
        "",
        "| Метрика | Значение |",
        "|---|---|",
        f"| distance, м | {r['distance_m']} |",
        f"| falls | {int(r['fell'])} |",
        f"| Начала эпизодов | {r['trigger_count']} |",
        f"| Активные записи | {r['active_tick_count']} |",
        f"| Ложные срабатывания | {false_label} |",
        f"| Просадка: пик, мм | {r['peak_body_drop_mm']} |",
        f"| Просадка: итог, мм | {r['final_body_drop_mm']} |",
        f"| min foot z, мм | {r.get('min_foot_z_mm')} |",
        f"| Наклон: максимум, ° | {r['max_tilt_deg']} |",
        f"| Начала по reason | {json.dumps(r['event_triggers'], ensure_ascii=False)} |",
        f"| Активные записи по reason | {json.dumps(r['event_active_ticks'], ensure_ascii=False)} |",
        f"| time to first search, с | {r.get('time_to_first_search_s')} |",
        f"| search duration, мс | {r.get('search_duration_ms')} |",
        f"| ground found | {r.get('ground_found')} |",
        f"| seed | {r.get('seed')} |",
        f"| Длительность, с | {r['duration_s']} |",
        "",
        "Начало эпизода и продолжение на следующем тике считаются отдельно. "
        "Ложность оценивается только в flat-контроле, где рефлексы не ожидаются; "
        "в остальных сценариях отсутствие оценки не означает ноль ошибок.",
        "",
        "*Схема 2: заранее исполненный MuJoCo-прогон, SHA256 файлов проверены.*",
    ]
    return "\n".join(lines)


def provenance_markdown():
    if BENCH is None:
        return f"Данные schema 2 недоступны: {BENCH_ERROR}"
    manifest = BENCH.manifest
    runtime = manifest["runtime"]
    return "\n".join([
        "### Происхождение результатов schema 2",
        f"- Git revision: `{manifest['git_revision']}`",
        f"- Source SHA256: `{manifest['source_sha256']}`",
        f"- Длительность: {manifest['duration_s']} с; стабилизация: {manifest['settling_s']} с",
        f"- Seed: {manifest['seed']}; {manifest['seed_policy']}",
        "- Runtime: " + ", ".join(f"{name} {value}" for name, value in runtime.items()),
        f"- Сформировано: {manifest['created_at']}",
        "- Контроллеры аналитические; neural checkpoint не используется.",
        "Сырые события содержат начала эпизодов и активные тики, а не полную траекторию тела.",
    ])


def reflex_timeline():
    ev = [event for event in load_events("B02-footcatch12", "R1b")
          if event["event_type"] == "trigger"]
    if not ev:
        return None
    fig, ax = plt.subplots(figsize=(9, 3.2))
    t = [e["t"] for e in ev]
    leg = [e["leg"] for e in ev]
    ax.scatter(t, leg, s=90, c="tab:red", zorder=3,
               label="R1B_FOOT_CATCH (триггер)")
    for e in ev:
        ax.annotate(f"leg{e['leg']}", (e["t"], e["leg"]),
                    textcoords="offset points", xytext=(0, 9), fontsize=8)
    ax.set_yticks(range(6))
    ax.set_yticklabels([f"leg {i}" for i in range(6)])
    ax.set_xlabel("t, с")
    ax.set_ylabel("нога")
    ax.set_title(f"B02-footcatch12 / R1b — {len(ev)} начал эпизодов foot-catch")
    ax.axvspan(7.0, 9.0, color="tab:orange", alpha=0.15,
               label="стена 12 мм")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    plt.close(fig)
    return fig


def reflex_summary():
    if BENCH is None:
        return f"Данные schema 2 недоступны: {BENCH_ERROR}"
    baseline = BENCH.result("B02-footcatch12", "BASE")
    reflex = BENCH.result("B02-footcatch12", "R1b")
    if baseline is None or reflex is None:
        return "Нет данных для сравнения BASE и R1b."
    return (f"- **BASE:** {baseline['distance_m']} м, падение: {int(baseline['fell'])}\n"
            f"- **R1b foot-catch:** {reflex['distance_m']} м, "
            f"падение: {int(reflex['fell'])}\n"
            f"- **Начала эпизодов:** {reflex['trigger_count']}; "
            "ложность срабатываний в этом сценарии не оценена.")


REFLEX_CHAIN = """## R1b foot-catch: цепочка срабатывания (B02)

1. **contact** — устойчивый контакт стопы с препятствием mid-swing
2. **persistent ≥ 8 тиков** (16 мс) — не случайное чирканье
3. **R1B_ON** — триггер: lift/retract
4. **contact cleared** — стопа перенесена
5. **nominal gait** — фаза продолжается

*Численные результаты и начала эпизодов выше взяты из проверенного прогона schema 2.*
"""


def cpg_view(experiment, drive):
    base = f"{experiment}_{drive}"
    rast_path = os.path.join(CPG, f"raster_{base}.npz")
    met_path = os.path.join(CPG, f"metrics_{base}.json")
    if not os.path.exists(rast_path):
        return None, "нет данных"
    rast = np.load(rast_path)["raster"]
    with open(met_path, encoding="utf-8") as f:
        metrics = json.load(f)
    fig, ax = plt.subplots(figsize=(9, 3.4))
    for i, nm in enumerate(NAMES):
        spk_t = np.where(rast[:, i] > 0.5)[0]
        ax.scatter(spk_t, [i] * len(spk_t), s=6, marker="|",
                   linewidths=0.6)
    ax.set_yticks(range(5))
    ax.set_yticklabels(NAMES)
    ax.set_xlabel("тик")
    ax.set_title(f"{experiment}, drive={drive}: период "
                 f"{metrics.get('osc_period_ticks')}, мощность "
                 f"{metrics.get('osc_power')}")
    fig.tight_layout()
    plt.close(fig)
    lines = [f"**{experiment}, drive={drive}**",
             "",
             f"osc_period_ticks = {metrics.get('osc_period_ticks')}",
             f"osc_power = {metrics.get('osc_power')}",
             f"alt_corr_max = {metrics.get('alt_corr_max')}",
             f"rates: " + ", ".join(
                 f"{nm}={metrics.get(nm + '_rate_mean')}"
                 for nm in NAMES[1:]),
             f"lag_E1_I2 = {metrics.get('lag_E1_I2')}",
             f"e1_cur_from_I2 = {metrics.get('e1_cur_from_I2')}",
             "",
             "Чтение: KO_E1 — генератор умер; KO_I1 — ритм остался; "
             "KO_I1I2 — E-клетки в тоническом насыщении."]
    return fig, "\n".join(lines)


def cpg_live(drive, ko_experiment):
    ko = KO_MAP.get(ko_experiment, ())
    rast = sim_cpg(drive=drive, ko=ko)
    m = cpg_metrics(rast)
    fig, ax = plt.subplots(figsize=(9, 3.4))
    for i, nm in enumerate(NAMES):
        spk_t = np.where(rast[:, i] > 0.5)[0]
        ax.scatter(spk_t, [i] * len(spk_t), s=6, marker="|",
                   linewidths=0.6)
    ax.set_yticks(range(5))
    ax.set_yticklabels(NAMES)
    ax.set_xlabel("тик")
    ax.set_title(f"live: {ko_experiment}, drive={drive} — период "
                 f"{m.get('osc_period_ticks')}")
    fig.tight_layout()
    plt.close(fig)
    lines = [f"**live: {ko_experiment}, drive={drive}**", "",
             f"osc_period_ticks = {m.get('osc_period_ticks')}",
             f"osc_power = {m.get('osc_power')}",
             f"alt_corr_max = {m.get('alt_corr_max')}",
             f"rates: " + ", ".join(
                 f"{nm}={m.get(nm + '_rate_mean')}"
                 for nm in NAMES[1:])]
    return fig, "\n".join(lines)


BENCH_TABLE = [
    ["B04-rough4_10", "общая адаптация ног", "planned", "—"],
    ["B05-turn", "T2 steering", "planned", "—"],
    ["B06-stuck", "recovery", "planned", "—"],
    ["B07-cpg-ko", "причинность CPG", "materials",
     "cpg_m0: KO×7 × drive×4"],
    ["B08-cpg-prc", "фазовый reset", "planned", "cpg_prc.py"],
    ["B09-six-cpg", "все 6 MaleCNS-модулей", "planned", "—"],
    ["B10-looming", "visual escape (LC16→MDN)", "future", "—"],
]


def benchmark_table():
    rows = []
    for scenario, description, modes in (
        ("B01-flat", "отсутствие ложных рефлексов", ("BASE", "R1b", "R3v2")),
        ("B02-footcatch12", "R1b foot-catch", ("BASE", "R1b")),
        ("B03-gap20", "R3 v2 searching", ("BASE", "R3v2")),
    ):
        results = [BENCH.result(scenario, mode) if BENCH is not None else None
                   for mode in modes]
        if any(row is None for row in results):
            rows.append([scenario, description, "нет данных", "—"])
        elif scenario == "B01-flat":
            rows.append([scenario, description, "measured / schema 2",
                         "/".join(str(row["false_events"]) for row in results) +
                         " (BASE/R1b/R3v2)"])
        elif scenario == "B02-footcatch12":
            rows.append([scenario, description, "measured / schema 2",
                         f"{results[0]['distance_m']} → {results[1]['distance_m']} м"])
        else:
            rows.append([scenario, description, "measured / schema 2",
                         f"fell {int(results[0]['fell'])}→{int(results[1]['fell'])}, "
                         f"пиковая просадка {results[0]['peak_body_drop_mm']}→"
                         f"{results[1]['peak_body_drop_mm']} мм"])
    return rows + BENCH_TABLE


def view_raw(filename):
    if BENCH is None:
        return f"Данные schema 2 недоступны: {BENCH_ERROR}"
    try:
        text = BENCH.read_raw(filename)
    except ValueError as exc:
        return str(exc)
    if len(text) > 20000:
        return text[:20000] + "\n… (обрезано)"
    return text


ROADMAP = """## Развитие Мухтара (реальная история + план)

- **v0 — CPG only** — `confirmed`: триподная ходьба A/Б/В, 2 м за 40 с,
  path_ratio 1.27–1.29
- **v0.1 — R1/R2/R3** — `confirmed`: tibia-R1 (артефакт tibia↔floor),
  R2 retraction, ранний R3 support-loss
- **v0.2 — foot-catch** — `confirmed`: R1b: ловушка 12 мм 0.486 → 1.238 м
- **v0.3 — prediction-error R3** — `confirmed`: R3 v2 (AMOS II):
  яма 20 мм fell 1→0; пиковая и конечная просадка — в таблице schema 2
- **Global neural metronome + I2 phase reset** — `failed`:
  локальная пертурбация ноги сбивала всю походку (global metronome хуже
  локальных CPG)
- **R4 v2 load-hold** — `failed`: deadlock «держать фазу vs активный
  lift-off» (flat 1.26→0.887 м); ждёт инверсной схемы или 6-CPG
- **R1a tibia-stumble** — `experimental`: на текущей геометрии тибия не
  достаёт препятствий; off по умолчанию
- **v0.4 — MaleCNS CPG** — `experimental`: модуль M0 (DgR/E1/E2/I1/I2)
  с KO-протоколом; 6 модулей — следующий шаг
- **v0.5 — visual reflex** — `planned` (LC16→MDN backward walking)
- **v1 — autonomous room navigation** — `planned`
"""


def build():
    with gr.Blocks(title="ARGOS-MUKHTAR Lab") as demo:
        gr.Markdown(
            "# ARGOS-MUKHTAR — Embodied connectome testbed\n"
            "Мухтар — стенд, где конкретные нервные цепи насекомого можно "
            "включить, отключить, нарушить и проверить, что они реально "
            "меняют в поведении шестиногого тела.\n\n"
            "> ARGOS-MUKHTAR is an embodied connectome testbed that "
            "connects anatomically identified insect neural circuits to "
            "a simulated six-legged body and measures their causal "
            "contribution to behavior.")
        with gr.Tabs():
            with gr.Tab("▶ Locomotion"):
                gr.Markdown("### MuJoCo-прогоны schema 2 (заранее исполнены)")
                with gr.Row():
                    scen = gr.Dropdown(list(SCENARIOS), value="B02-footcatch12",
                                       label="Сценарий")
                    mode = gr.Dropdown(MODES, value="R1b", label="Режим")
                loco_out = gr.Markdown()
                btn = gr.Button("Показать метрики")
                btn.click(loco_metrics, [scen, mode], loco_out)
            with gr.Tab("⚡ Reflex Bench"):
                gr.Markdown("### 12-mm foot trap")
                gr.Markdown(reflex_summary())
                tl = gr.Plot(reflex_timeline())
                gr.Markdown(REFLEX_CHAIN)
            with gr.Tab("🧠 MaleCNS CPG"):
                gr.Markdown("### Interactive-lite (исполняется прямо здесь) "
                            "— изолированный модуль T1-L: "
                            "DgR/E1/E2/I1/I2, LIF, 500 тиков")
                with gr.Row():
                    live_exp = gr.Dropdown(EXPERIMENTS, value="normal",
                                           label="Experiment (live)")
                    live_drive = gr.Slider(0.4, 1.6, value=0.8, step=0.4,
                                           label="drive")
                live_btn = gr.Button("Запустить")
                live_plot = gr.Plot()
                live_md = gr.Markdown()
                live_btn.click(cpg_live, [live_drive, live_exp],
                               [live_plot, live_md])
                gr.Markdown("### Записанные прогоны (нода, 27.09)")
                with gr.Row():
                    v_exp = gr.Dropdown(EXPERIMENTS, value="normal",
                                        label="Experiment (saved)")
                    v_drive = gr.Slider(0.4, 1.6, value=0.8, step=0.4,
                                        label="drive")
                v_btn = gr.Button("Показать raster + метрики")
                v_plot = gr.Plot()
                v_md = gr.Markdown()
                v_btn.click(cpg_view, [v_exp, v_drive], [v_plot, v_md])
            with gr.Tab("📊 Benchmarks"):
                gr.Markdown("### MUKHTAR-Bench — schema 2")
                gr.Dataframe(benchmark_table(),
                             headers=["Bench", "Что проверяет", "Статус",
                                      "Результат"],
                             interactive=False)
                gr.Markdown(provenance_markdown())
                gr.Markdown("### View raw")
                files = BENCH.raw_files if BENCH is not None else []
                fsel = gr.Dropdown(files, value="summary.json" if files else None,
                                   label="Файл")
                raw_btn = gr.Button("Показать")
                raw_out = gr.Textbox(lines=18, max_lines=30,
                                     label="raw")
                raw_btn.click(view_raw, fsel, raw_out)
            with gr.Tab("📈 Roadmap"):
                gr.Markdown(ROADMAP)
            with gr.Tab("🎮 ARC"):
                gr.Markdown(
                    "### ARC — второе тело Мухтара\n\n"
                    "Search only vs Search + Mukhtar ranker: уровни, "
                    "действия, повторы, счёт, задержка. Раздел появится "
                    "вместе с первыми воспроизводимыми прогонами "
                    "ARC-ранкера — сейчас данных для честной таблицы нет.")
            with gr.Tab("👁 Vision"):
                gr.Markdown("### Visual reflex (LC16 → MDN)\n\n"
                            "Looming-детектор → backward walking. "
                            "Планируется как первый визуальный рефлекс; "
                            "вкладка появится после первых прогонов.")
    return demo


demo = build()
if __name__ == "__main__":
    demo.launch()
