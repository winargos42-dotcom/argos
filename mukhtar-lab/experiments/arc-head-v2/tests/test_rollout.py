import importlib
import importlib.util
import json
from pathlib import Path

import numpy as np

from action_head import ActionHead
from experiment_data import FEATURE_DIM


def test_real_rollouts_use_equal_start_and_legal_actions(tmp_path):
    assert importlib.util.find_spec('evaluate_policies'),'No actual-game head evaluator'
    module=importlib.import_module('evaluate_policies')
    checkpoint=tmp_path/'head.npz';ActionHead(embed_dim=FEATURE_DIM).save(checkpoint)
    a=module.run_game('ls20-9607627b','search',tmp_path/'search',budget=8)
    b=module.run_game('ls20-9607627b','interaction',tmp_path/'interaction',budget=8,checkpoint=checkpoint)
    assert a['actions']==b['actions']==8
    assert a['initial_frame_sha256']==b['initial_frame_sha256']
    assert a['budget']==b['budget']==8
    assert b['backend']=='native_frame_features'
    assert b['checkpoint_sha256']
    for policy in ('search','interaction'):
        rows=[json.loads(line) for line in (tmp_path/policy/'actions.jsonl').read_text().splitlines()]
        assert all(row['action_id'] in row['available_before'] for row in rows)
        frames=np.load(tmp_path/policy/'frames.npz')['frames']
        assert len(frames)==9
    assert not a['won'] and not b['won']
