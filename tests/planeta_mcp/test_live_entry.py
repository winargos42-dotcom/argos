import asyncio
import re

from fastapi.testclient import TestClient

from integrations.planeta_mcp import entry_server
from integrations.planeta_mcp.audit import AuditLogger
from integrations.planeta_mcp.browser import BrowserResult
from integrations.planeta_mcp.defaults import default_argos_reboot_campaign
from integrations.planeta_mcp.entry_server import create_entry_app
from integrations.planeta_mcp.live_login import LiveLoginController
from integrations.planeta_mcp.security import ApprovalGate
from integrations.planeta_mcp.server import create_app
from integrations.planeta_mcp.service import PlanetaCampaignService
from integrations.planeta_mcp.store import CampaignStore


class EntryCoordinator:
    def __init__(self):
        self.controller = LiveLoginController(ttl_seconds=300)
        self.durability = "ephemeral"
        self.start_calls = 0
        self.last_token = None

    async def start(self):
        self.start_calls += 1
        session = self.controller.start()
        self.last_token = session.token
        return session

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


class SubmitBrowser:
    def __init__(self):
        self.submit_calls = 0

    async def fill_draft(self, campaign):
        return BrowserResult(status="ok", reason="noop")

    async def fill_rewards(self, campaign):
        return BrowserResult(status="ok", reason="noop", draft_snapshot={"rewards": []})

    async def read_draft(self, expected_region=None):
        return BrowserResult(status="ok", reason="noop")

    async def read_rewards(self):
        return BrowserResult(status="ok", reason="noop", draft_snapshot={"rewards": []})

    async def submit_for_moderation(self):
        self.submit_calls += 1
        return BrowserResult(status="ok", reason="submitted")


def make_submit_service(tmp_path):
    browser = SubmitBrowser()
    service = PlanetaCampaignService(
        store=CampaignStore(tmp_path / "campaign.json"),
        browser=browser,
        approval_gate=ApprovalGate(b"approval-secret", ttl_seconds=300),
        audit=AuditLogger(tmp_path / "audit.jsonl"),
    )
    asyncio.run(service.prepare_campaign(default_argos_reboot_campaign()))
    return service


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


def test_live_moderation_requires_draft_ready_and_final_post_submits(tmp_path, monkeypatch):
    coordinator = EntryCoordinator()
    core_app = create_app(
        service=None,
        enable_mcp=False,
        live_control_secret="control-secret",
        live_coordinator=coordinator,
    )
    service = make_submit_service(tmp_path)
    monkeypatch.setattr(entry_server.server_module, "build_default_service", lambda: service)
    app = create_entry_app(
        core_app,
        entry_token="entry-capability",
        control_secret="control-secret",
    )
    client = TestClient(app, base_url="https://testserver")

    exchanged = client.post(
        "/live-login/exchange",
        headers={"Authorization": "Bearer entry-capability"},
    )
    assert exchanged.status_code == 204

    blocked = client.get("/live-login/moderation")
    assert blocked.status_code == 409
    assert service.browser.submit_calls == 0

    assert coordinator.last_token is not None
    coordinator.controller.mark_ready(coordinator.last_token)
    approval = client.get("/live-login/moderation")
    assert approval.status_code == 200
    assert "Подтвердить и отправить на модерацию" in approval.text
    assert service.browser.submit_calls == 0
    assert approval.headers["cache-control"].startswith("no-store")

    action = re.search(r'<form method="post" action="([^"]+)">', approval.text)
    csrf = re.search(r'name="csrf_token" value="([^"]+)"', approval.text)
    assert action is not None
    assert csrf is not None

    submitted = client.post(action.group(1), data={"csrf_token": csrf.group(1)})
    assert submitted.status_code == 200
    assert "Кампания отправлена на модерацию" in submitted.text
    assert service.browser.submit_calls == 1

    repeated = client.post(action.group(1), data={"csrf_token": csrf.group(1)})
    assert repeated.status_code in {400, 404, 409}
    assert service.browser.submit_calls == 1
