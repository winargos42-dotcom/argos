# Planeta.ru Live Browser Bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let the owner authenticate/CAPTCHA inside the exact Chromium context used by `planeta-mcp-v4`, then automatically prepare, fill, save, and sync Planeta.ru draft `251138` without submitting it for moderation.

**Architecture:** `planeta-mcp-v4` hosts a non-headless Chromium on an internal Xvfb display, exposes that display through a token-gated noVNC view, and attaches `PlanetaBrowser` to the same Chromium over loopback-only CDP. A separate control bearer secret starts the live-login session; after the known draft editor is detected, the session is encrypted with the existing `SessionStore`, the ARGOS REBOOT payload is prepared, and fill/sync runs. Moderation submission remains exclusively behind the existing digest-bound explicit approval gate.

**Tech Stack:** Python 3.12, FastAPI, Playwright/Chromium, Xvfb, x11vnc, noVNC/websockify, cryptography/Fernet, pytest, Railway Docker.

## Global Constraints

- Never accept or persist the Planeta.ru password in ARGOS, GitHub, Railway variables, application forms, or audit logs.
- Never automate CAPTCHA solving or bypass Planeta.ru anti-bot controls.
- Never expose CDP or raw VNC publicly; both bind to loopback only.
- Browser-view capability URLs are one-time, short-lived, `Cache-Control: no-store`, and invalidated after successful session capture.
- Live browser navigation must remain on `https://planeta.ru`; unexpected origins fail closed.
- Passport, INN, SMS/e-mail codes, identity verification, and legal acceptance remain human Planeta.ru actions.
- `planeta_fill_draft`, live login, and sync must never submit for moderation.
- Final moderation submission continues to require the existing separate owner confirmation flow.
- If `/data/planeta` has no Railway volume, report authorization as ephemeral rather than durable.

---

### Task 1: One-time live-login capability controller

**Files:**
- Create: `integrations/planeta_mcp/live_login.py`
- Create: `tests/planeta_mcp/test_live_login.py`

**Interfaces:**
- Produces: `LiveLoginState`, `LiveLoginSession`, `LiveLoginController.start()`, `LiveLoginController.get(token)`, `LiveLoginController.mark_ready(token)`, `LiveLoginController.invalidate(token)`.
- `start()` returns a random URL-safe token and expiry without logging the token.

- [ ] **Step 1: Write the failing token lifecycle tests**

```python
from integrations.planeta_mcp.live_login import LiveLoginController


def test_live_login_token_is_one_time_and_expires(monkeypatch):
    now = [1000.0]
    ctl = LiveLoginController(ttl_seconds=300, clock=lambda: now[0])
    session = ctl.start()
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
```

- [ ] **Step 2: Run RED test**

Run: `python -m pytest tests/planeta_mcp/test_live_login.py -v`
Expected: FAIL with `ModuleNotFoundError: integrations.planeta_mcp.live_login`.

- [ ] **Step 3: Implement the minimal controller**

```python
class LiveLoginState(StrEnum):
    WAITING_FOR_HUMAN = "waiting_for_human"
    HUMAN_LOGIN_IN_PROGRESS = "human_login_in_progress"
    DRAFT_READY = "draft_ready"
    EXPIRED = "expired"

@dataclass(slots=True)
class LiveLoginSession:
    token: str
    issued_at: float
    expires_at: float
    state: LiveLoginState

class LiveLoginController:
    def __init__(self, ttl_seconds: int = 600, clock=time.time): ...
    def start(self) -> LiveLoginSession: ...
    def get(self, token: str) -> LiveLoginSession | None: ...
    def mark_ready(self, token: str) -> LiveLoginSession: ...
    def invalidate(self, token: str) -> None: ...
```

Use `secrets.token_urlsafe(32)` and `hmac.compare_digest` for token lookup comparisons. Keep sessions memory-only.

- [ ] **Step 4: Run GREEN test**

Run: `python -m pytest tests/planeta_mcp/test_live_login.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add integrations/planeta_mcp/live_login.py tests/planeta_mcp/test_live_login.py
git commit -m "feat(planeta): add one-time live login controller"
```

---

### Task 2: Attach `PlanetaBrowser` to an existing Chromium over CDP

