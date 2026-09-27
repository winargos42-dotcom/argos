"""cpg_prc.py — Phase Response Curve T1-L CPG (M2).

Протокол:
 1. Реперный прогон (drive 0.8, 600 тиков): mean ISI спайков E1 = опорный период.
 2. Импульс +2.0 (1 тик) в E1 и в I2 на задержках d от 0 до P (13 точек) после
    спайка E1: сдвиг следующего спайка E1 => PRC(фаза) = 2*pi*(t_next-t_exp)/P.
 3. Perturbation recovery: подавление I2 на 5 тиков на 3 фазах, возврат,
    следующие 3 ISI E1 vs опорный период.
 4. Потолок генератора: прямой drive в E1 [0.5..3.5] (DgR OFF), период.
Артефакты: /tmp/cpg_m2/*.json
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


def step_state(W, mem, spk, cur, silenced=()):
    recurrent = (W @ spk.T).T
    pre = BETA * mem + cur + recurrent
    s = spike(pre, THR)
    for nm in silenced:
        s[0, IDX[nm]] = 0.0
    mem = soft_clamp(pre - s * THR, 30.0)
    return mem, s


def run_plain(W, drive_dgr, ticks=600, warmup=100):
    """Реперный прогон: drive в DgR, возвращает спайк-таймы E1 (после warmup)."""
    mem = torch.zeros(1, 5)
    spk = torch.zeros(1, 5)
    cur = torch.zeros(1, 5)
    cur[0, IDX['DgR']] = drive_dgr
    e1_times = []
    for t in range(ticks):
        mem, spk = step_state(W, mem, spk, cur)
        if t >= warmup and spk[0, IDX['E1']] > 0:
            e1_times.append(t)
    return e1_times


def run_pulse(W, drive_dgr, target, pulse_tick, silenced_during=()):
    """Прогон с импульсом +2.0 в target на tick pulse_tick; возвращает
    спайк-таймы E1 и полный растр."""
    mem = torch.zeros(1, 5)
    spk = torch.zeros(1, 5)
    cur = torch.zeros(1, 5)
    cur[0, IDX['DgR']] = drive_dgr
    e1_times = []
    for t in range(600):
        if t == pulse_tick:
            cur[0, IDX[target]] += 2.0
        mem, spk = step_state(W, mem, spk, cur, silenced_during)
        if spk[0, IDX['E1']] > 0:
            e1_times.append(t)
    return e1_times


def main():
    os.makedirs(OUT, exist_ok=True)
    W = build_W()
    drive = 0.8
    res = {}

    # 1. опорный период
    e1_ref = run_plain(W, drive)
    isis = np.diff(e1_ref)
    P = float(isis.mean())
    res['ref'] = {'drive': drive, 'P_ticks': round(P, 3),
                  'isi_std': round(float(isis.std()), 3),
                  'n_cycles': int(len(isis)), 'e1_rate': round(len(e1_ref) / 500, 3)}

    # 2. PRC: импульсы в E1 и I2
    for target in ('E1', 'I2'):
        prc = []
        for d in np.linspace(0, int(P), 13):
            d = int(round(d))
            pulse_tick = 350 + d  # якорь: фаза от ближайшего цикла, простой способ
            e1_t = run_pulse(W, drive, target, pulse_tick)
            # ожидаемый следующий спайк после pulse_tick: ищем последний спайк <= pulse_tick
            prev = [t for t in e1_t if t <= pulse_tick]
            after = [t for t in e1_t if t > pulse_tick]
            if not prev or not after:
                prc.append({'d': d, 'phi': round(2 * np.pi * d / P, 2),
                            'dt': None, 'dphi': None})
                continue
            t_exp = prev[-1] + P
            t_next = after[0]
            dt = t_next - t_exp
            prc.append({'d': d, 'phi': round(2 * np.pi * d / P, 2),
                        'dt': round(float(dt), 3),
                        'dphi': round(float(2 * np.pi * dt / P), 3)})
        res[f'prc_{target}'] = prc

    # 3. perturbation recovery: I2 silenced 5 тиков на 3 фазах
    rec = []
    for d in (int(P * 0.25), int(P * 0.5), int(P * 0.75)):
        pulse_tick = 350 + d
        silenced = {t for t in range(pulse_tick, pulse_tick + 5)}
        mem = torch.zeros(1, 5)
        spk = torch.zeros(1, 5)
        cur = torch.zeros(1, 5)
        cur[0, IDX['DgR']] = drive
        e1_times = []
        for t in range(600):
            mem, spk = step_state(W, mem, spk, cur,
                                  silenced=('I2',) if t in silenced else ())
            if spk[0, IDX['E1']] > 0:
                e1_times.append(t)
        after = [t for t in e1_times if t >= pulse_tick + 5]
        isi_after = np.diff(after)[:3]
        rec.append({'phase': round(2 * np.pi * d / P, 2),
                    'isi_1': float(isi_after[0]) if len(isi_after) > 0 else None,
                    'isi_2': float(isi_after[1]) if len(isi_after) > 1 else None,
                    'isi_3': float(isi_after[2]) if len(isi_after) > 2 else None})
    res['i2_suppress_recovery'] = rec

    # 4. потолок генератора: прямой drive в E1 (DgR OFF)
    ceiling = []
    for ed in (0.5, 1.0, 1.55, 2.5, 3.5):
        mem = torch.zeros(1, 5)
        spk = torch.zeros(1, 5)
        cur = torch.zeros(1, 5)
        cur[0, IDX['E1']] = ed
        e1_times = []
        for t in range(600):
            mem, spk = step_state(W, mem, spk, cur)
            if t >= 100 and spk[0, IDX['E1']] > 0:
                e1_times.append(t)
        isis = np.diff(e1_times)
        ceiling.append({'e1_drive': ed,
                        'period': round(float(isis.mean()), 3) if len(isis) else None,
                        'e1_rate': round(len(e1_times) / 500, 3)})
    res['e1_direct_drive_ceiling'] = ceiling

    json.dump(res, open(f'{OUT}/prc_results.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False), flush=True)
    print('CPG_PRC_DONE', flush=True)


if __name__ == '__main__':
    main()
