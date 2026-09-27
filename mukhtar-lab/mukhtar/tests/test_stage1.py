import numpy as np

from mukhtar.reflexes.base import ReflexOutput
from mukhtar.reflexes.mixer import mix_reflex_outputs
from mukhtar.sensors.contact_pipeline import ContactPipeline


def test_reflex_output_joint_delta_is_not_shared():
    a = ReflexOutput()
    b = ReflexOutput()
    a.joint_delta[0] = 1.0
    assert b.joint_delta[0] == 0.0


def test_mixer_combines_outputs_and_keeps_safest_speed_scale():
    a = ReflexOutput(
        joint_delta=np.array([0.1, 0.2, 0.0], dtype=np.float32),
        phase_delta=0.3,
        phase_hold=True,
        speed_scale=0.8,
        active=True,
        reasons=("R1_STUMBLE",),
    )
    b = ReflexOutput(
        joint_delta=np.array([0.2, -0.1, 0.4], dtype=np.float32),
        phase_delta=-0.1,
        inhibit_swing=True,
        speed_scale=0.6,
        active=True,
        reasons=("R4_LOAD",),
    )

    out = mix_reflex_outputs([a, b], joint_delta_limit=np.array([0.25, 0.25, 0.25]), phase_delta_limit=0.15)

    np.testing.assert_allclose(out.joint_delta, [0.25, 0.1, 0.25], atol=1e-6)
    assert out.phase_delta == 0.15
    assert out.phase_hold is True
    assert out.inhibit_swing is True
    assert out.speed_scale == 0.6
    assert out.reasons == ("R1_STUMBLE", "R4_LOAD")


class FakeContact:
    def __init__(self, geom1, geom2, pos=(1.0, 2.0, 3.0), frame=None):
        self.geom1 = geom1
        self.geom2 = geom2
        self.pos = np.asarray(pos, dtype=float)
        self.frame = np.eye(3, dtype=float).reshape(-1) if frame is None else np.asarray(frame, dtype=float)


class FakeData:
    def __init__(self, contacts):
        self.contact = contacts
        self.ncon = len(contacts)


class FakeModel:
    pass


def test_contact_pipeline_tracks_part_force_and_duration():
    # geom 10 = leg0 foot; geom 20 = environment.
    # Force is expressed in MuJoCo's contact frame: [normal, tangent1, tangent2, torque...].
    forces = {
        0: np.array([5.0, 3.0, 4.0, 0.0, 0.0, 0.0]),
    }

    def force_reader(model, data, contact_index):
        return forces[contact_index]

    pipe = ContactPipeline(
        model=FakeModel(),
        geom_map={10: (0, "foot")},
        dt=0.002,
        force_reader=force_reader,
    )

    data = FakeData([FakeContact(10, 20)])
    first = pipe.update(data)[0]["foot"]
    second = pipe.update(data)[0]["foot"]

    assert first.active is True
    assert first.normal_force == 5.0
    assert first.tangential_force == 5.0
    assert first.duration_s == 0.002
    assert second.duration_s == 0.004


def test_contact_pipeline_resets_duration_when_contact_disappears():
    def force_reader(model, data, contact_index):
        return np.array([2.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    pipe = ContactPipeline(
        model=FakeModel(),
        geom_map={10: (0, "foot")},
        dt=0.002,
        force_reader=force_reader,
    )

    pipe.update(FakeData([FakeContact(10, 20)]))
    out = pipe.update(FakeData([]))

    assert out[0]["foot"].active is False
    assert out[0]["foot"].duration_s == 0.0