**Files:**
- Modify: `integrations/planeta_mcp/browser.py`
- Modify: `tests/planeta_mcp/test_browser.py`

**Interfaces:**
- `PlanetaBrowser(..., cdp_url: str | None = None)`.
- When `cdp_url` is set, `_ensure_page()` uses `playwright.chromium.connect_over_cdp(cdp_url)` and the first existing browser context/page instead of launching another Chromium.
- Existing launch behavior remains unchanged when `cdp_url is None`.

- [ ] **Step 1: Write failing CDP attachment test**

Add an async test that launches a temporary Chromium with `--remote-debugging-port`, opens a page, constructs `PlanetaBrowser(cdp_url=<local endpoint>)`, calls `_ensure_page()`, and asserts the returned page belongs to the pre-existing context rather than a newly launched browser.

```python
@pytest.mark.asyncio
async def test_browser_attaches_to_existing_cdp_context():
    async with async_playwright() as pw:
        context = await pw.chromium.launch_persistent_context(
            tempfile.mkdtemp(),
            headless=True,
            args=["--remote-debugging-port=9333", "--remote-debugging-address=127.0.0.1"],
        )
        page = context.pages[0]
        await page.set_content("<title>shared</title>")
        adapter = PlanetaBrowser(cdp_url="http://127.0.0.1:9333")
        attached = await adapter._ensure_page()
        assert await attached.title() == "shared"
        await adapter.close()
        await context.close()
```

- [ ] **Step 2: Run RED test**

Run: `python -m pytest tests/planeta_mcp/test_browser.py -k cdp -v`
Expected: FAIL because `PlanetaBrowser.__init__` does not accept `cdp_url`.

- [ ] **Step 3: Implement minimal CDP mode**

Add `cdp_url` to the constructor. In `_ensure_page()`, call `connect_over_cdp`, select `contexts[0]`, then `pages[0]` or create one page if absent. Track whether the browser was attached so `close()` closes only the adapter connection and does not terminate the externally owned persistent Chromium.

- [ ] **Step 4: Run browser tests**

Run: `python -m pytest tests/planeta_mcp/test_browser.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add integrations/planeta_mcp/browser.py tests/planeta_mcp/test_browser.py
git commit -m "feat(planeta): support shared Chromium CDP sessions"
```

---

### Task 3: Live Chromium/Xvfb/VNC runtime

**Files:**
- Create: `integrations/planeta_mcp/live_browser.py`
- Create: `tests/planeta_mcp/test_live_browser.py`
- Modify: `integrations/planeta_mcp/Dockerfile.railway`
- Modify: `integrations/planeta_mcp/requirements.txt`

**Interfaces:**
- Produces `LiveBrowserRuntime.start()`, `LiveBrowserRuntime.stop()`, `LiveBrowserRuntime.cdp_url`, `LiveBrowserRuntime.websockify_url`, and `LiveBrowserRuntime.storage_state()`.
- Runtime binds Chromium CDP to `127.0.0.1:9222`, x11vnc to `127.0.0.1:5900`, and websockify to `127.0.0.1:6080`.
- Chromium persistent profile: `/data/planeta/browser-profile`.

- [ ] **Step 1: Write failing runtime contract tests**

```python
def test_live_browser_runtime_uses_loopback_only(tmp_path):
    runtime = LiveBrowserRuntime(data_dir=tmp_path)
    assert runtime.cdp_url == "http://127.0.0.1:9222"
    assert runtime.vnc_host == "127.0.0.1"
    assert runtime.vnc_port == 5900
    assert runtime.websockify_url == "ws://127.0.0.1:6080"
```

Add a process-argument test asserting the Chromium arguments contain both `--remote-debugging-address=127.0.0.1` and `--remote-debugging-port=9222`, x11vnc uses `-localhost`, and websockify listens on `127.0.0.1:6080`.

- [ ] **Step 2: Run RED test**

Run: `python -m pytest tests/planeta_mcp/test_live_browser.py -v`
Expected: FAIL because `live_browser.py` does not exist.

- [ ] **Step 3: Implement runtime**

`LiveBrowserRuntime.start()` must:

