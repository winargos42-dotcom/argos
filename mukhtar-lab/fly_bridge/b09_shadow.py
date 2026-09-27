"""b09_shadow.py — B09-SHADOW-6CPG (шаг 1 из стека Мухтара).

Controller Б реально ведёт тело (MuJoCo 20 с). Параллельно 6 MaleCNS
CPG-модулей (T1L..T3R, из BASE-артефакта male_cns_spikewhale.pt)
работают независимо, actuator output = OFF.

Снимаем на модуль:
  period_i (тики и с), phase_i, phase drift между ногами,
  burst jitter, dropouts, CPU/tick.

PASS: все 6 живут весь прогон (burst в конце), dropouts=0,
jitter низкий, периоды воспроизводимы между повторами.
"""

import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, '/opt/argos-roach')
sys.path.insert(0, '/opt/argos-roach/controllers')

import mujoco  # noqa: E402
from contact_reflex import SineContactController  # noqa: E402

BETA = 0.9
THR = 1.0
DRIVE = 0.8
TICK_DT = 0.02          # секунд на тик CPG (50 Гц внутренних тиков)
DURATION = 20.0         # с симуляции
REPEATS = 3
_ERF_K = 0.8862269254527580
_erf = np.vectorize(math.erf)

ORDER = ['T1L', 'T2L', 'T3L', 'T1R', 'T2R', 'T3R']
CELL_ORDER = ['dng', 'E1', 'E2', 'I1', 'I2']


def load_modules():
    d = json.load(open('/tmp/cpg_m5/modules.json'))
    Ws = []
    for name in ORDER:
        md = d[name]
        W = np.zeros((5, 5), dtype=np.float32)
        for edge, w in md['edges'].items():
            pre, post = edge.split('->')
            W[CELL_ORDER.index(post), CELL_ORDER.index(pre)] = w
        Ws.append(W)
    return Ws


def tick_all(states, Ws, drive=DRIVE):
    """Один тик всех 6 модулей (numpy): [(mem,spk), ...]."""
    new_states = []
    for (mem, spk), W in zip(states, Ws):
        rec = W @ spk
        pre = BETA * mem + rec
        pre[0] += drive  # DNg drive
        s = (pre >= THR).astype(np.float32)
        mem2 = (30.0 * _erf((pre - s * THR) * (_ERF_K / 30.0))
                ).astype(np.float32)
        new_states.append((mem2, s))
    return new_states


def run_one(rng_idx):
    model = mujoco.MjModel.from_xml_path('/opt/argos-roach/models/hexapod.xml')
    data = mujoco.MjData(model)
    data.qpos[2] += 0.012
    mujoco.mj_forward(model, data)
    ctrl = SineContactController(freq=1.0, k_ret=0.30)
    ctrl.control_dt = 0.002
    ctrl.reset()
    ctrl.set_command("GO", 0.0)
    jr = np.asarray(model.jnt_range[1:19], dtype=float)
    foot_ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM,
                                  f'foot{i}') for i in range(6)]
    edges = None
    Ws = load_modules()
    states = [(np.zeros(5, dtype=np.float32), np.zeros(5, dtype=np.float32))
              for _ in Ws]
    n_ticks = int(DURATION / TICK_DT)
    raster = np.zeros((n_ticks, 6, 5), dtype=np.float32)
    t = 0.0
    cpg_acc = 0.0
    tick_i = 0
    # CPU-бенч: 200 тиков отдельно
    t0 = time.perf_counter()
    for _ in range(200):
        states = tick_all(states, Ws)
    cpu_ms_per_tick = 1000.0 * (time.perf_counter() - t0) / 200.0
    # основной прогон
    while t < DURATION:
        fpos = np.asarray([data.geom_xpos[f] for f in foot_ids])
        fz = [float(p[2] - 0.016) for p in fpos]
        state = {"dt": model.opt.timestep, "t": t,
                 "qpos": data.qpos[7:].copy(), "qvel": data.qvel[6:].copy(),
                 "body_pos": data.qpos[0:3].copy(),
                 "body_quat": data.qpos[3:7].copy(),
                 "body_angvel": data.qvel[3:6].copy(),
                 "foot_contact": [0] * 6, "tibia_contact": [0] * 6,
                 "foot_load": [0.0] * 6, "contact_duration": [0.0] * 6,
                 "foot_z": fz, "foot_pos": fpos, "joint_range": jr,
                 "settling": t < 1.0}
        tg = ctrl.step(t, state)
        data.ctrl[:] = tg
        mujoco.mj_step(model, data)
        t += model.opt.timestep
        # продвигаем CPG на dt_sim/TICK_DT тиков (дробный аккумулятор)
        cpg_acc += model.opt.timestep
        while cpg_acc >= TICK_DT and tick_i < n_ticks:
            states = tick_all(states, Ws)
            for mi, (_, s) in enumerate(states):
                raster[tick_i, mi] = s
            cpg_acc -= TICK_DT
            tick_i += 1
    body_x = float(data.qpos[0])
    return raster, cpu_ms_per_tick, body_x


