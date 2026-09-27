import hashlib
import importlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest


def module():
    assert importlib.util.find_spec('experiment_data'), 'No verified pre-action dataset loader'
    return importlib.import_module('experiment_data')


def write_recording(root):
    frames=np.stack([np.full((64,64),color,dtype=np.uint8) for color in range(5)])
    np.savez_compressed(root/'frames.npz',frames=frames)
    rows=[]
    for i,levels in enumerate((1,5,6,7)):
        rows.append({'step':i+1,'action_key':f'A{i+1}','action_id':i+1,
                     'data':None,'available_before':[1,2,3,4],
                     'before_hash':hashlib.sha256(frames[i].tobytes()).hexdigest(),
                     'after_hash':hashlib.sha256(frames[i+1].tobytes()).hexdigest(),
                     'levels_completed':levels})
    (root/'actions.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in rows))
    (root/'manifest.json').write_text(json.dumps({'execution':'offline_local_game',
       'artifacts_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest()
                          for name in ('frames.npz','actions.jsonl')}}))
    return frames,rows


def test_dataset_uses_pre_action_frames_and_previous_level_for_split(tmp_path):
    frames,rows=write_recording(tmp_path)
    data=module().load_examples(tmp_path)
    assert data['levels'].tolist()==[1,2,6,7]
    assert data['targets'].tolist()==[0,1,2,3]
    train,held=module().level_split(data)
    assert train.tolist()==[0,1] and held.tolist()==[2,3]
    np.testing.assert_array_equal(data['features'][0],module().encode_state(frames[0]))
    assert not np.array_equal(data['features'][0],module().encode_state(frames[1]))
    assert not set(data['frame_hashes'][train]) & set(data['frame_hashes'][held])


def test_corrupt_raw_artifact_is_rejected(tmp_path):
    write_recording(tmp_path)
    with (tmp_path/'actions.jsonl').open('a') as stream:
        stream.write('{}\n')
    with pytest.raises(ValueError,match='SHA256'):
        module().load_examples(tmp_path)


def test_encoder_preserves_spatial_colour_and_causal_previous_action():
    m=module(); frame=np.zeros((64,64),dtype=np.uint8)
    left=frame.copy();left[:8,:8]=9
    right=frame.copy();right[:8,-8:]=9
    assert not np.array_equal(m.encode_state(left),m.encode_state(right))
    assert not np.array_equal(m.encode_state(left,previous_action='A1'),
                              m.encode_state(left,previous_action='A2'))
    assert np.isfinite(m.encode_state(left)).all()


def test_split_rejects_reused_frames_between_train_and_heldout():
    with pytest.raises(ValueError,match='overlap'):
        module().level_split({'levels':np.array([1,6]),'frame_hashes':np.array(['same','same'])})