1. create `/data/planeta/browser-profile`;
2. spawn `Xvfb :99 -screen 0 1365x768x24 -nolisten tcp`;
3. spawn `x11vnc -display :99 -localhost -forever -shared -rfbport 5900 -nopw`;
4. spawn `websockify 127.0.0.1:6080 127.0.0.1:5900`;
5. launch Playwright persistent Chromium with `headless=False`, `DISPLAY=:99`, user-data directory, and loopback-only CDP arguments;
6. open `PLANETA_DRAFT_URL` if configured.

`stop()` terminates only owned processes/context. `storage_state()` delegates to the persistent Playwright context.

- [ ] **Step 4: Add Railway packages**

Extend the existing apt install line in `Dockerfile.railway` with:

```text
xvfb x11vnc novnc websockify
```

Do not expose ports 5900, 6080, or 9222 in Railway networking.

- [ ] **Step 5: Run tests and compile**

Run:

```bash
python -m pytest tests/planeta_mcp/test_live_browser.py tests/planeta_mcp/test_browser.py -v
python -m compileall integrations/planeta_mcp
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add integrations/planeta_mcp/live_browser.py integrations/planeta_mcp/Dockerfile.railway integrations/planeta_mcp/requirements.txt tests/planeta_mcp/test_live_browser.py
git commit -m "feat(planeta): add live Chromium runtime"
```

---

### Task 4: Token-gated noVNC routes and automated draft handoff

**Files:**
- Modify: `integrations/planeta_mcp/server.py`
- Modify: `tests/planeta_mcp/test_server.py`
- Modify: `integrations/planeta_mcp/config.py`

**Interfaces:**
- New config: `PLANETA_LIVE_CONTROL_SECRET` (required only for live-login start), `PLANETA_LIVE_TTL_SECONDS` default `600`.
- `POST /live-login/start` requires `Authorization: Bearer <PLANETA_LIVE_CONTROL_SECRET>`.
- `GET /live-login/{token}/` serves a no-store noVNC shell only for an active token.
- `WS /live-login/{token}/websockify` validates the token then proxies binary/text frames to `ws://127.0.0.1:6080`.
- `GET /live-login/status/{token}` returns sanitized state only.
- Background watcher captures encrypted storage state and runs prepare/fill/sync only after the real draft editor is classified `OK`.

- [ ] **Step 1: Write failing route/auth tests**

```python
def test_live_login_start_requires_control_secret(tmp_path):
    client = TestClient(create_app(service=make_service(tmp_path), enable_mcp=False, live_control_secret="control"))
    assert client.post("/live-login/start").status_code == 401
    ok = client.post("/live-login/start", headers={"Authorization": "Bearer control"})
    assert ok.status_code == 200
    assert "/live-login/" in ok.json()["browser_url"]


def test_live_login_page_is_no_store(tmp_path):
    client = ...
    start = client.post(...).json()
    response = client.get(urlsplit(start["browser_url"]).path)
    assert response.headers["cache-control"].startswith("no-store")
    assert response.headers["x-frame-options"] == "DENY"
```

Add a test that invalid/expired tokens receive 404 and a test that the live-login path cannot invoke `submit_for_moderation`.

- [ ] **Step 2: Run RED tests**

Run: `python -m pytest tests/planeta_mcp/test_server.py -k live_login -v`
Expected: FAIL with missing routes/arguments.

- [ ] **Step 3: Implement start/status/page/websocket routes**

Use the `LiveLoginController` from Task 1. Browser URL must be constructed from `_public_base_url()` and the capability token. HTML references the bundled noVNC `vnc.html` assets but never embeds credentials or page data. Add strict no-store/CSP/referrer headers.

- [ ] **Step 4: Implement authenticated draft watcher**

After `LiveBrowserRuntime.start()`, poll the shared draft page every second for at most the live-login TTL. Classification rules:

```python
state = await shared_browser.inspect()
if state.status == "ok":
    encrypted_store.save_storage_state(await runtime.storage_state())
    await service.prepare_campaign(default_argos_reboot_campaign())
    fill = await service.fill_draft()
    if fill.status == "ok":
        sync = await service.sync_draft()
        controller.mark_ready(token)
        controller.invalidate(token)
```

