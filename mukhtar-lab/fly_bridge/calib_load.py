"""calib_load.py — калибровка R4: реальные Fz ног в триподной ходьбе flat.

Метрики по каждой ноге за 10 c: mean/max normal_force в STANCE и SWING,
доля тиков с контактом в stance. Это основа порогов R4 load-based.
"""

import math
import sys

import numpy as np

sys.path.insert(0, '/opt/argos-roach')
sys.path.insert(0, '/opt/argos-roach/controllers')
sys.path.insert(0, '/opt/argos-roach/fly_bridge')
sys.path.insert(0, '/opt/argos-roach/mukhtar')

import mujoco  # noqa: E402

from contact_reflex import SineContactController  # noqa: E402
from mukhtar.sensors.contact_pipeline import ContactPipeline  # noqa: E402

TWO_PI = 2.0 * math.pi


def build_geom_map(model):
    gm = {}
    for i in range(6):
        for part in ('coxa', 'femur', 'foot', 'tibia'):
            gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM,
                                    f'{part}{i}')
            if gid >= 0:
                gm[gid] = (i, part)
    return gm


def build_kind_map(model):
    km = {}
    for name, kind in (('floor', 'floor'), ('plate_l', 'floor'),
                       ('plate_r', 'floor'), ('wire', 'obstacle')):
        gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, name)
        if gid >= 0:
            km[gid] = kind
    return km


def main():
    model = mujoco.MjModel.from_xml_path('/opt/argos-roach/models/hexapod.xml')
    pipe = ContactPipeline(model=model, geom_map=build_geom_map(model),
                           dt=0.002, kind_by_geom=build_kind_map(model))
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
    # накопители: stance_force[leg] список значений
    stance_forces = [[] for _ in range(6)]
    swing_forces = [[] for _ in range(6)]
    stance_contact_frac = [0] * 6
    stance_ticks = [0] * 6
    t = 0.0
    while t < 10.0:
        lc = pipe.update(data)
        for leg in range(6):
            phi = ctrl.phases[leg] % TWO_PI if hasattr(ctrl, 'phases') \
                else 0.0
            foot = lc[leg].get('foot')
            f = float(foot.normal_force) if foot is not None else 0.0
            swing = phi < math.pi
            if swing:
                swing_forces[leg].append(f)
            else:
                stance_forces[leg].append(f)
                stance_ticks[leg] += 1
                if foot is not None and foot.active:
                    stance_contact_frac[leg] += 1
        fpos = np.asarray([data.geom_xpos[f] for f in foot_ids])
        fz = [float(p[2] - 0.016) for p in fpos]
        state = {"dt": model.opt.timestep, "t": t,
                 "qpos": data.qpos[7:].copy(), "qvel": data.qvel[6:].copy(),
                 "body_pos": data.qpos[0:3].copy(),
                 "body_quat": data.qpos[3:7].copy(),
                 "body_angvel": data.qvel[3:6].copy(),
                 "foot_contact": [1 if lc[i]['foot'].active else 0
                                  for i in range(6)],
                 "tibia_contact": [0] * 6,
                 "foot_load": [lc[i]['foot'].normal_force for i in range(6)],
                 "contact_duration": [0.0] * 6,
                 "foot_z": fz, "foot_pos": fpos,
                 "joint_range": jr, "settling": t < 1.0}
        tg = ctrl.step(t, state)
        data.ctrl[:] = tg
        mujoco.mj_step(model, data)
        t += model.opt.timestep
    for leg in range(6):
        st = np.asarray(stance_forces[leg])
        sw = np.asarray(swing_forces[leg])
        print(f"leg{leg}: stance Fz mean={st.mean():.3f} "
              f"max={st.max():.3f} | swing Fz max={sw.max():.3f} | "
              f"stance contact frac={stance_contact_frac[leg] / max(1, stance_ticks[leg]):.2f}",
              flush=True)
    print("CALIB_DONE", flush=True)


if __name__ == '__main__':
    main()
