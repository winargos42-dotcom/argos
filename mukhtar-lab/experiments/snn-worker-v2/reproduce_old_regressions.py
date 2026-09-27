"""Expected RED against frozen live worker: functional, not source-string checks."""
import contextlib
import io
import unittest
from unittest.mock import patch
import numpy as np
import torch
import snn_rank_worker as old


class OldRegressions(unittest.TestCase):
    def test_spike_propagates_to_post_not_pre(self):
        old.G=(2,np.array([0,0,1]),torch.tensor([0]),torch.tensor([2.]),
               torch.tensor([0]),torch.tensor([1]),1)
        with patch.multiple(old,TICKS=10,READOUT_LAST=5,SYN_SCALE=1.):
            out,_,rate,_=old.run([64.])
        self.assertGreater(rate,0.,'0 -> 1 edge must activate post 1')

    def test_layer_follows_downstream(self):
        # 2 -> 0, 0 -> 1; downstream(0) is 1, not 2.
        actual=old.layer_from(np.array([0]),np.array([0,1,2,2]),
                              np.array([2,0]),np.array([5.,2.]),10)
        np.testing.assert_array_equal(actual,[1])

    def test_cycle_has_unique_nodes_and_consistent_csr(self):
        pt={'crow':torch.tensor([0,1,2]),'col':torch.tensor([1,0]),
            'weights':torch.tensor([2.,3.])}
        with patch.object(old.torch,'load',return_value=pt),patch.multiple(old,N_IN=1,N_OUT=2,CAP_LAYER=2),contextlib.redirect_stderr(io.StringIO()):
            graph=old.load_graph()
        self.assertEqual(graph[0],2,'a two-node cycle must remain two nodes')

if __name__=='__main__': unittest.main()
