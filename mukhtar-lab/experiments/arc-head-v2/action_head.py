"""Version 2 ARC candidate head with trainable state-action interactions.

score(state, action) = state @ W @ action_features + action_features @ bias.
No pretrained knowledge is implied by initialization. The embedding backend is
external; this head can consume SNN embeddings or explicitly labelled features.
"""
import math
import re

import numpy as np


class ActionHead:
    FORMAT_VERSION=2

    def __init__(self, embed_dim=64, n_tags=8, seed=7):
        if type(embed_dim) is not int or not 1 <= embed_dim <= 4096:
            raise ValueError('embed_dim must be 1..4096')
        if type(n_tags) is not int or not 1 <= n_tags <= 8:
            raise ValueError('n_tags must be 1..8')
        self.embed_dim,self.n_tags=embed_dim,n_tags
        self.action_dim=n_tags+3
        rng=np.random.default_rng(seed)
        self.w_state_action=rng.normal(0,.01,(embed_dim,self.action_dim))
        self.w_action=np.zeros(self.action_dim)

    def action_features(self,tags):
        if not 1 <= len(tags) <= 512:
            raise ValueError('candidate count must be 1..512')
        features=np.zeros((len(tags),self.action_dim))
        for i,tag in enumerate(tags):
            match=re.fullmatch(r'A([1-8])(?::(\d{1,2}),(\d{1,2}))?',str(tag))
            if match is None:
                raise ValueError('Unknown action tag')
            action=int(match[1])-1
            if action>=self.n_tags:
                raise ValueError('Action tag out of range')
            features[i,action]=1
            if match[2] is not None:
                x,y=int(match[2]),int(match[3])
                if not 0 <= x <= 63 or not 0 <= y <= 63:
                    raise ValueError('Click coordinates must be within 0..63')
                features[i,-3:]=[2*x/63-1,2*y/63-1,1]
        return features

    def tag_onehot(self,tags,n_tags=None):
        if n_tags is not None and n_tags!=self.n_tags:
            raise ValueError('n_tags does not match model')
        return self.action_features(tags)[:,:self.n_tags]

    def _inputs(self,embeds,tags,legal_mask):
        features=self.action_features(tags)
        embeds=np.asarray(embeds,dtype=float)
        if embeds.shape!=(len(tags),self.embed_dim) or not np.isfinite(embeds).all():
            raise ValueError('Embeddings must be finite [candidates,embed_dim]')
        mask=np.ones(len(tags),dtype=bool) if legal_mask is None else np.asarray(legal_mask,dtype=bool)
        if mask.shape!=(len(tags),) or not mask.any():
            raise ValueError('At least one legal candidate is required')
        return embeds,features,mask

    def scores(self,embeds,tags,legal_mask=None):
        embeds,features,mask=self._inputs(embeds,tags,legal_mask)
        scores=np.einsum('nd,dk,nk->n',embeds,self.w_state_action,features)+features@self.w_action
        return np.where(mask,scores,-np.inf)

    def train_step(self,embeds,tags,teacher_idx,lr=.01,legal_mask=None):
        embeds,features,mask=self._inputs(embeds,tags,legal_mask)
        if type(teacher_idx) is not int or not 0 <= teacher_idx < len(tags) or not mask[teacher_idx]:
            raise ValueError('Teacher must refer to a legal candidate')
        if not math.isfinite(lr) or not 0 < lr <= 1:
            raise ValueError('lr must be finite within (0,1]')
        logits=self.scores(embeds,tags,mask)
        logits-=np.max(logits)
        probability=np.exp(logits);probability/=probability.sum()
        loss=-logits[teacher_idx]+np.log(np.exp(logits).sum())
        grad=probability;grad[teacher_idx]-=1
        self.w_state_action-=lr*np.einsum('n,nd,nk->dk',grad,embeds,features)
        self.w_action-=lr*(grad@features)
        return float(loss)

    def save(self,path):
        np.savez(path,format_version=self.FORMAT_VERSION,embed_dim=self.embed_dim,
                 n_tags=self.n_tags,w_state_action=self.w_state_action,w_action=self.w_action)

    def load(self,path):
        with np.load(path,allow_pickle=False) as archive:
            if 'format_version' not in archive or int(archive['format_version'])!=self.FORMAT_VERSION:
                raise ValueError('Unsupported legacy checkpoint/version; explicit retraining required')
            if int(archive['embed_dim'])!=self.embed_dim or int(archive['n_tags'])!=self.n_tags:
                raise ValueError('Checkpoint dimensions do not match model')
            weights=np.array(archive['w_state_action'],dtype=float)
            bias=np.array(archive['w_action'],dtype=float)
            if weights.shape!=self.w_state_action.shape or bias.shape!=self.w_action.shape:
                raise ValueError('Checkpoint parameter shapes do not match')
            if not np.isfinite(weights).all() or not np.isfinite(bias).all():
                raise ValueError('Nonfinite checkpoint weights')
        self.w_state_action,self.w_action=weights,bias
