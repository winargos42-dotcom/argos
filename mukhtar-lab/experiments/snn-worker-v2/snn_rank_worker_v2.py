"""Guarded CPU SNN bridge: CSR[post, pre] @ spikes, unique downstream graph.

This fixes graph algebra, not neural ranking quality. Retains the old bridge's
40-tick delayed-threshold LIF convention and explicit 0.05 synapse scale;
it is NOT numerically identical to canonical ConnectomeSNN.step (scale/timing).
JSONL protocol: ping, {"vecs": [[160 finite numbers]], "diag": false},
or {"op": "info"}. One bounded response per request, errors are recoverable.
"""
from collections import OrderedDict
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

CHECKPOINT='/root/output/male_cns_spikewhale.pt'
CHECKPOINT_SHA256='b381422e88d41ad3525f63284815784b3bbadfe32b59d8166986f92d7083f6fb'
MAX_BATCH=16
MAX_LINE_CHARS=262144


@dataclass(frozen=True)
class Dynamics:
    ticks: int=40
    readout_last: int=15
    beta: float=.9
    threshold: float=1.
    injection_scale: float=1.
    synapse_scale: float=.05

    def __post_init__(self):
        if not 1 <= self.readout_last <= self.ticks <= 200:
            raise ValueError('invalid tick bounds')
        if not all(np.isfinite(v) for v in asdict(self).values()):
            raise ValueError('dynamics must be finite')
        if not 0 <= self.beta < 1 or self.threshold <= 0:
            raise ValueError('invalid beta or threshold')


@dataclass
class Graph:
    global_ids: np.ndarray
    crow: np.ndarray
    col: np.ndarray
    weights: np.ndarray
    input_local: np.ndarray
    readout: np.ndarray


def validate_csr(crow,col,weights):
    if crow.ndim != 1 or col.ndim != 1 or weights.ndim != 1:
        raise ValueError('CSR arrays must be one dimensional')
    if crow.dtype.kind not in 'iu' or col.dtype.kind not in 'iu':
        raise ValueError('CSR indices must be integers')
    n=len(crow)-1
    if not 1 <= n <= 300000 or len(col)>50000000:
        raise ValueError('CSR size out of bounds')
    if crow[0]!=0 or crow[-1]!=len(col) or len(col)!=len(weights) or np.any(crow[1:]<crow[:-1]):
        raise ValueError('invalid CSR row pointers')
    if len(col) and (col.min()<0 or col.max()>=n):
        raise ValueError('CSR column out of bounds')
    if weights.dtype.kind != 'f' or not np.isfinite(weights).all():
        raise ValueError('CSR weights must be finite floats')


def csr_matvec(crow,col,weights,spikes):
    """Small NumPy reference oracle. Production uses torch.sparse.mm."""
    rows=np.repeat(np.arange(len(crow)-1),np.diff(crow))
    return np.bincount(rows,weights=weights*spikes[col],minlength=len(crow)-1).astype(np.float32)


def downstream_layer(pre_ids,crow,col,weights,cap):
    """Rank actual postsynaptic cells by |W[post, selected_pre]| mass.

    Scan in row blocks, avoiding a full nnz-sized row-index allocation.
    Ties resolve to ascending global index; inhibitory edges retain magnitude.
    """
    n=len(crow)-1
    selected=np.zeros(n,dtype=bool);selected[np.asarray(pre_ids,dtype=np.int64)]=True
    scores=np.zeros(n,dtype=np.float64)
    for first in range(0,n,2048):
        last=min(n,first+2048);lo,hi=int(crow[first]),int(crow[last])
        mask=selected[col[lo:hi]]
        if mask.any():
            rows=np.repeat(np.arange(last-first),np.diff(crow[first:last+1]))
            scores[first:last]=np.bincount(rows[mask],weights=np.abs(weights[lo:hi][mask]),minlength=last-first)
    order=np.argsort(-scores,kind='stable')
    return order[scores[order]>0][:cap].astype(np.int64)


def induced_subgraph(crow,col,weights,nodes,inputs,n_out):
    validate_csr(crow,col,weights)
    ids=np.unique(np.asarray(nodes,dtype=np.int64));n=len(crow)-1
    inputs=np.asarray(inputs,dtype=np.int64)
    if not len(ids) or ids.min()<0 or ids.max()>=n:
        raise ValueError('subgraph nodes out of bounds')
    if np.any(inputs<0) or np.any(inputs>=n) or len(np.unique(inputs))!=len(inputs):
        raise ValueError('invalid input nodes')
    lookup=np.full(n,-1,dtype=np.int64);lookup[ids]=np.arange(len(ids))
    if np.any(lookup[inputs]<0): raise ValueError('input missing from subgraph')
    columns=[];values=[];counts=[];mass=[]
    for post in ids:
        lo,hi=int(crow[post]),int(crow[post+1])
        local=lookup[col[lo:hi]];keep=local>=0
        ws=weights[lo:hi][keep]
        columns.append(local[keep]);values.append(ws)
        counts.append(int(keep.sum()));mass.append(float(np.abs(ws).sum(dtype=np.float64)))
    sub_crow=np.concatenate([np.zeros(1,dtype=np.int64),np.cumsum(counts,dtype=np.int64)])
    readout=np.argsort(-np.asarray(mass),kind='stable')[:n_out].astype(np.int64)
    return Graph(ids,sub_crow,np.concatenate(columns),np.concatenate(values).astype(np.float32),lookup[inputs],readout)


