"""stage1_matrix.py — матрица 27.09 после двух фиксов (kind-классификация,
armed-R3, hold/cooldown-жизненный цикл).

Сцены: flat / 12 мм ловушка / stuck (высокая кромка для R1a) / gap 12 мм.
Прогоны: BASE, R1b-only, R1a-only, R3-only, FULL.

Критерии (спек Севы):
- flat: все варианты — ложных 0;
- 12 мм: BASE контроль (0.486), R1b-only должен пройти;
- stuck: R1a-only проверка stumble;
- gap: R3-only expected-touchdown (событие есть, коллапса нет);
- FULL на 12 мм: без регрессии >= R1b-only.

Event-log сохраняет каждый активный тик; event_type различает начало
reason-эпизода (trigger) и продолжение (active_tick).
"""

import json
import math
import re
import sys
from pathlib import Path

import numpy as np

LAB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_ROOT))

import mujoco  # noqa: E402

from controllers.contact_reflex import SineContactController  # noqa: E402
from controllers.gait_controller import LEG_COUNT, SIDE  # noqa: E402
from mukhtar.reflexes import (R1FootCatchReflex, R1StumbleReflex,  # noqa: E402
                              R3SearchingReflex, R4LoadCoordinationReflex,
                              ReflexContext, mix_reflex_outputs)
from mukhtar.sensors.contact_pipeline import ContactPipeline  # noqa: E402
from mukhtar.telemetry.metrics import BodyMetrics, EventMetrics  # noqa: E402

TWO_PI = 2.0 * math.pi
CONTROL_DT = 0.002
EXPECTED_LO = math.pi
EXPECTED_HI = TWO_PI - 0.02 * math.pi


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


