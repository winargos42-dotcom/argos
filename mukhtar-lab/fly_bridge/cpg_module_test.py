"""cpg_module_test.py — изолированный T1-L модуль CPG (DNg100_R drive).

Клетки: DgR(10056), E1_T1L(800173), E2_T1L(800863),
        I1_T1L(801884), I2_T1L(800374).
Рёбра (pre->post, из BASE, правильная ориентация row=post/col=pre):
  DgR->E1 +1.55   DgR->E2 +0.01   DgR->I2 +0.07
  E1->E2  +4.65   E2->E1  +0.11   E1->DgR +0.01
  E2->I1  +0.38   E1->I1  +0.06   E1->I2 +0.84   E2->I2 +2.15
  I1->E1  -5.26   I1->E2  -1.21   I1->I2 -0.02
  I2->E1  -3.28   I2->E2  -0.56
Варианты:
  A_BASE  — BASE-веса как есть
  B_ARC   — trained-веса из /tmp/cpg_arc_edges.json (если есть)
  C_LOCAL_DALE — B с обнулением sign-violating CPG-рёбер
  D_RESCUE     — B с точными BASE-весами на CPG-рёбрах
Одинаковый sweep drive [0.4, 0.8, 1.2, 1.6] в DgR, 500 тиков.
Метрики: частота групп, FFT-период/мощность, альтернация E<->I,
autocorr-пик каждой группы (настоящая периодичность).
"""
import json
import math
import sys

import numpy as np
import torch

sys.path.insert(0, '/root/malecns/code')
from upstream.lif import spike, soft_clamp  # noqa: E402

TICKS = 500
DRIVES = [0.4, 0.8, 1.2, 1.6]
BETA = 0.9
THR = 1.0

# pre -> post -> w  (BASE)
BASE_EDGES = {
    ('DgR', 'E1'): 1.55, ('DgR', 'E2'): 0.01, ('DgR', 'I2'): 0.07,
    ('E1', 'E2'): 4.65, ('E2', 'E1'): 0.11, ('E1', 'DgR'): 0.01,
    ('E2', 'I1'): 0.38, ('E1', 'I1'): 0.06,
    ('E1', 'I2'): 0.84, ('E2', 'I2'): 2.15,
    ('I1', 'E1'): -5.26, ('I1', 'E2'): -1.21, ('I1', 'I2'): -0.02,
    ('I2', 'E1'): -3.28, ('I2', 'E2'): -0.56,
}
NAMES = ['DgR', 'E1', 'E2', 'I1', 'I2']
IDX = {nm: i for i, nm in enumerate(NAMES)}


def build_W(edges):
    W = np.zeros((5, 5), dtype=np.float32)
    for (pre, post), w in edges.items():
        W[IDX[post], IDX[pre]] = w  # row=post, col=pre
    return torch.from_numpy(W)


def load_arc_edges(path='/tmp/cpg_arc_edges.json'):
    try:
        d = json.load(open(path))
        return {tuple(k.split('->')): float(v) for k, v in d.items()}
    except FileNotFoundError:
        return None


def run(W, drive, ticks=TICKS, beta=BETA, thr=THR):
    mem = torch.zeros(1, 5)
    spk = torch.zeros(1, 5)
    cur = torch.zeros(1, 5)
    cur[0, IDX['DgR']] = drive
    raster = []
    for _ in range(ticks):
        recurrent = (W @ spk.T).T  # W[post,pre]: I[post] = sum_pre W[post,pre]*spk[pre]
        pre = beta * mem + cur + recurrent
        s = spike(pre, thr)
        mem = soft_clamp(pre - s * thr, 30.0)
        spk = s
        raster.append(s[0].clone())
    return torch.stack(raster)


