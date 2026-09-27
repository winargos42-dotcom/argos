"""Execute the benchmark's real MuJoCo loop and export measured state."""
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import sys
import time
import zipfile

SPACE = Path(__file__).resolve().parent
LAB = SPACE / 'runtime' if (SPACE / 'runtime').is_dir() else SPACE.parent
sys.path.insert(0, str(LAB))
sys.path.insert(0, str(LAB / 'fly_bridge'))

SCENARIOS = ('B01-flat', 'B02-footcatch12', 'B03-gap20', 'B04-rough4_10')
MODES = {'BASE': (), 'R1b': ('r1b',), 'R3v2': ('r3',),
         'R1b+R3v2': ('r1b', 'r3'), 'R4': ('r4',)}


def _json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def run_trial(scenario, mode, duration=20.0, *, output):
    if scenario not in SCENARIOS or mode not in MODES:
        raise ValueError('Неизвестный сценарий или контроллер')
    if isinstance(duration, bool) or not math.isfinite(float(duration)) or not 2 <= float(duration) <= 20:
        raise ValueError('Длительность должна быть от 2 до 20 секунд')
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    import mujoco
    from bench_jsonl import source_provenance, verify_import_origins
    from stage1_matrix import Stage1Controller, build_gap, build_wall, pipeline_for, run
    from controllers.contact_reflex import SineContactController
    from rough_lab import build_rough, pipeline_for_rough
    verify_import_origins()
    output.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    xml = LAB / 'models' / 'hexapod.xml'
    if scenario == 'B02-footcatch12':
        model = build_wall(str(xml), 0.012)
    elif scenario == 'B03-gap20':
        model = build_gap(str(xml), depth=0.020)
    elif scenario == 'B04-rough4_10':
        model = build_rough(xml)
    else:
        model = mujoco.MjModel.from_xml_path(str(xml))
    mujoco.mj_saveLastXML(str(output / 'model.xml'), model)
    enabled = MODES[mode]
    ctrl = (Stage1Controller(freq=1.0, k_ret=0.30, enabled=enabled, apply_response=True)
            if enabled else SineContactController(freq=1.0, k_ret=0.30))
    feet = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, f'foot{i}') for i in range(6)]
    frames = []
    next_sample = 0.0
    kinematics = mujoco.MjData(model)

    def record(current_model, data):
        nonlocal next_sample
        if data.time + 1e-9 < next_sample and data.time < float(duration):
            return
        # Compute post-integration geometry in a separate buffer. Observation
        # must not modify the simulation's solver or next controller inputs.
        kinematics.qpos[:] = data.qpos
        mujoco.mj_kinematics(current_model, kinematics)
        frames.append({'time_s': round(float(data.time), 9),
                       'qpos': data.qpos.tolist(), 'qvel': data.qvel.tolist(),
                       'feet_xyz': kinematics.geom_xpos[feet].tolist()})
        next_sample = float(data.time) + 0.05

    pipeline = pipeline_for_rough(model) if scenario == 'B04-rough4_10' else pipeline_for(model)
    metrics = run(model, lambda: ctrl, pipeline, duration=float(duration),
                  label=f'{scenario}_{mode}', expected_no_reflex=scenario == 'B01-flat',
                  observer=record)
    metrics.update(scenario=scenario, controller=mode, duration_s=float(duration),
                   distance_m=metrics['x'], fell=bool(metrics['fell']))
    elapsed = time.perf_counter() - start
    _json(output / 'summary.json', metrics)
    for name, rows in (('trajectory.jsonl', frames), ('events.jsonl', getattr(ctrl, 'event_log', []))):
        with (output / name).open('w') as stream:
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + '\n')
    provenance = source_provenance()
    provenance['runner_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    build_info = LAB / 'build_info.json'
    if build_info.is_file():
        provenance['deployment'] = json.loads(build_info.read_text())
    manifest = {'schema_version': 2, 'status': 'complete', 'execution': 'live_mujoco',
                'created_at': datetime.now(timezone.utc).isoformat(),
                'scenario': scenario, 'controller': mode, 'duration_s': float(duration),
                'wall_time_s': round(elapsed, 4), 'settling_s': 1.0,
                'seed': None, 'seed_policy': 'Deterministic analytic controllers; no stochastic inputs',
                'checkpoint_sha256': None, 'checkpoint_reason': 'Analytic controllers',
                'telemetry_kind': 'sampled_kinematics_and_reflex_events',
                'sample_interval_s': 0.05, 'frames': len(frames),
                'runtime': {**{name: importlib.metadata.version(name) for name in ('numpy', 'mujoco')},
                            'python': platform.python_version()}, **provenance,
                'artifacts': {name: hashlib.sha256((output / name).read_bytes()).hexdigest()
                              for name in ('model.xml', 'summary.json', 'trajectory.jsonl', 'events.jsonl')}}
    _json(output / 'manifest.json', manifest)
    archive = output / 'run.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
        for name in list(manifest['artifacts']) + ['manifest.json']:
            bundle.write(output / name, arcname=name)
    return {'metrics': metrics, 'manifest': manifest, 'trajectory': frames, 'archive': str(archive)}


def plot_trajectory(result):
    import matplotlib.pyplot as plt
    import numpy as np
    frames = result['trajectory']
    times = np.asarray([frame['time_s'] for frame in frames])
    position = np.asarray([frame['qpos'][:3] for frame in frames])
    feet = np.asarray([frame['feet_xyz'] for frame in frames])
    figure, axes = plt.subplots(1, 3, figsize=(12, 3.4))
    axes[0].plot(position[:, 0], position[:, 1])
    axes[0].set(xlabel='x, m', ylabel='y, m', title='Measured body path')
    axes[1].plot(times, position[:, 2])
    axes[1].set(xlabel='t, s', ylabel='z, m', title='Body height')
    for leg in range(6):
        axes[2].plot(times, feet[:, leg, 2], label=f'leg {leg}')
    axes[2].set(xlabel='t, s', ylabel='z, m', title='Foot centres')
    axes[2].legend(fontsize=6)
    figure.tight_layout()
    plt.close(figure)
    return figure
