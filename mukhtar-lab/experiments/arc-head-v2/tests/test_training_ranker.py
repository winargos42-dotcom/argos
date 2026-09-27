import importlib
import importlib.util
from types import SimpleNamespace

import numpy as np
import pytest

from action_head import ActionHead


def trainer():
    assert importlib.util.find_spec('train_experiment'),'No bounded CPU trainer'
    return importlib.import_module('train_experiment')


def ranker_class():
    assert importlib.util.find_spec('interaction_ranker'),'No repaired candidate adapter'
    return importlib.import_module('interaction_ranker').InteractionRanker


def test_batched_trainer_learns_state_dependent_targets():
    x=np.array([[1.,0.],[-1.,0.]]*8);y=np.array([0,1]*8)
    head=ActionHead(embed_dim=2)
    trainer().fit(head,x,y,epochs=100,lr=.2,l2=0)
    assert np.argmax(head.scores(np.tile([1.,0.],(4,1)),['A1','A2','A3','A4']))==0
    assert np.argmax(head.scores(np.tile([-1.,0.],(4,1)),['A1','A2','A3','A4']))==1


def test_withheld_labels_and_features_cannot_change_trained_weights():
    data={'features':np.array([[1.,0.],[-1.,0.],[0.,1.],[0.,-1.]]),
          'targets':np.array([0,1,2,3]),'levels':np.array([1,5,6,7]),
          'frame_hashes':np.array(['a','b','c','d'])}
    first,_=trainer().train_split(data,epochs=20,lr=.1,l2=0,seed=7)
    data['targets'][2:]=[0,0];data['features'][2:]=1e8
    second,_=trainer().train_split(data,epochs=20,lr=.1,l2=0,seed=7)
    np.testing.assert_array_equal(first.w_state_action,second.w_state_action)
    np.testing.assert_array_equal(first.w_action,second.w_action)


def test_ranker_removes_illegal_high_scoring_action():
    head=ActionHead(embed_dim=2);head.w_state_action[:]=0;head.w_action[0]=1000
    ranker=ranker_class()(head)
    candidates=[('A1',SimpleNamespace(value=1),None),('A2',SimpleNamespace(value=2),None)]
    result=ranker.rank_embedding('state',candidates,[0.,0.],available_actions=[2])
    assert result==[candidates[1]]
    with pytest.raises(ValueError,match='legal'):
        ranker.rank_embedding('state',candidates,[0.,0.],available_actions=[3])


def test_ranker_keeps_click_coordinates_attached_to_selected_action():
    head=ActionHead(embed_dim=2);head.w_state_action[:]=0;head.w_action[:]=0
    head.w_state_action[0,-3]=1
    ranker=ranker_class()(head)
    candidates=[('A6:0,32',SimpleNamespace(value=6),{'x':0,'y':32}),
                ('A6:63,32',SimpleNamespace(value=6),{'x':63,'y':32})]
    assert ranker.rank_embedding('s',candidates,[1.,0.],available_actions=[6])[0] is candidates[1]
    assert ranker.rank_embedding('s',candidates,[-1.,0.],available_actions=[6])[0] is candidates[0]
