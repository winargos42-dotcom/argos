"""stage1_regression.py — 12-мм regression модульного контура ПОВЕРХ базы Севы.

Сценарий: стенка 4 мм × 12 мм на x=0.5 (эталонная ловушка зацепа стопы).
Протокол (A/B аблейшн): BASE / R1b / R1a+R1b / все.
Эталон (27.09): BASE застревает на 0.486 м (6289 ударов);
модульный R1b — проход (~1.28 м).

Контракт:
- MuJoCo -> ContactPipeline.update(data) -> leg_contacts[leg][part]
  (ContactSignal, ignore_leg_leg отсекает самоконтакты)
- ReflexContext(contacts=leg_contacts[leg], expected_contact=явно)
- mix_reflex_outputs -> joint_delta/phase_delta/phase_hold
- q_target = q_nominal + joint_delta (SIDE-знаки limb_reflexes) -> clip
- phase_hold -> phases[leg] = prev_phases[leg]
"""

import json
import math
import re
import sys

import numpy as np

sys.path.insert(0, '/opt/argos-roach')
sys.path.insert(0, '/opt/argos-roach/controllers')
sys.path.insert(0, '/opt/argos-roach/fly_bridge')
sys.path.insert(0, '/opt/argos-roach/mukhtar')

import mujoco  # noqa: E402

from contact_reflex import SineContactController  # noqa: E402
from gait_controller import LEG_COUNT, SIDE  # noqa: E402
from mukhtar.reflexes import (R1FootCatchReflex, R1StumbleReflex,  # noqa: E402
                              R3SearchingReflex, ReflexContext,
                              mix_reflex_outputs)
from mukhtar.sensors.contact_pipeline import ContactPipeline  # noqa: E402

TWO_PI = 2.0 * math.pi
DURATION = 20.0
CONTROL_DT = 0.002
WALL_X = 0.5
WALL_H = 0.012
EXPECTED_LO = math.pi
EXPECTED_HI = TWO_PI - 0.02 * math.pi


def build_geom_map(model):
    """Все геомы ног -> (leg, part): ignore_leg_leg отсекает нога-нога."""
    gm = {}
    for i in range(6):
        for part in ('coxa', 'femur', 'foot', 'tibia'):
            gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM,
                                    f'{part}{i}')
            if gid >= 0:
                gm[gid] = (i, part)
    return gm


class Stage1Controller(SineContactController):
    """Б (SineContactController) + модульный рефлекторный контур."""

    def __init__(self, control_dt=CONTROL_DT,
                 enabled=('r1a', 'r1b', 'r3'), **kw):
        # рефлексы ДО super().__init__(): родительский __init__ зовёт reset()
        self.control_dt = control_dt
        self.enabled = tuple(enabled)
        self.r1a = [R1StumbleReflex() for _ in range(LEG_COUNT)]
        self.r1b = [R1FootCatchReflex(dt=control_dt) for _ in
                    range(LEG_COUNT)]
        self.r3 = [R3SearchingReflex(error_threshold=0.20) for _ in
                   range(LEG_COUNT)]
        self._stage1_boost = np.zeros((LEG_COUNT, 5), dtype=float)
        self.events = {}
        super().__init__(**kw)

    def reset(self, rng=None):
        super().reset(rng=rng)
        for r in self.r1a + self.r1b + self.r3:
            r.reset()
        self._stage1_boost.fill(0.0)
        self.events = {}

    def _apply_reflex(self, state, dt, prev_phases):
        super()._apply_reflex(state, dt, prev_phases)
        if getattr(self, 'mode', 'go') != 'go':
            return
        if state.get('settling', False):
            return
        t = float(state.get('t', 0.0))
        leg_contacts = state.get('leg_contacts')
        if not leg_contacts:
            return
        self._stage1_boost *= math.exp(-dt / 0.30)
        for leg in range(LEG_COUNT):
            prev_phi = float(prev_phases[leg]) % TWO_PI
            swing = prev_phi < math.pi
            stance = not swing
            expected = (1.0 if (stance and EXPECTED_LO < prev_phi
                                < EXPECTED_HI) else 0.0)
            ctx = ReflexContext(
                dt=dt, t=t, leg=leg, phase=prev_phi,
                swing=swing, stance=stance,
                contacts=leg_contacts[leg],
                expected_contact=expected,
            )
            outs = []
            if 'r1a' in self.enabled:
                outs.append(self.r1a[leg].update(ctx))
            if 'r1b' in self.enabled:
                outs.append(self.r1b[leg].update(ctx))
            if 'r3' in self.enabled:
                outs.append(self.r3[leg].update(ctx))
            out = mix_reflex_outputs(
                outs,
                joint_delta_limit=np.array([0.3, 0.4, 0.4]),
                phase_delta_limit=0.5,
            )
            if out.reasons:
                key = '|'.join(out.reasons)
                self.events.setdefault(key, []).append(t)
            if out.phase_hold:
                self.phases[leg] = prev_phi
            elif out.phase_delta:
                self.phases[leg] = max(0.0, prev_phi + out.phase_delta)
            b = self._stage1_boost[leg]
            b[0] += float(out.joint_delta[1])  # femur lift
            b[1] += float(out.joint_delta[0])  # coxa retract
            b[2] += float(out.joint_delta[2])  # tibia tuck

    def _post_targets(self, state, targets):
        targets = super()._post_targets(state, targets)
        targets = np.asarray(targets, dtype=float)
        for leg in range(LEG_COUNT):
            s = SIDE[leg]
            b = self._stage1_boost[leg]
            targets[3 * leg + 0] += +s * b[1]   # coxa
            targets[3 * leg + 1] += +s * b[0]   # femur
            targets[3 * leg + 2] += -s * b[2]   # tibia
        jr = state.get('joint_range')
        if jr is not None:
            jr = np.asarray(jr, dtype=float)
            if jr.shape == (18, 2):
                targets = np.clip(targets, jr[:, 0], jr[:, 1])
        return targets


