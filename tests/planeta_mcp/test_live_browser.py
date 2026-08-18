import pytest

from integrations.planeta_mcp import live_browser as live_browser_module
from integrations.planeta_mcp.live_browser import LiveBrowserRuntime


class RecordingPage:
    def __init__(self, events):
        self.events = events

    async def goto(self, url, **_kwargs):
        self.events.append(("goto", url))


class RecordingContext:
    def __init__(self, events):
        self.events = events
        self.pages = [RecordingPage(events)]

    async def add_cookies(self, cookies):
        self.events.append(("cookies", cookies))

    async def add_init_script(self, *, script):
        self.events.append(("init_script", script))

    async def close(self):
        return None


class RecordingChromium:
    def __init__(self, context):
        self.context = context

    async def launch_persistent_context(self, *_args, **_kwargs):
        return self.context


class RecordingPlaywright:
    def __init__(self, context):
        self.chromium = RecordingChromium(context)

    async def stop(self):
        return None


class RecordingPlaywrightManager:
    def __init__(self, playwright):
        self.playwright = playwright

    async def start(self):
        return self.playwright


def test_live_browser_runtime_uses_loopback_only(tmp_path):
    runtime = LiveBrowserRuntime(data_dir=tmp_path)

    assert runtime.cdp_url == "http://127.0.0.1:9222"
    assert runtime.vnc_host == "127.0.0.1"
    assert runtime.vnc_port == 5900
    assert runtime.websockify_url == "tcp://127.0.0.1:5900"


def test_live_browser_commands_never_expose_control_ports(tmp_path):
    runtime = LiveBrowserRuntime(data_dir=tmp_path)

    assert runtime.xvfb_command() == [
        "Xvfb",
        ":99",
        "-screen",
        "0",
        "1365x768x24",
        "-nolisten",
        "tcp",
    ]
    assert "-localhost" in runtime.vnc_command()
    assert runtime.vnc_command()[runtime.vnc_command().index("-rfbport") + 1] == "5900"
    assert "--remote-debugging-address=127.0.0.1" in runtime.chromium_args()
    assert "--remote-debugging-port=9222" in runtime.chromium_args()


def test_live_browser_profile_is_inside_data_dir(tmp_path):
    runtime = LiveBrowserRuntime(data_dir=tmp_path)
    assert runtime.profile_dir == tmp_path / "browser-profile"


@pytest.mark.asyncio
async def test_live_browser_rehydrates_same_origin_state_before_draft_navigation(
    tmp_path, monkeypatch
):
    events = []
    context = RecordingContext(events)
    playwright = RecordingPlaywright(context)
    monkeypatch.setattr(
        live_browser_module,
        "async_playwright",
        lambda: RecordingPlaywrightManager(playwright),
    )

    storage_state = {
        "cookies": [
            {
                "name": "sid",
                "value": "saved",
                "domain": ".planeta.ru",
                "path": "/",
            }
        ],
        "origins": [
            {
                "origin": "https://planeta.ru",
                "localStorage": [{"name": "draft-mode", "value": "restored"}],
            },
            {
                "origin": "https://id.planeta.ru",
                "localStorage": [{"name": "foreign", "value": "blocked"}],
            },
        ],
    }
    draft_url = "https://planeta.ru/campaigns/251138/edit/about"
    runtime = LiveBrowserRuntime(data_dir=tmp_path, draft_url=draft_url)

    async def no_spawn(_command, *, env=None):
        return None

    monkeypatch.setattr(runtime, "_spawn", no_spawn)
    runtime.set_storage_state(storage_state)

    try:
        await runtime.start()
    finally:
        await runtime.stop()

    assert [event[0] for event in events] == ["cookies", "init_script", "goto"]
    assert events[0][1] == storage_state["cookies"]
    assert "draft-mode" in events[1][1]
    assert "restored" in events[1][1]
    assert "foreign" not in events[1][1]
    assert "blocked" not in events[1][1]
    assert events[2] == ("goto", draft_url)
