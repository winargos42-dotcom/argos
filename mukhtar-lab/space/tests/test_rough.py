import importlib
import sys
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import mujoco
import numpy as np
import pytest


LAB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LAB / 'fly_bridge'))
sys.path.insert(0, str(LAB))


def rough():
    assert importlib.util.find_spec('rough_lab'), 'No reproducible rough terrain adapter'
    return importlib.import_module('rough_lab')


def test_rough_geometry_matches_physical_source_and_preserves_body():
    module = rough()
    model = module.build_rough(LAB / 'models/hexapod.xml')
    original = mujoco.MjModel.from_xml_path(str(LAB / 'models/hexapod.xml'))
    assert model.ngeom == original.ngeom + 7
    assert (model.nq, model.nv, model.nu) == (original.nq, original.nv, original.nu)
    for i, height in enumerate([.004, .006, .008, .010, .008, .006, .004]):
        gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, f'bump{i}')
        np.testing.assert_allclose(model.geom_size[gid], [.012, .30, height / 2])
        np.testing.assert_allclose(model.geom_pos[gid], [.40 + i * .05, 0, height / 2])


def test_rough_pipeline_classifies_actual_named_contact_as_obstacle():
    module = rough()
    model = module.build_rough(LAB / 'models/hexapod.xml')
    pipeline = module.pipeline_for_rough(model)
    foot = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, 'foot0')
    bump = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, 'bump0')
    pipeline.force_reader = lambda *_: np.array([1., 0, 0, 0, 0, 0])
    contact = SimpleNamespace(geom1=foot, geom2=bump, pos=np.zeros(3), frame=np.eye(3))
    signal = pipeline.update(SimpleNamespace(ncon=1, contact=[contact]))[0]['foot']
    assert signal.kind == 'obstacle'
    assert signal.pair == ('foot0', 'bump0')
    assert signal.active


def test_missing_floor_is_rejected(tmp_path):
    path = tmp_path / 'no-floor.xml'
    path.write_text('<mujoco><worldbody/></mujoco>')
    with pytest.raises(ValueError, match='floor'):
        rough().build_rough(path)
