import asyncio

import pytest
from cryptography.fernet import Fernet

from integrations.planeta_mcp.audit import AuditLogger
from integrations.planeta_mcp.browser import BrowserResult
from integrations.planeta_mcp.config import PlanetaConfig
from integrations.planeta_mcp.live_bridge import LiveLoginCoordinator, _is_allowed_human_auth_origin
from integrations.planeta_mcp.live_login import LiveLoginController
from integrations.planeta_mcp.security import ApprovalGate
from integrations.planeta_mcp.service import PlanetaCampaignService
from integrations.planeta_mcp.session_store import SessionStore
from integrations.planeta_mcp.store import CampaignStore


class IdleBrowser:
    async def close(self):
        return None


class SharedDraftBrowser:
    def __init__(self):
        self.submit_calls = 0
        self.rewards_snapshot = []

    async def inspect(self):
        return BrowserResult(status="ok", reason="known draft editor detected")

    async def fill_draft(self, campaign):
        return BrowserResult(
            status="ok",
            reason="saved",
            draft_snapshot={
                "title": campaign.title,
                "target_amount": str(campaign.target_amount),
                "summary": campaign.summary,
                "story": campaign.story,
            },
        )

    async def fill_rewards(self, campaign):
        self.rewards_snapshot = [
            {
                "title": reward.title,
                "amount": str(reward.amount),
                "description": reward.description,
                "physical": reward.physical,
            }
            for reward in campaign.rewards
        ]
        return BrowserResult(
            status="ok",
            reason="rewards saved",
            draft_snapshot={"rewards": self.rewards_snapshot},
        )

    async def read_draft(self):
        campaign = self.campaign_store.load_required()
        return BrowserResult(
            status="ok",
            reason="read",
            draft_snapshot={
                "title": campaign.title,
                "target_amount": str(campaign.target_amount),
                "summary": campaign.summary,
                "story": campaign.story,
            },
        )

    async def read_rewards(self):
        return BrowserResult(
            status="ok",
            reason="rewards read",
            draft_snapshot={"rewards": self.rewards_snapshot},
        )

    async def submit_for_moderation(self):
        self.submit_calls += 1
        return BrowserResult(status="ok", reason="should not happen")

    async def close(self):
        return None


class RecoveringSharedBrowser(SharedDraftBrowser):
    def __init__(self, runtime, draft_url):
        super().__init__()
        self.runtime = runtime
        self.draft_url = draft_url
        self.navigate_calls = 0

    async def inspect(self):
        if self.runtime.page.url != self.draft_url:
            return BrowserResult(status="ui_changed", reason="known draft selectors are missing or ambiguous")
        return await super().inspect()

    async def navigate_to_draft(self):
        self.navigate_calls += 1
        self.runtime.page.url = self.draft_url
        return BrowserResult(status="ok", reason="draft opened")


class FakeRuntime:
    cdp_url = "http://127.0.0.1:9222"
    websockify_url = "ws://127.0.0.1:6080"

    def __init__(self):
        self.started = False
        self.stopped = False
        self.page = type("Page", (), {"url": "https://planeta.ru/campaigns/251138/edit/about"})()

    async def start(self):
        self.started = True
        return self.page

    async def storage_state(self):
        return {
            "cookies": [{"name": "sid", "value": "session-cookie", "domain": ".planeta.ru", "path": "/"}],
            "origins": [],
        }

    async def stop(self):
        self.stopped = True


def test_live_bridge_default_runtime_uses_session_dir(tmp_path):
    state_path = tmp_path / "work" / "campaign.json"
    session_dir = tmp_path / "persistent"
    config = PlanetaConfig(
        draft_url="https://planeta.ru/campaigns/251138/edit/about",
        state_path=state_path,
        session_dir=session_dir,
    )
    service = PlanetaCampaignService(
        store=CampaignStore(state_path),
        browser=IdleBrowser(),
        approval_gate=ApprovalGate(b"approval-secret", ttl_seconds=300),
        audit=AuditLogger(state_path.parent / "audit.jsonl"),
    )
    coordinator = LiveLoginCoordinator(
        service=service,
        config=config,
        session_store=SessionStore(session_dir / "session.enc", Fernet.generate_key()),
    )

    runtime = coordinator._runtime_factory()

    assert runtime.data_dir == session_dir
    assert runtime.profile_dir == session_dir / "browser-profile"


def test_human_auth_origin_allows_https_planeta_subdomains_only():
    base = "https://planeta.ru"
    assert _is_allowed_human_auth_origin("https://planeta.ru/nuborn_session", base) is True
    assert _is_allowed_human_auth_origin("https://id.planeta.ru/login", base) is True
    assert _is_allowed_human_auth_origin("https://school.planeta.ru/check", base) is True
    assert _is_allowed_human_auth_origin("http://id.planeta.ru/login", base) is False
    assert _is_allowed_human_auth_origin("https://planeta.ru.evil.example/login", base) is False
    assert _is_allowed_human_auth_origin("https://example.com/login", base) is False


