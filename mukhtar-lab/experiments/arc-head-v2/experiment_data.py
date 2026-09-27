"""Verified native-frame dataset and causal, non-neural ARC state features."""
import hashlib
import json
from pathlib import Path
import re

import numpy as np

FEATURE_DIM=8*8*16+8*8+8
FEATURE_PROTOCOL='8x8 spatial colour occupancy + causal changed fraction + previous action; no level/step input'


def _frame(frame):
    frame=np.asarray(frame)
    if frame.shape!=(64,64) or not np.isfinite(frame).all() or np.any(frame<0) or np.any(frame>15):
        raise ValueError('Expected native 64x64 colours 0..15')
    if not np.equal(frame,np.floor(frame)).all():
        raise ValueError('Colours must be integer IDs')
    return frame.astype(np.uint8)


def encode_state(frame,previous_frame=None,previous_action=None):
    frame=_frame(frame)
    onehot=np.eye(16,dtype=float)[frame]
    occupancy=onehot.reshape(8,8,8,8,16).mean(axis=(1,3)).reshape(-1)
    changed=np.zeros(64)
    if previous_frame is not None:
        changed=(frame!=_frame(previous_frame)).reshape(8,8,8,8).mean(axis=(1,3)).reshape(-1)
    previous=np.zeros(8)
    if previous_action is not None:
        match=re.fullmatch(r'A([1-8])(?::\d{1,2},\d{1,2})?',str(previous_action))
        if match is None:
            raise ValueError('Invalid previous action')
        previous[int(match[1])-1]=1
    return np.concatenate([occupancy,changed,previous])


def load_examples(recording):
    recording=Path(recording)
    manifest=json.loads((recording/'manifest.json').read_text())
    if manifest.get('execution')!='offline_local_game':
        raise ValueError('Expected measured offline game recording')
    for name in ('frames.npz','actions.jsonl'):
        digest=hashlib.sha256((recording/name).read_bytes()).hexdigest()
        if digest!=manifest['artifacts_sha256'].get(name):
            raise ValueError('SHA256 mismatch for '+name)
    with np.load(recording/'frames.npz',allow_pickle=False) as archive:
        frames=archive['frames']
    rows=[json.loads(line) for line in (recording/'actions.jsonl').read_text().splitlines() if line.strip()]
    if not 1<=len(rows)<=800 or frames.shape!=(len(rows)+1,64,64):
        raise ValueError('Frame/action count mismatch or excessive dataset')
    features=[];targets=[];levels=[];hashes=[]
    level=1
    for i,row in enumerate(rows):
        before=hashlib.sha256(_frame(frames[i]).tobytes()).hexdigest()
        after=hashlib.sha256(_frame(frames[i+1]).tobytes()).hexdigest()
        if row['step']!=i+1 or row['before_hash']!=before or row['after_hash']!=after:
            raise ValueError('Action/frame alignment mismatch')
        tag=row['action_key']
        if tag not in ('A1','A2','A3','A4') or row['action_id']!=int(tag[1:]):
            raise ValueError('LS20 training requires directional teacher actions')
        if set(row['available_before'])!={1,2,3,4}:
            raise ValueError('Unexpected teacher legal action set')
        features.append(encode_state(frames[i],frames[i-1] if i else None,
                                     rows[i-1]['action_key'] if i else None))
        targets.append(int(tag[1:])-1);levels.append(level);hashes.append(before)
        observed_levels=int(row['levels_completed'])
        if observed_levels<level-1:
            raise ValueError('Recording reset/level regression is not allowed in split')
        level=observed_levels+1
    return {'features':np.stack(features),'targets':np.array(targets),
            'levels':np.array(levels),'frame_hashes':np.array(hashes),
            'source_manifest':manifest,'rows':rows}


def level_split(data):
    levels=np.asarray(data['levels'])
    train=np.flatnonzero((levels>=1)&(levels<=5))
    held=np.flatnonzero((levels>=6)&(levels<=7))
    if not len(train) or not len(held) or len(train)+len(held)!=len(levels):
        raise ValueError('Expected nonempty levels 1..5 train and 6..7 withheld')
    if set(data['frame_hashes'][train]) & set(data['frame_hashes'][held]):
        raise ValueError('Raw frame overlap across train/withheld split')
    return train,held
