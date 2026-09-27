"""foot_catch.py — сценарий «зацеп лапы»: тонкая стенка ловит СТОПУ.

Стенка h мм (2 мм толщиной) поперёк пути на x=0.5. В середине переноса
стопа идёт на высоте 10-15 мм — стенка 12-14 мм ловит именно стопу;
тибия выше (20+ мм) может её не задеть. Текущий R1 смотрит ТОЛЬКО
tibia_contact — проверяем, видит ли он такой зацеп, и помогает ли
вариант с foot-catch-детектом (контакт стопы в середине swing).
Варианты: BASE (синус), REFLEX (R1-R3 tibia), FOOTCATCH (R1 + зацеп).
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

DURATION = 20.0
HEIGHTS = [0.010, 0.012, 0.014]


def build_wire(xml_path, h):
    src = open(xml_path).read()
    m = re.search(r'<geom name="floor".*?/>', src, flags=re.S)
    original = m.group(0)
    terrain = (original + '\n'
               f'<geom name="wire" type="box" size="0.002 0.30 {h/2}" '
               f'pos="0.5 0 {h/2}" friction="0.8 0.005 0.0001"/>')
    src = src.replace(original, terrain)
    return mujoco.MjModel.from_xml_string(src)


def run(model, ctrl_factory, h):
    data = mujoco.MjData(model)
    data.qpos[2] += 0.012
    mujoco.mj_forward(model, data)
    foot_ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, f'foot{i}')
                for i in range(6)]
    tibia_ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM,
                                   f'tibia{i}') for i in range(6)]
    wire_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, 'wire')
    static_ids = {mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, 'floor'),
                  wire_id}
    jr = np.asarray(model.jnt_range[1:19], dtype=float)
    ctrl = ctrl_factory()
    ctrl.reset()
    ctrl.set_command("GO", 0.0)
    fell = False
    max_foot_z = -99.0
    foot_wire_hits = 0
    tibia_wire_hits = 0
    foot_debounce = np.full(6, -9.0)
    tibia_debounce = np.full(6, -9.0)
    t = 0.0
    dt = model.opt.timestep
    while t < DURATION:
        f_wire = contact_any(data, set(foot_ids), {wire_id})
        t_wire = contact_any(data, set(tibia_ids), {wire_id})
        f_hits = contact_any(data, set(foot_ids), static_ids)
        t_hits = contact_any(data, set(tibia_ids), static_ids)
        fc = [1 if i in f_hits else 0 for i in foot_ids]
        tc = [1 if i in t_hits else 0 for i in tibia_ids]
        fw = [1 if i in f_wire else 0 for i in foot_ids]
        tw = [1 if i in t_wire else 0 for i in tibia_ids]
        for i in range(6):
            if fw[i] and t - foot_debounce[i] > 0.3:
                foot_wire_hits += 1
                foot_debounce[i] = t
            if tw[i] and t - tibia_debounce[i] > 0.3:
                tibia_wire_hits += 1
                tibia_debounce[i] = t
        fpos = np.asarray([data.geom_xpos[f] for f in foot_ids])
        fz = [float(p[2] - 0.016) for p in fpos]
        max_foot_z = max(max_foot_z, max(fz))
        state = {"dt": dt, "t": t,
                 "qpos": data.qpos[7:].copy(), "qvel": data.qvel[6:].copy(),
                 "body_pos": data.qpos[0:3].copy(),
                 "body_quat": data.qpos[3:7].copy(),
                 "body_angvel": data.qvel[3:6].copy(),
                 "foot_contact": fc, "tibia_contact": tc,
                 "foot_z": fz, "foot_pos": fpos,
                 "joint_range": jr, "settling": t < 0.5}
        tg = ctrl.step(t, state)
        data.ctrl[:] = tg
        mujoco.mj_step(model, data)
        if data.qpos[2] < 0.10:
            fell = True
        t += dt
    stumbles = sum(1 for e in getattr(ctrl, 'reflex_telemetry', [])
                   if e.get('kind') == 'stumble')
    return {'h_mm': round(h * 1000, 1), 'x': round(float(data.qpos[0]), 3),
            'fell': int(fell),
            'foot_wire_hits': foot_wire_hits,
            'tibia_wire_hits': tibia_wire_hits,
            'stumble_events': stumbles,
            'clearance_mm': round(max_foot_z * 1000, 1)}


def main():
    xml_path = '/opt/argos-roach/models/hexapod.xml'
    variants = [
        ('BASE', lambda: SineContactController(freq=1.0, k_ret=0.30)),
        ('REFLEX', lambda: ReflexController(freq=1.0, k_ret=0.30)),
        ('FOOTCATCH', lambda: FootCatchReflexController(freq=1.0,
                                                        k_ret=0.30)),
    ]
    for h in HEIGHTS:
        model = build_wire(xml_path, h)
        for name, factory in variants:
            r = run(model, factory, h)
            print(json.dumps({'ctrl': name, **r}, ensure_ascii=False),
                  flush=True)
    print('FOOT_CATCH_DONE', flush=True)


if __name__ == '__main__':
    main()
