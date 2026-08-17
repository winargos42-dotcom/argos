# Planeta Session Storage Separation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep the authorized Planeta.ru browser session in the Railway volume while storing the writable campaign state separately in `/tmp`.

**Architecture:** Extend `PlanetaConfig` with an independently configurable `session_dir`. Campaign state and audit continue to use `state_path` and its parent, while `SessionStore`, the persistent Chromium profile, and bootstrap session capture use `session_dir`. The default remains `state_path.parent` so existing deployments are unchanged unless `PLANETA_SESSION_DIR` is set.

**Tech Stack:** Python 3.12, dataclasses, pathlib, pytest, Playwright, FastAPI, Railway.

## Global Constraints

- `PLANETA_SESSION_DIR=/data/planeta` on Railway v4.
- `PLANETA_STATE_PATH=/tmp/planeta_campaign.json` on Railway v4.
- `PLANETA_SESSION_DURABILITY=durable` on Railway v4.
- Do not change campaign copy, rewards, budget, approval gating, or moderation submission behavior.
- Do not change Railway volume ownership or run the application as root.
- Do not submit the campaign for moderation during implementation or verification.
- Preserve backward compatibility when `PLANETA_SESSION_DIR` is absent or blank.

---

### Task 1: Add the independent session-directory configuration contract

**Files:**
- Modify: `tests/planeta_mcp/test_config.py`
- Modify: `integrations/planeta_mcp/config.py:8-39`

**Interfaces:**
- Consumes: `PLANETA_STATE_PATH` and optional `PLANETA_SESSION_DIR` environment variables.
- Produces: `PlanetaConfig.session_dir: Path`, guaranteed to resolve to a `Path` after initialization.

- [ ] **Step 1: Write the failing configuration tests**

Add to `tests/planeta_mcp/test_config.py`:

```python
from pathlib import Path


def test_session_dir_can_be_independent_from_campaign_state(monkeypatch, tmp_path):
    state_path = tmp_path / "work" / "campaign.json"
    session_dir = tmp_path / "persistent-session"
    monkeypatch.setenv("PLANETA_STATE_PATH", str(state_path))
    monkeypatch.setenv("PLANETA_SESSION_DIR", str(session_dir))

    config = PlanetaConfig.from_env()

    assert config.state_path == state_path
    assert config.session_dir == session_dir


def test_session_dir_defaults_to_campaign_parent(monkeypatch, tmp_path):
    state_path = tmp_path / "work" / "campaign.json"
    monkeypatch.setenv("PLANETA_STATE_PATH", str(state_path))
    monkeypatch.delenv("PLANETA_SESSION_DIR", raising=False)

    config = PlanetaConfig.from_env()

    assert config.session_dir == state_path.parent


def test_blank_session_dir_defaults_to_campaign_parent(monkeypatch, tmp_path):
    state_path = tmp_path / "work" / "campaign.json"
    monkeypatch.setenv("PLANETA_STATE_PATH", str(state_path))
    monkeypatch.setenv("PLANETA_SESSION_DIR", "   ")

    config = PlanetaConfig.from_env()

    assert config.session_dir == state_path.parent


def test_direct_config_defaults_session_dir_to_state_parent(tmp_path):
    state_path = tmp_path / "campaign.json"

    config = PlanetaConfig(state_path=state_path)

    assert config.session_dir == state_path.parent
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```bash
python -m pytest tests/planeta_mcp/test_config.py -q
```

Expected: FAIL because `PlanetaConfig` has no `session_dir` field.

- [ ] **Step 3: Implement the minimal configuration behavior**

Update `integrations/planeta_mcp/config.py` so the dataclass accepts an optional session directory but normalizes it immediately:

```python
@dataclass(frozen=True, slots=True)
class PlanetaConfig:
    base_url: str = "https://planeta.ru"
    draft_url: str | None = None
    headless: bool = True
    submit_ttl_seconds: int = 300
    live_ttl_seconds: int = 600
    state_path: Path = Path("/data/planeta/campaign.json")
    session_dir: Path | None = None

    def __post_init__(self) -> None:
        if self.session_dir is None:
            object.__setattr__(self, "session_dir", self.state_path.parent)
