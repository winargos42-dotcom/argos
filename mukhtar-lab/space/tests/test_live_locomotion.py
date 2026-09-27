"""Live runs must contain MuJoCo state, never a relabelled stored summary."""
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import sys
import zipfile

import pytest

SPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SPACE))


def runner():
    assert importlib.util.find_spec('live_locomotion') is not None, 'No live MuJoCo runner'
    return importlib.import_module('live_locomotion').run_trial


def test_live_motion_has_consistent_raw_state_and_verified_artifacts(tmp_path):
    output = tmp_path / 'trial'
    result = runner()('B01-flat', 'BASE', duration=2.0, output=output)
    frames = [json.loads(line) for line in (output / 'trajectory.jsonl').read_text().splitlines()]
    assert frames[0]['time_s'] == 0
    assert 2 <= frames[-1]['time_s'] < 2.01
    assert len(frames) >= 40
    assert frames[-1]['qpos'][0] > frames[0]['qpos'][0] + 0.04
    assert len(frames[-1]['qpos']) == 25
    assert len(frames[-1]['feet_xyz']) == 6
    assert abs(frames[-1]['qpos'][0] - result['metrics']['distance_m']) < 0.00051
    manifest = json.loads((output / 'manifest.json').read_text())
    assert manifest['execution'] == 'live_mujoco'
    assert manifest['telemetry_kind'] == 'sampled_kinematics_and_reflex_events'
    assert manifest['runtime']['mujoco']
    assert manifest['source_files']
    for name, digest in manifest['artifacts'].items():
        assert hashlib.sha256((output / name).read_bytes()).hexdigest() == digest
    with zipfile.ZipFile(result['archive']) as archive:
        assert json.loads(archive.read('manifest.json')) == manifest
        assert archive.read('trajectory.jsonl') == (output / 'trajectory.jsonl').read_bytes()


def test_footcatch_live_run_reproduces_physical_reflex_benefit(tmp_path):
    run = runner()
    base = run('B02-footcatch12', 'BASE', duration=20, output=tmp_path / 'base')['metrics']
    reflex = run('B02-footcatch12', 'R1b', duration=20, output=tmp_path / 'reflex')['metrics']
    assert base['distance_m'] == pytest.approx(0.486, abs=0.002)
    assert reflex['distance_m'] == pytest.approx(1.238, abs=0.002)
    assert reflex['trigger_count'] == 9
    assert reflex['false_events'] is None
    assert not reflex['fell']


@pytest.mark.parametrize('scenario,mode,duration', [
    ('../../etc', 'BASE', 2), ('B01-flat', 'unknown', 2),
    ('B01-flat', 'BASE', float('nan')), ('B01-flat', 'BASE', 21),
    ('B01-flat', 'BASE', 1),
])
def test_invalid_live_request_creates_no_artifacts(tmp_path, scenario, mode, duration):
    output = tmp_path / 'invalid'
    with pytest.raises(ValueError):
        runner()(scenario, mode, duration=duration, output=output)
    assert not output.exists()


def test_existing_output_is_not_replaced(tmp_path):
    run = runner()
    (tmp_path / 'sentinel').write_text('keep')
    with pytest.raises(FileExistsError):
        run('B01-flat', 'BASE', duration=2, output=tmp_path)
    assert (tmp_path / 'sentinel').read_text() == 'keep'


def test_live_ui_returns_measured_metrics_plot_and_download():
    app = importlib.import_module('app')
    assert hasattr(app, 'run_locomotion'), 'Space has no real run action'
    metrics, plot, download = app.run_locomotion('B01-flat', 'BASE', 2)
    assert metrics['execution'] == 'live_mujoco'
    assert metrics['result']['distance_m'] > 0.04
    assert plot is not None
    with zipfile.ZipFile(download) as archive:
        assert json.loads(archive.read('manifest.json'))['duration_s'] == 2
