"""Bounded real-checkpoint verification. Synthetic inputs, no training/ARC wins."""
import gc,hashlib,importlib.util,json,resource,subprocess,sys,time
from pathlib import Path
import numpy as np
import torch
import snn_rank_worker as old
import snn_rank_worker_v2 as v2

torch.set_num_threads(1)
torch.set_num_interop_threads(1)
ROOT=Path(__file__).resolve().parent
OLD_SHA='0fee7c638a513eb5bfc7d48760c2bf86502cb0a1e4d5d2d43ed488d0cf64ace3'
assert v2.sha256_file('/opt/argos-roach/fly_bridge/snn_rank_worker.py')==OLD_SHA
started=time.monotonic()
graph,provenance=v2.load_graph()
provenance['worker_sha256']=v2.sha256_file(ROOT/'snn_rank_worker_v2.py')
new=v2.TorchRunner(graph)
report={'provenance':provenance,'old_worker_sha256':OLD_SHA,'torch_threads':1,
        'input_scope':'four deterministic synthetic probes; not ARC quality evaluation',
        'comparisons':[],'canonical_sources':{}}
for path in ['/root/malecns/code/model.py','/root/malecns/code/sparse_mm.py','/root/malecns/code/sparse_mm_fast.py']:
    report['canonical_sources'][path]=v2.sha256_file(path)

# Actual checkpoint: canonical SparseRecurrent versus independent NumPy row sum.
pt=torch.load(v2.CHECKPOINT,map_location='cpu',weights_only=True)
spec=importlib.util.spec_from_file_location('canonical_sparse','/root/malecns/code/sparse_mm.py')
canonical=importlib.util.module_from_spec(spec);spec.loader.exec_module(canonical)
n=len(pt['crow'])-1
spikes=torch.zeros(1,n);spikes[0,graph.global_ids[graph.input_local[:3]]]=torch.tensor([1.,.5,-.25])
actual=canonical.SparseRecurrent.apply(pt['weights'],pt['crow'],pt['col'],spikes).numpy()[0]
crow=pt['crow'].numpy();cols=pt['col'].numpy();weights=pt['weights'].numpy()
products=weights*spikes.numpy()[0,cols]
expected=np.zeros(n,dtype=np.float32);nonempty=np.flatnonzero(np.diff(crow))
expected[nonempty]=np.add.reduceat(products,crow[nonempty])
error=float(np.max(np.abs(actual-expected)))
assert np.allclose(actual,expected,rtol=1e-5,atol=1e-6)
report['canonical_checkpoint_matvec']={'max_abs_error':error,'nonzero_posts':int(np.count_nonzero(actual)),
    'checked_all_neurons':n,'pre_global_ids':graph.global_ids[graph.input_local[:3]].tolist()}
in_pool=np.argsort(-np.diff(crow))[:old.N_IN]
l1=old.layer_from(in_pool,crow,cols,weights,old.CAP_LAYER)
l2=old.layer_from(l1,crow,cols,weights,old.CAP_LAYER)
old_nodes=np.sort(np.concatenate([in_pool,l1,l2]))
report['old_subgraph_nodes']=len(old_nodes)
report['old_unique_nodes']=len(np.unique(old_nodes))
report['old_duplicate_nodes']=len(old_nodes)-len(np.unique(old_nodes))
del pt,crow,cols,weights,products,actual,expected,spikes;gc.collect()

# Native old graph, frozen code; each vector starts with zero membrane in both.
native_old=old.load_graph()
report['old_subgraph_edges']=len(native_old[2])
# Isolated bug ablation: old scatter recurrence on EXACT new graph/input/readout.
same_graph=(len(graph.global_ids),graph.crow,torch.from_numpy(graph.col),
            torch.from_numpy(graph.weights),torch.from_numpy(graph.input_local),torch.from_numpy(graph.readout),len(graph.readout))
vectors={'zero':[0.]*160,'constant64':[64.]*160,
         'one_input64':[64.]+[0.]*159,'signed_ramp':np.linspace(-64.,128.,160).tolist()}
for name,vector in vectors.items():
    t=time.monotonic();r_new=new(vector);new_seconds=time.monotonic()-t
    old.G=same_graph;t=time.monotonic();r_same=old.run(vector);same_seconds=time.monotonic()-t
    old.G=native_old;t=time.monotonic();r_old=old.run(vector);old_seconds=time.monotonic()-t
    assert all(np.isfinite(x).all() for x in [r_new['readout'],r_same[0].numpy(),r_old[0].numpy()])
    row={'input':name,'input_vector':vector,'new':r_new,
         'old_operator_same_graph':{'readout':r_same[0].tolist(),'in_rate':r_same[1],'ro_rate':r_same[2]},
         'old_native':{'readout':r_old[0].tolist(),'in_rate':r_old[1],'ro_rate':r_old[2]},
         'same_graph_max_readout_delta':float(np.max(np.abs(np.asarray(r_new['readout'])-r_same[0].numpy()))),
         'seconds':{'new':new_seconds,'old_operator_same_graph':same_seconds,'old_native':old_seconds}}
    report['comparisons'].append(row)
assert report['comparisons'][0]['new']['ro_rate']==0
assert any(r['same_graph_max_readout_delta']>0 for r in report['comparisons'][1:])
del old.G,native_old,same_graph,new,graph;gc.collect()

# Real persistent subprocess: invalid requests must not prevent later valid work.
lines=['null','{"vecs":[[1]]}','{"vecs": [[NaN]]}','x'*262145,'ping',
       json.dumps({'vecs':[[0.]*160],'diag':True}),json.dumps({'op':'info'})]
proc=subprocess.run([sys.executable,str(ROOT/'snn_rank_worker_v2.py')],input='\n'.join(lines)+'\n',
                    text=True,capture_output=True,timeout=60)
assert proc.returncode==0,proc.stderr[-500:]
responses=[json.loads(x) for x in proc.stdout.splitlines()]
assert len(responses)==len(lines)
assert all('error' in r for r in responses[:4])
assert responses[4]=={'pong':1}
assert len(responses[5]['readout'][0])==64 and all(x==0 for x in responses[5]['readout'][0])
assert responses[6]['provenance']['checkpoint_sha256']==v2.CHECKPOINT_SHA256
report['persistent_protocol']={'returncode':proc.returncode,'responses':len(responses),'invalid_requests_recovered':4,
                               'ping_after_errors':True,'valid_batch_after_errors':True,'provenance_present':True}
report['seconds_total']=time.monotonic()-started
report['peak_rss_mib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
report['limits']='single CPU Torch thread; 40 ticks; 4 unique 160-feature probes; no training; isolated /tmp staging'
report['comparison_caveat']='Only old_operator_same_graph vs new aligns readout coordinates. old_native has a different subgraph and readout; do not interpret its vector elementwise delta.'
(ROOT/'checkpoint-smoke.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['canonical_checkpoint_matvec','old_duplicate_nodes','persistent_protocol','seconds_total','peak_rss_mib']}))
print(json.dumps({'same_graph_deltas':{r['input']:r['same_graph_max_readout_delta'] for r in report['comparisons']}}))
