"""Numpy MaleCNS T1-L engine extracted unchanged from the deployed Space."""

import math
import numpy as np

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
def sim_cpg(drive=0.8, ko=(), ticks=500, beta=BETA, thr=THR, pulse=None):
    """Run the original Space engine, optionally injecting one current pulse.

    ``pulse=(zero_based_tick, cell_name, amplitude)`` affects only that tick.
    The ordinary no-pulse and zero-amplitude trajectories are unchanged.
    """
    if pulse is not None:
        if not isinstance(pulse, (tuple, list)) or len(pulse) != 3:
            raise ValueError("pulse must be (tick, target, amplitude)")
        tick, target, amplitude = pulse
        if (not isinstance(tick, (int, np.integer)) or not 0 <= tick < ticks
                or target not in IDX or not math.isfinite(float(amplitude))):
            raise ValueError("invalid pulse tick, target or amplitude")
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
        if pulse is not None and t == pulse[0] and pulse[2] != 0:
            pre[IDX[pulse[1]]] += pulse[2]
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
