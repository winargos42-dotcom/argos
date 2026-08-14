import pytest

from integrations.planeta_mcp.live_login import LiveLoginController


def test_live_login_token_is_one_time_and_expires():
    now = [1000.0]
    ctl = LiveLoginController(ttl_seconds=300, clock=lambda: now[0])
    session = ctl.start()

    assert ctl.get(session.token) is not None
    assert ctl.get(session.token).state == "waiting_for_human"

    ctl.mark_ready(session.token)
    assert ctl.get(session.token).state == "draft_ready"

    ctl.invalidate(session.token)
    assert ctl.get(session.token) is None


def test_live_login_expired_token_disappears():
    now = [1000.0]
    ctl = LiveLoginController(ttl_seconds=10, clock=lambda: now[0])
    token = ctl.start().token

    now[0] = 1011.0
    assert ctl.get(token) is None


def test_live_login_capability_exchanges_once_and_ready_disables_view():
    ctl = LiveLoginController(ttl_seconds=300)
    session = ctl.start()

    exchanged = ctl.exchange(session.token)
    assert exchanged.exchanged is True
    assert exchanged.view_active is True

    with pytest.raises(ValueError, match="already exchanged"):
        ctl.exchange(session.token)

    ready = ctl.mark_ready(session.token)
    assert ready.state == "draft_ready"
    assert ready.view_active is False
