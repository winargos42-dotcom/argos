"""Verify saved trial bytes, telemetry counts and replayed MuJoCo kinematics."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import mujoco
import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--results', type=Path, required=True)
parser.add_argument('--report', type=Path, required=True, help='New verification report')
args = parser.parse_args()
if args.report.exists():
    raise FileExistsError(args.report)
ROOT = args.results.resolve()
manifest = json.loads((ROOT / 'manifest.json').read_text())
assert manifest['status'] == 'complete'
for name, digest in manifest['artifacts'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
checked = []
for directory in sorted((ROOT / 'locomotion').iterdir()):
    summary = json.loads((directory / 'summary.json').read_text())
    provenance = json.loads((directory / 'manifest.json').read_text())
    for name, digest in provenance['artifacts'].items():
        assert hashlib.sha256((directory / name).read_bytes()).hexdigest() == digest
    frames = [json.loads(line) for line in (directory / 'trajectory.jsonl').read_text().splitlines()]
    events = [json.loads(line) for line in (directory / 'events.jsonl').read_text().splitlines()]
    assert len(frames) == provenance['frames']
    assert abs(frames[-1]['time_s'] - summary['duration_s']) <= 0.0021
    assert summary['distance_m'] == round(frames[-1]['qpos'][0], 3)
    assert summary['trigger_count'] == sum(row['event_type'] == 'trigger' for row in events)
    if summary['scenario'] == 'B01-flat':
        assert summary['false_events'] == summary['trigger_count']
    else:
        assert summary['false_events'] is None
    model = mujoco.MjModel.from_xml_path(str(directory / 'model.xml'))
    data = mujoco.MjData(model)
    feet = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, f'foot{i}') for i in range(6)]
    maximum_error = 0.0
    for frame in frames:
        assert all(math.isfinite(v) for v in frame['qpos'] + frame['qvel'])
        data.qpos[:] = frame['qpos']
        mujoco.mj_kinematics(model, data)
        maximum_error = max(maximum_error, float(np.max(np.abs(data.geom_xpos[feet] - frame['feet_xyz']))))
    assert maximum_error < 1e-12
    checked.append({'run':directory.name,'frames':len(frames),'events':len(events),
                    'max_foot_replay_error_m':maximum_error})
report = {'status':'passed','trial_count':len(checked),'hashed_artifacts':len(manifest['artifacts']),
          'checks':['SHA256','final time and displacement','raw event counts','false-event scope','finite states','foot kinematics from XML and qpos'],
          'trials':checked}
args.report.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
