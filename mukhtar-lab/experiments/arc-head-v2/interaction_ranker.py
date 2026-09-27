"""Candidate ranking adapter: keep legal actions, coordinates and state history."""
import numpy as np

from experiment_data import encode_state


class InteractionRanker:
    def __init__(self,head,memory=None):
        self.head=head
        self.memory=memory
        self.tabu=set()

    def rank_embedding(self,frame_hash,candidates,embedding,available_actions):
        if not candidates:
            return []
        tags=[candidate[0] for candidate in candidates]
        legal=[]
        for tag,action,data in candidates:
            action_id=int(action.value)
            if tag.split(':')[0]!=f'A{action_id}':
                raise ValueError('Candidate tag and action ID disagree')
            if ':' in tag:
                x,y=map(int,tag.split(':')[1].split(','))
                if data is None or data.get('x')!=x or data.get('y')!=y:
                    raise ValueError('Candidate tag and click coordinates disagree')
            legal.append(action_id in available_actions)
        embeds=np.repeat(np.asarray(embedding,dtype=float)[None,:],len(candidates),axis=0)
        scores=self.head.scores(embeds,tags,legal_mask=legal)
        def key(i):
            tabu=(frame_hash,tags[i]) in self.tabu
            if self.memory is not None:
                tabu=tabu or self.memory.is_dead_end(frame_hash,tags[i])
            return tabu,-float(scores[i])
        return [candidates[i] for i in sorted((i for i,valid in enumerate(legal) if valid),key=key)]

    def rank_frame(self,frame_hash,candidates,frame,available_actions,previous_frame=None,previous_action=None):
        embedding=encode_state(frame,previous_frame,previous_action)
        return self.rank_embedding(frame_hash,candidates,embedding,available_actions)

    def record(self,frame_hash,action_key,new_state):
        self.tabu.add((frame_hash,action_key))