```

In `from_env`, calculate both paths before returning:

```python
state_path = Path(os.getenv("PLANETA_STATE_PATH", "/data/planeta/campaign.json"))
session_dir_raw = os.getenv("PLANETA_SESSION_DIR", "").strip()
session_dir = Path(session_dir_raw) if session_dir_raw else state_path.parent
```

Pass both `state_path=state_path` and `session_dir=session_dir` to `cls(...)`.

- [ ] **Step 4: Run the focused tests and verify GREEN**

Run:

```bash
python -m pytest tests/planeta_mcp/test_config.py -q
```

Expected: all tests in `test_config.py` PASS.

- [ ] **Step 5: Commit the configuration contract**

```bash
git add integrations/planeta_mcp/config.py tests/planeta_mcp/test_config.py
git commit -m "fix(planeta): separate session directory config"
```

---

### Task 2: Wire session loading and live Chromium to the persistent directory

**Files:**
- Modify: `tests/planeta_mcp/test_production_wiring.py`
- Modify: `tests/planeta_mcp/test_live_bridge.py`
- Modify: `integrations/planeta_mcp/server.py:66-92,580-603`
- Modify: `integrations/planeta_mcp/live_bridge.py:62-67`

**Interfaces:**
- Consumes: `PlanetaConfig.session_dir`, `PlanetaConfig.state_path`.
- Produces: `SessionStore(config.session_dir / "session.enc", key)` and `LiveBrowserRuntime(data_dir=config.session_dir, ...)` while leaving `CampaignStore` and `AuditLogger` on the writable state path.

- [ ] **Step 1: Write a failing service-wiring test**

Add to `tests/planeta_mcp/test_production_wiring.py`:

```python
from integrations.planeta_mcp.session_store import SessionStore


def test_default_service_loads_session_from_independent_directory(monkeypatch, tmp_path):
    state_path = tmp_path / "work" / "campaign.json"
    session_dir = tmp_path / "persistent"
    session_key = Fernet.generate_key()
    cookie_state = {
        "cookies": [
            {"name": "sid", "value": "saved", "domain": ".planeta.ru", "path": "/"}
        ],
        "origins": [],
    }
    SessionStore(session_dir / "session.enc", session_key).save_storage_state(cookie_state)
    monkeypatch.setenv("PLANETA_APPROVAL_SECRET", "approval-secret")
    monkeypatch.setenv("PLANETA_SESSION_KEY", session_key.decode("ascii"))
    monkeypatch.setenv("PLANETA_STATE_PATH", str(state_path))
    monkeypatch.setenv("PLANETA_SESSION_DIR", str(session_dir))

    service = server.build_default_service()

    assert service.store.path == state_path
    assert service.audit.path == state_path.parent / "audit.jsonl"
    assert service.browser.storage_state == cookie_state
```

- [ ] **Step 2: Write a failing live-coordinator wiring test**

Add to `tests/planeta_mcp/test_live_bridge.py`:

```python
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
```

- [ ] **Step 3: Run both focused tests and verify RED**

Run:

```bash
python -m pytest \
  tests/planeta_mcp/test_production_wiring.py::test_default_service_loads_session_from_independent_directory \
  tests/planeta_mcp/test_live_bridge.py::test_live_bridge_default_runtime_uses_session_dir -q
```

Expected: the service does not load the saved cookie and the runtime points at `state_path.parent`.

- [ ] **Step 4: Implement the minimal production wiring**

In `build_default_service()` use:

```python
state_dir = config.state_path.parent
assert config.session_dir is not None
session_store = SessionStore(config.session_dir / "session.enc", session_key)
```

Keep these paths unchanged:

```python
store=CampaignStore(config.state_path)
audit=AuditLogger(state_dir / "audit.jsonl")
```

In `_module_app()` change the live `SessionStore` construction to:

```python
assert config.session_dir is not None
session_store = SessionStore(config.session_dir / "session.enc", session_key)
```

In `LiveLoginCoordinator.__init__`, change the default runtime factory to:

```python
assert config.session_dir is not None
self._runtime_factory = runtime_factory or (
    lambda: LiveBrowserRuntime(
        data_dir=config.session_dir,
        draft_url=config.draft_url,
    )
)
```

- [ ] **Step 5: Run the focused tests and verify GREEN**

Run:

```bash
python -m pytest \
  tests/planeta_mcp/test_production_wiring.py \
  tests/planeta_mcp/test_live_bridge.py -q
```

Expected: all selected tests PASS.

- [ ] **Step 6: Commit the service and runtime wiring**

```bash
git add \
  integrations/planeta_mcp/server.py \
  integrations/planeta_mcp/live_bridge.py \
  tests/planeta_mcp/test_production_wiring.py \
  tests/planeta_mcp/test_live_bridge.py
git commit -m "fix(planeta): keep browser session on persistent volume"
```

---

### Task 3: Wire bootstrap session capture to the same directory

**Files:**
- Create: `tests/planeta_mcp/test_bootstrap.py`
- Modify: `integrations/planeta_mcp/bootstrap_once.py:98-101`

**Interfaces:**
- Consumes: `PlanetaConfig.session_dir`.
- Produces: bootstrap writes encrypted storage state to `config.session_dir / "session.enc"`.

- [ ] **Step 1: Write a failing bootstrap-path test**

Create `tests/planeta_mcp/test_bootstrap.py` with lightweight fakes for the Playwright context. The test must set `PLANETA_BOOTSTRAP_URL`, return an `OK` classifier state, capture the path passed to `SessionStore`, and stop before real network or browser access:

```python
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
```

- [ ] **Step 2: Run the bootstrap test and verify RED**

Run:

```bash
python -m pytest tests/planeta_mcp/test_bootstrap.py -q
```

Expected: FAIL because bootstrap still constructs `SessionStore(config.state_path.parent / "session.enc", ...)`.

- [ ] **Step 3: Implement the one-line bootstrap wiring change**

In `integrations/planeta_mcp/bootstrap_once.py` use:

```python
assert config.session_dir is not None
store = SessionStore(config.session_dir / "session.enc", session_key)
```

- [ ] **Step 4: Run the bootstrap test and verify GREEN**

Run:

```bash
python -m pytest tests/planeta_mcp/test_bootstrap.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit the bootstrap wiring**

