import asyncio
import re
from urllib.parse import urlsplit

import pytest
from fastapi.testclient import TestClient

from integrations.planeta_mcp.audit import AuditLogger
from integrations.planeta_mcp.browser import BrowserResult
from integrations.planeta_mcp.defaults import default_argos_reboot_campaign
from integrations.planeta_mcp.live_login import LiveLoginController
from integrations.planeta_mcp.security import ApprovalError, ApprovalGate
from integrations.planeta_mcp.server import REGISTERED_TOOL_NAMES, create_app
from integrations.planeta_mcp.service import PlanetaCampaignService
from integrations.planeta_mcp.store import CampaignStore


class NoopBrowser:
    def __init__(self):
        self.submit_calls = 0

    async def fill_draft(self, campaign):
        return BrowserResult(status="ok", reason="noop")

    async def read_draft(self):
        return BrowserResult(status="ok", reason="noop")

    async def submit_for_moderation(self):
        self.submit_calls += 1
        return BrowserResult(status="ok", reason="noop")


class FakeLiveCoordinator:
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
        return {
            "state": session.state.value,
            "expires_at": session.expires_at,
            "durability": self.durability,
        }

    def websockify_url(self, token):
        session = self.controller.get(token)
        if session is None or not session.exchanged or not session.view_active:
            return None
        return "ws://127.0.0.1:6080"


def make_service(tmp_path):
    browser = NoopBrowser()
    service = PlanetaCampaignService(
        store=CampaignStore(tmp_path / "campaign.json"),
        browser=browser,
        approval_gate=ApprovalGate(b"approval-secret", ttl_seconds=300),
        audit=AuditLogger(tmp_path / "audit.jsonl"),
    )
    return service


def test_health():
    client = TestClient(create_app(service=None, enable_mcp=False))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["service"] == "planeta-mcp"


def test_tool_names_are_registered():
    assert {
        "planeta_campaign_status",
        "planeta_campaign_preview",
        "planeta_validate_campaign",
        "planeta_prepare_campaign",
        "planeta_fill_draft",
        "planeta_sync_draft",
        "planeta_request_submit_approval",
        "planeta_submit_for_moderation",
    } == set(REGISTERED_TOOL_NAMES)


def test_approval_get_is_read_only_and_post_confirms(tmp_path):
    service = make_service(tmp_path)
    campaign = default_argos_reboot_campaign()
    asyncio.run(service.prepare_campaign(campaign))
    request = asyncio.run(service.request_submit_approval())

    client = TestClient(create_app(service=service, enable_mcp=False))
    response = client.get(f"/approve/{request.request_id}")
    assert response.status_code == 200
    assert "Подтвердить отправку на модерацию" in response.text

    with pytest.raises(ApprovalError, match="human confirmation"):
        service.approval_gate.consume(request.request_id, campaign)

    match = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
    assert match is not None
    confirmed = client.post(
        f"/approve/{request.request_id}",
        data={"csrf_token": match.group(1)},
    )
    assert confirmed.status_code == 200
    assert "Подтверждение принято" in confirmed.text

    service.approval_gate.consume(request.request_id, campaign)


def test_live_login_start_requires_control_secret_and_hides_capability_from_path(tmp_path):
    coordinator = FakeLiveCoordinator()
    client = TestClient(
        create_app(
            service=make_service(tmp_path),
            enable_mcp=False,
            live_control_secret="control-secret",
            live_coordinator=coordinator,
        ),
        base_url="https://testserver",
    )

    denied = client.post("/live-login/start")
    assert denied.status_code == 401

    started = client.post(
        "/live-login/start",
        headers={"Authorization": "Bearer control-secret"},
    )
    assert started.status_code == 200
    browser_url = started.json()["browser_url"]
    parsed = urlsplit(browser_url)
    assert parsed.path == "/live-login/"
    assert parsed.query == ""
    assert parsed.fragment
    assert parsed.fragment not in parsed.path
    assert parsed.fragment not in parsed.query


def test_live_login_fragment_exchanges_for_http_only_cookie_and_status_is_sanitized(tmp_path):
    coordinator = FakeLiveCoordinator()
    service = make_service(tmp_path)
    client = TestClient(
        create_app(
            service=service,
            enable_mcp=False,
            live_control_secret="control-secret",
            live_coordinator=coordinator,
        ),
        base_url="https://testserver",
    )
    started = client.post(
        "/live-login/start",
        headers={"Authorization": "Bearer control-secret"},
    ).json()
    capability = urlsplit(started["browser_url"]).fragment

    page = client.get("/live-login/")
    assert page.status_code == 200
    assert page.headers["cache-control"].startswith("no-store")
    assert page.headers["x-frame-options"] == "DENY"
    assert capability not in page.text

    exchanged = client.post(
        "/live-login/exchange",
        headers={"Authorization": f"Bearer {capability}"},
    )
    assert exchanged.status_code == 204
    cookie = exchanged.headers["set-cookie"].lower()
    assert "httponly" in cookie
    assert "secure" in cookie
    assert "samesite=strict" in cookie

    duplicate = client.post(
        "/live-login/exchange",
        headers={"Authorization": f"Bearer {capability}"},
    )
    assert duplicate.status_code == 204

    status = client.get("/live-login/status")
    assert status.status_code == 200
    assert status.json()["state"] == "human_login_in_progress"
    assert status.json()["durability"] == "ephemeral"
    assert "token" not in status.json()
    assert "cookie" not in status.json()
    assert service.browser.submit_calls == 0


def test_live_login_client_removes_fragment_and_uses_protected_websocket(tmp_path):
    client = TestClient(
        create_app(
            service=make_service(tmp_path),
            enable_mcp=False,
            live_control_secret="control-secret",
            live_coordinator=FakeLiveCoordinator(),
        )
    )
    response = client.get("/live-login/client.js")
    assert response.status_code == 200
    assert response.headers["cache-control"].startswith("no-store")
    assert "location.hash" in response.text
    assert "history.replaceState" in response.text
    assert "/live-login/exchange" in response.text
    assert "/live-login/websockify" in response.text
    assert "/live-login/assets/core/rfb.js" in response.text
    assert "password" not in response.text.casefold()