def build_wall(xml_path):
    src = open(xml_path).read()
    m = re.search(r'<geom name="floor".*?/>', src, flags=re.S)
    wall = ('<geom name="wire" type="box" size="0.002 0.30 '
            f'{WALL_H / 2.0}" pos="{WALL_X} 0 {WALL_H / 2.0}" '
            'friction="0.8 0.005 0.0001"/>')
    src = src.replace(m.group(0), m.group(0) + '\n' + wall)
    return mujoco.MjModel.from_xml_string(src)


def run(model, ctrl_factory, pipeline=None):
    data = mujoco.MjData(model)
    data.qpos[2] += 0.012
    mujoco.mj_forward(model, data)
    foot_ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM,
                                  f'foot{i}') for i in range(6)]
    tibia_ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM,
                                   f'tibia{i}') for i in range(6)]
    jr = np.asarray(model.jnt_range[1:19], dtype=float)
    ctrl = ctrl_factory()
    ctrl.control_dt = CONTROL_DT
    ctrl.reset()
    ctrl.set_command("GO", 0.0)
    fell = False
    t = 0.0
    dt = model.opt.timestep
    wire_hits = 0
    wire_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, 'wire')
    while t < DURATION:
        if pipeline is not None:
            lc = pipeline.update(data)
            fc = [1 if lc[i]['foot'].active else 0 for i in range(6)]
            tc = [1 if lc[i]['tibia'].active else 0 for i in range(6)]
            loads = [lc[i]['foot'].normal_force for i in range(6)]
            durs = [lc[i]['foot'].duration_s for i in range(6)]
        else:
            hits = set()
            for i in range(data.ncon):
                c = data.contact[i]
                hits.add(int(c.geom1))
                hits.add(int(c.geom2))
            fc = [1 if f in hits else 0 for f in foot_ids]
            tc = [1 if f in hits else 0 for f in tibia_ids]
            loads = [0.0] * 6
            durs = [0.0] * 6
        for i in range(data.ncon):
            c = data.contact[i]
            if int(c.geom1) == wire_id or int(c.geom2) == wire_id:
                if int(c.geom1) in foot_ids or int(c.geom2) in foot_ids \
                        or int(c.geom1) in tibia_ids \
                        or int(c.geom2) in tibia_ids:
                    wire_hits += 1
        fpos = np.asarray([data.geom_xpos[f] for f in foot_ids])
        fz = [float(p[2] - 0.016) for p in fpos]
        state = {"dt": dt, "t": t,
                 "qpos": data.qpos[7:].copy(), "qvel": data.qvel[6:].copy(),
                 "body_pos": data.qpos[0:3].copy(),
                 "body_quat": data.qpos[3:7].copy(),
                 "body_angvel": data.qvel[3:6].copy(),
                 "foot_contact": fc, "tibia_contact": tc,
                 "foot_load": loads, "contact_duration": durs,
                 "foot_z": fz, "foot_pos": fpos,
                 "joint_range": jr, "settling": t < 1.0,
                 "leg_contacts": lc if pipeline is not None else None}
        tg = ctrl.step(t, state)
        data.ctrl[:] = tg
        mujoco.mj_step(model, data)
        if data.qpos[2] < 0.10:
            fell = True
        t += dt
    counts = {}
    times = {}
    for k, v in getattr(ctrl, 'events', {}).items():
        counts[k] = len(v)
        times[k] = [round(float(x), 2) for x in v[:6]]
    return {'x': round(float(data.qpos[0]), 3), 'fell': int(fell),
            'wire_hits_ticks': wire_hits, 'events': counts,
            'events_t': times}


def main():
    xml_path = '/opt/argos-roach/models/hexapod.xml'
    model = build_wall(xml_path)
    pipeline = ContactPipeline(
        model=model, geom_map=build_geom_map(model), dt=CONTROL_DT)
    # BASE (эталон застревания ~0.486)
    r_base = run(model, lambda: SineContactController(freq=1.0,
                                                      k_ret=0.30))
    print(json.dumps({'ctrl': 'BASE', **r_base}, ensure_ascii=False),
          flush=True)
    # аблейшн: R1b / R1a+R1b / все
    for name, enabled in [('STAGE1_R1B', ('r1b',)),
                          ('STAGE1_R1A_R1B', ('r1a', 'r1b')),
                          ('STAGE1_FULL', ('r1a', 'r1b', 'r3'))]:
        r = run(model,
                lambda e=enabled: Stage1Controller(freq=1.0, k_ret=0.30,
                                                   enabled=e),
                pipeline=pipeline)
        print(json.dumps({'ctrl': name, **r}, ensure_ascii=False),
              flush=True)
    print('STAGE1_REGRESSION_DONE', flush=True)


if __name__ == '__main__':
    main()
