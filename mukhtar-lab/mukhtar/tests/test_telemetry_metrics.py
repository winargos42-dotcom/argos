"""Pure metric checks: no simulator, model files or controller imports."""

import pytest


def test_false_events_use_episode_starts_only_with_explicit_oracle():
    from mukhtar.telemetry.metrics import EventMetrics

    events = EventMetrics()
    for _ in range(10):
        events.observe(0, "r4", ("R4_LOAD_HOLD",))
    events.observe(0, "r4", ())
    events.observe(0, "r4", ("R4_LOAD_HOLD",))
    events.observe(1, "r4", ("R4_LOAD_HOLD",))
    unknown = events.summary()
    assert unknown["false_events"] is None
    assert unknown["event_active_ticks"] == {"R4_LOAD_HOLD": 12}
    assert unknown["event_triggers"] == {"R4_LOAD_HOLD": 3}
    flat = events.summary(expected_no_reflex=True)
    assert flat["false_events"] == flat["trigger_count"] == 3


def test_reason_transition_marks_a_new_episode_without_a_silent_tick():
    from mukhtar.telemetry.metrics import EventMetrics

    events = EventMetrics()
    assert events.observe(0, "r3", ("SEARCH",)) == {"SEARCH": "trigger"}
    assert events.observe(0, "r3", ("SEARCH",)) == {"SEARCH": "active_tick"}
    assert events.observe(0, "r3", ("RETRACT",)) == {"RETRACT": "trigger"}
    assert events.summary()["trigger_count"] == 2


def test_unobserved_body_metrics_do_not_invent_a_reference_height():
    from mukhtar.telemetry.metrics import BodyMetrics

    report = BodyMetrics().summary()
    assert report["peak_body_drop_mm"] is None
    assert report["final_body_drop_mm"] is None
    assert report["max_tilt_deg"] is None


def test_body_tilt_accepts_scaled_quaternions_and_rejects_invalid_ones():
    from mukhtar.telemetry.metrics import BodyMetrics

    body = BodyMetrics()
    body.observe(0.0, (2.0, 0.0, 0.0, 2.0))
    body.observe(-0.02, (-2.0, 0.0, 0.0, -2.0))
    assert body.summary()["max_tilt_deg"] == 0.0
    assert body.summary()["peak_body_drop_mm"] == 20.0
    with pytest.raises(ValueError):
        body.observe(0.0, (0.0, 0.0, 0.0, 0.0))
