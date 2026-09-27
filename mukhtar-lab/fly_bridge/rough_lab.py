"""Real seven-strip rough terrain using the existing Stage1 physics loop.

Geometry follows /tmp/fly_bridge/rough_terrain.py's executable values:
4,6,8,10,8,6,4 mm high, 24 mm long, centres 50 mm apart starting at x=.40 m.
This is a new measured Stage1 experiment, not reproduction of the older
rough_terrain.py controller/settling protocol.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import sys
import time

import mujoco

ROUGH_HEIGHTS = (.004, .006, .008, .010, .008, .006, .004)
ROUGH_X0 = .40
ROUGH_SPACING = .05


def build_rough(xml_path):
    source = Path(xml_path).read_text()
    floors = list(re.finditer(r'<geom\s+name="floor"(?=\s|/)[^>]*/>', source))
    if len(floors) != 1:
        raise ValueError('expected exactly one floor geom')
    floor = floors[0].group()
    terrain = [floor]
    for i, height in enumerate(ROUGH_HEIGHTS):
        terrain.append(
            f'<geom name="bump{i}" type="box" size="0.012 0.30 {height / 2}" '
            f'pos="{ROUGH_X0 + i * ROUGH_SPACING} 0 {height / 2}" '
            'friction="0.8 0.005 0.0001"/>')
    return mujoco.MjModel.from_xml_string(source.replace(floor, '\n'.join(terrain), 1))


def pipeline_for_rough(model):
    from stage1_matrix import CONTROL_DT, build_geom_map, build_kind_map
    from mukhtar.sensors.contact_pipeline import ContactPipeline
    kinds = build_kind_map(model)
    for i in range(len(ROUGH_HEIGHTS)):
        gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, f'bump{i}')
        if gid < 0:
            raise ValueError(f'missing terrain geom bump{i}')
        kinds[gid] = 'obstacle'
    return ContactPipeline(model=model, geom_map=build_geom_map(model),
                           dt=CONTROL_DT, kind_by_geom=kinds)


def run_pair(lab_root, output):
    lab_root, output = Path(lab_root).resolve(), Path(output)
    if output.exists():
        raise FileExistsError(output)
    sys.path.insert(0, str(lab_root))
    sys.path.insert(0, str(lab_root / 'fly_bridge'))
    from bench_jsonl import source_provenance, verify_import_origins
    from stage1_matrix import Stage1Controller, run
    from controllers.contact_reflex import SineContactController
    verify_import_origins()
    output.mkdir(parents=True, exist_ok=False)
    results = []
    for mode in ('BASE', 'R1b'):
        model = build_rough(lab_root / 'models/hexapod.xml')
        if mode == 'BASE':
            ctrl = SineContactController(freq=1.0, k_ret=.30)
        else:
            ctrl = Stage1Controller(freq=1.0, k_ret=.30, enabled=('r1b',), apply_response=True)
        started = time.perf_counter()
        result = run(model, lambda: ctrl, pipeline_for_rough(model), duration=20.0,
                     label=f'B04-rough_{mode}', expected_no_reflex=False)
        result.update(scenario='B04-rough', controller=mode, duration_s=20.0,
                      wall_time_s=time.perf_counter() - started)
        results.append(result)
        with (output / f'{mode}_events.jsonl').open('w') as events:
            for event in getattr(ctrl, 'event_log', []):
                events.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + '\n')
        print(json.dumps(result, ensure_ascii=False, allow_nan=False), flush=True)
    mujoco.mj_saveLastXML(str(output / 'model.xml'), model)
    (output / 'summary.json').write_text(json.dumps(results, ensure_ascii=False, indent=2,
                                                    allow_nan=False) + '\n')
    manifest = {
        'schema_version': 2, 'execution': 'local_mujoco',
        'created_at': datetime.now(timezone.utc).isoformat(),
        'scenario': 'B04-rough', 'duration_s': 20, 'settling_s': 1,
        'terrain': {'height_m': list(ROUGH_HEIGHTS), 'x0_m': ROUGH_X0,
                    'spacing_m': ROUGH_SPACING, 'strip_length_m': .024,
                    'half_width_m': .30, 'contact_kind': 'obstacle'},
        'scope': 'Stage1 analytic BASE vs R1b; no neural CPG or checkpoint',
        'false_events_oracle': None,
        'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'runtime': {name: importlib.metadata.version(name) for name in ('numpy', 'mujoco')},
        **source_provenance(),
        'artifacts': {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in sorted(output.iterdir()) if path.is_file()},
    }
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False,
                                                     indent=2, allow_nan=False) + '\n')
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    run_pair(args.lab, args.out)


if __name__ == '__main__':
    main()