class Stage1Controller(SineContactController):
    def __init__(self, control_dt=CONTROL_DT,
                 enabled=('r1b', 'r3'), apply_response=True, **kw):
        # R1a = experimental/off по умолчанию (нет сценария на этом теле)
        self.control_dt = control_dt
        self.enabled = tuple(enabled)
        self.apply_response = bool(apply_response)
        self.r1a = [R1StumbleReflex() for _ in range(LEG_COUNT)]
        self.r1b = [R1FootCatchReflex(dt=control_dt) for _ in
                    range(LEG_COUNT)]
        self.r3 = [R3SearchingReflex(error_threshold=0.20) for _ in
                   range(LEG_COUNT)]
        self.r4 = [R4LoadCoordinationReflex() for _ in range(LEG_COUNT)]
        self._stage1_boost = np.zeros((LEG_COUNT, 5), dtype=float)
        self.events = {}
        self.event_log = []
        self.event_metrics = EventMetrics()
        self._r3_max_int = [0.0] * LEG_COUNT
        self.tibia_trace = []
        super().__init__(**kw)

    def reset(self, rng=None):
        super().reset(rng=rng)
        for r in self.r1a + self.r1b + self.r3 + self.r4:
            r.reset()
        self._stage1_boost.fill(0.0)
        self.events = {}
        self.event_log = []
        self.event_metrics = EventMetrics()
        self._r3_max_int = [0.0] * LEG_COUNT

    def _log_event(self, t, leg, reason, pair, kind, phase, armed=None,
                   cooldown_remaining=0.0, event_type="active_tick"):
        rec = {"t": round(float(t), 3), "leg": leg, "reason": reason,
               "contact_pair": list(pair),
               "contact_kind": kind,
               "leg_phase": round(float(phase), 2),
               "armed": armed, "cooldown_remaining":
                   round(float(cooldown_remaining), 3),
               "event_type": event_type}
        self.event_log.append(rec)
        self.events.setdefault(reason, []).append(t)

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
        loads_all = np.asarray(state.get('foot_load', [0.0] * 6),
                               dtype=float)
        for leg in range(LEG_COUNT):
            prev_phi = float(prev_phases[leg]) % TWO_PI
            swing = prev_phi < math.pi
            stance = not swing
            expected = (1.0 if (stance and EXPECTED_LO < prev_phi
                                < EXPECTED_HI) else 0.0)
            nb = np.concatenate([loads_all[:leg], loads_all[leg + 1:]])
            ctx = ReflexContext(
                dt=dt, t=t, leg=leg, phase=prev_phi,
                swing=swing, stance=stance,
                contacts=leg_contacts[leg],
                expected_contact=expected,
                neighbor_loads=nb,
            )
            outs = {}
            tibia = leg_contacts[leg].get('tibia')
            if (tibia is not None and tibia.active and len(
                    self.tibia_trace) < 200):
                self.tibia_trace.append(
                    (round(t, 3), leg, tibia.kind,
                     round(tibia.duration_s, 3), int(swing)))
            if 'r1a' in self.enabled:
                outs['r1a'] = self.r1a[leg].update(ctx)
            if 'r1b' in self.enabled:
                outs['r1b'] = self.r1b[leg].update(ctx)
            if 'r3' in self.enabled:
                outs['r3'] = self.r3[leg].update(ctx)
                self._r3_max_int[leg] = max(self._r3_max_int[leg],
                                            self.r3[leg].integral)
            if 'r4' in self.enabled:
                outs['r4'] = self.r4[leg].update(ctx)
            contacts = leg_contacts[leg]
            for name, o in outs.items():
                event_types = self.event_metrics.observe(leg, name, o.reasons)
                if not o.reasons:
                    continue
                if name == 'r1a':
                    tibia = contacts.get('tibia')
                    pair = tibia.pair if tibia is not None else ()
                    kind = tibia.kind if tibia is not None else "none"
                    armed = None
                    cd = self.r1a[leg].cooldown_remaining(t)
                elif name == 'r1b':
                    foot = contacts.get('foot')
                    pair = foot.pair if foot is not None else ()
                    kind = foot.kind if foot is not None else "none"
                    armed = None
                    cd = max(0.0, (self.r1b[leg]._last_t
                                   + self.r1b[leg].cooldown - t))
                elif name == 'r4':
                    foot = contacts.get('foot')
                    pair = foot.pair if foot is not None else ()
                    kind = foot.kind if foot is not None else "none"
                    armed = None
                    cd = 0.0
                else:
                    foot = contacts.get('foot')
                    pair = foot.pair if foot is not None else ()
                    kind = foot.kind if foot is not None else "none"
                    armed = self.r3[leg].armed
                    cd = 0.0
                for reason, event_type in event_types.items():
                    self._log_event(t, leg, reason, pair, kind, prev_phi,
                                    armed=armed, cooldown_remaining=cd,
                                    event_type=event_type)
            out = mix_reflex_outputs(
                list(outs.values()),
                joint_delta_limit=np.array([0.3, 0.4, 0.4]),
                phase_delta_limit=0.5,
            )
            if not self.apply_response:
                continue
            if out.speed_scale != 1.0:
                # замедление фазы ноги (не заморозка): масштабируем
                # уже сделанное _update_phases приращение
                cur = float(self.phases[leg]) % TWO_PI
                dphi = (cur - prev_phi) % TWO_PI
                self.phases[leg] = (prev_phi + dphi * out.speed_scale) \
                    % TWO_PI
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


def build_wall(xml_path, height):
    src = open(xml_path).read()
    m = re.search(r'<geom name="floor".*?/>', src, flags=re.S)
    wall = ('<geom name="wire" type="box" size="0.002 0.30 '
            f'{height / 2.0}" pos="0.5 0 {height / 2.0}" '
            'friction="0.8 0.005 0.0001"/>')
    src = src.replace(m.group(0), m.group(0) + '\n' + wall)
    return mujoco.MjModel.from_xml_string(src)


def build_gap(xml_path, gap=(0.60, 0.64), depth=0.012):
    src = open(xml_path).read()
    m = re.search(r'<geom name="floor".*?/>', src, flags=re.S)
    x1, x2 = gap
    lhx, lcx = (x1 + 10.0) / 2.0, (x1 - 10.0) / 2.0
    rhx, rcx = (10.0 - x2) / 2.0, (x2 + 10.0) / 2.0
    rz = -0.025 - depth
    terrain = (
        f'<geom name="plate_l" type="box" size="{lhx} 10 0.025" '
        f'pos="{lcx} 0 -0.025" friction="0.8 0.005 0.0001"/>\n'
        f'<geom name="plate_r" type="box" size="{rhx} 10 0.025" '
        f'pos="{rcx} 0 {rz}" friction="0.8 0.005 0.0001"/>')
    src = src.replace(m.group(0), terrain)
    return mujoco.MjModel.from_xml_string(src)