For `authentication_required`, `captcha_required`, and `human_action_required`, keep the live view active and expose only the sanitized status. For `ui_changed`, `network_error`, or expiry, stop without guessing or submitting.

- [ ] **Step 5: Run server and full connector tests**

Run:

```bash
python -m pytest tests/planeta_mcp/test_server.py -v
python -m pytest tests/planeta_mcp -v
```

Expected: all tests PASS and existing approval tests remain unchanged.

- [ ] **Step 6: Commit**

```bash
git add integrations/planeta_mcp/server.py integrations/planeta_mcp/config.py tests/planeta_mcp/test_server.py
git commit -m "feat(planeta): add token-gated live browser handoff"
```

---

### Task 5: Railway verification and real Planeta.ru draft fill

**Files:**
- Modify only if required by verified deployment behavior: `integrations/planeta_mcp/railway.json`
- Update after successful verification: `integrations/planeta_mcp/README.md`

**Interfaces:**
- Railway public service remains `planeta-mcp-v4` on port 8000.
- Draft URL remains `https://planeta.ru/campaigns/251138/edit/about`.
- Live control uses a newly generated random `PLANETA_LIVE_CONTROL_SECRET`; it is never printed in logs or committed.

- [ ] **Step 1: Run CI before deploy**

Run the repository Planeta workflow or equivalent commands:

```bash
python -m pytest tests/planeta_mcp -v
python -m compileall integrations/planeta_mcp
docker build -f integrations/planeta_mcp/Dockerfile.railway -t argos-planeta-live integrations/planeta_mcp
```

Expected: tests, compile, and Docker build PASS.

- [ ] **Step 2: Check persistence before live login**

Inspect Railway `planeta-mcp-v4` service config. If no volume mount exists at `/data/planeta`, attempt to attach a Railway volume through the available Railway control plane. If the available tool cannot create the volume, continue only for the current draft operation and explicitly classify session durability as `ephemeral`.

- [ ] **Step 3: Deploy `main` and verify health**

Wait for Railway deployment status `SUCCESS`; verify runtime logs include Uvicorn startup and Railway healthcheck `GET /health` returning `200 OK`.

- [ ] **Step 4: Create live-login session without exposing the control secret**

Generate `PLANETA_LIVE_CONTROL_SECRET` with at least 32 random bytes, store it only in Railway, then call `POST /live-login/start` with the bearer secret from a trusted operator context. Return only the generated one-time `browser_url` to the owner.

- [ ] **Step 5: Human login/CAPTCHA**

Owner opens the one-time HTTPS browser URL on the phone and completes login/CAPTCHA directly in the live Chromium. No password is sent through chat, GitHub, MCP arguments, or Railway variables.

- [ ] **Step 6: Verify real draft fill**

After the watcher reports `draft_ready`, verify sanitized logs/results show:

```text
prepare_campaign: ok
fill_draft: ok
sync_draft: ok
differences: []
```

Confirm the configured page is campaign `251138`. Do not invoke `planeta_request_submit_approval` or `planeta_submit_for_moderation` in this task.

- [ ] **Step 7: Remove live-login capability**

Invalidate the live token, stop the VNC/browser-view session, and rotate/remove `PLANETA_LIVE_CONTROL_SECRET` if it was created solely for this operation. Keep only encrypted Planeta browser state when persistence is available.

- [ ] **Step 8: Update README and commit deployment notes**

Document the live-login workflow, ephemeral-vs-durable session behavior, and the rule that final moderation submission always requires a separate owner confirmation.

```bash
git add integrations/planeta_mcp/README.md
git commit -m "docs(planeta): document live browser authorization"
```

## Plan Self-Review

- Spec coverage: live Chromium, human CAPTCHA, same-context CDP, encrypted session capture, draft prepare/fill/sync, fail-closed origin/UI handling, no public CDP/VNC, no moderation side effect, persistence check, and Railway verification are all mapped to tasks.
- Placeholder scan: no `TBD`, `TODO`, or unspecified implementation steps remain.
- Type consistency: `LiveLoginController`, `LiveBrowserRuntime`, `PlanetaBrowser(cdp_url=...)`, and live-login route names are consistent across tasks.
