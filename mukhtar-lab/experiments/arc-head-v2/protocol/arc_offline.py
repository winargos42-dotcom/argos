"""Bounded ARC-AGI-3 local game experiment, without API calls or an SNN claim.

Run as a standalone process: offline_guard patches process-wide networking.
The existing SearchRanker is loaded unchanged; route replay is explicitly a
precomputed sequence and must not be interpreted as autonomous problem solving.
"""
import argparse
from contextlib import contextmanager, ExitStack
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import importlib.util
import json
import logging
import os
from pathlib import Path
import platform
import re
import time
from unittest.mock import patch

import numpy as np


@contextmanager
def offline_guard():
    """Fail closed on DNS/connections and disable SDK dotenv/environment mode."""
    with ExitStack() as stack:
        stack.enter_context(patch.dict(os.environ, {
            'PYTHON_DOTENV_DISABLED': '1', 'OPERATION_MODE': 'offline'}))
        for operation in ('socket.getaddrinfo', 'socket.create_connection',
                          'socket.socket.connect', 'socket.socket.connect_ex',
                          'socket.socket.sendto'):
            stack.enter_context(patch(operation, side_effect=RuntimeError(
                'network prohibited in offline ARC experiment')))
        yield


def frame_hash(frame):
    array = np.asarray(frame, dtype=np.uint8)
    return hashlib.sha256(array.tobytes()).hexdigest()


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _frame(obs):
    if obs is None or not len(obs.frame):
        raise RuntimeError('Local engine returned no observable frame')
    array = np.asarray(obs.frame[-1], dtype=np.uint8)
    if array.ndim != 2 or array.size > 128 * 128:
        raise RuntimeError('Unexpected game frame dimensions')
    return array


def _tokens(frame):
    # Native pixel colours, not an ANSI terminal approximation. SearchRanker
    # uses state equality; the candidate generator keeps its existing logic.
    return [['█' if int(v) == 0 else f'{int(v)}:█' for v in row] for row in frame]


def _write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2)+'\n')