@pytest.mark.asyncio
async def test_live_bridge_captures_session_fills_syncs_and_never_submits(tmp_path):
    config = PlanetaConfig(
        base_url="https://planeta.ru",
        draft_url="https://planeta.ru/campaigns/251138/edit/about",
        headless=False,
        state_path=tmp_path / "campaign.json",
    )
    store = CampaignStore(config.state_path)
    shared_browser = SharedDraftBrowser()
    shared_browser.campaign_store = store
    service = PlanetaCampaignService(
        store=store,
        browser=IdleBrowser(),
        approval_gate=ApprovalGate(b"approval-secret", ttl_seconds=300),
        audit=AuditLogger(tmp_path / "audit.jsonl"),
    )
    session_store = SessionStore(tmp_path / "session.enc", Fernet.generate_key())
    runtime = FakeRuntime()
    controller = LiveLoginController(ttl_seconds=300)

    coordinator = LiveLoginCoordinator(
        service=service,
        config=config,
        session_store=session_store,
        controller=controller,
        runtime_factory=lambda: runtime,
        browser_factory=lambda _runtime: shared_browser,
        poll_interval=0.001,
        durability="ephemeral",
    )

    session = await coordinator.start()
    await coordinator.wait(session.token, timeout=2.0)

    status = coordinator.status(session.token)
    assert status is not None
    assert status["state"] == "draft_ready"
    assert status["fill_status"] == "ok"
    assert status["sync_status"] == "ok"
    assert status["differences"] == []
    assert status["durability"] == "ephemeral"
    assert session_store.load_storage_state()["cookies"][0]["value"] == "session-cookie"
    assert b"session-cookie" not in (tmp_path / "session.enc").read_bytes()
    assert shared_browser.submit_calls == 0
    assert runtime.started is True
    assert runtime.stopped is True
    assert controller.get(session.token).view_active is False


@pytest.mark.asyncio
async def test_live_bridge_returns_authenticated_same_origin_page_to_configured_draft(tmp_path):
    draft_url = "https://planeta.ru/campaigns/251138/edit/about"
    config = PlanetaConfig(
        base_url="https://planeta.ru",
        draft_url=draft_url,
        headless=False,
        state_path=tmp_path / "campaign.json",
    )
    store = CampaignStore(config.state_path)
    runtime = FakeRuntime()
    runtime.page.url = "https://planeta.ru/profile"
    shared_browser = RecoveringSharedBrowser(runtime, draft_url)
    shared_browser.campaign_store = store
    service = PlanetaCampaignService(
        store=store,
        browser=IdleBrowser(),
        approval_gate=ApprovalGate(b"approval-secret", ttl_seconds=300),
        audit=AuditLogger(tmp_path / "audit.jsonl"),
    )
    session_store = SessionStore(tmp_path / "session.enc", Fernet.generate_key())
    controller = LiveLoginController(ttl_seconds=300)
    coordinator = LiveLoginCoordinator(
        service=service,
        config=config,
        session_store=session_store,
        controller=controller,
        runtime_factory=lambda: runtime,
        browser_factory=lambda _runtime: shared_browser,
        poll_interval=0.001,
    )

    session = await coordinator.start()
    await coordinator.wait(session.token, timeout=2.0)

    status = coordinator.status(session.token)
    assert status is not None
    assert status["state"] == "draft_ready"
    assert shared_browser.navigate_calls == 1
    assert runtime.page.url == draft_url


@pytest.mark.asyncio
async def test_live_bridge_rejects_unexpected_top_level_origin_without_capture(tmp_path):
    config = PlanetaConfig(
        base_url="https://planeta.ru",
        draft_url="https://planeta.ru/campaigns/251138/edit/about",
        headless=False,
        state_path=tmp_path / "campaign.json",
    )
    store = CampaignStore(config.state_path)
    service = PlanetaCampaignService(
        store=store,
        browser=IdleBrowser(),
        approval_gate=ApprovalGate(b"approval-secret", ttl_seconds=300),
        audit=AuditLogger(tmp_path / "audit.jsonl"),
    )
    session_store = SessionStore(tmp_path / "session.enc", Fernet.generate_key())
    runtime = FakeRuntime()
    runtime.page.url = "https://example.com/phishing"
    controller = LiveLoginController(ttl_seconds=300)

    coordinator = LiveLoginCoordinator(
        service=service,
        config=config,
        session_store=session_store,
        controller=controller,
        runtime_factory=lambda: runtime,
        browser_factory=lambda _runtime: SharedDraftBrowser(),
        poll_interval=0.001,
    )

    session = await coordinator.start()
    await coordinator.wait(session.token, timeout=2.0)
    status = coordinator.status(session.token)

    assert status["state"] == "human_action_required"
    assert status["reason"] == "unexpected_origin"
    assert session_store.load_storage_state() is None
    assert runtime.stopped is True