```bash
git add integrations/planeta_mcp/bootstrap_once.py tests/planeta_mcp/test_bootstrap.py
git commit -m "fix(planeta): persist bootstrap session independently"
```

---

### Task 4: Document and run the full Planeta regression suite

**Files:**
- Modify: `integrations/planeta_mcp/README.md`

**Interfaces:**
- Consumes: new environment variable `PLANETA_SESSION_DIR`.
- Produces: deployment documentation describing the independent session and campaign paths.

- [ ] **Step 1: Document the Railway v4 variables**

Add a configuration note near the existing Railway environment-variable section:

```markdown
For a persistent authenticated browser with a separately writable campaign state:

- `PLANETA_SESSION_DIR=/data/planeta` stores `session.enc` and `browser-profile` on the Railway volume.
- `PLANETA_STATE_PATH=/tmp/planeta_campaign.json` stores the current normalized campaign in a writable runtime path.
- `PLANETA_SESSION_DURABILITY=durable` reports that the browser session is expected to survive service restarts.

If `PLANETA_SESSION_DIR` is omitted, it defaults to the parent directory of `PLANETA_STATE_PATH` for backward compatibility.
```

- [ ] **Step 2: Run the full Planeta MCP test suite**

Run:

```bash
python -m pytest tests/planeta_mcp -q
```

Expected: all tests PASS with no failures.

- [ ] **Step 3: Compile the integration package**

Run:

```bash
python -m compileall integrations/planeta_mcp
```

Expected: exit code 0 and no syntax errors.

- [ ] **Step 4: Review the diff for scope and secrets**

Run:

```bash
git diff --check
git diff --stat HEAD~3..HEAD
git diff HEAD~3..HEAD -- integrations/planeta_mcp tests/planeta_mcp
```

Expected: only the planned Planeta files changed; no cookies, tokens, session contents, or Railway secret values appear.

- [ ] **Step 5: Commit the documentation**

```bash
git add integrations/planeta_mcp/README.md
git commit -m "docs(planeta): explain persistent session directory"
```

---

### Task 5: Publish the tested fix and verify Railway v4 without moderation submission

**Files:**
- No additional source files.
- Railway service: `planeta-mcp-v4` (`66363694-d2f3-4e51-9eef-d6c1e3e3e4c8`).

**Interfaces:**
- Consumes: tested commits from Tasks 1-4 and Railway variables.
- Produces: a healthy v4 deployment that loads `/data/planeta/session.enc` and writes `/tmp/planeta_campaign.json`.

- [ ] **Step 1: Push the tested commits to `main`**

```bash
git status --short
git push origin main
```

Expected: push succeeds and does not include unrelated local changes.

- [ ] **Step 2: Set the three v4 variables as one scoped change**

Set exactly:

```text
PLANETA_SESSION_DIR=/data/planeta
PLANETA_STATE_PATH=/tmp/planeta_campaign.json
PLANETA_SESSION_DURABILITY=durable
```

Expected: only `planeta-mcp-v4` redeploys.

- [ ] **Step 3: Verify deployment health and configuration**

Check the latest v4 deployment and:

```text
GET https://planeta-mcp-v4-production.up.railway.app/health
```

Expected: deployment `SUCCESS`; health returns HTTP 200 with `"ok": true` and `"configured": true`.

- [ ] **Step 4: Verify local campaign state**

Call, in order:

```text
planeta_prepare_campaign
planeta_validate_campaign
planeta_campaign_preview
```

Use the already approved ARGOS REBOOT payload with the factual sentence that the fire destroyed the computer and local computing environment, not the apartment.

Expected: save succeeds; validation has no errors or warnings; preview contains the corrected sentence.

- [ ] **Step 5: Verify the restored authenticated browser and locate the accessible draft**

Open one diagnostic live session for v4. Confirm that the Planeta header shows the authenticated account rather than `Войти`. If the configured campaign URL returns 403, navigate read-only to the author's project list and identify the accessible draft URL; update only `PLANETA_DRAFT_URL` if the draft ID differs.

Expected: the saved account session is active and the configured draft belongs to that account.

- [ ] **Step 6: Fill and synchronize the draft**

Call:

```text
planeta_fill_draft
planeta_sync_draft
planeta_campaign_status
```

Expected: fill status `ok`; sync status `ok`; `differences` is empty; `last_browser_status` is `ok`.

- [ ] **Step 7: Stop before the final external action**

Do not call `planeta_request_submit_approval` or `planeta_submit_for_moderation`. Report the exact filled campaign title, target amount, rewards, validation result, and draft URL, then request the owner's separate confirmation for moderation submission.
