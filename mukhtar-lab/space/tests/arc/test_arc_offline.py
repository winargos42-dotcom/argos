import importlib
import importlib.util
import json
from pathlib import Path
import socket
import tempfile
import unittest
import zipfile

import numpy as np

ASSETS = Path(__file__).resolve().parents[2] / 'arc_runtime'
SOURCE = ASSETS / 'arc3'
GAMES = ASSETS / 'environment_files'


class OfflineTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('arc_offline'),
                             'No bounded offline ARC runner')
        return importlib.import_module('arc_offline')

    def test_explicit_network_guard_blocks_connections(self):
        with self.module().offline_guard():
            with self.assertRaisesRegex(RuntimeError, 'network'):
                socket.getaddrinfo('example.com', 443)

    def test_search_real_game_is_repeatable_and_preserves_raw_frames(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as directory:
            first = module.run_offline(GAMES, SOURCE, Path(directory)/'first', budget=12)
            second = module.run_offline(GAMES, SOURCE, Path(directory)/'second', budget=12)
            self.assertEqual(first['execution'], 'offline_local_game')
            self.assertEqual(first['policy'], 'existing_search_ranker')
            self.assertEqual(first['actions'], 12)
            a = np.load(Path(directory)/'first/frames.npz')['frames']
            b = np.load(Path(directory)/'second/frames.npz')['frames']
            np.testing.assert_array_equal(a,b)
            self.assertEqual(a.shape, (13,64,64))
            rows = [json.loads(line) for line in (Path(directory)/'first/actions.jsonl').read_text().splitlines()]
            self.assertTrue(all(row['action_id'] in row['available_before'] for row in rows))
            self.assertTrue(all(row['before_hash'] == module.frame_hash(a[i]) for i,row in enumerate(rows)))
            self.assertEqual(first['final_frame_sha256'], module.frame_hash(a[-1]))

    def test_replay_does_not_copy_recorded_win_labels(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as directory:
            route = Path(directory)/'route.jsonl'
            route.write_text(json.dumps({'teacher_action':'A3','state':'WIN','levels_completed':7})+'\n')
            result = module.run_offline(GAMES,SOURCE,Path(directory)/'out',
                                       mode='route_replay',route_path=route,budget=10)
            self.assertEqual(result['policy'], 'precomputed_route_replay')
            self.assertEqual(result['actions'],1)
            self.assertFalse(result['won'])
            self.assertEqual(result['levels_completed'],0)
            self.assertEqual(result['stop_reason'],'route_exhausted')

    def test_rejects_unbounded_budget_before_creating_output(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)/'out'
            with self.assertRaises(ValueError):
                module.run_offline(GAMES,SOURCE,out,budget=100000)
            self.assertFalse(out.exists())

    def test_space_wrapper_returns_measured_frames_and_download(self):
        self.assertIsNotNone(importlib.util.find_spec('arc_space'), 'No portable Space wrapper')
        wrapper = importlib.import_module('arc_space')
        summary, figure, download = wrapper.run_arc('ls20-9607627b', 12)
        self.assertEqual(summary['execution'], 'offline_local_game')
        self.assertEqual(summary['actions'],12)
        self.assertFalse(summary['won'])
        self.assertEqual(len(figure.axes),3)
        self.assertEqual(len(figure.axes[0].images),1)
        with zipfile.ZipFile(download) as bundle:
            self.assertEqual(json.loads(bundle.read('summary.json')),summary)
            self.assertEqual(len(bundle.read('actions.jsonl').splitlines()),12)
            self.assertIn('frames.npz',bundle.namelist())


if __name__ == '__main__':
    unittest.main()
