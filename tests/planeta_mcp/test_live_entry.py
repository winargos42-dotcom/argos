from fastapi.testclient import TestClient

from integrations.planeta_mcp.entry_server import create_entry_app
from integrations.planeta_mcp.live_login import LiveLoginController
from integrations.planeta_mcp.server import create_app


class EntryCoordinator:
    def __init__(self):
        self.controller = LiveLoginController(ttl_seconds=300)
        self.durability = "ephemeral"
        self.start_calls = 0

    async def start(self):
        self.start_calls += 1
        return self.controller.start()

    def exchange(self, token):
        return self.controller.exchange(token)

    def status(self, token):
        session = self.controller.get(token)
        if session is None:
            return None
        return {
            "state": session.state.value,
            "expires_at": session.expires_at,
            "durability": self.durability,
        }

    def websockify_url(self, token):
        return None


def test_entry_capability_starts_live_browser_once_and_becomes_session_cookie():
    coordinator = EntryCoordinator()
    core_app = create_app(
        service=None,
        enable_mcp=False,
        live_control_secret="control-secret",
        live_coordinator=coordinator,
    )
    app = create_entry_app(
        core_app,
        entry_token="entry-capability",
        control_secret="control-secret",
    )
    client = TestClient(app, base_url="https://testserver")

    first = client.post(
        "/live-login/exchange",
        headers={"Authorization": "Bearer entry-capability"},
    )
    assert first.status_code == 204
    assert coordinator.start_calls == 1
    cookie = first.headers["set-cookie"]
    assert "__Host-planeta_live=" in cookie
    assert "entry-capability" not in cookie

    second = client.post(
        "/live-login/exchange",
        headers={"Authorization": "Bearer entry-capability"},
    )
    assert second.status_code == 409
    assert coordinator.start_calls == 1


def test_entry_wrapper_passes_normal_live_sessions_through():
    coordinator = EntryCoordinator()
    core_app = create_app(
        service=None,
        enable_mcp=False,
        live_control_secret="control-secret",
        live_coordinator=coordinator,
    )
    app = create_entry_app(
        core_app,
        entry_token="entry-capability",
        control_secret="control-secret",
    )
    client = TestClient(app, base_url="https://testserver")

    started = client.post(
        "/live-login/start",
        headers={"Authorization": "Bearer control-secret"},
    ).json()
    actual = started["browser_url"].split("#", 1)[1]
    exchanged = client.post(
        "/live-login/exchange",
        headers={"Authorization": f"Bearer {actual}"},
    )

    assert exchanged.status_code == 204
    assert coordinator.start_calls == 1


def test_mobile_launcher_reuses_active_cookie_before_consuming_entry_capability():
    coordinator = EntryCoordinator()
    core_app = create_app(
        service=None,
        enable_mcp=False,
        live_control_secret="control-secret",
        live_coordinator=coordinator,
    )
    app = create_entry_app(
        core_app,
        entry_token="entry-capability",
        control_secret="control-secret",
    )
    client = TestClient(app, base_url="https://testserver")

    page = client.get("/live-login/mobile")
    assert page.status_code == 200
    assert "fetch('/live-login/status'" in page.text
    assert "fetch('/live-login/exchange'" in page.text
    assert page.text.index("fetch('/live-login/status'") < page.text.index("fetch('/live-login/exchange'")
    assert "credentials:'same-origin'" in page.text
