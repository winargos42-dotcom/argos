"""ARGOS-MUKHTAR-Lab — embodied connectome testbed (Gradio Space).

Честность исполнения: тяжёлые MuJoCo-прогоны НЕ запускаются в браузере —
показываются результаты, заранее полученные на ноде (npy/json/jsonl).
Прямо в Space исполняется только interactive-lite: изолированный
MaleCNS CPG-модуль (5 клеток, numpy) с knockout.
"""

import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import gradio as gr  # noqa: E402

DATA = os.path.join(os.path.dirname(__file__), "data")
CPG = os.path.join(DATA, "cpg_m0")

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
    best = 0.0
    for lag in range(2, min(60, len(e) // 2)):
        c = float(np.corrcoef(e[:-lag], i[lag:])[0, 1])
        if abs(c) > abs(best):
            best = c
    out["alt_corr_max"] = round(best, 3)
    for nm, r in rates.items():
        r = r - r.mean()
        ac = [float(np.corrcoef(r[:-l], r[l:])[0, 1]) for l in
              range(1, 61)]
        out[f"{nm}_autocorr_p1"] = round(max(ac[2:], key=abs), 3)
    for a, b in [("E1", "E2"), ("E1", "I1"), ("E2", "I1"),
                 ("E1", "I2"), ("E2", "I2")]:
        ra = rates[a] - rates[a].mean()
        rb = rates[b] - rates[b].mean()
        if ra.std() < 1e-9 or rb.std() < 1e-9:
            out[f"lag_{a}_{b}"] = None
            continue
        bestlag = 0
        for lag in range(-60, 61):
            if lag >= 0:
                c = float(np.corrcoef(ra[lag:],
                                      rb[:len(ra) - lag])[0, 1])
            else:
                c = float(np.corrcoef(ra[:len(ra) + lag],
                                      rb[-lag:])[0, 1])
            if abs(c) > abs(bestlag) or (abs(c) == abs(bestlag)
                                          and lag == 0):
                bestlag = lag if abs(c) > 0 else bestlag
        out[f"lag_{a}_{b}"] = bestlag
    return out


# ─────────────────────────── данные бенчей ──────────────────────────────
def load_summary():
    with open(os.path.join(DATA, "summary.json")) as f:
        return json.load(f)


def load_events(bid, ctrl):
    path = os.path.join(DATA, f"{bid}_{ctrl}_events.jsonl")
    if not os.path.exists(path):
        return []
    return [json.loads(line) for line in open(path)]


SCENARIOS = {
    "B01-flat": "Ровный пол: контроль ложных срабатываний (должно быть 0).",
    "B02-footcatch12": "Поперечная ловушка 12 мм: BASE застревает "
                       "(0.486 м), R1b foot-catch проходит (1.238 м).",
    "B03-gap20": "Яма 20 мм: BASE теряет опору (падение, просадка 152 мм), "
                 "R3 v2 ищет опору (fell 0, просадка ~19 мм).",
}
MODES = ["BASE", "R1b", "R3v2", "R1b+R3v2", "R4"]


def loco_metrics(scenario, mode):
    s = load_summary()
    rows = [r for r in s["results"] if r["bench_id"] == scenario
            and r["controller"] == mode]
    if not rows:
        return "Нет данных: этот режим в этом сценарии не прогонялся " \
               "(или не применим)."
    r = rows[0]
    lines = [
        f"## {scenario} / {mode}",
        "",
        SCENARIOS.get(scenario, ""),
        "",
        "| Метрика | Значение |",
        "|---|---|",
        f"| distance, м | {r.get('x')} |",
        f"| falls | {r.get('fell')} |",
        f"| false reflex events | {r.get('false_events')} |",
        f"| body drop, мм | {r.get('body_drop_mm')} |",
        f"| min foot z, мм | {r.get('min_foot_z_mm')} |",
        f"| max tilt, град | {r.get('max_tilt_deg')} |",
        f"| reflex events (событий) | "
        f"{json.dumps(r.get('events', {}), ensure_ascii=False)} |",
        f"| time to first search, с | {r.get('time_to_first_search_s')} |",
        f"| search duration, мс | {r.get('search_duration_ms')} |",
        f"| ground found | {r.get('ground_found')} |",
        f"| seed | {r.get('seed')} |",
        "",
        "*Полный прогон исполнен на ноде (MuJoCo), здесь — заранее "
        "полученный результат.*",
    ]
    return "\n".join(lines)


def reflex_timeline():
    ev = load_events("B02-footcatch12", "R1b")
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
    ax.set_title("B02-footcatch12 / R1b — 9 триггеров foot-catch")
    ax.axvspan(7.0, 9.0, color="tab:orange", alpha=0.15,
               label="стена 12 мм")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


REFLEX_CHAIN = """## R1b foot-catch: цепочка срабатывания (B02)

1. **contact** — устойчивый контакт стопы с препятствием mid-swing
2. **persistent ≥ 8 тиков** (16 мс) — не случайное чирканье
3. **R1B_ON** — триггер: lift/retract
4. **contact cleared** — стопа перенесена
5. **nominal gait** — фаза продолжается

*BASE: стопа упирается в стену 12 мм, походка деградирует → 0.486 м.*
*R1b: 9 триггеров → 1.238 м, 0 падений.*
"""


def cpg_view(experiment, drive):
    base = f"{experiment}_{drive}"
    rast_path = os.path.join(CPG, f"raster_{base}.npz")
    met_path = os.path.join(CPG, f"metrics_{base}.json")
    if not os.path.exists(rast_path):
        return None, "нет данных"
    rast = np.load(rast_path)["raster"]
    metrics = json.load(open(met_path))
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
    lines = [f"**live: {ko_experiment}, drive={drive}**", "",
             f"osc_period_ticks = {m.get('osc_period_ticks')}",
             f"osc_power = {m.get('osc_power')}",
             f"alt_corr_max = {m.get('alt_corr_max')}",
             f"rates: " + ", ".join(
                 f"{nm}={m.get(nm + '_rate_mean')}"
                 for nm in NAMES[1:])]
    return fig, "\n".join(lines)


BENCH_TABLE = [
    ["B01-flat", "отсутствие ложных рефлексов", "confirmed",
     "0/0/0 (BASE/R1b/R3v2)"],
    ["B02-footcatch12", "R1b foot-catch", "confirmed",
     "0.486 → 1.238 м, проход"],
    ["B03-gap20", "R3 v2 searching", "confirmed",
     "fell 1→0, просадка 152→19 мм"],
    ["B04-rough4_10", "общая адаптация ног", "planned", "—"],
    ["B05-turn", "T2 steering", "planned", "—"],
    ["B06-stuck", "recovery", "planned", "—"],
    ["B07-cpg-ko", "причинность CPG", "materials",
     "cpg_m0: KO×7 × drive×4"],
    ["B08-cpg-prc", "фазовый reset", "planned", "cpg_prc.py"],
    ["B09-six-cpg", "все 6 MaleCNS-модулей", "planned", "—"],
    ["B10-looming", "visual escape (LC16→MDN)", "future", "—"],
]


def view_raw(filename):
    path = os.path.join(DATA, filename)
    if not os.path.exists(path):
        return "нет файла"
    with open(path) as f:
        text = f.read()
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
  яма 20 мм fell 1→0, просадка 152→19 мм
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
                gr.Markdown("### MuJoCo-прогоны (заранее исполнены на ноде)")
                with gr.Row():
                    scen = gr.Dropdown(list(SCENARIOS), value="B02-footcatch12",
                                       label="Сценарий")
                    mode = gr.Dropdown(MODES, value="R1b", label="Режим")
                loco_out = gr.Markdown()
                btn = gr.Button("Показать метрики")
                btn.click(loco_metrics, [scen, mode], loco_out)
            with gr.Tab("⚡ Reflex Bench"):
                gr.Markdown("### 12-mm foot trap")
                gr.Markdown(
                    "- **BASE:** 0.486 м — **stuck**\n"
                    "- **R1b foot-catch:** 1.238 м — **passed**")
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
                gr.Markdown("### MUKHTAR-Bench v1")
                gr.Dataframe(BENCH_TABLE,
                             headers=["Bench", "Что проверяет", "Статус",
                                      "Результат"],
                             interactive=False)
                gr.Markdown("### View raw")
                files = sorted(os.listdir(DATA))
                fsel = gr.Dropdown(files, value="summary.json",
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
