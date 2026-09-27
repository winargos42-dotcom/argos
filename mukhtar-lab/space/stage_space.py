"""Build a self-contained HF Space from this checkout; no duplicated runtime sources in Git."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess


def stage(destination):
    space = Path(__file__).resolve().parent
    lab = space.parent
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError(destination)
    shutil.copytree(space, destination, ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache', 'tests'))
    runtime = destination / 'runtime'
    runtime.mkdir()
    for directory in ('controllers', 'models', 'mukhtar', 'fly_bridge'):
        shutil.copytree(lab / directory, runtime / directory,
                        ignore=shutil.ignore_patterns('__pycache__', 'tests', '*.log', '*.npz'))
    shutil.copy2(lab / 'pyproject.toml', runtime / 'pyproject.toml')
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=lab, text=True).strip()
    dirty = bool(subprocess.check_output(['git', 'status', '--porcelain', '--', '.'], cwd=lab, text=True).strip())
    (runtime / 'build_info.json').write_text(json.dumps(
        {'git_revision': revision, 'git_dirty': dirty,
         'repository': 'https://github.com/winargos42-dotcom/argos'}, indent=2) + '\n')
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    print(stage(parser.parse_args().out))
