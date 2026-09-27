"""Run the actual public-lab engines across all exposed scenarios and modes."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out', type=Path, required=True, help='New result directory')
args = parser.parse_args()
SPACE = Path(__file__).resolve().parents[1] / 'space'
sys.path.insert(0, str(SPACE))
from live_locomotion import SCENARIOS, MODES, run_trial
from prc_lab import run_prc, prc_json
from arc_space import GAMES, run_arc

ROOT = args.out.resolve()
ROOT.mkdir(exist_ok=False)
summaries = {'locomotion': [], 'prc': [], 'arc': []}
started = time.time()
for scenario in SCENARIOS:
    for mode in MODES:
        result = run_trial(scenario, mode, 20, output=ROOT / 'locomotion' / f'{scenario}_{mode}')
        assert result['manifest']['status'] == 'complete'
        for name, digest in result['manifest']['artifacts'].items():
            source = Path(result['archive']).parent / name
            assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
        row = result['metrics']
        summaries['locomotion'].append(row)
        print(json.dumps({'phase':'locomotion','scenario':scenario,'mode':mode,
                          'distance_m':row['distance_m'],'fell':row['fell'],
                          'trigger_count':row['trigger_count']}), flush=True)

(ROOT / 'prc').mkdir()
for drive in (0.4, 0.8, 1.2, 1.6):
    for target in ('E1', 'I1', 'I2'):
        result = run_prc(drive, target, 2.0)
        (ROOT / 'prc' / f'{drive}_{target}.json').write_text(prc_json(result) + '\n')
        row = {'drive':drive,'target':target,'status':result['status'],
               'period_ticks':result['baseline']['period_ticks'],
               'shift_ticks':[r['shift_ticks'] for r in result['trials']]}
        summaries['prc'].append(row)
        print(json.dumps({'phase':'prc',**row}), flush=True)

for game in GAMES:
    summary, figure, archive = run_arc(game, 400, 'search', output_dir=ROOT / 'arc' / game)
    figure.savefig(Path(archive).parent / 'frames.png', dpi=130)
    summaries['arc'].append(summary)
    print(json.dumps({'phase':'arc','game':game,'actions':summary['actions'],
                      'levels':summary['levels_completed'],'final_state':summary['final_state']}), flush=True)

(ROOT / 'summary.json').write_text(json.dumps(summaries, indent=2, allow_nan=False) + '\n')
manifest = {'status':'complete','suite':'all exposed locomotion modes, PRC drives/targets, ARC search games',
            'wall_time_s':time.time()-started,
            'scope':'Single deterministic trial per configuration; no statistical or neural-control claims',
            'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'artifacts':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(ROOT.rglob('*')) if p.is_file()}}
(ROOT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'status':'complete','counts':{k:len(v) for k,v in summaries.items()},
                  'wall_time_s':manifest['wall_time_s']}), flush=True)
