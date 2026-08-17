import pytest

from integrations.planeta_mcp import bootstrap_once
from integrations.planeta_mcp.browser import BrowserResult, BrowserState
from integrations.planeta_mcp.config import PlanetaConfig


@pytest.mark.asyncio
async def test_bootstrap_saves_session_in_configured_session_dir(monkeypatch, tmp_path):
    state_path = tmp_path / "work" / "campaign.json"
    session_dir = tmp_path / "persistent"
    config = PlanetaConfig(
        base_url="https://planeta.ru",
        draft_url="https://planeta.ru/campaigns/251138/edit/about",
        state_path=state_path,
        session_dir=session_dir,
    )
    captured = {}

    class FakePage:
        async def goto(self, *_args, **_kwargs):
            return None

        async def wait_for_timeout(self, _milliseconds):
            return None

    class FakeContext:
        async def new_page(self):
            return FakePage()

        async def storage_state(self):
            return {"cookies": [], "origins": []}

    class FakeBrowser:
        async def new_context(self):
            return FakeContext()

        async def close(self):
            return None

    class FakePlaywright:
        class Chromium:
            async def launch(self, **_kwargs):
                return FakeBrowser()

        chromium = Chromium()

    class FakePlaywrightManager:
        async def __aenter__(self):
            return FakePlaywright()

        async def __aexit__(self, *_args):
            return None

    class FakeClassifier:
        def __init__(self, **_kwargs):
            pass

        async def classify_page(self, _page):
            return BrowserState.OK

    class CapturingSessionStore:
        def __init__(self, path, _key):
            captured["path"] = path

        def save_storage_state(self, _state):
            captured["saved"] = True

    class FakeServiceBrowser:
        async def close(self):
            return None

    class FakeService:
        browser = FakeServiceBrowser()

        async def prepare_campaign(self, _payload):
            return None

        async def fill_draft(self):
            return BrowserResult(status="ui_changed", reason="stop after capture")

    async def empty_schema(_page):
        return []

    monkeypatch.setenv("PLANETA_BOOTSTRAP_URL", "https://planeta.ru/bootstrap")
    monkeypatch.setenv("PLANETA_SESSION_KEY", "test-key")
    monkeypatch.setattr(bootstrap_once.PlanetaConfig, "from_env", lambda: config)
    monkeypatch.setattr(bootstrap_once, "async_playwright", FakePlaywrightManager)
    monkeypatch.setattr(bootstrap_once, "PlanetaBrowser", FakeClassifier)
    monkeypatch.setattr(bootstrap_once, "SessionStore", CapturingSessionStore)
    monkeypatch.setattr(bootstrap_once, "_safe_form_schema", empty_schema)
    monkeypatch.setattr(bootstrap_once, "build_default_service", lambda: FakeService())

    assert await bootstrap_once.run() == 0
    assert captured == {"path": session_dir / "session.enc", "saved": True}