def build_graph(crow,col,weights,n_in=160,n_out=64,cap_layer=15000):
    validate_csr(crow,col,weights)
    if not 1<=n_in<=len(crow)-1 or not 1<=n_out or not 1<=cap_layer<=15000:
        raise ValueError('invalid subgraph limits')
    # Keep old bridge's input ordering for compatibility with its 160 features.
    inputs=np.argsort(-np.diff(crow))[:n_in].astype(np.int64)
    l1=downstream_layer(inputs,crow,col,weights,cap_layer)
    l2=downstream_layer(l1,crow,col,weights,cap_layer)
    return induced_subgraph(crow,col,weights,np.concatenate([inputs,l1,l2]),inputs,n_out)


def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b''): h.update(chunk)
    return h.hexdigest()


def load_graph(path=CHECKPOINT,expected_sha256=CHECKPOINT_SHA256):
    path=Path(path)
    if path.stat().st_size>1024**3: raise ValueError('checkpoint exceeds 1 GiB guard')
    digest=sha256_file(path)
    if digest!=expected_sha256: raise ValueError('checkpoint SHA256 mismatch; refusing deserialization')
    import torch
    # Same opened inode is not enough against modification: recheck after load.
    pt=torch.load(path,map_location='cpu',weights_only=True)
    if sha256_file(path)!=digest: raise ValueError('checkpoint SHA256 changed during load')
    arrays={k:pt[k].detach().cpu().numpy() for k in ('crow','col','weights')}
    graph=build_graph(**arrays)
    body_ids=pt['body_ids'].detach().cpu().numpy()
    if len(body_ids)!=len(arrays['crow'])-1 or len(np.unique(body_ids))!=len(body_ids):
        raise ValueError('checkpoint neuron identifiers invalid')
    node_hash=hashlib.sha256(graph.global_ids.tobytes()).hexdigest()
    graph_hash=hashlib.sha256(b''.join(a.tobytes() for a in (graph.global_ids,graph.crow,graph.col,graph.weights))).hexdigest()
    provenance={'worker_version':2,'checkpoint_path':str(path),'checkpoint_sha256':digest,
      'checkpoint_neurons':len(body_ids),'checkpoint_edges':len(arrays['col']),
      'checkpoint_config':pt.get('config',{}),'operator':'CSR[post, pre] @ spikes',
      'graph_nodes':len(graph.global_ids),'graph_edges':len(graph.col),'graph_sha256':graph_hash,
      'global_ids_sha256':node_hash,'input_global_ids':graph.global_ids[graph.input_local].tolist(),
      'readout_global_ids':graph.global_ids[graph.readout].tolist(),
      'readout_body_ids':body_ids[graph.global_ids[graph.readout]].tolist(),
      'dynamics':asdict(Dynamics()),'torch':torch.__version__,
      'scope':'untrained anatomical subgraph bridge; legacy bridge timing and synapse scale; not a trained ARC policy'}
    return graph,provenance


def simulate_numpy(graph,vector,dynamics=Dynamics()):
    """Independent bounded reference used for small directed regression graphs."""
    d=dynamics;n=len(graph.global_ids)
    injection=np.zeros(n,dtype=np.float32)
    injection[graph.input_local]=np.tanh(np.asarray(vector,dtype=np.float32)/64)*d.injection_scale
    v=np.zeros(n,dtype=np.float32);rate=np.zeros(n,dtype=np.float32)
    for tick in range(d.ticks):
        spikes=(v>=d.threshold).astype(np.float32)
        v=np.clip(v*d.beta+injection-spikes+csr_matvec(graph.crow,graph.col,graph.weights,spikes)*d.synapse_scale,-30,30)
        if tick>=d.ticks-d.readout_last: rate+=spikes
    rate/=d.readout_last
    return {'readout':np.tanh(rate[graph.readout]).tolist(),'in_rate':float(rate[graph.input_local].mean()),
            'ro_rate':float(rate[graph.readout].mean()),'ro':rate[graph.readout].tolist()}


