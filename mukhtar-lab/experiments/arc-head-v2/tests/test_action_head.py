import importlib.util
import inspect
from pathlib import Path

import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]


def head_class():
    # RED exercises the current real implementation, not a fabricated stub.
    path=ROOT/'action_head.py'
    if not path.exists():
        path=ROOT/'reference/mukhtar/action_head.py'
    spec=importlib.util.spec_from_file_location('under_test',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.ActionHead


def test_head_learns_opposite_actions_in_opposite_states():
    head=head_class()(embed_dim=2,seed=7)
    tags=['A1','A2']
    positive=np.tile([1.,0.],(2,1));negative=-positive
    for _ in range(200):
        head.train_step(positive,tags,0,lr=.05)
        head.train_step(negative,tags,1,lr=.05)
    assert np.argmax(head.scores(positive,tags))==0
    assert np.argmax(head.scores(negative,tags))==1


def test_click_coordinates_interact_with_state_instead_of_collapsing():
    head=head_class()(embed_dim=2,seed=7)
    tags=['A6:0,32','A6:63,32']
    positive=np.tile([1.,0.],(2,1));negative=-positive
    for _ in range(200):
        head.train_step(positive,tags,0,lr=.05)
        head.train_step(negative,tags,1,lr=.05)
    assert np.argmax(head.scores(positive,tags))==0
    assert np.argmax(head.scores(negative,tags))==1


def test_candidate_permutation_preserves_each_score():
    head=head_class()(embed_dim=2,seed=7)
    embeds=np.array([[1.,2.],[-1.,3.],[.5,.25]])
    tags=['A1','A6:0,63','A6:63,0']; order=[2,0,1]
    np.testing.assert_allclose(head.scores(embeds[order],[tags[i] for i in order]),
                               head.scores(embeds,tags)[order])


def test_illegal_action_cannot_win_or_receive_teacher_update():
    head=head_class()(embed_dim=2)
    assert 'legal_mask' in inspect.signature(head.scores).parameters,'no legal mask support'
    embeds=np.array([[1.,2.],[1.,2.]])
    scores=head.scores(embeds,['A1','A2'],legal_mask=[False,True])
    assert scores[0]==-np.inf and np.argmax(scores)==1
    with pytest.raises(ValueError,match='legal'):
        head.train_step(embeds,['A1','A2'],0,legal_mask=[False,True])


def test_saved_checkpoint_roundtrip_and_legacy_rejection(tmp_path):
    cls=head_class();head=cls(embed_dim=2,seed=7)
    assert hasattr(head,'w_state_action'),'state-action interaction weights absent'
    embeds=np.array([[1.,2.],[3.,4.]])
    head.train_step(embeds,['A1','A2'],1,lr=.05)
    path=tmp_path/'head.npz';head.save(path)
    restored=cls(embed_dim=2,seed=99);restored.load(path)
    np.testing.assert_array_equal(restored.scores(embeds,['A1','A2']),head.scores(embeds,['A1','A2']))
    with pytest.raises(ValueError,match='legacy|version'):
        cls().load(ROOT/'reference/results/arc3_head_stable_route.npz')


def test_update_matches_finite_difference_gradient():
    head=head_class()(embed_dim=2,seed=7)
    assert hasattr(head,'w_state_action'),'state-action interaction weights absent'
    embeds=np.array([[.2,-.5],[.3,.7]])
    tags=['A1','A2'];eps=1e-6
    def loss():
        scores=head.scores(embeds,tags)
        return np.logaddexp.reduce(scores)-scores[1]
    numeric=np.zeros_like(head.w_state_action)
    for index in np.ndindex(numeric.shape):
        original=head.w_state_action[index]
        head.w_state_action[index]=original+eps; plus=loss()
        head.w_state_action[index]=original-eps; minus=loss()
        head.w_state_action[index]=original
        numeric[index]=(plus-minus)/(2*eps)
    before=head.w_state_action.copy();head.train_step(embeds,tags,1,lr=.01)
    np.testing.assert_allclose((before-head.w_state_action)/.01,numeric,atol=1e-8,rtol=1e-5)


@pytest.mark.parametrize('tags,embeds',[
    (['A6:64,0'],[[1.,2.]]),(['state'],[[1.,2.]]),
    (['A1'],[[float('nan'),2.]]),(['A1','A2'],[[1.,2.]]),
])
def test_rejects_invalid_candidates_without_poisoning_model(tags,embeds):
    with pytest.raises(ValueError):
        head_class()(embed_dim=2).scores(embeds,tags)
