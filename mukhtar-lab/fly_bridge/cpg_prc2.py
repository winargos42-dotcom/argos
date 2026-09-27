"""cpg_prc2.py — Phase Response Curve T1-L CPG, исправленная версия.

Исправления против v1:
 1. Импульс: +2.0 ровно 1 тик, потом ток возвращается к базе (баг v1:
    cur не сбрасывался, для I2 это был вечный +2.0).
 2. Фаза: по burst-началам популяции E1+E2 (спайки E1 нерегулярны,
    isi_std ~ P — плохой якорь). Burst onset = сглаженный сигнал
    E1+E2 пересекает 0.6 вверх.
Протокол: drive 0.8 в DgR, якорь t0 = burst onset после 350,
импульс в target на t0+d, d = 0..P_b (13 точек),
dphi = 2*pi*(next_onset - (t0+P_b))/P_b.
Дополнительно: suppression I2 на 5 тиков на 3 фазах — возврат периода.
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
OUT = '/tmp/cpg_m2'
NAMES = ['DgR', 'E1', 'E2', 'I1', 'I2']
IDX = {nm: i for i, nm in enumerate(NAMES)}
BASE_EDGES = {
    ('DgR', 'E1'): 1.55, ('DgR', 'E2'): 0.01, ('DgR', 'I2'): 0.07,
    ('E1', 'E2'): 4.65, ('E2', 'E1'): 0.11, ('E1', 'DgR'): 0.01,
    ('E2', 'I1'): 0.38, ('E1', 'I1'): 0.06,
    ('E1', 'I2'): 0.84, ('E2', 'I2'): 2.15,
    ('I1', 'E1'): -5.26, ('I1', 'E2'): -1.21, ('I1', 'I2'): -0.02,
    ('I2', 'E1'): -3.28, ('I2', 'E2'): -0.56,
}


def build_W():
    W = np.zeros((5, 5), dtype=np.float32)
    for (pre, post), w in BASE_EDGES.items():
        W[IDX[post], IDX[pre]] = w
    return torch.from_numpy(W)


def run_to_raster(W, drive, ticks, pulse=None, suppress=None):
    """pulse=(tick, target, amp); suppress=set of ticks with I2 silenced.
    Возвращает растр (ticks,5)."""
    mem = torch.zeros(1, 5)
    spk = torch.zeros(1, 5)
    cur = torch.zeros(1, 5)
    cur[0, IDX['DgR']] = drive
    raster = []
    for t in range(ticks):
        if pulse is not None and t == pulse[0]:
            cur[0, IDX[pulse[1]]] += pulse[2]
        mem, s = step(W, mem, spk, cur)
        if pulse is not None and t == pulse[0]:
            cur[0, IDX[pulse[1]]] -= pulse[2]  # сброс: импульс ровно 1 тик
        if suppress is not None and t in suppress:
            s[0, IDX['I2']] = 0.0
        spk = s
        raster.append(s[0].clone())
    return torch.stack(raster)


def step(W, mem, spk, cur):
    recurrent = (W @ spk.T).T
    pre = BETA * mem + cur + recurrent
    s = spike(pre, THR)
    mem2 = soft_clamp(pre - s * THR, 30.0)
    return mem2, s


def burst_onsets(raster, warmup=100):
    """Сигнал = E1+E2 (сумма двух столбцов), сглаженный окном 3.
    Onset: переход сглаженного сигнала через 0.6 вверх."""
    e = raster[:, IDX['E1']].float().numpy() + raster[:, IDX['E2']].float().numpy()
    sm = np.convolve(e, np.ones(3) / 3, mode='same')
    onsets = []
    above = False
    for t in range(warmup, len(sm)):
        if not above and sm[t] >= 0.6:
            onsets.append(t)
            above = True
        elif sm[t] < 0.2:
            above = False
    return onsets


def main():
    os.makedirs(OUT, exist_ok=True)
    W = build_W()
    drive = 0.8
    res = {}

    # опорный период по burst-началам
    raster_ref = run_to_raster(W, drive, 800)
    ons_ref = burst_onsets(raster_ref)
    P_b = float(np.mean(np.diff(ons_ref)))
    res['ref'] = {'P_burst_ticks': round(P_b, 3),
                  'isi_std': round(float(np.std(np.diff(ons_ref))), 3),
                  'n_bursts': len(ons_ref)}

    for target in ('E1', 'I2'):
        prc = []
        for d in np.linspace(0, int(P_b), 13):
            d = int(round(d))
            raster = run_to_raster(W, drive, 800)
            # якорь: первый onset после 350
            ons = burst_onsets(raster)
            anchor = [o for o in ons if o >= 350]
            if not anchor:
                prc.append({'d': d, 'dphi': None, 'dt': None})
                continue
            t0 = anchor[0]
            # повторный прогон с импульсом в t0+d (несколько проб для стабильности)
            shifts = []
            for trial in range(3):
                r2 = run_to_raster(W, drive, 800, pulse=(t0 + d, target, 2.0))
                ons2 = burst_onsets(r2)
                nxt = [o for o in ons2 if o > t0 + d]
                if not nxt:
                    shifts.append(None)
                    continue
                dt = nxt[0] - (t0 + P_b)
                shifts.append(dt)
            dt_mean = (float(np.mean([s for s in shifts if s is not None]))
                       if any(s is not None for s in shifts) else None)
            prc.append({'d': d,
                        'phi': round(2 * np.pi * d / P_b, 2),
                        'dt': round(dt_mean, 2) if dt_mean is not None else None,
                        'dphi': round(2 * np.pi * dt_mean / P_b, 2)
                        if dt_mean is not None else None,
                        'trials': [round(s, 2) if s is not None else None
                                   for s in shifts]})
        res[f'prc_{target}'] = prc

    # I2 suppression recovery (5 тиков) на 3 фазах, меряем по burst-периодам
    rec = []
    for d in (int(P_b * 0.25), int(P_b * 0.5), int(P_b * 0.75)):
        raster = run_to_raster(W, drive, 800)
        ons = burst_onsets(raster)
        anchor = [o for o in ons if o >= 350][0]
        t0 = anchor + d
        r2 = run_to_raster(W, drive, 800, suppress=set(range(t0, t0 + 5)))
        ons2 = burst_onsets(r2)
        after = [o for o in ons2 if o >= t0]
        isis = np.diff(after)[:3]
        rec.append({'phase': round(2 * np.pi * d / P_b, 2),
                    'isi_1': round(float(isis[0]), 1) if len(isis) > 0 else None,
                    'isi_2': round(float(isis[1]), 1) if len(isis) > 1 else None,
                    'isi_3': round(float(isis[2]), 1) if len(isis) > 2 else None,
                    'P_b': round(P_b, 1)})
    res['i2_suppress_recovery'] = rec

    json.dump(res, open(f'{OUT}/prc_results2.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False), flush=True)
    print('CPG_PRC2_DONE', flush=True)


if __name__ == '__main__':
    main()