def run(model, make_ctrl, pipeline, duration=20.0, label="",
        expected_no_reflex=False, observer=None):
    """Measure a trial; only an explicit no-reflex oracle labels false events."""
    data = mujoco.MjData(model)
    data.qpos[2] += 0.012
    mujoco.mj_forward(model, data)
    foot_ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM,
                                  f'foot{i}') for i in range(6)]
    jr = np.asarray(model.jnt_range[1:19], dtype=float)
    ctrl = make_ctrl()
    ctrl.control_dt = CONTROL_DT
    ctrl.reset()
    ctrl.set_command("GO", 0.0)
    fell = False
    t = 0.0
    dt = model.opt.timestep
    n_self = 0
    min_foot_z = 9.0
    body_metrics = BodyMetrics()
    x_first_search = None
    if observer is not None:
        observer(model, data)
    while t < duration:
        lc = pipeline.update(data)
        n_self += len(pipeline.last_self_pairs)
        loads = [lc[i]['foot'].normal_force for i in range(6)]
        fc = [1 if lc[i]['foot'].active else 0 for i in range(6)]
        tc = [1 if lc[i]['tibia'].active else 0 for i in range(6)]
        durs = [lc[i]['foot'].duration_s for i in range(6)]
        fpos = np.asarray([data.geom_xpos[f] for f in foot_ids])
        fz = [float(p[2] - 0.016) for p in fpos]
        if t >= 1.0:
            min_foot_z = min(min_foot_z, min(fz))
            body_metrics.observe(data.qpos[2], data.qpos[3:7])
            if x_first_search is None and hasattr(ctrl, 'r3') \
                    and any(r.t_first_search is not None for r in ctrl.r3):
                x_first_search = float(data.qpos[0])
        state = {"dt": dt, "t": t,
                 "qpos": data.qpos[7:].copy(), "qvel": data.qvel[6:].copy(),
                 "body_pos": data.qpos[0:3].copy(),
                 "body_quat": data.qpos[3:7].copy(),
                 "body_angvel": data.qvel[3:6].copy(),
                 "foot_contact": fc, "tibia_contact": tc,
                 "foot_load": loads, "contact_duration": durs,
                 "foot_z": fz, "foot_pos": fpos,
                 "joint_range": jr, "settling": t < 1.0,
                 "leg_contacts": lc}
        tg = ctrl.step(t, state)
        data.ctrl[:] = tg
        mujoco.mj_step(model, data)
        if observer is not None:
            observer(model, data)
        if data.qpos[2] < 0.10:
            fell = True
        t += dt
    if t >= 1.0:
        body_metrics.observe(data.qpos[2], data.qpos[3:7])
    counts = {k: len(v) for k, v in getattr(ctrl, 'events', {}).items()}
    res = {'ctrl': label, 'x': round(float(data.qpos[0]), 3),
           'metrics_schema_version': 2,
           'fell': int(fell),
           'events': counts, 'self_contacts': n_self,
           'min_foot_z_mm': round(1000.0 * min_foot_z, 1),
           'net_progress': (round(float(data.qpos[0])
                                  - (x_first_search or 0.0), 3)
                            if x_first_search is not None else None)}
    res.update(body_metrics.summary())
    event_metrics = getattr(ctrl, 'event_metrics', EventMetrics())
    res.update(event_metrics.summary(expected_no_reflex=expected_no_reflex))
    if hasattr(ctrl, 'r3'):
        tf = [r.t_first_search for r in ctrl.r3
              if r.t_first_search is not None]
        res['time_to_first_search_s'] = (round(min(tf), 3) if tf else None)
        res['search_duration_ms'] = round(
            1000.0 * max(r.search_total for r in ctrl.r3), 1)
        res['ground_found'] = any(r.ground_found for r in ctrl.r3)
        res['n_searches'] = sum(r.n_searches for r in ctrl.r3)
    if hasattr(ctrl, 'r4'):
        holds = sum(r.n_holds for r in ctrl.r4)
        rels = sum(r.n_releases for r in ctrl.r4)
        hms = [v for r in ctrl.r4 for v in r.hold_ms]
        res['r4_holds'] = holds
        res['r4_releases'] = rels
        res['r4_hold_mean_ms'] = round(float(np.mean(hms)), 1) if hms \
            else 0.0
        res['r4_hold_max_ms'] = round(float(np.max(hms)), 1) if hms \
            else 0.0
        res['r4_chatter'] = sum(r.n_chatter for r in ctrl.r4)
    if hasattr(ctrl, 'tibia_trace') and ctrl.tibia_trace:
        res['tibia_trace'] = ctrl.tibia_trace[:12]
    return res


