"""cpg_m5b.py — M5: все 6 leg-модулей, BASE и TRAINED, единый протокол.

Веса: BASE из артефакта, TRAINED из /tmp/cpg_base_vs_trained_edges.csv
(trained_signed_w = sign(nt_pre)*count*0.01).
Протокол для всех модулей одинаковый: drive sweep [0.4,0.8,1.2,1.6] в
контралатеральный DNg (L<-DgR, R<-DgL), 500 тиков, LIF beta 0.9/thr 1.0,
init zero. Метрики: burst-period, spectral power, rates E1/E2/I1/I2,
autocorr E1, dominant inhibitor, lag E1->E2.
"""
import csv
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, '/root/malecns/code')
from upstream.lif import spike, soft_clamp  # noqa: E402

BETA = 0.9
THR = 1.0
OUT = '/tmp/cpg_m5'
DRIVES = [0.4, 0.8, 1.2, 1.6]

MODULES = {
    'T1L': {'dng': 10056, 'E1': 800173, 'E2': 800863, 'I1': 801884, 'I2': 800374},
    'T2L': {'dng': 10056, 'E1': 800009, 'E2': 801728, 'I1': 903139, 'I2': 800233},
    'T3L': {'dng': 10056, 'E1': 800003, 'E2': 801149, 'I1': 801257, 'I2': 800494},
    'T1R': {'dng': 10045, 'E1': 800288, 'E2': 903216, 'I1': 803183, 'I2': 800411},
    'T2R': {'dng': 10045, 'E1': 818556, 'E2': 802025, 'I1': 904079, 'I2': 800103},
    'T3R': {'dng': 10045, 'E1': 800114, 'E2': 801429, 'I1': 801916, 'I2': 800119},
}


def load_weights():
    """{ (pre_body, post_body): (base_w, trained_w) } из CSV."""
    out = {}
    with open('/tmp/cpg_base_vs_trained_edges.csv') as f:
        rd = csv.reader(f)
        next(rd)
        for r in rd:
            pre, post = int(r[0]), int(r[2])
            bw = float(r[6]) if r[6] else None
            tw = float(r[7]) if r[7] else None
            out[(pre, post)] = (bw, tw)
    return out


def module_edges(wmap, cells, variant):
    body2name = {v: k for k, v in cells.items()}
    out = {}
    for (pre, post), (bw, tw) in wmap.items():
        if pre in body2name and post in body2name:
            w = bw if variant == 'BASE' else tw
            if w is not None:
                out[f'{body2name[pre]}->{body2name[post]}'] = w
    return out


def run_module(edges, drive, ticks=500):
    names = ['dng', 'E1', 'E2', 'I1', 'I2']
    idx = {n: i for i, n in enumerate(names)}
    W = np.zeros((5, 5), dtype=np.float32)
    for e, w in edges.items():
        a, b = e.split('->')
        W[idx[b], idx[a]] = w
    W = torch.from_numpy(W)
    mem = torch.zeros(1, 5)
    spk = torch.zeros(1, 5)
    cur = torch.zeros(1, 5)
    cur[0, idx['dng']] = drive
    raster = []
    for _ in range(ticks):
        recurrent = (W @ spk.T).T
        pre = BETA * mem + cur + recurrent
        s = spike(pre, THR)
        mem = soft_clamp(pre - s * THR, 30.0)
        spk = s
        raster.append(s[0].clone())
    raster = torch.stack(raster)
    rates = {n: float(raster[:, idx[n]].float().mean())
             for n in ('E1', 'E2', 'I1', 'I2')}
    # burst period + power
    e = raster[:, idx['E1']].float().numpy() + raster[:, idx['E2']].float().numpy()
    sm = np.convolve(e, np.ones(3) / 3, mode='same')
    onsets = []
    above = False
    for t in range(100, len(sm)):
        if not above and sm[t] >= 0.6:
            onsets.append(t)
            above = True
        elif sm[t] < 0.2:
            above = False
    period = float(np.mean(np.diff(onsets))) if len(onsets) > 3 else None
    spec = np.abs(np.fft.rfft(sm[100:] - sm[100:].mean()))
    freqs = np.fft.rfftfreq(len(sm[100:]), d=1.0)
    band = (freqs > 0.005) & (freqs < 0.15)
    power = (float(spec[band].max() / max(1e-9, spec[band].mean()))
             if band.any() and spec[band].sum() > 1e-9 else 0.0)
    # autocorr E1
    r1 = raster[:, idx['E1']].float().numpy()
    r1 = r1 - r1.mean()
    ac = 0.0
    if r1.std() > 1e-9:
        acs = [float(np.corrcoef(r1[:-l], r1[l:])[0, 1]) for l in range(2, 60)]
        ac = max(acs, key=abs)
    dom = 'I2' if rates['I2'] >= rates['I1'] else 'I1'
    return {'period': round(period, 2) if period else None,
            'power': round(power, 1), 'rates': rates,
            'E1_autocorr': round(ac, 3), 'dom_inhibitor': dom}


def main():
    os.makedirs(OUT, exist_ok=True)
    wmap = load_weights()
    res = {}
    table = []
    for name, cells in MODULES.items():
        res[name] = {}
        row = {'module': name}
        for variant in ('BASE', 'TRAINED'):
            edges = module_edges(wmap, cells, variant)
            best = None
            for drive in DRIVES:
                m = run_module(edges, drive)
                m['drive'] = drive
                res[name].setdefault(variant, []).append(m)
                if drive == 0.8:
                    best = m
            row[f'{variant}_period'] = best['period'] if best else None
            row[f'{variant}_power'] = best['power'] if best else None
            row[f'{variant}_dom'] = best['dom_inhibitor'] if best else None
            if best:
                row[f'{variant}_rates'] = best['rates']
            print(f'{name} {variant} drive=0.8:', json.dumps(best,
                  ensure_ascii=False), flush=True)
        table.append(row)
    json.dump({'modules': res}, open(f'{OUT}/modules_b_t.json', 'w'),
              ensure_ascii=False, indent=1)
    print('=== TABLE ===')
    for r in table:
        print(json.dumps(r, ensure_ascii=False))
    print('CPG_M5B_DONE')


if __name__ == '__main__':
    main()
