"""Actual local-game A/B: unchanged SearchRanker versus trained interaction head.

Same seed, start, candidate generator, tabu semantics and action budget.
No route file is read during rollout. The backend is explicitly native features,
not SNN inference. Run as a standalone process because the offline guard is global.
"""
import argparse
from datetime import datetime,timezone
import hashlib
import importlib.metadata
import json
import logging
from pathlib import Path
import platform
import time

import numpy as np

from action_head import ActionHead
from experiment_data import FEATURE_DIM
from interaction_ranker import InteractionRanker
from protocol import arc_offline as protocol

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'protocol/arc_runtime'
GAMES=('ls20-9607627b','cd82-fb555c5d','vc33-5430563c','sc25-635fd71a','ft09-0d8bbf25')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path,value):
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')


def run_game(game_id,policy,output,budget=400,checkpoint=None):
    if game_id not in GAMES or policy not in ('search','interaction'):
        raise ValueError('Unknown game/policy')
    if type(budget) is not int or not 1<=budget<=400:
        raise ValueError('budget must be integer 1..400')
    output=Path(output)
    if output.exists():
        raise FileExistsError(output)
    head=None
    if policy=='interaction':
        if checkpoint is None:
            raise ValueError('Interaction evaluation requires a trained checkpoint')
        head=ActionHead(embed_dim=FEATURE_DIM);head.load(checkpoint)
    output.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter()
    with protocol.offline_guard():
        import arc_agi
        search=protocol._load(ASSETS/'arc3/search_policy.py','_fixed_search')
        memory=protocol._load(ASSETS/'arc3/world_memory.py','_fixed_memory')
        candidates=protocol._load(ASSETS/'arc3/candidate_generator.py','_fixed_candidates')
        world=memory.WorldMemory()
        ranker=search.SearchRanker(world) if head is None else InteractionRanker(head,world)
        logger=logging.getLogger('arc-head-evaluation');logger.setLevel(logging.WARNING)
        arcade=arc_agi.Arcade(arc_api_key='offline-local',operation_mode=arc_agi.OperationMode.OFFLINE,
                             environments_dir=str(ASSETS/'environment_files'),
                             recordings_dir=str(output/'sdk-recordings'),logger=logger)
        env=arcade.make(game_id,seed=0,render_mode=None,save_recording=False)
        if env is None or type(env).__name__!='LocalEnvironmentWrapper':
            raise RuntimeError('Expected a real local game')
        obs=env.reset();frame=protocol._frame(obs).copy();frames=[frame.copy()]
        initial=protocol.frame_hash(frame);current_hash=initial;unique={initial}
        previous_frame=None;previous_action=None
        rows=[];inference=[];levels=int(obs.levels_completed);stop='budget_exhausted'
        for step in range(1,budget+1):
            if time.perf_counter()-started>=60:
                stop='wall_time_limit';break
            available=[int(value) for value in obs.available_actions]
            cands=candidates.candidate_list(available,protocol._tokens(frame))
            if not cands:
                stop='no_candidates';break
            before=time.perf_counter()
            if head is None:
                ordered=ranker.rank(current_hash,cands,features=None)
            else:
                ordered=ranker.rank_frame(current_hash,cands,frame,available,
                                           previous_frame,previous_action)
            inference.append((time.perf_counter()-before)*1000)
            key,action,data=ordered[0]
            if action.value not in available:
                raise RuntimeError('Policy proposed an unavailable action')
            obs=env.step(action,data=data)
            next_frame=protocol._frame(obs).copy();next_hash=protocol.frame_hash(next_frame)
            changed=next_hash!=current_hash
            ranker.record(current_hash,key,changed)
            rows.append({'step':step,'action_key':key,'action_id':int(action.value),'data':data,
                         'available_before':available,'before_hash':current_hash,'after_hash':next_hash,
                         'levels_completed':int(obs.levels_completed),'state_after':obs.state.name,
                         'frame_changed':changed})
            frames.append(next_frame);unique.add(next_hash);levels=max(levels,int(obs.levels_completed))
            previous_frame,frame=frame,next_frame;previous_action=key;current_hash=next_hash
            if obs.state.name in ('WIN','GAME_OVER','LOSE','FINISHED'):
                stop='terminal_state';break
        closed=arcade.close_scorecard()
        if closed is not None:
            dump(output/'local_scorecard.json',closed.model_dump(mode='json',exclude={'api_key'}))
    result={'game_id':game_id,'policy':policy,'backend':'native_frame_features' if head is not None else 'search_rules',
            'execution':'offline_local_game','seed':0,'budget':budget,'actions':len(rows),
            'levels_completed':levels,'final_state':obs.state.name,'won':obs.state.name=='WIN',
            'unique_frames':len(unique),'unchanged_frame_actions':sum(not row['frame_changed'] for row in rows),
            'initial_frame_sha256':initial,'final_frame_sha256':current_hash,'stop_reason':stop,
            'inference_ms_mean':float(np.mean(inference)) if inference else None,
            'wall_time_s':time.perf_counter()-started,
            'checkpoint_sha256':sha(checkpoint) if head is not None else None,
            'training_scope':'LS20 levels1..5 only; no SNN; click actions untrained' if head is not None else None}
    dump(output/'summary.json',result)
    np.savez_compressed(output/'frames.npz',frames=np.stack(frames))
    (output/'actions.jsonl').write_text(''.join(json.dumps(row,allow_nan=False)+'\n' for row in rows))
    base,version=game_id.split('-');game_dir=ASSETS/'environment_files'/base/version
    sources=[*ROOT.glob('*.py'),ROOT/'protocol/arc_offline.py',*sorted((ASSETS/'arc3').glob('*.py')),
             game_dir/(base+'.py'),game_dir/'metadata.json']
    dump(output/'manifest.json',{'schema_version':1,'created_at':datetime.now(timezone.utc).isoformat(),
        'sources_sha256':{str(path.relative_to(ROOT)):sha(path) for path in sources},
        'artifacts_sha256':{path.name:sha(path) for path in sorted(output.iterdir()) if path.is_file()},
        'checkpoint_sha256':result['checkpoint_sha256'],
        'runtime':{'python':platform.python_version(),**{p:importlib.metadata.version(p) for p in ('numpy','arc-agi','arcengine')}},
        'protocol':'same local game version, seed0, initial state, 400-action cap, legal candidates, tabu; only ranking differs'})
    return result


def evaluate_all(checkpoint,output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    results=[]
    for game in GAMES:
        pair=[]
        for policy in ('search','interaction'):
            result=run_game(game,policy,output/(game+'_'+policy),checkpoint=checkpoint)
            results.append(result);pair.append(result)
            print(json.dumps(result,allow_nan=False),flush=True)
        if pair[0]['initial_frame_sha256']!=pair[1]['initial_frame_sha256']:
            raise RuntimeError('A/B initial state mismatch')
    dump(output/'summary.json',results)
    return results


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();evaluate_all(args.checkpoint,args.out)
