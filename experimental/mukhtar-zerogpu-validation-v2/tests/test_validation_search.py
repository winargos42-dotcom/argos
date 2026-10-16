import copy
import sys
import unittest
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation_search import (
    stratified_split, validate_grid, search_model, SEEDS, LEARNING_RATES, SPLIT_SEED,
    CHECKPOINT_SCHEMA,
)


def make_fixture():
    torch.set_num_threads(1)
    rng = np.random.default_rng(20261010)
    x = rng.normal(size=(360, 4)).astype('float32')
    target = np.c_[0.7*x[:, 0]+.2*x[:, 1], .3*x[:, 2]-.25*x[:, 3]].astype('float32')
    labels = np.repeat(['clean', 'noise20', 'antennaL_off', 'antennaR_off'], 90)
    xx = rng.normal(size=(128, 4)).astype('float32')
    yy = np.c_[.7*xx[:, 0]+.2*xx[:, 1], .3*xx[:, 2]-.25*xx[:, 3]].astype('float32')
    torch.manual_seed(111)
    def build():
        return torch.nn.Sequential(torch.nn.Linear(4, 64), torch.nn.ReLU(),
                                  torch.nn.Linear(64, 32), torch.nn.ReLU(),
                                  torch.nn.Linear(32, 2))
    init = copy.deepcopy(build().state_dict())
    return build, init, x, target, labels, xx, yy


class SplitTests(unittest.TestCase):
    def test_scenario_balanced(self):
        labels = make_fixture()[4]
        result = stratified_split(labels)
        self.assertEqual(len(result.train_indices), 288)
        self.assertEqual(len(result.val_indices), 72)
        self.assertEqual(len(result.groups), 4)
        for item in result.groups.values():
            self.assertEqual(item, {'train': 72, 'val': 18})
        self.assertFalse(np.intersect1d(result.train_indices, result.val_indices).size)

    def test_repeat_same_indices(self):
        labels = make_fixture()[4]
        a = stratified_split(labels)
        b = stratified_split(labels)
        self.assertTrue(np.array_equal(a.val_indices, b.val_indices))
        self.assertEqual(a.val_indices_sha256, b.val_indices_sha256)
        c = stratified_split(labels, seed=SPLIT_SEED+1)
        self.assertNotEqual(a.val_indices_sha256, c.val_indices_sha256)

    def test_undersized_scenario_fails(self):
        with self.assertRaises(ValueError):
            stratified_split(np.asarray(['rare']*4+['common']*356))

    def test_split_fraction_limited(self):
        with self.assertRaises(ValueError):
            stratified_split(make_fixture()[4], fraction=.9)


class GuardTests(unittest.TestCase):
    def test_default_grid_is_bounded(self):
        validate_grid(SEEDS[:2], LEARNING_RATES, 80, 34)

    def test_too_many_candidates(self):
        with self.assertRaises(ValueError):
            validate_grid(SEEDS, (.0001,.0003,.001), 80, 34)

    def test_unapproved_parameters_rejected(self):
        bad = [((999,), (.0001,), 80, 34), ((7,), (.01,), 80, 34),
               ((7,), (.0001,), 1000, 34), ((7,), (.0001,), 20, 100),
               ((7,7), (.0001,), 20, 34)]
        for row in bad:
            with self.subTest(row=row), self.assertRaises(ValueError):
                validate_grid(*row)


class SelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = make_fixture()

    def run_small(self, y_test=None):
        model, init, x, y, groups, xx, yy = self.fixture
        if y_test is not None:
            yy = y_test
        return search_model(model, init, x, y, groups, xx, yy,
                            seeds=(7,), learning_rates=(.0003,), steps=40,
                            device='cpu', max_seconds=34)

    def test_complete_and_best_score_not_worse_than_baseline(self):
        report, state = self.run_small()
        self.assertEqual(report['schema'], CHECKPOINT_SCHEMA)
        self.assertTrue(report['grid_completed'])
        self.assertEqual(report['train_count'], 288)
        self.assertEqual(report['validation_count'], 72)
        self.assertEqual(report['heldout_count'], 128)
        self.assertEqual(len(report['candidates']), 1)
        self.assertLessEqual(report['best']['val_mae'], report['baseline_val_mae']+1e-7)
        self.assertFalse(report['heldout_used_in_selection'])
        self.assertTrue(all(torch.isfinite(v).all().item() for v in state.values()))

    def test_test_labels_do_not_change_winner(self):
        first, state1 = self.run_small()
        bogus = np.zeros((128, 2), dtype='float32')
        second, state2 = self.run_small(y_test=bogus)
        self.assertEqual(first['best'], second['best'])
        self.assertEqual(first['candidates'], second['candidates'])
        self.assertEqual(first['validation_index_sha256'], second['validation_index_sha256'])
        self.assertNotEqual(first['final_heldout_mae'], second['final_heldout_mae'])
        for name in state1:
            self.assertTrue(torch.equal(state1[name], state2[name]))

    def test_cuda_is_not_faked(self):
        model, init, x, y, groups, xx, yy = self.fixture
        if not torch.cuda.is_available():
            with self.assertRaises(RuntimeError):
                search_model(model, init, x, y, groups, xx, yy,
                             seeds=(7,), learning_rates=(.0001,), steps=20,
                             device='cuda')

    def test_invalid_data_fails_closed(self):
        model, init, x, y, groups, xx, yy = self.fixture
        bad = x.copy();bad[0, 0] = np.nan
        with self.assertRaises(ValueError):
            search_model(model, init, bad, y, groups, xx, yy,
                         seeds=(7,), learning_rates=(.0001,), steps=20,
                         device='cpu')


if __name__ == '__main__':
    unittest.main()
