"""scan_tibia.py — факт: на каких высотах стены тибия реально бьёт СТЕНУ.

Прямые пары tibia↔wire из data.contact (по именам), BASE-контроллер,
12 с на высоту. Ищем физический сценарий R1a (tibia↔obstacle в swing).
"""

import math
import re
import sys

import numpy as np

sys.path.insert(0, '/opt/argos-roach')
sys.path.insert(0, '/opt/argos-roach/controllers')
sys.path.insert(0, '/opt/argos-roach/fly_bridge')

import mujoco  # noqa: E402

from contact_reflex import SineContactController  # noqa: E402

TWO_PI = 2.0 * math.pi


def build_wall(xml_path, height):
    src = open(xml_path).read()
    m = re.search(r'<geom name="floor".*?/>', src, flags=re.S)
    wall = ('<geom name="wire" type="box" size="0.002 0.30 '
            f'{height / 2.0}" pos="0.5 0 {height / 2.0}" '
            'friction="0.8 0.005 0.0001"/>')
    src = src.replace(m.group(0), m.group(0) + '\n' + wall)
    return mujoco.MjModel.from_xml_string(src)


def scan(model, height):
    data = mujoco.MjData(model)
    data.qpos[2] += 0.012
    mujoco.mj_forward(model, data)
    ctrl = SineContactController(freq=1.0, k_ret=0.30)
    ctrl.control_dt = 0.002
    ctrl.reset()
    ctrl.set_command("GO", 0.0)
    tibia_ids = {mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM,
                                   f'tibia{i}') for i in range(6)}
    wire_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, 'wire')
    foot_ids = {mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM,
                                  f'foot{i}') for i in range(6)}
    tibia_wire = 0
    foot_wire = 0
    jr = np.asarray(model.jnt_range[1:19], dtype=float)
    t = 0.0
    x = 0.0
    while t < 12.0:
        hits = set()
        for i in range(data.ncon):
            c = data.contact[i]
            g1, g2 = int(c.geom1), int(c.geom2)
            if g1 == wire_id or g2 == wire_id:
                o = g2 if g1 == wire_id else g1
                if o in tibia_ids:
                    tibia_wire += 1
                elif o in foot_ids:
                    foot_wire += 1
            hits.add(g1)
            hits.add(g2)
        fc = [1 if f in hits else 0 for f in sorted(foot_ids)]
        tc = [1 if f in hits else 0 for f in sorted(tibia_ids)]
        fpos = np.asarray([data.geom_xpos[f] for f in sorted(foot_ids)])
        fz = [float(p[2] - 0.016) for p in fpos]
        state = {"dt": model.opt.timestep, "t": t,
                 "qpos": data.qpos[7:].copy(), "qvel": data.qvel[6:].copy(),
                 "body_pos": data.qpos[0:3].copy(),
                 "body_quat": data.qpos[3:7].copy(),
                 "body_angvel": data.qvel[3:6].copy(),
                 "foot_contact": fc, "tibia_contact": tc,
                 "foot_load": [0.0] * 6, "contact_duration": [0.0] * 6,
                 "foot_z": fz, "foot_pos": fpos,
                 "joint_range": jr, "settling": t < 1.0}
        tg = ctrl.step(t, state)
        data.ctrl[:] = tg
        mujoco.mj_step(model, data)
        t += model.opt.timestep
        x = float(data.qpos[0])
    return x, tibia_wire, foot_wire


def main():
    xml_path = '/opt/argos-roach/models/hexapod.xml'
    for h in (0.012, 0.014, 0.016, 0.018, 0.020, 0.024, 0.028):
        m = build_wall(xml_path, h)
        x, tw, fw = scan(m, h)
        print(f"H={h*1000:.0f}мм x={x:.3f} tibia_wire={tw} foot_wire={fw}",
              flush=True)
    print("SCAN_DONE", flush=True)


if __name__ == '__main__':
    main()
