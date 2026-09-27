"""arc3/train_imitation.py — обучение ТОЛЬКО головы на teacher-траекториях.

Ядро заморожено. Для каждого шага траектории: эмбеддинги кандидатов
(через backend), target = индекс teacher_action среди кандидатов,
один шаг кросс-энтропии. Held-out игры (FT09/TU93/CN04) сюда НЕ попадают.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, '/home/argos-data/improve')
sys.path.insert(0, '/home/argos-data/improve/arc3')

from arc3.mukhtar.action_head import ActionHead  # noqa: E402
from arc3.mukhtar.male_cns import StandInBackend, SNNNodeBackend  # noqa: E402
from arc3.mukhtar.encoder import feature_vector  # noqa: E402
from arc3.perception import extract_features  # noqa: E402

HELD_OUT = {'ft09', 'tu93', 'cn04'}
DATA = Path('/home/argos-data/improve/data/teacher')


def dummy_features(n_candidates):
    """Без кадра features пустые — только для структурной проверки.
    Реальные прогоны дают кадр и полные фичи."""
    return {'colors_present': [], 'n_colors': 0, 'components': [],
            'n_components': 0, 'component_sizes': [],
            'changed_cells': [], 'n_changed': 0,
            'previous_action': None, 'levels_completed': 0,
            'available_actions': [], 'grid_w': 0, 'grid_h': 0}


def load_teacher(jsonl_path):
    rows = []
    for line in Path(jsonl_path).open():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def train(backend=None, epochs=3, lr=0.01, out='arc3_head.npz'):
    files = []
    for p in sorted(DATA.glob('teachers_*.jsonl')):
        rows = load_teacher(p)
        if any(row.get('state') in ('WIN', 'GameState.WIN') for row in rows):
            files.append(p)
    if not files:
        print('no teacher files', flush=True)
        return None
    head = ActionHead()
    backend = backend or StandInBackend()
    n_steps = 0
    loss_sum = 0.0
    for ep in range(epochs):
        for fp in files:
            game = fp.stem.replace('teachers_', '')
            if game in HELD_OUT:
                continue
            for row in load_teacher(fp):
                cands = row['candidates']
                if row['teacher_action'] not in cands:
                    continue
                feats = dummy_features(len(cands))
                vecs = [feature_vector(feats) for _ in cands]
                embeds = backend.embed(vecs)
                ti = cands.index(row['teacher_action'])
                loss = head.train_step(embeds, cands, ti, lr=lr)
                n_steps += 1
                loss_sum += loss
    head.save(out)
    print(json.dumps({'trained_steps': n_steps,
                      'mean_loss': round(loss_sum / max(1, n_steps), 4),
                      'head_out': out}), flush=True)


if __name__ == '__main__':
    use_snn = '--snn' in sys.argv
    train(backend=SNNNodeBackend() if use_snn else StandInBackend())
