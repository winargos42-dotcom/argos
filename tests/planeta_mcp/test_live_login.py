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
