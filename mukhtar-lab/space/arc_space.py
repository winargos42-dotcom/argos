"""Portable Space API: run_arc(game_id, max_actions, mode='search').

Returns measured summary, actual-frame Figure, downloadable ZIP. The game runs
in a bounded subprocess so its offline socket guard cannot affect Gradio.
Requires Python >=3.12 with arc-agi==0.9.9 / arcengine==0.9.3 in that process.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

import numpy as np

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'arc_runtime'
GAMES = ('ls20-9607627b', 'cd82-fb555c5d', 'vc33-5430563c',
         'sc25-635fd71a', 'ft09-0d8bbf25')
MODES = ('search', 'route_replay')
# ARC SDK rendering.py palette, MIT ARC Prize Foundation 2026.
PALETTE = ('#FFFFFF', '#CCCCCC', '#999999', '#666666', '#333333', '#000000',
           '#E53AA3', '#FF7BCC', '#F93C31', '#1E93FF', '#88D8F1', '#FFDC00',
           '#FF851B', '#921231', '#4FCC30', '#A356D6')


def plot_frames(frames):
    from matplotlib.colors import ListedColormap
    from matplotlib.figure import Figure
    figure = Figure(figsize=(10, 3.5), constrained_layout=True)
    axes = figure.subplots(1, 3)
    last = len(frames)-1
    for axis, index, title in zip(axes, (0, last//2, last), ('Initial','Middle','Final')):
        axis.imshow(frames[index], cmap=ListedColormap(PALETTE), vmin=0, vmax=15,
                    interpolation='nearest')
        axis.set_title(f'{title}: after {index} actions')
        axis.set_axis_off()
    return figure


def run_arc(game_id='ls20-9607627b', max_actions=200, mode='search', *, output_dir=None):
    if game_id not in GAMES or mode not in MODES:
        raise ValueError('Unknown local game or mode')
    if isinstance(max_actions, bool) or not float(max_actions).is_integer() or not 1 <= float(max_actions) <= 400:
        raise ValueError('Action budget must be an integer in [1,400]')
    if mode == 'route_replay' and game_id != 'ls20-9607627b':
        raise ValueError('The recorded route is only available for LS20')
    executable = os.environ.get('ARC_OFFLINE_PYTHON', sys.executable)
    if executable == sys.executable and sys.version_info < (3,12):
        raise RuntimeError('ARC SDK requires Python >=3.12; run this Space on Python 3.12+')
    root = Path(output_dir) if output_dir is not None else Path(tempfile.mkdtemp(prefix='mukhtar-arc-'))
    root.mkdir(parents=True, exist_ok=True)
    output = root / 'run'
    command = [executable, str(ROOT / 'arc_offline.py'),
               '--environments', str(ASSETS / 'environment_files'),
               '--source', str(ASSETS / 'arc3'), '--out', str(output),
               '--game', game_id, '--budget', str(int(max_actions)), '--mode', mode]
    if mode == 'route_replay':
        command += ['--route', str(ASSETS / 'ls20_route.jsonl')]
    environment = {**os.environ, 'PYTHON_DOTENV_DISABLED':'1',
                   'OPERATION_MODE':'offline', 'PYTHONDONTWRITEBYTECODE':'1'}
    process = subprocess.run(command, cwd=root, env=environment, capture_output=True,
                             text=True, timeout=75, check=False)
    if process.returncode:
        raise RuntimeError('Offline game run failed: '+process.stderr[-2000:])
    manifest = json.loads((output / 'manifest.json').read_text())
    for name, digest in manifest['artifacts_sha256'].items():
        path = output / name
        if path.parent != output or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError('ARC output integrity check failed')
    summary = json.loads((output / 'summary.json').read_text())
    with np.load(output / 'frames.npz', allow_pickle=False) as bundle:
        frames = bundle['frames']
    figure = plot_frames(frames)
    archive = root / 'arc-run.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
        for name in list(manifest['artifacts_sha256']) + ['manifest.json']:
            bundle.write(output / name, arcname=name)
    return summary, figure, str(archive)
