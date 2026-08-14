from fastapi.testclient import TestClient

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
    app = create_app(
        service=None,
        enable_mcp=False,
        live_control_secret="control-secret",
        live_entry_token="entry-capability",
        live_coordinator=coordinator,
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
