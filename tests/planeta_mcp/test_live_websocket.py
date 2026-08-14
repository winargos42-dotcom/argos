from urllib.parse import urlsplit

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from integrations.planeta_mcp.live_login import LiveLoginController
from integrations.planeta_mcp.server import create_app


class FakeCoordinator:
    def __init__(self):
        self.controller = LiveLoginController(ttl_seconds=300)
        self.durability = "ephemeral"

    async def start(self):
        return self.controller.start()

    def exchange(self, token):
        return self.controller.exchange(token)

    def status(self, token):
        session = self.controller.get(token)
        if session is None:
            return None
        return {"state": session.state.value, "expires_at": session.expires_at, "durability": self.durability}

    def websockify_url(self, token):
        session = self.controller.get(token)
        if session is None or not session.exchanged or not session.view_active:
            return None
        return "ws://127.0.0.1:6080"


def test_live_websocket_requires_cookie_and_relays_only_to_loopback():
    coordinator = FakeCoordinator()
    seen = []

    async def fake_relay(websocket, target):
        seen.append(target)
        await websocket.accept()
        await websocket.send_text("relay-ok")

    app = create_app(
        service=None,
        enable_mcp=False,
        live_control_secret="control-secret",
        live_coordinator=coordinator,
        live_ws_relay=fake_relay,
    )

    unauthenticated = TestClient(app, base_url="https://testserver")
    with pytest.raises(WebSocketDisconnect) as exc:
        with unauthenticated.websocket_connect("/live-login/websockify"):
            pass
    assert exc.value.code == 4401

    client = TestClient(app, base_url="https://testserver")
    started = client.post(
        "/live-login/start",
        headers={"Authorization": "Bearer control-secret"},
    ).json()
    capability = urlsplit(started["browser_url"]).fragment
    exchanged = client.post(
        "/live-login/exchange",
        headers={"Authorization": f"Bearer {capability}"},
    )
    assert exchanged.status_code == 204

    with client.websocket_connect("/live-login/websockify") as websocket:
        assert websocket.receive_text() == "relay-ok"

    assert seen == ["ws://127.0.0.1:6080"]