def run_offline(environments_dir, arc_source_root, output, *,
                game_id='ls20-9607627b', mode='search', budget=200,
                route_path=None, seed=0):
    """Execute up to 800 actions / 60 seconds and return measured summary.

    ``mode``: search or route_replay. Only native observations determine wins.
    The raw artifact records the last observable frame after each action;
    intermediate animation frames are not included.
    """
    if type(budget) is not int or not 1 <= budget <= 800:
        raise ValueError('budget must be an integer in [1,800]')
    if type(seed) is not int or not 0 <= seed < 2**32:
        raise ValueError('seed must be an integer in [0,2**32)')
    if mode not in ('search', 'route_replay'):
        raise ValueError('mode must be search or route_replay')
    if not re.fullmatch(r'[a-z0-9]{4}-[a-z0-9]{8}', game_id):
        raise ValueError('Use an explicit local game ID and version')
    games, source, output = Path(environments_dir).resolve(), Path(arc_source_root).resolve(), Path(output)
    base, version = game_id.split('-')
    game_dir = games / base / version
    metadata = game_dir / 'metadata.json'
    game_source = game_dir / f'{base}.py'
    if not metadata.is_file() or not game_source.is_file():
        raise FileNotFoundError('Local metadata/source missing for '+game_id)
    route = None
    if mode == 'route_replay':
        if route_path is None:
            raise ValueError('route_replay requires a recorded route JSONL')
        route_path = Path(route_path).resolve()
        if route_path.stat().st_size > 2_000_000:
            raise ValueError('route file exceeds 2MB')
        route = [json.loads(line)['teacher_action'] for line in route_path.read_text().splitlines() if line.strip()]
        if not route or len(route) > 800 or any(not re.fullmatch(r'A[1-7]', str(key)) for key in route):
            raise ValueError('route must contain 1..800 discrete action tags A1..A7')
    if output.exists():
        raise FileExistsError(output)
    source_paths = [source / p for p in ('search_policy.py','world_memory.py','candidate_generator.py')]
    provenance = {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                  for path in [*source_paths, metadata, game_source, Path(__file__).resolve()]}
    if route_path is not None:
        provenance[str(route_path)] = hashlib.sha256(Path(route_path).read_bytes()).hexdigest()
    output.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    with offline_guard():
        import arc_agi
        from arcengine import GameAction
        search = _load(source_paths[0], '_arc_local_search')
        memory = _load(source_paths[1], '_arc_local_memory')
        candidates = _load(source_paths[2], '_arc_local_candidates')
        ranker = search.SearchRanker(memory.WorldMemory())
        logger = logging.getLogger('mukhtar.arc.offline')
        logger.setLevel(logging.WARNING)
        arcade = arc_agi.Arcade(
            arc_api_key='offline-local', operation_mode=arc_agi.OperationMode.OFFLINE,
            environments_dir=str(games), recordings_dir=str(output / 'sdk-recordings'), logger=logger)
        if arcade.operation_mode != arc_agi.OperationMode.OFFLINE:
            raise RuntimeError('SDK is not offline')
        env = arcade.make(game_id, seed=seed, render_mode=None, save_recording=False)
        if env is None or type(env).__name__ != 'LocalEnvironmentWrapper':
            raise RuntimeError('Local game could not be loaded')
        obs = env.reset()
        frames = [_frame(obs).copy()]
        current_hash = frame_hash(frames[-1])
        seen = {current_hash}
        rows = []
        inference_ms = []
        unchanged = 0
        levels = int(obs.levels_completed)
        stop_reason = 'budget_exhausted'
        for step in range(1, budget+1):
            if time.perf_counter() - started >= 60:
                stop_reason = 'wall_time_limit'
                break
            if route is not None and step > len(route):
                stop_reason = 'route_exhausted'
                break
            available = [int(v) for v in obs.available_actions]
            cands = candidates.candidate_list(available, _tokens(frames[-1]))
            if not cands:
                stop_reason = 'no_candidates'
                break
            tick = time.perf_counter()
            if route is None:
                key, action, data = ranker.rank(current_hash, cands, features=None)[0]
            else:
                key = route[step-1]
                action, data = GameAction.from_id(int(key[1:])), None
                if action.value not in available:
                    stop_reason = 'route_action_unavailable'
                    break
            inference_ms.append((time.perf_counter()-tick)*1000)
            before_state = obs.state.name
            obs = env.step(action, data=data)
            frame = _frame(obs)
            next_hash = frame_hash(frame)
            changed = current_hash != next_hash
            unchanged += int(not changed)
            ranker.record(current_hash, key, changed)
            levels = max(levels, int(obs.levels_completed))
            rows.append({'step':step, 'action_key':key, 'action_id':int(action.value),
                         'data':data, 'available_before':available,
                         'before_hash':current_hash, 'after_hash':next_hash,
                         'state_before':before_state, 'state_after':obs.state.name,
                         'levels_completed':int(obs.levels_completed), 'frame_changed':changed})
            frames.append(frame.copy())
            seen.add(next_hash)
            current_hash = next_hash
            if obs.state.name in ('WIN','GAME_OVER','LOSE','FINISHED'):
                stop_reason = 'terminal_state'
                break
        closed = arcade.close_scorecard()
        if closed is not None:
            _write_json(output / 'local_scorecard.json', closed.model_dump(mode='json', exclude={'api_key'}))
    summary = {
        'execution':'offline_local_game', 'game_id':game_id, 'seed':seed,
        'policy':'existing_search_ranker' if route is None else 'precomputed_route_replay',
        'neural_backend':None, 'trained_checkpoint':None,
        'actions':len(rows), 'action_budget':budget, 'unique_frames':len(seen),
        'unchanged_frame_actions':unchanged, 'levels_completed':levels,
        'final_state':obs.state.name, 'won':obs.state.name == 'WIN',
        'stop_reason':stop_reason, 'final_frame_sha256':current_hash,
        'inference_ms_mean':float(np.mean(inference_ms)) if inference_ms else None,
        'wall_time_s':time.perf_counter()-started,
        'local_scorecard_closed':closed is not None,
        'claim_scope':'Local practice game only; route replay is not an autonomous solver or held-out result',
    }
    np.savez_compressed(output / 'frames.npz', frames=np.stack(frames))
    with (output / 'actions.jsonl').open('w') as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False)+'\n')
    _write_json(output / 'summary.json',summary)
    _write_json(output / 'manifest.json',{
        'schema_version':1, 'created_at':datetime.now(timezone.utc).isoformat(),
        'execution':'offline_local_game', 'network':'OFFLINE SDK plus blocked DNS/socket connection calls',
        'observation':'native last frame per action; uint8 colours; intermediate animation frames omitted',
        'runtime':{'python':platform.python_version(), **{p:importlib.metadata.version(p) for p in ('arc-agi','arcengine','numpy')}},
        'sources_sha256':provenance,
        'artifacts_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.iterdir()) if p.is_file()},
    })
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--environments',type=Path,required=True)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--game',default='ls20-9607627b')
    parser.add_argument('--mode',choices=('search','route_replay'),default='search')
    parser.add_argument('--budget',type=int,default=200)
    parser.add_argument('--route',type=Path)
    args=parser.parse_args()
    print(json.dumps(run_offline(args.environments,args.source,args.out,
                     game_id=args.game,mode=args.mode,budget=args.budget,route_path=args.route),ensure_ascii=False))


if __name__ == '__main__':
    main()
