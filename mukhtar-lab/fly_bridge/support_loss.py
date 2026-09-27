"""support_loss.py — пропажа опоры: пол обрывается, stance-нога уходит в пустоту.

Геометрия: плита до x=0.60, затем зазор 8 см (0.60-0.68), дальше пол на
-0.06 м (ниже на 60 мм). Нога, ожидающая опору (stance), проваливается.
Критерий (спека Севы): реакция начинается ДО заметного падения корпуса.
Мерим: x, falls, min_body_z, момент первого погружения стопы (foot_z<-8мм),
момент первого telemetry-события рефлекса, лаг между ними, события.
Варианты: BASE / REFLEX / FOOTCATCH.
"""
import json
import re
import sys
import time

import numpy as np

sys.path.insert(0, '/opt/argos-roach')
sys.path.insert(0, '/opt/argos-roach/tests')
sys.path.insert(0, '/opt/argos-roach/fly_bridge')
sys.path.insert(0, '/opt/argos-roach/controllers')

import mujoco
from contact_reflex import SineContactController
from limb_reflexes import ReflexController
from foot_catch_reflex import FootCatchReflexController
from reflex_bench import contact_any

DURATION = 15.0


def build_gap(xml_path, gap=(0.60, 0.64), depth=0.045):
    src = open(xml_path).read()
    m = re.search(r'<geom name="floor".*?/>', src, flags=re.S)
    original = m.group(0)
    x1, x2 = gap
    lhx, lcx = (x1 + 10.0) / 2.0, (x1 - 10.0) / 2.0
    rhx, rcx = (10.0 - x2) / 2.0, (x2 + 10.0) / 2.0
    rz = -0.025 - depth
    terrain = (
        f'<geom name="plate_l" type="box" size="{lhx} 10 0.025" '
        f'pos="{lcx} 0 -0.025" friction="0.8 0.005 0.0001"/>\n'
        f'<geom name="plate_r" type="box" size="{rhx} 10 0.025" '
        f'pos="{rcx} 0 {rz}" friction="0.8 0.005 0.0001"/>')
    src = src.replace(original, terrain)
    return mujoco.MjModel.from_xml_string(src)


def run(model, ctrl_factory):
    data = mujoco.MjData(model)
    data.qpos[2] += 0.012
    mujoco.mj_forward(model, data)
    foot_ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, f'foot{i}')
                for i in range(6)]
    tibia_ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM,
                                   f'tibia{i}') for i in range(6)]
    static_ids = {mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, n)
                  for n in ('floor', 'plate_l', 'plate_r')
                  if mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, n) >= 0}
    jr = np.asarray(model.jnt_range[1:19], dtype=float)
    ctrl = ctrl_factory()
    ctrl.reset()
    ctrl.set_command("GO", 0.0)
    fell = False
    min_body_z = 99.0
    z0 = float(data.qpos[2])
    sink_t = None       # первое погружение стопы ниже уровня пола
    event_t = None      # первое событие рефлекса после sink
    t = 0.0
    dt = model.opt.timestep
    while t < DURATION:
        f_hits = contact_any(data, set(foot_ids), static_ids)
        t_hits = contact_any(data, set(tibia_ids), static_ids)
        fc = [1 if i in f_hits else 0 for i in foot_ids]
        tc = [1 if i in t_hits else 0 for i in tibia_ids]
        fpos = np.asarray([data.geom_xpos[f] for f in foot_ids])
        fz = [float(p[2] - 0.016) for p in fpos]
        if sink_t is None and t >= 0.5 and min(fz) < -0.006:
            sink_t = t
        state = {"dt": dt, "t": t,
                 "qpos": data.qpos[7:].copy(), "qvel": data.qvel[6:].copy(),
                 "body_pos": data.qpos[0:3].copy(),
                 "body_quat": data.qpos[3:7].copy(),
                 "body_angvel": data.qvel[3:6].copy(),
                 "foot_contact": fc, "tibia_contact": tc,
                 "foot_z": fz, "foot_pos": fpos,
                 "joint_range": jr, "settling": t < 0.5}
        tg = ctrl.step(t, state)
        tele = getattr(ctrl, 'reflex_telemetry', [])
        if sink_t is not None and event_t is None and tele:
            event_t = tele[-1]['t']
        data.ctrl[:] = tg
        mujoco.mj_step(model, data)
        min_body_z = min(min_body_z, float(data.qpos[2]))
        if data.qpos[2] < 0.10:
            fell = True
        t += dt
    telemetry = getattr(ctrl, 'reflex_telemetry', [])
    kinds = {}
    for ev in telemetry:
        kinds[ev['kind']] = kinds.get(ev['kind'], 0) + 1
    return {
        'x': round(float(data.qpos[0]), 3),
        'fell': int(fell),
        'body_drop_mm': round((z0 - min_body_z) * 1000.0, 1),
        'sink_t_s': round(sink_t, 3) if sink_t is not None else None,
        'first_event_t_s': round(event_t, 3) if event_t is not None else None,
        'reaction_lag_ms': (round((event_t - sink_t) * 1000.0, 1)
                            if event_t is not None and sink_t is not None
                            else None),
        'events': kinds,
    }


def main():
    xml_path = '/opt/argos-roach/models/hexapod.xml'
    model = build_gap(xml_path, gap=(0.60, 0.63), depth=0.012)
    variants = [
        ('BASE', lambda: SineContactController(freq=1.0, k_ret=0.30)),
        ('REFLEX', lambda: ReflexController(freq=1.0, k_ret=0.30)),
        ('FOOTCATCH', lambda: FootCatchReflexController(freq=1.0,
                                                        k_ret=0.30)),
    ]
    for name, factory in variants:
        r = run(model, factory)
        print(json.dumps({'ctrl': name, **r}, ensure_ascii=False),
              flush=True)
    print('SUPPORT_LOSS_DONE', flush=True)


if __name__ == '__main__':
    main()