def metrics(raster):
    out = {'modules': {}}
    for mi, name in enumerate(ORDER):
        # burst onset = спайк E1 или E2
        e_spk = (raster[:, mi, 1] + raster[:, mi, 2]) > 0.5
        onsets = np.where(np.diff(e_spk.astype(int)) == 1)[0] + 1
        if len(onsets) < 3:
            out['modules'][name] = {'alive': False, 'n_bursts':
                                    len(onsets)}
            continue
        isi = np.diff(onsets).astype(float)
        period = float(np.median(isi))
        jitter = float(np.std(isi) / max(1e-9, period))
        dropouts = int((isi > 3.0 * period).sum())
        alive = bool(onsets[-1] > 0.85 * len(raster))
        out['modules'][name] = {
            'alive': alive,
            'n_bursts': int(len(onsets)),
            'period_ticks': round(period, 1),
            'period_s': round(period * TICK_DT, 3),
            'jitter': round(jitter, 3),
            'dropouts': dropouts,
            'last_burst_tick': int(onsets[-1]),
            'first_burst_tick': int(onsets[0]),
        }
    return out


def main():
    os.makedirs('/tmp/b09_shadow', exist_ok=True)
    results = []
    for rep in range(REPEATS):
        raster, cpu_ms, body_x = run_one(rep)
        m = metrics(raster)
        m['repeat'] = rep
        m['cpu_ms_per_tick_6modules'] = round(cpu_ms, 3)
        m['body_x_m'] = round(body_x, 3)
        np.savez_compressed(f'/tmp/b09_shadow/raster_rep{rep}.npz',
                            raster=raster)
        results.append(m)
        print(f"rep{rep}: cpu={cpu_ms:.3f} ms/tick body_x={body_x:.2f} "
              f"periods="
              f"{[m['modules'][n].get('period_ticks') for n in ORDER]}",
              flush=True)
    # воспроизводимость периодов между повторами
    repro = {}
    for name in ORDER:
        pers = [r['modules'][name].get('period_ticks')
                for r in results[:REPEATS]]
        if all(p is not None for p in pers):
            repro[f'{name}_period_repro_std'] = round(
                float(np.std(pers)), 2)
    results.append(repro)
    # PASS-суммирование
    all_alive = all(r['modules'][n].get('alive')
                    for r in results[:REPEATS] for n in ORDER)
    no_dropouts = all(r['modules'][n].get('dropouts', 1) == 0
                      for r in results[:REPEATS] for n in ORDER)
    json.dump(results, open('/tmp/b09_shadow/results.json', 'w'),
              ensure_ascii=False, indent=2)
    print('B09_SHADOW_DONE', flush=True)
    print(f'PASS alive={all_alive} no_dropouts={no_dropouts}', flush=True)


if __name__ == '__main__':
    main()
