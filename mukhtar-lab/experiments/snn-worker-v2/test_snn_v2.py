import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
import numpy as np
import snn_rank_worker_v2 as v2


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.crow=np.array([0,1,2,3,3])
        self.col=np.array([2,0,1])
        self.w=np.array([5.,2.,-3.],dtype=np.float32)

    def test_directed_matvec_matches_dense_with_sign_and_empty_row(self):
        x=np.array([1.,2.,3.,4.],dtype=np.float32)
        np.testing.assert_allclose(v2.csr_matvec(self.crow,self.col,self.w,x),[15.,2.,-6.,0.])

    def test_downstream_is_post_not_input_neighbour(self):
        np.testing.assert_array_equal(v2.downstream_layer([0],self.crow,self.col,self.w,10),[1])
        np.testing.assert_array_equal(v2.downstream_layer([1],self.crow,self.col,self.w,10),[2])

    def test_induced_subgraph_deduplicates_and_preserves_dense_operator(self):
        g=v2.induced_subgraph(self.crow,self.col,self.w,[2,0,2,1,0],[0],2)
        np.testing.assert_array_equal(g.global_ids,[0,1,2])
        np.testing.assert_array_equal(g.input_local,[0])
        np.testing.assert_allclose(v2.csr_matvec(g.crow,g.col,g.weights,np.array([1.,2.,3.])),[15.,2.,-6.])
        self.assertEqual(g.crow[-1],3)

    def test_downstream_cap_uses_total_absolute_weight_and_stable_ties(self):
        crow=np.array([0,0,2,3,4]);col=np.array([0,0,0,0]);w=np.array([1.,-2.,3.,2.])
        np.testing.assert_array_equal(v2.downstream_layer([0],crow,col,w,2),[1,2])

    def test_empty_graph_edges_are_valid(self):
        g=v2.induced_subgraph(np.array([0,0,0]),np.array([],dtype=np.int64),np.array([],dtype=np.float32),[1,0],[0],2)
        np.testing.assert_array_equal(g.crow,[0,0,0])
        np.testing.assert_allclose(v2.simulate_numpy(g,[0.])['readout'],[0.,0.])

    def test_invalid_csr_rejected(self):
        for crow,col,w in [([1,1],[0],[1.]),([0,2,1],[0],[1.]),([0,1],[1],[1.]),([0,1],[0],[float('nan')])]:
            with self.subTest(crow=crow,col=col,w=w), self.assertRaises(ValueError):
                v2.validate_csr(np.array(crow),np.array(col),np.array(w))

    def test_two_hop_graph_uses_unique_global_nodes(self):
        g=v2.build_graph(np.array([0,1,2]),np.array([1,0]),np.array([2.,3.],dtype=np.float32),n_in=1,n_out=2,cap_layer=2)
        self.assertEqual(len(g.global_ids),2)
        np.testing.assert_array_equal(g.input_local,[0])

    def test_recurrent_signal_reaches_uninjected_post_neuron(self):
        g=v2.induced_subgraph(np.array([0,0,1]),np.array([0]),np.array([2.],dtype=np.float32),[0,1],[0],2)
        result=v2.simulate_numpy(g,[64.],v2.Dynamics(ticks=10,readout_last=5,synapse_scale=1.))
        post=list(g.readout).index(1)
        self.assertGreater(result['readout'][post],0.)
        np.testing.assert_array_equal(v2.simulate_numpy(g,[0.])['readout'],[0.,0.])

    @unittest.skipUnless(importlib.util.find_spec('torch'),'Torch checked on Coral')
    def test_torch_csr_simulation_matches_independent_numpy(self):
        g=v2.induced_subgraph(self.crow,self.col,self.w,[0,1,2,3],[0,1],4)
        cfg=v2.Dynamics(ticks=20,readout_last=10,synapse_scale=.7)
        runner=v2.TorchRunner(g,cfg)
        for vector in ([64.,0.],[64.,128.],[0.,0.],[-64.,64.]):
            expected=v2.simulate_numpy(g,vector,cfg)
            actual=runner(vector)
            np.testing.assert_allclose(actual['readout'],expected['readout'],rtol=1e-6,atol=1e-7)


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.calls=[]
        def run(vec):
            self.calls.append(vec)
            return {'readout':[float(sum(vec))], 'in_rate':0., 'ro_rate':0., 'ro':[0.]}
        self.session=v2.Session(run,n_in=2,provenance={'sha256':'fixture'},max_batch=2,cache_size=2)

    def test_valid_batch_preserves_order_duplicates_and_diagnostics(self):
        out=self.session.handle({'vecs':[[1.,2.],[1.,2.]],'diag':True})
        self.assertEqual(out['readout'],[[3.],[3.]])
        self.assertEqual(len(out['diag']),2)
        self.assertEqual(len(self.calls),1)

    def test_cache_is_exact_not_six_decimal_aliasing_and_bounded(self):
        for v in ([1.,2.],[1.0000001,2.],[1.0000002,2.]): self.session.handle({'vecs':[v]})
        self.assertEqual(len(self.calls),3)
        self.assertEqual(len(self.session.cache),2)

    def test_entire_request_validated_before_any_simulation(self):
        out=self.session.handle({'vecs':[[1.,2.],[1.]]})
        self.assertIn('error',out)
        self.assertEqual(self.calls,[])

    def test_invalid_requests_do_not_kill_persistent_stream(self):
        invalid=[None,[],{}, {'vecs':1},{'vecs':[[]]},{'vecs':[[1,True]]},{'vecs':[['1',2]]},
                 {'vecs':[[1,float('inf')]]},{'vecs':[[1,float('nan')]]},{'vecs':[[1,1e300]]},
                 {'vecs':[[1,2]]*3},{'vecs':[[1,2]],'diag':1}]
        lines='broken\n'+'\n'.join(json.dumps(x) for x in invalid)+'\nping\n'+json.dumps({'vecs':[[1,2]]})+'\n'
        out=io.StringIO();v2.serve(io.StringIO(lines),out,self.session)
        responses=[json.loads(s) for s in out.getvalue().splitlines()]
        self.assertTrue(all('error' in r for r in responses[:-2]))
        self.assertEqual(responses[-2],{'pong':1})
        self.assertEqual(responses[-1]['readout'],[[3.]])

    def test_oversized_line_drained_before_next_ping(self):
        out=io.StringIO();v2.serve(io.StringIO('x'*150+'\nping\n'),out,self.session,max_line_chars=64)
        self.assertEqual([json.loads(x) for x in out.getvalue().splitlines()][-1],{'pong':1})

    def test_info_reports_provenance_and_limits(self):
        r=self.session.handle({'op':'info'})
        self.assertEqual(r['provenance']['sha256'],'fixture')
        self.assertEqual(r['limits']['max_batch'],2)

    def test_hash_guard_rejects_before_deserialization(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'checkpoint.pt';p.write_bytes(b'not a pickle')
            with self.assertRaisesRegex(ValueError,'SHA256'):
                v2.load_graph(p,'0'*64)

if __name__=='__main__': unittest.main()