def pipeline_for(model):
    return ContactPipeline(model=model, geom_map=build_geom_map(model),
                           dt=CONTROL_DT, kind_by_geom=build_kind_map(model))


def main():
    xml_path = str(LAB_ROOT / 'models' / 'hexapod.xml')
    out = []
    # ---- FLAT: ложных 0 (R1b known-good, R1a off, R3 v2) ----
    mf = mujoco.MjModel.from_xml_path(xml_path)
    pf = pipeline_for(mf)
    for label, en, ar in [('FLAT_BASE', (), True),
                          ('FLAT_R1B', ('r1b',), True),
                          ('FLAT_R3V2', ('r3',), True)]:
        r = run(mf, lambda e=en, a=ar: Stage1Controller(
            freq=1.0, k_ret=0.30, enabled=e, apply_response=a), pf,
            label=label, expected_no_reflex=True)
        out.append(r)
    # ---- 12 мм ловушка ----
    m12 = build_wall(xml_path, 0.012)
    p12 = pipeline_for(m12)
    out.append(run(m12, lambda: SineContactController(freq=1.0, k_ret=0.30),
                   p12, label='W12_BASE'))
    out.append(run(m12, lambda: Stage1Controller(freq=1.0, k_ret=0.30,
                                                 enabled=('r1b',)), p12,
                   label='W12_R1B'))
    # ---- gap 12 мм: R3 v2 (тройка: BASE / detector-only / v2) ----
    mg = build_gap(xml_path)
    pg = pipeline_for(mg)
    out.append(run(mg, lambda: SineContactController(freq=1.0, k_ret=0.30),
                   pg, label='GAP_BASE'))
    out.append(run(mg, lambda: Stage1Controller(freq=1.0, k_ret=0.30,
                                                enabled=('r3',),
                                                apply_response=False), pg,
                   label='GAP_R3_DETECT'))
    out.append(run(mg, lambda: Stage1Controller(freq=1.0, k_ret=0.30,
                                                enabled=('r3',),
                                                apply_response=True), pg,
                   label='GAP_R3V2'))
    # ---- gap: скан глубины (ищем сценарий, где BASE теряет опору) ----
    # известно: 20 мм — BASE падает, R3 v2 спасает; здесь — combined + R4
    md = build_gap(xml_path, depth=0.020)
    pd = pipeline_for(md)
    out.append(run(md, lambda: SineContactController(freq=1.0, k_ret=0.30),
                   pd, label='GAP20_BASE'))
    out.append(run(md, lambda: Stage1Controller(
        freq=1.0, k_ret=0.30, enabled=('r1b', 'r3', 'r4'),
        apply_response=True), pd, label='GAP20_R1B_R3V2_R4'))
    # ---- flat + 12 мм с R4 (дребезг / не ломает known-good) ----
    mf2 = mujoco.MjModel.from_xml_path(xml_path)
    pf2 = pipeline_for(mf2)
    out.append(run(mf2, lambda: Stage1Controller(
        freq=1.0, k_ret=0.30, enabled=('r4',), apply_response=True), pf2,
        label='FLAT_R4', expected_no_reflex=True))
    m12b = build_wall(xml_path, 0.012)
    p12b = pipeline_for(m12b)
    out.append(run(m12b, lambda: Stage1Controller(
        freq=1.0, k_ret=0.30, enabled=('r1b', 'r4'),
        apply_response=True), p12b, label='W12_R1B_R4'))
    for r in out:
        print(json.dumps(r, ensure_ascii=False), flush=True)
    print('MATRIX_DONE', flush=True)


if __name__ == '__main__':
    main()
