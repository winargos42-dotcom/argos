"""cpg_m5.py — все 6 leg-модулей: изоляция + проверка осцилляции.

Каждый модуль: DNg (контралатеральный: L<-DgR, R<-DgL) + E1/E2/I1/I2
данного neuromere+side. Рёбра берутся из BASE артефакта (row=post, col=pre).
Протокол идентичен M0: drive [0.4,0.8,1.2,1.6] в DNg, 500 тиков, LIF beta
0.9/thr 1.0. Метрики: период (burst-onset), power, rates.
Сохранение: /tmp/cpg_m5/modules.json — рёбра всех модулей (для моста).
"""
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

MODULES = {
    'T1L': {'dng': 10056, 'E1': 800173, 'E2': 800863, 'I1': 801884, 'I2': 800374},
    'T2L': {'dng': 10056, 'E1': 800009, 'E2': 801728, 'I1': 903139, 'I2': 800233},
    'T3L': {'dng': 10056, 'E1': 800003, 'E2': 801149, 'I1': 801257, 'I2': 800494},
    'T1R': {'dng': 10045, 'E1': 800288, 'E2': 903216, 'I1': 803183, 'I2': 800411},
    'T2R': {'dng': 10045, 'E1': 818556, 'E2': 802025, 'I1': 904079, 'I2': 800103},
    'T3R': {'dng': 10045, 'E1': 800114, 'E2': 801429, 'I1': 801916, 'I2': 800119},
}
DRIVES = [0.8, 1.2]


def load_base_edges():
    pt = torch.load('/root/output/male_cns_spikewhale.pt', map_location='cpu',
                    weights_only=False)
    crow, col, w, ids = pt['crow'], pt['col'], pt['weights'], pt['body_ids']
    id2i = {int(b): i for i, b in enumerate(ids.tolist())}
    row_of_edge = torch.repeat_interleave(torch.arange(ids.numel()),
                                          crow[1:] - crow[:-1])
    pre_body = ids[col.long()].tolist()
    post_body = ids[row_of_edge].tolist()
    edges = {}
    for i in range(len(pre_body)):
        edges[(int(pre_body[i]), int(post_body[i]))] = float(w[i])
    return edges


def module_edges(all_edges, cells):
    """Извлечь рёбра подграфа модуля (пре->пост, имена)."""
    body2name = {v: k for k, v in cells.items()}
    out = {}
    for (pre, post), w in all_edges.items():
        if pre in body2name and post in body2name:
            out[f'{body2name[pre]}->{body2name[post]}'] = w
    return out


def run_module(edges, cells, drive, ticks=500):
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
    rates = {n: round(float(raster[:, idx[n]].float().mean()), 3)
             for n in ('E1', 'E2', 'I1', 'I2')}
    return period, rates


def main():
    os.makedirs(OUT, exist_ok=True)
    all_edges = load_base_edges()
    res = {}
    for name, cells in MODULES.items():
        edges = module_edges(all_edges, cells)
        res[name] = {'cells': cells, 'edges': edges, 'runs': []}
        for drive in DRIVES:
            period, rates = run_module(edges, cells, drive)
            res[name]['runs'].append({'drive': drive,
                                      'period': round(period, 2) if period else None,
                                      'rates': rates})
            print(f'{name} drive={drive} period={period} rates={rates}',
                  flush=True)
    json.dump(res, open(f'{OUT}/modules.json', 'w'), ensure_ascii=False, indent=1)
    print('CPG_M5_DONE')


if __name__ == '__main__':
    main()