def metrics(raster):
    rates = {nm: raster[:, IDX[nm]].float().numpy() for nm in NAMES[1:]}
    out = {}
    for nm, r in rates.items():
        out[f'{nm}_rate_mean'] = round(float(r.mean()), 3)
    e_all = rates['E1'] + rates['E2']
    i_all = rates['I1'] + rates['I2']
    total = e_all + i_all
    spec = np.abs(np.fft.rfft(total - total.mean()))
    freqs = np.fft.rfftfreq(len(total), d=1.0)
    band = (freqs > 0.005) & (freqs < 0.15)
    if band.any() and spec[band].sum() > 1e-9:
        k = int(np.argmax(spec[band]))
        out['osc_period_ticks'] = round(float(1.0 / freqs[band][k]), 1)
        out['osc_power'] = round(float(spec[band][k] / max(1e-9, spec[band].mean())), 1)
    else:
        out['osc_period_ticks'] = None
        out['osc_power'] = 0.0
    # альтернация E и I (антикорреляция на сдвиге = противоволна)
    e = e_all - e_all.mean()
    i = i_all - i_all.mean()
    best = 0.0
    for lag in range(2, min(60, len(e) // 2)):
        c = float(np.corrcoef(e[:-lag], i[lag:])[0, 1])
        if abs(c) > abs(best):
            best = c
    out['alt_corr_max'] = round(best, 3)
    # автокорреляция каждой группы: есть ли реальный ритм
    for nm, r in rates.items():
        r = r - r.mean()
        ac = [float(np.corrcoef(r[:-lag], r[lag:])[0, 1]) for lag in range(1, 61)]
        # период = первый лаг с локальным максимумом после минимума
        out[f'{nm}_autocorr_p1'] = round(max(ac[2:], key=abs), 3)
    # фазовые отношения пар (лаг максимальной корреляции)
    pairs = [('E1', 'E2'), ('E1', 'I1'), ('E2', 'I1'), ('E1', 'I2'), ('E2', 'I2')]
    for a, b in pairs:
        ra = rates[a] - rates[a].mean()
        rb = rates[b] - rates[b].mean()
        if ra.std() < 1e-9 or rb.std() < 1e-9:
            out[f'lag_{a}_{b}'] = None
            continue
        best, bestlag = 0.0, 0
        for lag in range(-60, 61):
            if lag >= 0:
                c = float(np.corrcoef(ra[lag:], rb[:len(ra) - lag])[0, 1])
            else:
                c = float(np.corrcoef(ra[:len(ra) + lag], rb[-lag:])[0, 1])
            if abs(c) > abs(best):
                best, bestlag = c, lag
        out[f'lag_{a}_{b}'] = bestlag
        out[f'corr_{a}_{b}'] = round(best, 3)
    return out


def main():
    arc_edges = load_arc_edges()
    variants = {}
    W_base = build_W(BASE_EDGES)
    variants['A_BASE'] = W_base
    if arc_edges is not None:
        W_arc = build_W(arc_edges)
        variants['B_TRAINED'] = W_arc
        # C: TRAINED + BASE-local restore — CPG-рёбра обратно к BASE
        W_c = W_arc.clone()
        W_c[W_base != 0] = W_base[W_base != 0]
        variants['C_RESTORE'] = W_c
    # D: минимальный литературный мотив E1/E2/I1 (без I2), BASE-магнитуды,
    # drive прямо в E1
    results = []
    for vname, W in variants.items():
        for drive in DRIVES:
            raster = run(W, drive)
            m = metrics(raster)
            m.update({'variant': vname, 'drive': drive})
            results.append(m)
            print(json.dumps(m, ensure_ascii=False), flush=True)
    # D: мотив
    motif_edges = {
        ('E1', 'E2'): 4.65, ('E2', 'E1'): 0.11,
        ('E2', 'I1'): 0.38, ('E1', 'I1'): 0.06,
        ('I1', 'E1'): -5.26, ('I1', 'E2'): -1.21,
    }
    Wm = build_W(motif_edges)
    for drive in DRIVES:
        mem = torch.zeros(1, 5)
        spk = torch.zeros(1, 5)
        cur = torch.zeros(1, 5)
        cur[0, IDX['E1']] = drive  # drive в E1 (DNg-команда уже учтена)
        raster = []
        for _ in range(TICKS):
            recurrent = (Wm @ spk.T).T
            pre = BETA * mem + cur + recurrent
            s = spike(pre, THR)
            mem = soft_clamp(pre - s * THR, 30.0)
            spk = s
            raster.append(s[0].clone())
        m = metrics(torch.stack(raster))
        m.update({'variant': 'D_MOTIF', 'drive': drive})
        results.append(m)
        print(json.dumps(m, ensure_ascii=False), flush=True)
    json.dump(results, open('/tmp/cpg_module.json', 'w'), ensure_ascii=False)
    print('CPG_MODULE_DONE', flush=True)


if __name__ == '__main__':
    main()
