"""Fixed-protocol CPU head training on LS20 levels 1..5; 6..7 withheld.

No SNN inference, dummy features, level IDs, step IDs, heldout model selection,
or stored route actions are used by the trained policy at inference time.
"""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import time

import numpy as np

from action_head import ActionHead
from experiment_data import FEATURE_PROTOCOL,load_examples,level_split

TAGS=['A1','A2','A3','A4']


def fit(head,features,targets,epochs=250,lr=.1,l2=.0001):
    features=np.asarray(features,dtype=float);targets=np.asarray(targets)
    if features.ndim!=2 or features.shape[1]!=head.embed_dim or not 1<=len(features)<=800:
        raise ValueError('Invalid training matrix')
    if not np.isfinite(features).all() or targets.shape!=(len(features),) or not np.issubdtype(targets.dtype,np.integer) or np.any(targets<0) or np.any(targets>3):
        raise ValueError('Invalid features/targets')
    if type(epochs) is not int or not 1<=epochs<=1000 or not math.isfinite(lr) or not 0<lr<=1 or not math.isfinite(l2) or not 0<=l2<=1:
        raise ValueError('Invalid bounded training settings')
    action=head.action_features(TAGS)
    history=[]
    for epoch in range(epochs):
        logits=(features@head.w_state_action)@action.T+action@head.w_action
        logits-=logits.max(axis=1,keepdims=True)
        probabilities=np.exp(logits);denom=probabilities.sum(axis=1,keepdims=True)
        probabilities/=denom
        loss=float(np.mean(-logits[np.arange(len(targets)),targets]+np.log(denom[:,0])))
        grad=probabilities;grad[np.arange(len(targets)),targets]-=1;grad/=len(targets)
        head.w_state_action-=lr*(features.T@grad@action+l2*head.w_state_action)
        head.w_action-=lr*(grad.sum(axis=0)@action)
        if epoch==0 or (epoch+1)%25==0 or epoch==epochs-1:
            history.append({'epoch':epoch+1,'train_cross_entropy_before_update':loss})
    return history


def train_split(data,epochs=250,lr=.1,l2=.0001,seed=7):
    train,_=level_split(data)
    head=ActionHead(embed_dim=data['features'].shape[1],seed=seed)
    history=fit(head,data['features'][train],data['targets'][train],epochs=epochs,lr=lr,l2=l2)
    return head,history


def evaluate(head,features,targets,prior):
    action=head.action_features(TAGS)
    logits=(features@head.w_state_action)@action.T+action@head.w_action
    prediction=logits.argmax(axis=1)
    baseline=int(np.argmax(prior))
    shifted=logits-logits.max(axis=1,keepdims=True)
    ce=np.mean(-shifted[np.arange(len(targets)),targets]+np.log(np.exp(shifted).sum(axis=1)))
    return {'n':len(targets),'teacher_action_accuracy':float(np.mean(prediction==targets)),
            'train_only_action_prior_accuracy':float(np.mean(targets==baseline)),
            'cross_entropy':float(ce),'action_prior':prior.tolist(),
            'predicted_action_counts':np.bincount(prediction,minlength=4).tolist()}


def run_training(recording,output,epochs=250,lr=.1,l2=.0001,seed=7):
    output=Path(output)
    if output.exists():
        raise FileExistsError(output)
    data=load_examples(recording);train,held=level_split(data)
    started=time.perf_counter()
    head,history=train_split(data,epochs,lr,l2,seed)
    output.mkdir(parents=True,exist_ok=False)
    checkpoint=output/'head_v2.npz'
    head.save(checkpoint)
    # Freeze weights and checkpoint before the first heldout measurement.
    checkpoint_sha=hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    prior=np.bincount(data['targets'][train],minlength=4)/len(train)
    report={'created_at':datetime.now(timezone.utc).isoformat(),
            'protocol':'fixed hyperparameters; levels1..5 train; levels6..7 withheld; final epoch only',
            'scope':'Teacher-action prediction within LS20; not held-out games or general ARC solving',
            'backend':'non-neural native-frame spatial features',
            'feature_protocol':FEATURE_PROTOCOL,
            'config':{'epochs':epochs,'learning_rate':lr,'l2':l2,'seed':seed,'feature_dim':head.embed_dim},
            'train':evaluate(head,data['features'][train],data['targets'][train],prior),
            'withheld':evaluate(head,data['features'][held],data['targets'][held],prior),
            'per_withheld_level':{str(level):evaluate(head,data['features'][data['levels']==level],data['targets'][data['levels']==level],prior) for level in (6,7)},
            'frame_overlap_train_withheld':0,'checkpoint_sha256':checkpoint_sha,
            'checkpoint_frozen_before_withheld_evaluation':True,
            'history':history,'wall_time_s':time.perf_counter()-started,
            'runtime':{'python':platform.python_version(),'numpy':np.__version__},
            'source_files_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob('*.py'))},
            'dataset_manifest_sha256':hashlib.sha256((Path(recording)/'manifest.json').read_bytes()).hexdigest(),
            'dataset_artifact_sha256':data['source_manifest']['artifacts_sha256'],
            'train_frame_hashes':data['frame_hashes'][train].tolist(),
            'withheld_frame_hashes':data['frame_hashes'][held].tolist()}
    (output/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recording',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    result=run_training(args.recording,args.out)
    print(json.dumps({k:result[k] for k in ('train','withheld','wall_time_s','checkpoint_sha256')},allow_nan=False))