class TorchRunner:
    def __init__(self,graph,dynamics=Dynamics()):
        import torch
        self.torch=torch;self.graph=graph;self.dynamics=dynamics
        self.csr=torch.sparse_csr_tensor(torch.from_numpy(graph.crow),torch.from_numpy(graph.col),
                   torch.from_numpy(graph.weights),size=(len(graph.global_ids),len(graph.global_ids)),check_invariants=True)
        self.inputs=torch.from_numpy(graph.input_local);self.readout=torch.from_numpy(graph.readout)

    def __call__(self,vector):
        torch=self.torch;d=self.dynamics;n=len(self.graph.global_ids)
        with torch.inference_mode():
            injection=torch.zeros(n)
            injection[self.inputs]=torch.tanh(torch.tensor(vector,dtype=torch.float32)/64)*d.injection_scale
            v=torch.zeros(n);rate=torch.zeros(n)
            for tick in range(d.ticks):
                spikes=(v>=d.threshold).float()
                recurrent=torch.sparse.mm(self.csr,spikes[:,None]).squeeze(1)
                v=(v*d.beta+injection-spikes+recurrent*d.synapse_scale).clamp(-30,30)
                if tick>=d.ticks-d.readout_last: rate+=spikes
            rate/=d.readout_last
            return {'readout':torch.tanh(rate[self.readout]).tolist(),'in_rate':float(rate[self.inputs].mean()),
                    'ro_rate':float(rate[self.readout].mean()),'ro':rate[self.readout].tolist()}


class Session:
    def __init__(self,run,n_in=160,provenance=None,max_batch=MAX_BATCH,cache_size=128):
        self.run=run;self.n_in=n_in;self.provenance=provenance or {}
        self.max_batch=max_batch;self.cache_size=cache_size;self.cache=OrderedDict()

    def handle(self,request):
        try:
            if not isinstance(request,dict): raise ValueError('request must be a JSON object')
            if request=={'op':'info'}:
                return {'provenance':self.provenance,'limits':{'max_batch':self.max_batch,'cache_entries':self.cache_size,'n_in':self.n_in,'max_line_chars':MAX_LINE_CHARS}}
            if set(request)-{'vecs','diag'}: raise ValueError('unknown request fields')
            if 'diag' in request and not isinstance(request['diag'],bool): raise ValueError('diag must be boolean')
            vectors=request.get('vecs')
            if not isinstance(vectors,list) or not 0<=len(vectors)<=self.max_batch: raise ValueError('vecs must be a bounded list')
            keys=[]
            for v in vectors:
                if not isinstance(v,list) or len(v)!=self.n_in: raise ValueError(f'each vector must have {self.n_in} values')
                if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not np.isfinite(x) or abs(x)>1e6 for x in v):
                    raise ValueError('vector values must be finite numbers with |x| <= 1e6')
                keys.append(tuple(float(x) for x in v))
            out=[];diag=[]
            for key in keys:
                if key not in self.cache:
                    self.cache[key]=self.run(key)
                    if len(self.cache)>self.cache_size: self.cache.popitem(last=False)
                self.cache.move_to_end(key);r=self.cache[key]
                out.append(r['readout'])
                if request.get('diag'): diag.append({k:r[k] for k in ('in_rate','ro_rate','ro')})
            response={'readout':out}
            if request.get('diag'): response['diag']=diag
            return response
        except (ValueError,TypeError,OverflowError) as exc:
            return {'error':str(exc),'error_type':'invalid_request'}


def serve(input_stream,output_stream,session,max_line_chars=MAX_LINE_CHARS):
    while True:
        line=input_stream.readline(max_line_chars+1)
        if not line: break
        if len(line)>max_line_chars:
            while line and not line.endswith('\n'): line=input_stream.readline(max_line_chars+1)
            response={'error':'request line exceeds limit','error_type':'invalid_request'}
        elif not line.strip(): continue
        elif line.strip()=='ping': response={'pong':1}
        else:
            try:
                request=json.loads(line,parse_constant=lambda _: (_ for _ in ()).throw(ValueError('non-finite JSON number')))
                response=session.handle(request)
            except (ValueError,TypeError,RecursionError):
                response={'error':'invalid JSON','error_type':'invalid_request'}
            except Exception:
                # Do not emit internal paths/exception contents or kill the stream.
                response={'error':'inference failed','error_type':'inference_error'}
        output_stream.write(json.dumps(response,allow_nan=False,separators=(',',':'))+'\n');output_stream.flush()


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint',default=CHECKPOINT)
    parser.add_argument('--expected-sha256',default=CHECKPOINT_SHA256)
    args=parser.parse_args()
    import torch
    torch.set_num_threads(1)
    graph,provenance=load_graph(args.checkpoint,args.expected_sha256)
    provenance['worker_sha256']=sha256_file(__file__)
    print(json.dumps({'ready':True,'provenance':provenance}),file=sys.stderr,flush=True)
    serve(sys.stdin,sys.stdout,Session(TorchRunner(graph),provenance=provenance))


if __name__=='__main__': main()
